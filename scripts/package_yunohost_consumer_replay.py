#!/usr/bin/env python3
"""Build the journal supplement and verify its extracted copy offline."""
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import zipfile

from replay_yunohost_consumer_results import CASES, REPLAY
from check_yunohost_bun_direct import RESULTS as BUN_RESULTS
from check_yunohost_npm_unresolved import RESULTS as NPM_RESULTS
from replay_yunohost_budgets import PROJECTION as BUDGET_DATA, RESULTS as BUDGET_RESULTS, SUMMARY, TABLE
from study_yunohost_empty_declared_roots import PROTOCOL as ROOT_PROTOCOL, RESULTS as ROOT_RESULTS
from study_yunohost_empty_pnpm_roots import PROTOCOL as EMPTY_PROTOCOL, RESULTS as EMPTY_RESULTS
from study_yunohost_holdout import ROOT, RUN
from study_yunohost_yarn_classic import RUN as YARN

MODULES = (
    "check_yunohost_bun_direct", "check_yunohost_npm_unresolved", "collect_consumer_pilot",
    "collect_yunohost_observations", "collect_yunohost_root_evidence",
    "compare_yunohost_npm_extractors", "consumer_holdout", "evaluate_consumer_pilot",
    "replay_yunohost_budgets", "replay_yunohost_consumer_results", "study_npm_parser_development",
    "study_pnpm_parser_development", "study_yunohost_holdout", "study_yunohost_yarn_classic",
    "study_yunohost_empty_declared_roots", "study_yunohost_empty_pnpm_roots", "verify_yunohost_empty_pnpm_roots",
    "verify_pnpm_registry_integrity", "verify_yunohost_holdout", "verify_yunohost_root_evidence",
    "verify_yunohost_yarn_classic",
)
README = """# Replication companion for the paired YunoHost consumer comparison

From the extracted directory, run with Python 3.10 or newer:

    python scripts/replay_yunohost_consumer_results.py
    python scripts/verify_yunohost_empty_pnpm_roots.py
    python scripts/study_yunohost_empty_declared_roots.py verify
    python scripts/check_yunohost_bun_direct.py verify
    python scripts/check_yunohost_npm_unresolved.py verify
    python scripts/replay_yunohost_budgets.py

The command starts from retained dependency paths and registry observations.
It recomputes exact-version joins, project classifications, and the paired
bounds before and after the Yarn Classic follow-up. It checks the primary
comparison, both cutoff alternatives, and the identical-portfolio control
against every retained project row and the manuscript table.
The second command reproduces the post hoc pnpm sensitivity from the
root declaration counts in the companion. The third checks the combined
empty-root analysis. The fourth recomputes the Bun direct joins, and the
fifth checks the npm evidence and the combined five-account bounds.
The sixth verifies both the paired summary and the exploratory budget
check from a wider projection of the retained registry memberships.
Pinned hashes identify the source files checked for these records.

The included registry projection keeps exact package and version keys, receipt
status, SHA-512 tokens and membership in the frozen portfolios as numeric
indices. Yarn rows also retain the dependency declarations and flags used by
the path verifier. The extraction outputs preserve completeness decisions
under the frozen rules. Re-extracting from the original package files or
verifying the original HTTP receipts requires the acquisition inputs.

The pinned source links, corroborated positive paths and checked location
counts for the five confirmed primary differences are in:

    research/consumer_holdout/runs/yunohost-yarn-classic/confirmed_cases.md

The archive covers the 215-project comparison and the follow-up analyses
reported in the manuscript table.
"""


def main():
    output = ROOT / "submission/emse/EMSE_Consumer_Replication.zip"
    filenames = ("paths.json.gz", "protocol.json", "registry_queue.json", "results.json")
    sources = [
        *(ROOT / f"scripts/{name}.py" for name in MODULES),
        *(folder / name for folder in (RUN, YARN) for name in filenames),
        REPLAY, CASES, EMPTY_PROTOCOL, EMPTY_RESULTS, ROOT_PROTOCOL, ROOT_RESULTS, BUN_RESULTS, NPM_RESULTS,
        BUDGET_DATA, BUDGET_RESULTS, TABLE, SUMMARY,
        ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex",
    ]
    with TemporaryDirectory(prefix="consumer-replay-") as directory:
        scratch = Path(directory)
        candidate = scratch / output.name
        with zipfile.ZipFile(candidate, "w", zipfile.ZIP_DEFLATED) as archive:
            archive.writestr("README.md", README)
            for path in sources:
                archive.write(path, path.relative_to(ROOT))
        extracted = scratch / "extracted"
        with zipfile.ZipFile(candidate) as archive:
            archive.extractall(extracted)
        checks = (("replay_yunohost_consumer_results",), ("verify_yunohost_empty_pnpm_roots",),
                  ("study_yunohost_empty_declared_roots", "verify"), ("check_yunohost_bun_direct", "verify"),
                  ("check_yunohost_npm_unresolved", "verify"), ("replay_yunohost_budgets",))
        for script, *arguments in checks:
            subprocess.run([sys.executable, "-I", "-c", "import runpy, sys; sys.path.insert(0, 'scripts'); "
                            "runpy.run_path(sys.argv.pop(1), run_name='__main__')", f"scripts/{script}.py",
                            *arguments],
                           cwd=extracted, check=True)
        output.write_bytes(candidate.read_bytes())
    print(f"Verified standalone companion: {output}")


if __name__ == "__main__":
    main()
