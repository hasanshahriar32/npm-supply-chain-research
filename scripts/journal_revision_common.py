"""Shared, read-only inputs and objective implementations for revision experiments."""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shutil
import sqlite3
import tempfile
import zipfile

import study_structural_interventions as ssi

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'manuscript_q1/results/revision_validation'


def stamp():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def dump(path, obj):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + '\n')


def baseline():
    """Derive repository incidence without altering the retained database archive."""
    cache = OUT / 'baseline_incidence.json'
    archive = ROOT / 'data/npm_ecosystem.db.zip'
    if cache.exists():
        obj = json.loads(cache.read_text())
        assert obj['archive_sha256'] == sha(archive)
        return obj
    with tempfile.TemporaryDirectory(prefix='revision-baseline-') as tmp:
        db = Path(tmp) / 'baseline.db'
        with zipfile.ZipFile(archive) as z, z.open('npm_ecosystem.db') as src, db.open('wb') as dst:
            shutil.copyfileobj(src, dst)
        conn = sqlite3.connect(f'file:{db}?mode=ro&immutable=1', uri=True)
        names, ids, portfolios, pm, adj, wf, checked, rn, wn, sn, pop = ssi.load_data(conn)
        comp, members, edges, topo = ssi.scc_condensation(adj)
        pkg_reach = ssi.propagate_endpoint_bits(comp, members, edges, topo, wn)
        ep = ssi.endpoint_data(pkg_reach, portfolios)
        repos = set()
        records = defaultdict(list)
        for pkg, version, url, owner, repo, flag in conn.execute(
                'SELECT package_name,version,repository_url,github_owner,github_repo,has_github_workflows FROM package_versions'):
            if owner and repo:
                repo = repo.lower().removesuffix('.git')
                key = owner.lower() + '/' + repo
                repos.add(key)
                if flag == 1:
                    records[key].append({'package': pkg, 'version': version, 'original_repository_url': url})
        repo_names = sorted(repos)
        sources = [0] * len(repo_names)
        for m, mask in enumerate(ep['masks']):
            for r in ssi.bit_indices(mask):
                sources[r] |= 1 << m
        observed = ssi.union(wn)
        endpoints = [{'index': r, 'repository': repo_names[r], 'source_mask': hex(sources[r]),
                      'source_count': sources[r].bit_count(),
                      'original_mappings': sorted(records[repo_names[r]], key=lambda x: (x['package'], x['version']))}
                     for r in ssi.bit_indices(observed)]
        obj = {'archive_sha256': sha(archive), 'derived_at_utc': stamp(), 'population': pop,
               'maintainers': [x[0] for x in ids], 'maintainer_masks': [hex(x) for x in ep['masks']],
               'scores': ep['scores'], 'total_pairs': ep['total_pairs'], 'endpoints': endpoints}
        assert len(endpoints) == 7171 and sum(bool(int(x['source_mask'], 16)) for x in endpoints) == 7158
        assert obj['total_pairs'] == 462170
        conn.close()
    dump(cache, obj)
    return obj


def metric(order, masks, sources, endpoint_total=None):
    selected = sum(1 << m for m in order)
    covered = ssi.union(masks[m] for m in order)
    pairs = sum(m.bit_count() for m in masks)
    observed = endpoint_total if endpoint_total is not None else ssi.union(masks).bit_count()
    active = [s for s in sources if s]
    return {'C': covered.bit_count(), 'C_pct': 100 * covered.bit_count() / observed if observed else None,
            'H_pct': 100 * sum(masks[m].bit_count() for m in order) / pairs if pairs else None,
            'P': sum((s & selected) == s for s in active), 'endpoint_total': observed,
            'source_reachable_endpoints': len(active), 'pair_denominator': pairs}


def exclusion_order(masks, sources, budget, cap=10, reciprocal=True, coverage_tie=True,
                    immediate_only=False, tie_seed=None, candidates=None):
    """Original lexicographic rule with explicit component and tie variants.

    Sources are complete original sets. Outside-candidate sources remain present.
    Ascending candidate enumeration makes random tie draws reproducible.
    """
    import random
    import time
    t0 = time.perf_counter()
    available = set(range(len(masks))) if candidates is None else set(candidates)
    active_sources = [s for s in sources if s]
    reverse = [[] for _ in masks]
    for r, src in enumerate(active_sources):
        for m in ssi.bit_indices(src):
            reverse[m].append(r)
    remaining = list(active_sources)
    counts = [s.bit_count() for s in remaining]
    rng = random.Random(tie_seed)
    selected, selected_mask, covered = [], 0, 0
    for _ in range(min(budget, len(available))):
        cand = set()
        for src, count in zip(remaining, counts):
            if count > 0 and (cap is None or count <= cap):
                cand.update(ssi.bit_indices(src))
        cand &= available
        if not cand:
            cand = set(available)
        best, best_score = None, None
        for m in sorted(cand):
            bit = 1 << m
            immediate, fraction = 0, 0.0
            for r in reverse[m]:
                if remaining[r] & bit:
                    if counts[r] == 1:
                        immediate += 1
                    elif reciprocal and not immediate_only:
                        fraction += 1 / counts[r]
            marginal = (masks[m] & ~covered).bit_count() if coverage_tie else 0
            tie = rng.random() if tie_seed is not None else -m
            score = (immediate, fraction, marginal, tie)
            if best_score is None or score > best_score:
                best, best_score = m, score
        selected.append(best)
        available.remove(best)
        selected_mask |= 1 << best
        covered |= masks[best]
        for r in reverse[best]:
            if remaining[r] & (1 << best):
                remaining[r] &= ~(1 << best)
                counts[r] -= 1
    return selected, {'wall_seconds': time.perf_counter() - t0}
