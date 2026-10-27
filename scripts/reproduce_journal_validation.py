#!/usr/bin/env python3
"""Offline numeric reproduction from the versioned research artifact."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from journal_revision_common import ROOT, OUT, dump, sha, stamp
from verify_journal_revision import verify


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--recompute-cohort',action='store_true');args=ap.parse_args()
    os.environ['NPM_RESEARCH_OFFLINE']='1'
    manifest=ROOT/'RESEARCH_ARTIFACT_MANIFEST.json'
    if manifest.exists():
        recorded=json.loads(manifest.read_text())
        for path,expected in recorded['files'].items():assert sha(ROOT/path)==expected,path
        print('Release input checksums: PASS',flush=True)
    result=verify(raw_evidence=False)
    print('Numeric and source-set gates: PASS',flush=True)
    result['raw_source_exclusion']='Third-party workflow/manifest bodies are referenced by pinned URLs and hashes; derived observations are released. This mode does not re-annotate or certify them.'
    if args.recompute_cohort:
        expected=json.loads((OUT/'replication/study_summary.json').read_text())
        with tempfile.TemporaryDirectory(prefix='offline-cohort-') as tmp:
            workspace=Path(tmp)
            shutil.copytree(ROOT/'scripts',workspace/'scripts',ignore=shutil.ignore_patterns('__pycache__'))
            (workspace/'data').mkdir();shutil.copy2(ROOT/'data/npm_ecosystem.db.zip',workspace/'data/npm_ecosystem.db.zip')
            (workspace/'manuscript_q1/results/revision_validation').mkdir(parents=True)
            shutil.copytree(OUT/'replication',workspace/'manuscript_q1/results/revision_validation/replication')
            shutil.copytree(ROOT/'manuscript_q1/protocols',workspace/'manuscript_q1/protocols')
            env={**os.environ,'NPM_RESEARCH_OFFLINE':'1'}
            run=subprocess.run([sys.executable,str(workspace/'scripts/study_replication_cohort.py')],
                               cwd=workspace,env=env,capture_output=True,text=True,timeout=180)
            if run.returncode:raise RuntimeError(run.stderr[-4000:])
            actual=json.loads((workspace/'manuscript_q1/results/revision_validation/replication/study_summary.json').read_text())
            for field in ['results','common_results','overlaps','workflow_repository_endpoints','maintainers',
                          'name_pair_mass','version_pair_mass','metadata_versions_acquired']:
                assert actual[field]==expected[field],field
            result['isolated_offline_cohort_recomputation']='PASS'
        print('Isolated offline cohort recomputation: PASS',flush=True)
    result['reproduced_at_utc']=stamp()
    dump(ROOT/'REPRODUCTION_RESULT.json',result)
    print(json.dumps(result,indent=2))


if __name__=='__main__':main()
