# Publication figures and editable sources

Figures use native vector drawings and retained measurements. PDF is embedded in LaTeX, SVG is editable, and PNG is a preview. The original illustrated architecture is preserved byte for byte.

| Conference figure | Stem | Evidence / role |
|---|---|---|
| 1 | study_system | Original measurement architecture and retained counts |
| 2 | source_multiplicity_compact | Remaining-source ECDF before and after budget-100 selections |
| 3 | objective_tradeoff | C/H curves at six budgets, analytic random expectation and additional budget-100 selections |
| 4 | coverage_partition | All-source exclusion, covered residual sources, and uncovered endpoints |
| 5 | representation_detail | Name/version pair mass, coverage and exposure |

The journal adds `observation_scope`, `graph_semantics`, `study_methodology`, `source_multiplicity`, `representation_matrix`, `q1_pareto_frontier`, `q1_supermodular_p`, and `q1_weight_sensitivity`, and uses the full source distribution instead of the compact conference variant. It contains twelve numbered figures in total.

`graph_semantics` is an illustrative version-splicing example. Other new plots use measured structural results or explicitly assumed weights. No figure establishes an installed tree, compromise probability, or deployed-control benefit. `observation_workflow`, `objective_mechanism`, and the former combined journal plot remain alternative or historical assets outside the active figure lists.

From the repository root:

```sh
python3 scripts/reconcile_full_manuscript.py
python3 manuscript/scripts/render_research_figures.py
python3 manuscript_q1/scripts/render_q1_figures.py
python3 scripts/verify_reconciled_papers.py
```

The shared renderer invokes `scripts/render_review_figures.py` for the new source distributions, representation matrix and observation diagram. Provenance appears in the manuscript result manifests and [the journal figure record](../../manuscript_q1/results/journal_figure_data.json).

Retained source histograms and every displayed matrix cell are checked against their inputs. Thirteen source-free endpoints are excluded from the ECDFs; H denominators follow the evaluation representation. Exact bibliography and figure labels are preserved without detector-oriented alterations. See [Report 20](../../reports/20_evidence_reconciliation_and_figures.md) for the final correction record and checks.
