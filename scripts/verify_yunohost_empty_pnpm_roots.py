#!/usr/bin/env python3
"""Check the empty-root sensitivity from released declaration observations."""
from study_yunohost_empty_pnpm_roots import (
    INITIAL, PROTOCOL, RESULTS, candidates, check_bounds, inputs,
)


def verify():
    protocol = INITIAL.read(PROTOCOL)
    result = INITIAL.read(RESULTS)
    assert protocol["inputs"] == inputs()
    assert result["protocol_sha256"] == INITIAL.sha(PROTOCOL)
    observations = result["observations"]
    assert [row["sample_id"] for row in observations] == protocol["projects"] == candidates()
    supported = {row["sample_id"] for row in observations
                 if row["manifest"]["dependencies"] == row["root_importer"]["dependencies"] == 0}
    assert sorted(supported) == result["verified_empty_roots"]
    assert check_bounds(supported) == result["comparisons"]
    columns = [result["comparisons"][f"version_{i}"] for i in range(1, 4)]
    table = (INITIAL.ROOT / "manuscript_q1/tables/yunohost_consumer_holdout_table.tex").read_text()
    resolved = " & ".join(str(column["resolved_pairs"]) for column in columns)
    assert "Sensitivity resolved pairs & " + resolved + r"\\" in table
    for label, field in ((r"Sensitivity turnover (\%)", "turnover_bounds"),
                         ("Sensitivity net change (pp)", "net_bounds")):
        values = [f"$[{100 * lo:.1f},{100 * hi:.1f}]$" for lo, hi in (column[field] for column in columns)]
        assert " & ".join([label, *values]) + r"\\" in table
    print(f"Reproduced empty-root sensitivity with {len(supported)} corroborated common negatives")


if __name__ == "__main__":
    verify()
