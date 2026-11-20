# Generated endpoint assessments

`rule_a.csv` and `rule_b.csv` contain deterministic computer-generated assessments. Their labels reproduce the machine sheets first recorded in commit `eb62a6c0ee35`. The rule B notes now identify its fixed overrides as simulated. Regenerate them with the two build scripts in the parent directory. Both programs write exclusively to this directory.

`scenario_disagreements.csv` retains the twelve decisions recorded in the legacy reconciliation ledger. Its reviewer columns refer to the two generated variants. The ledger does not establish independent human adjudication. `scenario_labels.json`, `scenario_comparison.json`, the two transport tables and `scenario_summary.json` preserve that run's numerical results for provenance. The 588 matches measure similarity between generated outputs.
