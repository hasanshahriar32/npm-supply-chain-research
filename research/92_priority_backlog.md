# Priority Backlog

## P0 — Research validity before model complexity

| ID | Task | Output | Dependency |
|---|---|---|---|
| P0.1 | Freeze the research question and terminology | Approved RQ and definitions | None |
| P0.2 | Create version-level incident-label registry | `labels_compromise_v01.csv` and evidence notes | Source audit |
| P0.3 | Define observation dates and label windows | `configs/temporal_splits.yaml` | Label registry |
| P0.4 | Build feature-availability ledger | `manifests/feature_availability.csv` | Data provenance |
| P0.5 | Standardize database paths and CLI configuration | Updated collection scripts | Current repository |

## P1 — Benchmark foundation

| ID | Task | Output | Dependency |
|---|---|---|---|
| P1.1 | Implement version-aware dependency resolution | Resolved package-version graph | P0.3 |
| P1.2 | Add population and sampling report | Coverage and missingness report | P0.3 |
| P1.3 | Add maintainer aggregation variants | Max, sum, concentration, recency features | P0.4 |
| P1.4 | Parse workflow-security features | Permissions, triggers, actions, OIDC, runners, missingness | P0.4 |
| P1.5 | Add popularity and activity controls | Time-valid controls | P0.4 |
| P1.6 | Build baseline runner | Popularity, graph, maintainer, workflow, tabular models | P1.1–P1.5 |

## P2 — Evaluation and robustness

| ID | Task | Output | Dependency |
|---|---|---|---|
| P2.1 | Implement rolling-origin evaluation | Metrics and rank outputs | P1.6 |
| P2.2 | Add incident-level confidence intervals | Bootstrap or hierarchical uncertainty | P2.1 |
| P2.3 | Run feature-family ablations | Ablation tables and plots | P2.1 |
| P2.4 | Run resolution and missingness sensitivity | Robustness report | P2.1 |
| P2.5 | Measure calibration and review cost | Reliability and budget curves | P2.1 |

## P3 — Graph learning

| ID | Task | Output | Dependency |
|---|---|---|---|
| P3.1 | Implement homogeneous graph baseline | Reproducible graph model | P2.1 |
| P3.2 | Implement HeteroData builder | Typed graph artifact | P1.1–P1.4 |
| P3.3 | Implement HGAT/HAN candidate | Training and inference code | P3.2 |
| P3.4 | Compare seeds, graph truncation, and negative construction | Variance and stability report | P3.3 |
| P3.5 | Compare interpretability and cost | Model-selection memo | P3.4 |

## P4 — Publication and operationalization

| ID | Task | Output | Dependency |
|---|---|---|---|
| P4.1 | Freeze final test protocol | Signed experiment manifest | P2.1–P3.5 |
| P4.2 | Run final out-of-time evaluation | Final results package | P4.1 |
| P4.3 | Write paper and limitations | Draft manuscript | P4.2 |
| P4.4 | Release safe artifacts and checksums | Reproducibility bundle | P4.2 |
| P4.5 | Consider prospective monitoring | Optional prototype | Publication-ready benchmark |

## Suggested first experiment

Before implementing HGAT, run a small, fully auditable experiment on the current snapshot and a manually reviewed subset of historical labels. Compare:

- transitive dependent count;
- maintainer maximum reach;
- workflow-presence blast radius;
- popularity plus graph features;
- regularized logistic regression;
- gradient-boosted trees.

This experiment should measure rank overlap, Precision@K, Recall@K, Average Precision, and uncertainty. Its purpose is not to produce the final result, but to test whether the proposed feature families have enough signal and label coverage to justify graph-learning development.

## Checkpoint cadence

Push a GitHub checkpoint after each completed priority group, with a commit message tied to the backlog IDs. Do not create an unattended time-based process until the desired frequency, branch policy, and permissions are explicitly defined.
