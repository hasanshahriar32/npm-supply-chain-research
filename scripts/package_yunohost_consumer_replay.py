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
from replay_selfhosted_comparison import INPUTS as SELFHOSTED_FILES, RUN as SELFHOSTED_RUN
from replay_selfhosted_comparison import PROJECTION as SELFHOSTED_PROJECTION, RESULT as SELFHOSTED_RESULT
from replay_yunohost_budgets import PROJECTION as BUDGET_DATA, RESULTS as BUDGET_RESULTS, SUMMARY, TABLE
from study_yunohost_empty_declared_roots import PROTOCOL as ROOT_PROTOCOL, RESULTS as ROOT_RESULTS
from study_yunohost_empty_pnpm_roots import PROTOCOL as EMPTY_PROTOCOL, RESULTS as EMPTY_RESULTS
from study_yunohost_holdout import ROOT, RUN
from study_yunohost_yarn_classic import RUN as YARN
import study_selfhosted_lockfile_followup as SELFHOSTED_LOCKS
import study_selfhosted_registry_extension as SELFHOSTED_REGISTRY
import study_selfhosted_yarn_evidence as SELFHOSTED_YARN
from check_consumer_pair_support import OUTPUT as SUPPORT_RESULTS
from check_selfhosted_modern_yarn_roots import RESULT as MODERN_YARN_RESULTS

MODULES = (
    "check_yunohost_bun_direct", "check_yunohost_npm_unresolved", "collect_consumer_pilot",
    "collect_yunohost_observations", "collect_yunohost_root_evidence",
    "compare_yunohost_npm_extractors", "consumer_holdout", "evaluate_consumer_pilot",
    "replay_selfhosted_comparison", "replay_yunohost_budgets", "replay_yunohost_consumer_results",
    "study_npm_parser_development",
    "study_pnpm_parser_development", "study_yunohost_holdout", "study_yunohost_yarn_classic",
    "study_yunohost_empty_declared_roots", "study_yunohost_empty_pnpm_roots", "verify_yunohost_empty_pnpm_roots",
    "verify_pnpm_registry_integrity", "verify_yunohost_holdout", "verify_yunohost_root_evidence",
    "verify_yunohost_yarn_classic",
    "study_selfhosted_lockfile_followup", "study_selfhosted_registry_extension",
    "study_selfhosted_yarn_evidence", "collect_yarn_registry", "check_consumer_pair_support",
    "check_selfhosted_modern_yarn_roots",
)
README = """# Replication companion for the paired consumer comparisons

From the extracted directory, run with Python 3.10 or newer:

    python scripts/replay_yunohost_consumer_results.py
    python scripts/verify_yunohost_empty_pnpm_roots.py
    python scripts/study_yunohost_empty_declared_roots.py verify
    python scripts/check_yunohost_bun_direct.py verify
    python scripts/check_yunohost_npm_unresolved.py verify
    python scripts/replay_yunohost_budgets.py
    python scripts/replay_selfhosted_comparison.py
    python scripts/study_selfhosted_lockfile_followup.py verify
    python scripts/study_selfhosted_registry_extension.py verify
    python scripts/study_selfhosted_yarn_evidence.py verify
    python scripts/check_consumer_pair_support.py verify
    python scripts/check_selfhosted_modern_yarn_roots.py verify

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
The seventh verifies all four frozen Awesome-Selfhosted comparisons
and recomputes its empty-root sensitivity and six-budget comparison.
The next three validate the npm and pnpm follow-ups and the Yarn Classic
follow-up from the retained paths and dated observations. The last two
recount the pairs by root evidence and verify the modern Yarn empty roots.
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

The archive covers both the 215-project YunoHost and 155-project
Awesome-Selfhosted comparisons and their reported follow-ups.
"""


def main():
    output = ROOT / "submission/emse/EMSE_Consumer_Replication.zip"
    filenames = ("paths.json.gz", "protocol.json", "registry_queue.json", "results.json")
    sources = [
        *(ROOT / f"scripts/{name}.py" for name in MODULES),
        *(folder / name for folder in (RUN, YARN) for name in filenames),
        REPLAY, CASES, EMPTY_PROTOCOL, EMPTY_RESULTS, ROOT_PROTOCOL, ROOT_RESULTS, BUN_RESULTS, NPM_RESULTS,
        BUDGET_DATA, BUDGET_RESULTS, TABLE, SUMMARY,
        *(SELFHOSTED_RUN / name for name in SELFHOSTED_FILES),
        SELFHOSTED_PROJECTION, SELFHOSTED_RESULT,
        SELFHOSTED_LOCKS.TRACES, SELFHOSTED_LOCKS.RESULTS,
        SELFHOSTED_REGISTRY.QUEUE, SELFHOSTED_REGISTRY.PROJECTED, SELFHOSTED_REGISTRY.RESULT,
        SELFHOSTED_YARN.PROTOCOL, SELFHOSTED_YARN.TRACES, SELFHOSTED_YARN.QUEUE, SELFHOSTED_YARN.PROJECTED,
        SELFHOSTED_YARN.RESULTS, SUPPORT_RESULTS, MODERN_YARN_RESULTS, ROOT / "scripts/consumer_yarn_classic.cjs",
        ROOT / "scripts/consumer_npm_development.cjs", ROOT / "scripts/consumer_pnpm_development.cjs",
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
                  ("check_yunohost_npm_unresolved", "verify"), ("replay_yunohost_budgets",),
                  ("replay_selfhosted_comparison",), ("study_selfhosted_lockfile_followup", "verify"),
                  ("study_selfhosted_registry_extension", "verify"), ("study_selfhosted_yarn_evidence", "verify"),
                  ("check_consumer_pair_support", "verify"), ("check_selfhosted_modern_yarn_roots", "verify"))
        for script, *arguments in checks:
            subprocess.run([sys.executable, "-I", "-c", "import runpy, sys; sys.path.insert(0, 'scripts'); "
                            "runpy.run_path(sys.argv.pop(1), run_name='__main__')", f"scripts/{script}.py",
                            *arguments],
                           cwd=extracted, check=True)
        output.write_bytes(candidate.read_bytes())
    print(f"Verified standalone companion: {output}")


if __name__ == "__main__":
    main()
