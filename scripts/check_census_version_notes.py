"""Offline consistency check of recorded dependency-version examples from Report 27."""
import csv
import hashlib
import json
import re
import shutil
import subprocess
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/full_census/census_audit_labels.csv"
OUT = ROOT / "research/consumer_evaluation/census_note_check.json"
NOTE = re.compile(r"Version: '.*?' \((?:dependencies|devDependencies|peerDependencies) '(.*?)'\) resolved to '(.*?)' in (\S+) ")
CHECK = """
const req = require('node:module').createRequire(require('node:fs').realpathSync(process.argv[1]));
const semver = req('semver');
const pairs = JSON.parse(require('node:fs').readFileSync(0, 'utf8'));
const statuses = pairs.map(([range, version]) => {
    if (semver.validRange(range) === null || !semver.valid(version)) return 'unassessable';
    return semver.satisfies(version, range) ? 'in_range' : 'outside_range';
});
console.log(JSON.stringify({version: req('semver/package.json').version, statuses}));
"""


def main():
    with SOURCE.open(newline="") as f:
        rows = list(csv.DictReader(f))
    records = []
    for row in rows:
        if row["dependency_version_supported"] == "supported":
            match = NOTE.search(row["evidence_notes"])
            if not match:
                raise ValueError(f"Unrecognized positive note in {row['audit_id']}")
            records.append(match.groups())
    proc = subprocess.run(["node", "-e", CHECK, shutil.which("npm")], check=True,
                          input=json.dumps(records), capture_output=True, text=True)
    output = json.loads(proc.stdout)
    grouped = defaultdict(Counter)
    for record, status in zip(records, output["statuses"], strict=True):
        grouped[record[2]][status] += 1
    result = {"unit": "one recorded example per machine-positive census row",
              "input_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
              "node_semver_version": output["version"], "census_rows": len(rows),
              "positive_notes": len(records), "totals": dict(Counter(output["statuses"])),
              "by_lockfile": grouped}
    OUT.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")


if __name__ == "__main__":
    main()
