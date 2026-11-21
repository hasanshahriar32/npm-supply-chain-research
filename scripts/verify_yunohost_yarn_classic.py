#!/usr/bin/env python3
"""Audit the follow-up pair ledger and reconcile the manuscript table."""
from collections import Counter
import gzip
import json

from study_yunohost_yarn_classic import (
    GRAPH, LEDGER, ROOT, RUN, baseline, read, read_ledger, sha, verify_protocol,
)


def verify():
    records = read_ledger(verify_protocol())
    followup = read(RUN / "results.json")
    original_path = baseline.RUN / "results.json"
    original = read(original_path)
    assert followup["prior_results_sha256"] == sha(original_path)
    assert followup["paths_sha256"] == sha(GRAPH) and followup["registry_ledger_sha256"] == sha(LEDGER)
    assert len(records) == followup["registry_requests"]
    assert followup["usable_maintainer_lists"] == sum(
        r["status"] == "observed" and r["accounts"] is not None for r in records
    )
    graphs = json.loads(gzip.decompress(GRAPH.read_bytes()))
    yarn_ids = {g["sample_id"] for g in graphs}
    assert len(yarn_ids) == len(graphs) == followup["yarn_candidates"] == 35

    resolved_deltas = {}
    contrasts = followup["comparisons"]
    table = (ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    for key, comparison in contrasts.items():
        prior = original["comparisons"][key]
        project_deltas, cells = [], Counter()
        for before, after in zip(prior["projects"], comparison["projects"], strict=True):
            assert before["sample_id"] == after["sample_id"]
            if after["sample_id"] in yarn_ids:
                assert before["documented"] == [0, 0]
                allowed = [pair for pair in before["feasible"]
                           if all(value >= hit for value, hit in zip(pair, after["documented"], strict=True))]
                assert after["feasible"] == allowed
            else:
                assert before == after
            cells["".join(map(str, after["documented"]))] += 1
            project_deltas.append({v - n for n, v in after["feasible"]})
        n = len(project_deltas)
        assert n == followup["denominator"] == original["denominator"] == 215
        assert comparison["documented_cells"] == {cell: cells[cell] for cell in ("00", "01", "10", "11")}
        assert comparison["resolved_pairs"] == sum(len(row["feasible"]) == 1 for row in comparison["projects"])
        for field, transform in (("turnover_bounds", abs), ("net_bounds", int)):
            limits = [{transform(d) for d in deltas} for deltas in project_deltas]
            assert comparison[field] == [sum(min(d) for d in limits) / n, sum(max(d) for d in limits) / n]
        resolved_deltas[key] = comparison["resolved_pairs"] - prior["resolved_pairs"]

    assert contrasts["identical_control"]["turnover_bounds"] == contrasts["identical_control"]["net_bounds"] == [0, 0]
    versions = [contrasts[f"version_{i}"] for i in range(1, 4)]
    resolved = " & ".join(str(r["resolved_pairs"]) for r in versions)
    assert "Follow-up resolved pairs & " + resolved + r"\\" in table
    for label, field in ((r"Follow-up turnover (\%)", "turnover_bounds"), ("Follow-up net change (pp)", "net_bounds")):
        values = [f"$[{100 * lo:.1f},{100 * hi:.1f}]$" for lo, hi in (r[field] for r in versions)]
        assert " & ".join([label, *values]) + r"\\" in table

    print(json.dumps({"checks": "passed", "rows": followup["denominator"], "additional_resolved": resolved_deltas}, indent=2))


if __name__ == "__main__":
    verify()
