#!/usr/bin/env python3
"""Validate source binding, generated quantities, and reference completeness."""
import hashlib
import json
from pathlib import Path
import re
import sys

PAPER = Path(__file__).resolve().parents[1]
ROOT = PAPER.parent
data = json.loads((PAPER / "results/artifact_audit.json").read_text())
failures = []
# The prose reports a specific study, not whatever inputs happen to exist later.
pinned_archives = {
    "data/metrics_summary.csv.zip": "43e1845a106719ef9fb8c7d72d174959cc25e6f8fe8a3c6bfcd6cb7ca8e90a35",
    "data/npm_ecosystem.db.zip": "ab45439cf94cf43f3133b0aaff644557d55e86e99430a0a7937bfd0ce5266315",
}
for name, expected in pinned_archives.items():
    if data["sources_sha256"].get(name) != expected:
        failures.append(f"Study archive changed; review manuscript prose before updating the pinned study: {name}")
expected_temporal = {"ledger_records": 47, "family_identifiers": 31, "retained_source_objects": 45,
                    "retained_family_identifiers": 30, "declared_edges": 258}
for field, expected in expected_temporal.items():
    if data["temporal_inventory"][field] != expected:
        failures.append(f"Temporal count changed; revise manuscript prose: {field}")
for name, expected in data["sources_sha256"].items():
    path = ROOT / name
    if not path.exists():
        failures.append(f"Missing repository audit input: {name}")
    elif hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        failures.append(f"Audit input changed; rerun audit: {name}")
if any(data["database_recomputation_mismatches"].values()):
    failures.append("Database metrics no longer reproduce; revise paper claims")
if data["roi_mismatches_after_rounding_database_to_six_decimals"] != data["cross_archive_mismatched_packages_by_field"]["attacker_roi"]:
    failures.append("Rounding changes score mismatch interpretation")
if data["temporal_inventory"]["source_time_after_cutoff_rows"]:
    failures.append("Temporal inventory includes post-cutoff source timestamp")
content = "\n".join(p.read_text() for p in PAPER.rglob("*.tex") if "build" not in p.parts)
bib = (PAPER / "bibliography/references.bib").read_text()
keys = set(re.findall(r"@\w+\s*\{\s*([^,]+),", bib))
citations = {key.strip() for block in re.findall(r"\\cite(?:\[[^\]]*\])?\{([^}]+)\}", content) for key in block.split(",")}
for key in sorted(citations-keys):
    failures.append(f"Undefined citation: {key}")
for relative in re.findall(r"\\input\{([^}]+)\}", content):
    if not (PAPER / (relative+".tex")).exists():
        failures.append(f"Missing TeX input: {relative}")
for relative in re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}", content):
    if not (PAPER / "figures" / relative).exists():
        failures.append(f"Missing figure: {relative}")
macros = (PAPER / "results/numbers.tex").read_text()
for name, expected in {"PackageCount":data["population"], "ReviewBudget":data["review_budget"],
    "DBReachPositive": data["database_summary"]["blast_radius"]["nonzero"],
    "ScoreQueueIntersection": data["cross_archive_queues"]["legacy_score"]["intersection"]}.items():
    if "\\newcommand{\\"+name+"}{"+f"{expected:,}"+"}" not in macros:
        failures.append(f"Generated numeric macro is stale: {name}")
if failures:
    print("\n".join(failures), file=sys.stderr)
    sys.exit(1)
print(f"Verified {len(data['sources_sha256'])} source hashes, seven metric fields, generated values, {len(citations)} citations, and TeX inputs/figures.")
