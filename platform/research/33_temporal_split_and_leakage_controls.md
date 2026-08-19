# Temporal Split and Leakage Controls

## Core rule

For every package scored at observation time \(t\), every feature must be constructed from information observable no later than \(t\). The target event must occur after \(t\) within a pre-specified horizon.

## Recommended evaluation timeline

Use rolling-origin evaluation rather than a single split:

| Split | Feature cutoff | Label window | Purpose |
|---|---|---|---|
| Development | Earlier historical dates | Subsequent fixed windows | Feature and model design |
| Validation | Later historical date | Subsequent window | Hyperparameter and threshold selection |
| Final test | Latest pre-registered cutoff | Future incident window | One-time final evaluation |
| Prospective holdout | After final test if available | Future observations | Optional monitoring evaluation |

The exact dates should be chosen after inspecting data availability but before final model fitting. If incident dates determine the cutoff, document that choice and avoid tuning to the final target event.

## Leakage checklist

| Potential leakage | Control |
|---|---|
| Current dependency graph used for historical ranking | Reconstruct or retrieve graph as of the historical cutoff |
| Current maintainer ownership used for past scores | Use historical registry snapshots or restrict claims to present-day ranking |
| Current GitHub workflow state used for past incidents | Use commit history or historical workflow snapshots; otherwise mark feature unavailable |
| Advisory text published after the cutoff used as a feature | Exclude advisory content from pre-incident features |
| Package removal or deprecation status used before removal | Treat as post-incident information |
| Incident package name used to engineer features | Exclude incident-specific indicators and known malicious dependency names |
| Label propagation through shared campaigns | Split by campaign family and time; do not place linked versions across train and test casually |
| Popularity measured after incident | Use time-stamped download or dependent-count observations |
| Duplicate versions or aliases across splits | Group by package family and incident family where appropriate |
| Model selection on final test ranks | Freeze the test protocol before inspecting results |

## Feature availability ledger

Every feature should have a record:

| Field | Description |
|---|---|
| `feature_name` | Stable feature identifier |
| `source_system` | npm, deps.dev, GitHub, OSV, incident review, derived |
| `observed_at` | When the source observation was retrieved or committed |
| `effective_at` | When the observation became true or available |
| `cutoff_rule` | How the feature is filtered for a historical score |
| `historical_fidelity` | exact, reconstructed, approximate, current-only |
| `leakage_risk` | low, medium, high |
| `notes` | Missingness or resolution caveats |

## Historical fidelity levels

- **Exact:** the source provides a historical snapshot or commit-level reconstruction.
- **Reconstructed:** the state is rebuilt from dated events with documented assumptions.
- **Approximate:** current or coarse data are used as a proxy for a historical state.
- **Current-only:** no valid historical reconstruction exists; use only for descriptive analysis, not temporal prediction.

A result based materially on approximate or current-only features must not be described as a strict pre-incident back-test.

## Robustness analyses

Run the primary experiment under at least two feature-fidelity regimes: strict historical features only, and a broader approximate regime. Report the performance difference. If the conclusion changes, the strict regime controls the main claim.

Perform package-family and incident-family grouping where shared code, maintainers, or campaign artifacts could cause correlated records. Keep an untouched final test period and do not select the best split after reviewing final results.

## Reporting language

Use “out-of-time evaluation” only when the feature cutoff and label window are genuinely separated. Use “historical reconstruction” when workflow or ownership state is inferred from dated commits. Use “case study” when the sample is too small for a general predictive claim.
