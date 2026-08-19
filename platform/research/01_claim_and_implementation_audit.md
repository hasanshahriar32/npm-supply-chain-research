# Claim and Implementation Audit

## Purpose

This audit compares the supplied Notion draft and PDFs with the current GitHub repository. It prevents proposed methods and draft results from being reported as completed empirical findings.

## Claim status matrix

| Draft or project claim | Evidence currently available | Status | Required follow-up |
|---|---|---|---|
| npm dependency topology can be combined with maintainer and GitHub infrastructure data | `collect_data.py` defines package, maintainer, dependency, version, repository, workflow, and advisory tables; the repository includes a populated SQLite snapshot | Repository-supported | Document snapshot date, coverage, missingness, and provenance |
| Shared maintainers create lateral propagation potential | Prior npm ecosystem research reports maintainer-account concentration and single points of failure; current code counts packages per maintainer | Supported premise; metric still proposed | Validate identity resolution, distinguish maintainers from publishers, and compare max versus sum aggregation |
| Downstream CI/CD exposure can be estimated from public GitHub workflow presence | Current collector checks whether `HEAD:.github/workflows` exists for mapped repositories | Repository-supported proxy; interpretation limited | Measure workflow files, permissions, secrets/OIDC indicators, recency, repository activity, and private-repository missingness |
| Attacker ROI is a useful ranking construct | Current code computes a weighted normalized score | Proposed construct | Establish a defensive decision use case, compare against baselines, and validate with out-of-time labels |
| A heterogeneous graph is required | Draft methodology describes package, maintainer, and repository relations | Proposed architecture | Test whether relation-aware models outperform tabular and homogeneous graph baselines |
| HGAT can forecast high-value entry points | HGAT is described in the thesis and implementation memo, but no model-training code is present in the repository | Unverified | Implement, train, calibrate, and evaluate with strict temporal splits |
| The model successfully back-tests against named 2025–2026 incidents | The thesis draft asserts this, but no experiment artifacts, predictions, labels, or metrics are committed | Unverified | Verify incident dates and affected versions from authoritative reports; publish pre-incident predictions and confidence intervals |
| The project covers the top 100,000 npm packages | Methodology documents propose this; current repository snapshot contains about 25,000 packages and seeds from a high-impact list | Not currently supported | Define the population and sampling frame; report coverage rather than using the intended target as a completed result |
| OSV advisories provide ground-truth compromise labels | Current collector imports keyword-filtered OSV npm advisories from a date window | Partial and noisy | Build a manually reviewed, high-precision incident taxonomy; report label confidence and false positives |
| Public workflow visibility approximates infrastructure privilege | Public workflow directories are observable for many repositories | Unverified proxy assumption | Treat it as an exposure signal, not a privilege measurement; add permissions, secrets, OIDC, artifact, deployment, and environment indicators where lawful and available |
| The proposed score identifies attackers’ optimal targets | No causal or behavioral evidence establishes attacker optimization from the current data | Overclaim | Use “defensive structural leverage ranking” unless a prospective or multi-incident validation supports stronger language |

## Repository implementation status

### Implemented

The repository implements resumable collection from the npm registry and deps.dev, GitHub GraphQL workflow-directory checks, OSV advisory import, SQLite schema initialization, retry and backoff behavior, progress reporting, and deterministic metric computation. The metric script constructs reverse dependency adjacency, computes transitive dependent counts, counts workflow-bearing dependents, normalizes wormability and blast radius, and exports rankings.

The current data snapshot contains approximately 25,228 packages, 22,340 package versions, 12,217 maintainers, 121,885 dependency edges, 21,527 GitHub mappings, 21,523 workflow checks, 15,300 positive workflow detections, 153,488 advisory rows, and 25,228 package-metric rows. These figures were obtained by read-only inspection of the committed database archive and should be accompanied by a snapshot identifier in future releases.

### Partial or fragile

The current seed strategy is based on a high-impact package list and recursive discovery through deps.dev rather than a documented ecosystem-wide sampling frame. The workflow feature is binary directory presence rather than a semantic characterization of CI/CD privilege. The advisory importer uses keyword matching and a date window, which can produce both false positives and false negatives. `check_progress.py` expects a database in the current working directory, unlike the main scripts that use `data/npm_ecosystem.db`.

### Absent

The repository currently has no HGAT or other graph-learning implementation, no PyTorch/PyG dependency manifest, no temporal snapshot builder, no label-review workflow, no experiment configuration, no baseline suite, no train/validation/test split code, no calibration analysis, no confidence intervals, no ablation study, no incident-level prediction artifacts, and no automated test suite.

## Claim language recommended for the next draft

Replace “we demonstrate that the HGAT accurately predicts optimal attacker entry points” with:

> “We propose and evaluate a defensive ranking framework for structural supply-chain leverage. We test whether dependency reach, maintainer-sharing structure, and publicly observable downstream CI/CD features improve out-of-time prioritization of historically compromised packages relative to established baselines.”

Use “Wormability” and “Blast Radius” as operational feature names, not as direct measurements of attacker behavior or private infrastructure privilege. Use “historically compromised” only for labels backed by a documented incident source and affected-version evidence.

## References

[1]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/scripts/collect_data.py "Current collection implementation"

[2]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/scripts/calculate_metrics.py "Current metric implementation"

[3]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/docs/paper1.txt "Supplied thesis manuscript"

[4]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/docs/paper2.txt "Supplied methodology memo"

[5]: https://arxiv.org/abs/2112.10165 "npm weak-link study"

[6]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "npm single-point-of-failure study"
