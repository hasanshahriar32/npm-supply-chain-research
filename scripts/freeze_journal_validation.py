#!/usr/bin/env python3
"""Freeze the new audit protocol and probability sample before network acquisition."""
from collections import Counter
import csv
import json
import random

from journal_revision_common import ROOT, OUT, baseline, dump, sha, stamp

SEED = 2026102701


def stratum(n):
    return '1' if n == 1 else '2-5' if n <= 5 else '6-50' if n <= 50 else '>50'


def main():
    proto = ROOT / 'manuscript_q1/protocols'
    proto.mkdir(exist_ok=True)
    path = proto / 'revision_validation_protocol.json'
    if path.exists():
        print('Protocol already frozen; preserving sample and timestamp')
        return
    data = baseline()
    groups = {s: [] for s in ['1', '2-5', '6-50', '>50']}
    for row in data['endpoints']:
        if row['source_count']:
            groups[stratum(row['source_count'])].append(row)
    rng = random.Random(SEED)
    rows = []
    for group, frame in groups.items():
        n = min(30, len(frame))
        for row in sorted(rng.sample(frame, n), key=lambda r: r['repository']):
            rows.append({**row, 'audit_id': f'A{len(rows)+1:03}', 'stratum': group,
                         'stratum_population': len(frame), 'stratum_sample': n,
                         'inclusion_probability': n / len(frame), 'design_weight': len(frame) / n})
    assert len(rows) == 120
    dump(proto / 'endpoint_audit_sample.json', rows)
    with (proto / 'endpoint_audit_sample.csv').open('w', newline='') as f:
        keys = ['audit_id', 'repository', 'stratum', 'source_count', 'stratum_population',
                'stratum_sample', 'inclusion_probability', 'design_weight']
        w = csv.DictWriter(f, keys); w.writeheader()
        w.writerows({k: r[k] for k in keys} for r in rows)
    # New independently sampled roots within the original ordinary-name frame.
    import sqlite3, tempfile, zipfile, shutil
    with tempfile.TemporaryDirectory() as t:
        from pathlib import Path
        db = Path(t) / 'a.db'
        with zipfile.ZipFile(ROOT/'data/npm_ecosystem.db.zip') as z, z.open('npm_ecosystem.db') as s, db.open('wb') as d:
            shutil.copyfileobj(s,d)
        c = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        names = sorted(r[0] for r in c.execute('SELECT name FROM packages') if '>' not in r[0])
        c.close()
    roots = sorted(random.Random(SEED + 1).sample(names, 100))
    dump(proto/'replication_roots.json', roots)
    protocol = {
        'version': 'journal-validation-v1', 'frozen_at_utc': stamp(), 'seed': SEED,
        'baseline_archive_sha256': data['archive_sha256'], 'frame_endpoints': 7158,
        'stratum_populations': {k:len(v) for k,v in groups.items()}, 'sample_size': len(rows),
        'sample_sha256': sha(proto/'endpoint_audit_sample.json'),
        'hypotheses': ['Measure C/H/P tradeoff persistence under stricter audited endpoints',
                       'Measure sensitivity of direct P to cap, scoring and ties; allow null results',
                       'Measure descriptive transport to newly acquired baseline-frame roots'],
        'audit_acquisition': {'time_scope':'current retrieval; not retrospective validation of old HEAD',
                             'retries':2, 'replace_failed_units':False, 'immutable_commit_files':True,
                             'max_workflow_files_per_repo':20, 'max_manifest_candidates':12,
                             'max_lockfile_bytes':2000000,
                             'installation_label':'static directive only; execution not measured'},
        'labels':['repository_mapping_supported','workflow_file_present','install_directive_observed',
                  'lockfile_present','dependency_version_supported'],
        'human_review':{'authors_available':2, 'completed':False, 'independent_initial_labels':True,
                        'automated_labels_are_human_labels':False},
        'evaluation':{'budgets':[1,5,10,25,50,100], 'primary_selections':'frozen original orders',
                      'retain_full_source_sets':True, 'population_estimates':'design weighted; no npm-wide claim',
                      'unknowns':'retain and report; all-in/all-out H scenarios are not sharp bounds'},
        'heuristic':{'caps':[1,5,10,20,None], 'tie_seeds':list(range(30)),
                     'exact_candidates':20,'exact_budgets':[1,3,5], 'exact_empirical_instances':20,
                     'synthetic_instances':12, 'outside_candidate_sources':'remain unselected',
                     'immediate_only_fallback':'coverage then ascending identity'},
        'replication':{'root_count':100, 'root_frame_count':len(names),
                       'root_frame':'ordinary-shaped names in original seeded graph, not all npm',
                       'root_sha256':sha(proto/'replication_roots.json'), 'max_nodes':2500,
                       'max_dependency_nodes_per_root':500, 'version_policy':'latest root frozen on retrieval',
                       'required_new_observations':['npm metadata','deps.dev version dependency observations'],
                       'registry_requests_concurrency':6, 'not_an_independent_ecosystem_sample':True},
        'baseline_result_sha256':sha(ROOT/'manuscript/results/structural_interventions/results.json'),
        'protocol_script_sha256':sha(__file__), 'plan':'reports/22_journal_improvement_plan.md'}
    dump(path,protocol)
    (proto/'revision_validation_protocol.md').write_text(
        '# Frozen journal validation protocol\n\nFrozen at '+protocol['frozen_at_utc']+
        '. This is a new protocol, not preregistration of the original study.\n\n'
        'The machine-readable JSON specifies the frozen probability sample, acquisition limits, '
        'labels, human review, objective evaluation, heuristic ablations and new acquisition. '
        'Original archive and prospective cohort are preserved. Automated evidence is provisional '
        'until independent author review; failures are retained and no favorable-result threshold is used.\n')
    with (proto/'revision_claim_matrix.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['claim','existing_evidence','new_test','permitted_interpretation'])
        w.writerows([
            ['C/H/P favor different selections','six-budget retained graph','audited endpoint transport','conditional structural comparison'],
            ['version continuity changes reach','name/version edge-union comparisons','new cohort representation analysis','representation sensitivity, not installed exploits'],
            ['direct P improves exclusion','retained P=1022','ablations and candidate-restricted exact benchmarks','heuristic empirical gain, no global optimum'],
            ['workflow observation is useful','HEAD directory lookup','commit-pinned package/workflow evidence','static evidence only, not observed execution'],
            ['findings transport','single retained acquisition','new 100-root acquisition','bounded baseline-frame cohort, not npm-wide generalization']])
    print(json.dumps({'frozen':protocol['frozen_at_utc'],'strata':protocol['stratum_populations'],'sample':120}))


if __name__ == '__main__':
    main()
