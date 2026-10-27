#!/usr/bin/env python3
"""Prepare a versioned, standalone data/code asset without publishing the paper."""
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import shutil
import tempfile
import zipfile

from journal_revision_common import ROOT, OUT, dump, sha, stamp

DEST=ROOT/'submission/research_artifact'
TAG='research-validation-2026-10-28'
CODE=['journal_revision_common.py','freeze_journal_validation.py','collect_endpoint_validation.py',
      'collect_replication_cohort.py','study_exclusion_heuristic_validation.py','study_validated_endpoints.py',
      'study_replication_cohort.py','render_journal_validation.py','verify_journal_revision.py',
      'reproduce_journal_validation.py','study_structural_interventions.py','collect_data.py','research_observations.py',
      'collect_github_evidence_requests.py']


def main():
    DEST.mkdir(parents=True,exist_ok=True)
    receipt=DEST/'package_manifest.json'
    if receipt.exists() and json.loads(receipt.read_text()).get('verified_public'):
        raise SystemExit('This artifact version is already published. Choose a new tag/asset version before repackaging.')
    selected=[ROOT/'data/npm_ecosystem.db.zip',
              ROOT/'manuscript/results/structural_interventions/results.json',
              ROOT/'manuscript_q1/results/quorum_reproducibility.json',
              ROOT/'manuscript_q1/requirements-revision.txt']
    selected += [ROOT/'scripts'/name for name in CODE]
    selected += list((ROOT/'scripts/tests').glob('test_journal_revision.py'))
    selected += [p for p in (ROOT/'manuscript_q1/protocols').rglob('*') if p.is_file()]
    for p in OUT.rglob('*'):
        if not p.is_file():continue
        rel=p.relative_to(OUT)
        if p.name=='baseline_incidence.json':continue
        if 'github_responses' in rel.parts and '__file_' in p.name:continue
        selected.append(p)
    selected += list((ROOT/'manuscript_q1/tables').glob('revision_*_table.tex'))
    selected += [p for p in (ROOT/'manuscript_q1/figures').glob('revision_*') if p.suffix in ['.pdf','.png','.svg']]
    with tempfile.TemporaryDirectory(prefix='research-release-') as tmp:
        stage=Path(tmp)
        for p in sorted(set(selected)):
            target=stage/p.relative_to(ROOT);target.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,target)
        readme='''# npm structural-prioritization research artifact

Version: research-validation-2026-10-28. This prerelease contains completed computational experiments and provisional automated audit evidence. Independent human endpoint annotations remain pending. It is not a published manuscript or an assertion that the paper has been approved or accepted.

Download the attached npm-research-validation-2026-10-28.zip asset. The automatically generated GitHub source-code ZIP follows the base repository tag and is not the standalone executed artifact.

## Reproduce offline

Use Python 3.10 or newer. The executed environment is recorded in ENVIRONMENT.json. The numerical verification path uses the standard library; installing manuscript_q1/requirements-revision.txt also enables YAML extraction and figure rendering.

```sh
python3 scripts/reproduce_journal_validation.py --recompute-cohort
```

This verifies release checksums, independently rebuilds all 12,217 original account masks, checks 228 ablation rows, recomputes the restricted exact optima underlying 288 comparisons, checks the 120 fresh-cohort metric rows, and recomputes the fresh cohort in an isolated temporary workspace with live network acquisition disabled. Timing and generation timestamps are not expected to reproduce byte-for-byte.

The original archive is preserved unchanged. Public registry identifiers are retained for replication; they are not anonymized or evidence of misconduct, present-day insecurity, independent credentials, or historical publishing rights. Source counts and hypothetical hardening outcomes are structural quantities, not incident probabilities or deployed prevention measurements.

The exact acquisition collector is preserved under manuscript_q1/protocols/executed_scripts/ and in release-base commit 43c039bebe7c36b07a5aeb50b1c8a412ad058e0f. Its hash matches the acquisition manifest. The current collector adds an offline-network guard after acquisition; online collection logic is unchanged.

## Inputs and provenance

- data/npm_ecosystem.db.zip: original retained database archive.
- manuscript_q1/protocols/: protocol and probability samples frozen before the new acquisition.
- results/revision_validation/heuristic/: full/candidate-cap/component/tie experiments and exact-instance records.
- results/revision_validation/replication/: newly retrieved root/dependency/registry observations, pinned workflow-directory metadata, graph, incidence and comparisons.
- results/revision_validation/endpoint_audit/: registry metadata and derived static evidence candidates; GitHub metadata includes the observed commits/directories.
- results/revision_validation/endpoint_transport/: provisional diagnostics using machine evidence, not human-validated conclusions.

The paths abbreviated as results/ above are under manuscript_q1/. The original 100-identifier prospective outcome cohort is a different study and is not relabeled by this artifact.

Raw third-party workflow/manifest/lockfile bodies are not redistributed in this asset. The derived evidence records retain pinned source paths, commits, hashes and concise installation/dependency evidence so those sources can be inspected at their original repositories. Offline numeric reproduction uses the released derived observations; it does not claim to redo independent human annotation or to certify the source-body evidence. Complete raw-source checks were performed in the working repository and are separately identified in its verification report.

## Source attribution

The observations originate from the npm registry, the deps.dev API, and public GitHub repository metadata/source. Original identifiers, observation URLs and timestamps are retained where relevant. Existing third-party terms and authorship are not altered by this release. No blanket license for third-party source code is asserted. See https://docs.deps.dev/api/v3/ for API semantics and source data information.

## Study limits

The 100 new roots are sampled from the original ordinary-name frame rather than all npm. The acquisition yields 94 dependency graphs and 66 eligible workflow-associated repository endpoints, with recorded failures. The 120-endpoint audit has machine evidence and pending human review. Exact benchmarks are restricted to 20 eligible candidates and never establish the full-graph optimum. Changing H denominators requires within-population interpretation. Null and unfavorable results are retained.
'''
        (stage/'README.md').write_text(readme)
        env={'python':platform.python_version(),'platform':platform.platform(),
             'packages':{name:importlib.metadata.version(name) for name in ['matplotlib','numpy']},
             'note':'PyYAML 6.x was used in a separate collection environment; numeric reproduction does not require it.'}
        (stage/'ENVIRONMENT.json').write_text(json.dumps(env,indent=2)+'\n')
        files={str(p.relative_to(stage)):sha(p) for p in stage.rglob('*') if p.is_file()}
        manifest={'tag':TAG,'created_at_utc':stamp(),'human_endpoint_review_complete':False,
                  'paper_included':False,'raw_third_party_source_bodies_included':False,'files':files}
        (stage/'RESEARCH_ARTIFACT_MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
        zipout=DEST/'npm-research-validation-2026-10-28.zip'
        with zipfile.ZipFile(zipout,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
            for p in sorted(stage.rglob('*')):
                if p.is_file():z.write(p,str(p.relative_to(stage)))
    receipt={'tag':TAG,'asset':str(zipout.relative_to(ROOT)),'bytes':zipout.stat().st_size,
             'sha256':sha(zipout),'files':len(files)+1,'public_url':None,'verified_public':False}
    dump(DEST/'package_manifest.json',receipt)
    print(json.dumps(receipt,indent=2))


if __name__=='__main__':main()
