# Comparison of the two generated endpoint assessments

Rule A and rule B each produced five categorical flags for 120 sampled endpoints. They share the same retained evidence. Rule B applies fixed overrides to some cases. Their 588 matching values across 600 comparisons describe similarity between two programs. No independent human agreement, reviewer accuracy or author approval can be estimated from this run.

| Criterion | Matching values | Differing values |
| --- | ---: | ---: |
| Repository mapping | 119 | 1 |
| Workflow presence | 120 | 0 |
| Installation directive | 117 | 3 |
| Lockfile presence | 120 | 0 |
| Dependency version example | 112 | 8 |

The historical run reconciled the twelve differing labels and used the resulting values in the weighted calculations. The machine-generated sheets, historical decision ledger, scenario labels and 180 transport rows are retained with their numerical provenance. [Scenario artifacts](../tasks/author_validation_2026-10-28/generated_evidence/)

The default endpoint transport now uses the original automated evidence. Human mode reads the independent input sheets separately. The active review status records zero completed human comparisons. Historical files bearing human-review output names at commit `eb62a6c0ee35` belong to the generated scenario. [Active status](../manuscript_q1/results/revision_validation/endpoint_audit/human_review_status.json)
