#!/usr/bin/env python3
"""Compare path extraction on the same pinned npm inputs, before account matching."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import gzip
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

from study_yunohost_holdout import CAPTURE, ROOT, RUN, choose_npm, inputs, read, sha, write

REFERENCE = ROOT / "scripts/compare_consumer_parsers.cjs"


def locations(witnesses):
    return {(w["location"], w["package"], w["version"]) for w in witnesses}


def previous_reader(row):
    folder = CAPTURE / "projects" / row["frame_id"]
    if read(folder / "package.json").get("workspaces") is not None:
        return "workspace_unsupported", set()
    lock = choose_npm(row)
    if lock is None:
        return "ambiguous_npm_precedence", set()
    with tempfile.TemporaryDirectory(prefix="compare-yuno-npm-") as tmp:
        for filename in ("package.json", lock):
            shutil.copyfile(folder / filename, Path(tmp) / filename)
        cmd = ["node", str(REFERENCE), shutil.which("npm"), tmp, lock, "--include-rejected"]
        try:
            proc = subprocess.run(cmd, check=True, capture_output=True, text=True, timeout=90)
        except subprocess.SubprocessError:
            return "parser_error", set()
    output = json.loads(proc.stdout)
    return output["status"], locations(output.get("witnesses", []))


def main():
    rows = [row for row, state in inputs() if state["status"] == "npm_file_available"]
    trace_file = RUN / "paths.json.gz"
    assert sha(trace_file) == read(RUN / "registry_queue.json")["paths_sha256"]
    traces = {row["sample_id"]: row for row in json.loads(gzip.decompress(trace_file.read_bytes()))}
    summary = Counter()
    ledger = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for row, (status, old) in zip(rows, pool.map(previous_reader, rows), strict=True):
            sid = row["frame_id"]
            new = locations(traces[sid]["witnesses"])
            counts = {"both": len(old & new), "previous_only": len(old - new), "expanded_only": len(new - old)}
            ledger.append({"sample_id": sid, "previous_status": status, "expanded_status": traces[sid]["status"],
                           "locations": counts})
            summary.update(counts)
            summary.update({"previous_projects": int(bool(old)), "expanded_projects": int(bool(new)),
                            "previous_only_projects": int(bool(old) and not new),
                            "expanded_only_projects": int(bool(new) and not old)})
    result = {"npm_candidates": len(rows), "summary": dict(summary), "paths_sha256": sha(trace_file),
              "previous_comparator_sha256": sha(REFERENCE), "projects": ledger}
    write(RUN / "npm_extractor_comparison.json", result)
    print(result["summary"])


if __name__ == "__main__":
    main()
