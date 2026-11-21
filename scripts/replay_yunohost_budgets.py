#!/usr/bin/env python3
"""Replay the exploratory budget comparison on frozen YunoHost evidence."""
import argparse
from collections import Counter
import gzip
import json

import check_yunohost_npm_unresolved as npm
from replay_yunohost_consumer_results import REPLAY, read_graphs, registry_index

INITIAL = npm.INITIAL
YARN = npm.bun.FOLLOWUP
ROOT = INITIAL.ROOT
RUN = INITIAL.RUN.with_name("yunohost-budget-sensitivity")
PROJECTION = RUN / "membership_projection.json.gz"
RESULTS = RUN / "results.json"
BUDGETS = (1, 5, 10, 25, 50, 100)
TABLE = ROOT / "manuscript_q1/tables/yunohost_budget_sensitivity.tex"
SUMMARY = ROOT / "manuscript_q1/tables/yunohost_paired_summary.tex"


def bindings():
    paths = (REPLAY, npm.bun.TRACES, YARN.GRAPH, npm.bun.PAIRS,
             npm.RESULTS, npm.bun.EMPTY_RESULTS, npm.bun.PNPM_RESULTS, npm.bun.RESULTS)
    return {str(p.relative_to(ROOT)): INITIAL.sha(p) for p in paths}


def export():
    graph = INITIAL.read(INITIAL.INCIDENCE)
    assert INITIAL.sha(INITIAL.INCIDENCE) == INITIAL.FROZEN
    orders = {kind: graph[f"orders_{kind}"]["exact_union"][:max(BUDGETS)] for kind in ("name", "version")}
    members = {graph["maintainers"][i]: i for order in orders.values() for i in order}
    projected = read_graphs(REPLAY)
    initial = INITIAL.read_collection("registry")
    later = YARN.read_ledger(YARN.verify_protocol())
    memberships = {}
    for key, rows in (("initial", initial), ("yarn", later)):
        output = []
        for index, (receipt, reference) in enumerate(zip(rows, projected[key], strict=True)):
            assert all(receipt[k] == reference[k] for k in ("package", "version", "status"))
            if receipt["status"] == "observed":
                assert (receipt["accounts"] is None) == (reference["accounts"] is None)
                if receipt["accounts"] is not None:
                    values = sorted(members[a] for a in receipt["accounts"] if a in members)
                    if values:
                        output.append([index, values])
        memberships[key] = output
    RUN.mkdir(exist_ok=True)
    data = {"input_sha256": bindings(), "training_sha256": INITIAL.FROZEN,
            "orders": orders, "memberships": memberships}
    PROJECTION.write_bytes(gzip.compress(json.dumps(data, separators=(",", ":")).encode(), mtime=0))
    INITIAL.write(RESULTS, score())
    TABLE.write_text(budget_table(INITIAL.read(RESULTS)["budgets"]))
    SUMMARY.write_text(primary_table())


def common_zeros():
    return set(INITIAL.read(npm.RESULTS)["additional_common_negatives"]) | set(
        INITIAL.read(npm.bun.EMPTY_RESULTS)["additional_common_negatives"]
    ) | set(INITIAL.read(npm.bun.PNPM_RESULTS)["verified_empty_roots"])


def score():
    data = read_graphs(PROJECTION)
    assert data["input_sha256"] == bindings() and data["training_sha256"] == INITIAL.FROZEN
    observations = read_graphs(REPLAY)
    selected = set().union(*data["orders"].values())
    assert all(len(order) == len(set(order)) == max(BUDGETS) for order in data["orders"].values())
    original = INITIAL.read(INITIAL.RUN / "protocol.json")["portfolio_fingerprints"]
    for kind, key in (("name", "name"), ("version", "version_1")):
        five = sorted(data["orders"][kind][:5])
        assert INITIAL.digest(json.dumps(five).encode()) == original[key]

    indexes = {}
    for key, directory in (("initial", INITIAL.RUN), ("yarn", YARN.RUN)):
        rows = observations[key]
        added = dict(data["memberships"][key])
        assert len(added) == len(data["memberships"][key])
        for i, members in added.items():
            assert 0 <= i < len(rows) and members and set(members) <= selected
            assert rows[i]["status"] == "observed" and rows[i]["accounts"] is not None
        for i, row in enumerate(rows):
            if row.get("accounts") is not None:
                row["accounts"] = added.get(i, [])
        indexes[key] = registry_index(rows, directory)

    initial, _ = INITIAL.frame_paths(read_graphs(npm.bun.TRACES), indexes["initial"])
    followup = {g["sample_id"]: YARN.witnesses(g, indexes["yarn"])[0] for g in read_graphs(YARN.GRAPH)}
    zeros = common_zeros()
    observations = [(row[0], set(), True, 0) if row[0] in zeros else followup.get(row[0], row)
                    for row in initial]
    results = {}
    for budget in BUDGETS:
        name, version = (set(data["orders"][k][:budget]) for k in ("name", "version"))
        paired = INITIAL.paired(observations, name, version)
        differences = {row["sample_id"]: row["feasible"][0] for row in paired["projects"]
                       if len(row["feasible"]) == 1 and sum(row["feasible"][0]) == 1}
        results[str(budget)] = {"shared_accounts": len(name & version), "confirmed_differences": differences,
                                **{key: paired[key] for key in ("resolved_pairs", "turnover_bounds", "net_bounds")}}
    return {"scope": "Exploratory retrospective use of the frozen additive orders. Retained npm, pnpm and "
                     "Yarn Classic evidence and corroborated empty roots. The Bun join is scoped to the "
                     "original portfolios and is excluded across all six budgets.",
            "denominator": len(observations), "projection_sha256": INITIAL.sha(PROJECTION), "budgets": results}


def budget_table(budgets):
    lines = [r"\begin{table}[t]", r"\centering", r"\footnotesize",
             r"\caption{Exploratory budget check on the common evidence scope. Shared counts refer to accounts in both portfolios. Bounds give turnover as a percentage of 215 projects.}",
             r"\label{tab:consumer_budget_check}", r"\begin{tabularx}{\linewidth}{@{}Yrrrr@{}}", r"\toprule",
             r"Budget & Shared & Resolved & Changes & Bounds (\%)\\", r"\midrule"]
    for b, r in budgets.items():
        lo, hi = r["turnover_bounds"]
        lines.append(f"{b} & {r['shared_accounts']} & {r['resolved_pairs']} & {len(r['confirmed_differences'])} & "
                     rf"$[{100*lo:.1f},{100*hi:.1f}]$" + r"\\")
    return "\n".join(lines + [r"\bottomrule", r"\end{tabularx}", r"\end{table}", ""])


def primary_table():
    yarn = INITIAL.read(npm.bun.PAIRS)["comparisons"]["version_1"]
    fixed = Counter(tuple(r["feasible"][0]) for r in yarn["projects"] if len(r["feasible"]) == 1)
    fixed[0, 0] += len(common_zeros())
    for source in (npm.bun.RESULTS, npm.RESULTS):
        fixed[1, 1] += sum({"name", "version_1"}.issubset(r["covered_by"])
                           for r in INITIAL.read(source)["registry_join"])
    resolved = INITIAL.read(npm.RESULTS)["comparisons"]["version_1"]["resolved_pairs"]
    assert sum(fixed.values()) == resolved
    return "\n".join([
        r"\begin{table}[t]", r"\centering", r"\footnotesize",
        r"\caption{Paired outcomes for the frozen five-account contrast on YunoHost after the evidence follow-ups.}",
        r"\label{tab:consumer_paired_summary}", r"\begin{tabularx}{\linewidth}{@{}Yr@{}}", r"\toprule",
        r"Paired outcome & Projects\\", r"\midrule",
        *[f"{label} & {fixed[n, v]}" + r"\\" for label, n, v in (
            ("Both portfolios", 1, 1), ("Neither portfolio", 0, 0), ("Name portfolio only", 1, 0),
            ("Version portfolio only", 0, 1))],
        f"Unresolved & {len(yarn['projects'])-resolved}" + r"\\",
        r"\bottomrule", r"\end{tabularx}", r"\end{table}", "",
    ])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--export", action="store_true")
    if parser.parse_args().export:
        export()
    else:
        result = INITIAL.read(RESULTS)
        assert result == score()
        assert TABLE.read_text() == budget_table(result["budgets"])
        assert SUMMARY.read_text() == primary_table()
        print("Reproduced the six-budget comparison and the 215-project paired summary")
