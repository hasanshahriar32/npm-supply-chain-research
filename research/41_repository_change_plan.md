# Repository Change Plan

## Immediate hardening of the current prototype

1. Add a shared configuration module for paths, API user agent, retry policy, and snapshot metadata.
2. Add `--db` and `--output-dir` options to every script, including `check_progress.py`.
3. Replace silent exception swallowing with structured warnings and retryable failure records.
4. Store source and retrieval metadata in a provenance table.
5. Add row-count and completion-status checks to `--stats`.
6. Preserve raw package/version identifiers and distinguish approximate from resolved dependency edges.
7. Add tests for `parse_github_url`, reverse graph traversal, normalization, missing workflow data, and advisory classification.

## Data pipeline milestones

### M1 — Snapshot manifest

Create a manifest for the existing database and compressed CSV, including file checksums, expansion size, row counts, collection date, and code revision. This establishes a reproducible baseline without recollecting the ecosystem.

### M2 — Version-aware resolution

Add a resolution stage that stores package-version edges, declared ranges, selected versions, resolver source, and confidence. Compare the current package-level graph with the resolved graph on a fixture before scaling.

### M3 — Incident-label registry

Add a reviewed label table with evidence URLs, publication and event times, affected versions, incident family, confidence, and exclusion reason. Separate ordinary advisories from confirmed targeted compromise.

### M4 — Workflow feature extraction

Replace the single workflow flag with a parser that reports workflow presence, permissions, triggers, action pinning, deployment behavior, OIDC indicators, runner type, recency, parser errors, and repository observability status. Never store secret values.

### M5 — Baseline runner

Implement a single interface for popularity, graph centrality, maintainer reach, workflow exposure, weak-link metadata, logistic regression, and gradient-boosted-tree baselines. Every model must consume a versioned feature table and temporal split configuration.

### M6 — Temporal benchmark

Implement rolling-origin splits, feature-availability checks, incident-family grouping, and final holdout protection. Output rankings, metrics, calibration, confidence intervals, and per-incident tables.

### M7 — Heterogeneous graph experiments

Only after M1–M6 are reliable, implement homogeneous and heterogeneous graph models. Record graph metadata, seeds, negative construction, truncation, hyperparameters, and compute cost. Compare against baselines under identical splits.

## Definition of done for a publishable result

The codebase should be able to regenerate a result from a manifest, produce the same fixture output twice, identify every feature’s source and cutoff, and report both positive and negative findings. A paper claim is not considered supported merely because a model runs; it needs a reproducible ranking, baseline comparison, uncertainty estimate, and limitation statement.
