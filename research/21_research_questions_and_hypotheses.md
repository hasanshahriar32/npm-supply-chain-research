# Research Questions and Hypotheses

## Primary research question

**RQ0.** Given only data available before an observation date, can a time-aligned cross-domain model rank npm packages associated with later documented supply-chain compromises more effectively than established graph, metadata, behavior, and workflow-security baselines?

## Secondary research questions

| ID | Question |
|---|---|
| RQ1 | Does maintainer-sharing structure add predictive value beyond package popularity and dependency reach? |
| RQ2 | Does public CI/CD security exposure add predictive value beyond dependency reach and package metadata? |
| RQ3 | Does accurate version-aware dependency resolution change package rankings materially compared with package-level reachability? |
| RQ4 | Does a heterogeneous graph model generalize better than interpretable tabular and homogeneous-graph models under temporal validation? |
| RQ5 | Are rankings calibrated and stable across incident families, ecosystems, package popularity strata, and observation dates? |
| RQ6 | Which structural features are useful for defensive review even when they do not predict compromise probability? |

## Candidate hypotheses

The hypotheses below are proposed for testing. They should not be stated as confirmed findings until the experiment is complete.

### H1 — Maintainer reach adds information

A model using maintainer-sharing features will achieve higher out-of-time ranking performance than a model using only popularity and dependency-graph features.

**Required test:** compare `W_max`, `W_sum`, maintainer concentration, and identity-quality features against popularity and graph-only baselines, using the same time split and candidate population.

### H2 — Workflow security exposure adds information

A model using downstream workflow-security features will achieve higher out-of-time ranking performance than a model using only package popularity, dependency reach, and maintainer features.

**Required test:** compare directory presence with progressively richer workflow features, while reporting private-repository missingness and parser coverage.

### H3 — Accurate dependency resolution changes rankings

Version-aware dependency-tree resolution will produce materially different and more accurate downstream rankings than a package-level graph that links dependencies to the latest version.

**Required test:** compare resolved lockfile-compatible graphs, deps.dev relations, and simplified package-level projections; quantify rank correlation and incident recall differences.

### H4 — Relation-aware learning may help, but is not assumed to win

A heterogeneous graph model will improve ranking, calibration, or transfer to later incidents over matched-feature tabular and homogeneous-graph baselines.

**Required test:** compare performance and variance under repeated temporal splits, not only a single random split. If no improvement appears, prefer the simpler model.

### H5 — Structural leverage and compromise likelihood are separable

Structural reach and later compromise likelihood will exhibit only partial overlap; a model trained to predict confirmed compromise will not perfectly reproduce a structural-leverage ranking.

**Required test:** report correlation, overlap@K, and separate outcomes for high-leverage non-compromised packages and compromised packages with modest structural reach.

### H6 — Public workflow observability is a noisy proxy

Public workflow presence will correlate with downstream exposure but will have lower discriminative value than richer workflow-security features and will be biased toward public repositories.

**Required test:** measure feature missingness, workflow parser coverage, and performance by repository visibility and package popularity stratum.

### H7 — Temporal validation will reduce apparent performance

Random splits will overestimate performance because package, maintainer, incident, and ecosystem records are correlated over time. Strict temporal evaluation will produce more conservative but more credible estimates.

**Required test:** compare random, group, and temporal splits; treat temporal performance as primary.

## Minimum publishable result

The project can produce a defensible empirical paper if it answers RQ0–RQ3 with a versioned dataset, high-precision labels, leakage controls, strong baselines, uncertainty estimates, and feature ablations. HGAT is necessary only if RQ4 is a central claim and the model improves on simpler alternatives.

## Non-hypotheses to avoid

The following statements are not suitable hypotheses without additional causal design:

- “Attackers always choose the highest-ROI package.”
- “A workflow directory proves cloud credential exposure.”
- “HGAT attention weights reveal the attacker’s true objective.”
- “A high score means a package is exploitable.”
- “Historical back-testing proves future attack prevention.”
