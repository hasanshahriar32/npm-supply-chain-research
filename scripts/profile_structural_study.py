#!/usr/bin/env python3
"""Measure repeated full offline runs without overwriting scientific artifacts."""
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import statistics
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/study_structural_interventions.py"
REFERENCE = ROOT / "manuscript/results/structural_interventions/results.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    trials = []
    for repetition in range(3):
        with tempfile.TemporaryDirectory(prefix="npm-profile-") as directory:
            command = [sys.executable, str(SCRIPT), "--output", directory]
            started = time.perf_counter()
            with tempfile.TemporaryFile(mode="w+") as log:
                process = subprocess.Popen(command, cwd=ROOT, stdout=log, stderr=subprocess.STDOUT)
                _, status, usage = os.wait4(process.pid, 0)
                process.returncode = os.waitstatus_to_exitcode(status)
                elapsed = time.perf_counter() - started
                if process.returncode:
                    log.seek(0)
                    raise RuntimeError(log.read())
            result = Path(directory) / "results.json"
            if digest(result) != digest(REFERENCE):
                raise RuntimeError("Profiled scientific results differ from the frozen study")
            trials.append({"repetition": repetition + 1, "wall_seconds": elapsed,
                "user_cpu_seconds": usage.ru_utime, "system_cpu_seconds": usage.ru_stime,
                "peak_rss_kib_linux": usage.ru_maxrss,
                "scientific_results_equal_frozen": True})
            print(f"Run {repetition+1}: {elapsed:.2f} s, {usage.ru_maxrss/1024:.1f} MiB peak RSS", flush=True)
    wall = [r["wall_seconds"] for r in trials]
    report = {"profiled_at_utc": datetime.now(timezone.utc).isoformat(),
        "scope": "Complete offline structural study: extraction, graph construction, all baselines, 200 random orders, sensitivities and output serialization",
        "repetitions": trials, "wall_seconds_mean": statistics.mean(wall),
        "wall_seconds_sample_sd": statistics.stdev(wall),
        "wall_seconds_min": min(wall), "wall_seconds_max": max(wall),
        "peak_rss_mib_max": max(r["peak_rss_kib_linux"] for r in trials) / 1024,
        "environment": {"python": sys.version, "platform": platform.platform(),
            "machine": platform.machine(), "logical_cpu_count": os.cpu_count()},
        "network_requests": 0, "npm_payloads_executed": 0,
        "source_sha256": {str(SCRIPT.relative_to(ROOT)): digest(SCRIPT),
            "scripts/profile_structural_study.py": digest(Path(__file__)),
            "data/npm_ecosystem.db.zip": digest(ROOT / "data/npm_ecosystem.db.zip")},
        "reference_results_sha256": digest(REFERENCE),
        "limitations": ["Three repeated executions on one host; descriptive resource measurements, not a population confidence interval.",
            "Filesystem and OS caches are warm and uncontrolled; no cold-start or parallel-load claim.",
            "Total process runtime and peak RSS, not per-package inference latency, API collection cost, or deployed triage cost.",
            "No LLM is called by the measured study; development assistance cost is outside the measured process."]}
    target = ROOT / "manuscript/results/structural_interventions/performance_profile.json"
    target.write_text(json.dumps(report, indent=2) + "\n")
    print(f"Saved {target.relative_to(ROOT)}", flush=True)


if __name__ == "__main__":
    main()
