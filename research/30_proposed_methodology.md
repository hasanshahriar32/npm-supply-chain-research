# Proposed Methodology

## Study objective

Evaluate whether structural features from the npm dependency and maintainer graph, enriched with public downstream CI/CD security observations, improve defensive prioritization of packages associated with later documented supply-chain compromises.

The primary output is a **ranking**, not an exploitability verdict. The model should be evaluated on information available before the prediction horizon and should produce uncertainty and feature-availability records.

## Study design overview

| Stage | Output | Main validity control |
|---|---|---|
| 1. Population and snapshots | Versioned package, maintainer, dependency, repository, and workflow tables | Snapshot date and source checksum |
| 2. Entity resolution | Stable package-version, maintainer, repository, and incident identifiers | Alias and ambiguity logs |
| 3. Feature construction | Time-valid graph and tabular features | Feature cutoff enforcement |
| 4. Label construction | Version-level and incident-level compromise labels | Manual review and evidence provenance |
| 5. Baselines | Popularity, graph, maintainer, metadata, workflow, and tabular models | Matched candidate sets |
| 6. Graph models | Homogeneous and heterogeneous graph candidates | Same features, splits, and label protocol |
| 7. Evaluation | Ranking, calibration, robustness, and cost metrics | Temporal and group-aware validation |
| 8. Sensitivity analysis | Sampling, missingness, resolution, and label sensitivity | Pre-specified variants |

## Population and sampling

The population should be defined before model fitting. A recommended primary population is all npm packages with sufficient version, dependency, and maintainer metadata in the selected historical snapshots. If the full ecosystem cannot be retained, use a transparent sampling design:

- a high-adoption stratum;
- a medium-adoption stratum;
- a low-adoption stratum;
- packages with and without public repositories;
- packages with and without maintainers shared across packages;
- all packages in the confirmed incident label set.

Do not seed only from a popularity list and then describe the result as ecosystem-wide. Report inclusion probability, coverage, exclusions, and the number of packages lost at each data-collection stage.

## Time-indexed data construction

For each observation date \(t\), construct a snapshot containing only records observable at or before \(t\):

1. package and version publication metadata;
2. dependency relations and valid version ranges;
3. maintainer or publisher associations;
4. repository mapping and public workflow state;
5. package popularity and activity controls;
6. known advisories only if they were public by \(t\), and never use future advisory content to construct the features;
7. incident labels only for evaluation windows after \(t\).

The deps.dev service provides APIs and a BigQuery dataset and is designed to expose package structure and historical change; the pipeline should record the exact API or dataset version, query, retrieval time, and snapshot date.[1] OSV aggregates advisory databases and represents affected versions, but an OSV entry is not automatically a targeted-compromise label.[2]

## Entity resolution

### Packages and versions

Use canonical npm package names and exact version identifiers. Store both package-level and package-version-level keys. Preserve scoped names and avoid splitting identifiers on `@` without a version-aware parser.

### Maintainers

Store npm usernames as registry identifiers, but do not assume that equal names represent the same human or credential across all time. Preserve the timestamp, source field, and relationship type. Treat email hashes as privacy-preserving identifiers, not as proof of identity.

### Repositories

Normalize repository URLs to provider, owner, repository, and canonical URL. Record redirect, archive, deletion, visibility, and mapping-confidence status. A package may have multiple repository fields or a repository that differs from the publish source.

## Dependency graph

Use version-aware relations whenever possible. The primary graph should respect npm dependency-resolution semantics or use a trusted resolved graph source. A package-level graph may be retained as a scalable projection, but its projection rule must be documented and compared with the version-aware graph. Liu et al. show that dependency-tree resolution can materially change propagation conclusions in npm.[3]

For each package or version, derive:

- direct dependent count;
- resolved transitive dependent count;
- depth-weighted reach;
- number of distinct paths, with a documented cap if necessary;
- dependency criticality under removal or substitution simulations;
- package popularity and age controls.

## Maintainer features

Candidate features include maximum and summed package reach per maintainer, number of maintainers, maintainer concentration, maintainer tenure, recent ownership changes, publisher-versus-maintainer distinction, and ambiguity indicators. These features should be constructed only from historical records available at the cutoff date.

## CI/CD features

The first binary workflow-presence feature may be retained for comparability, but it should be supplemented by a feature family:

| Feature group | Examples |
|---|---|
| Workflow existence | Any workflow file; number of workflows; last modification date |
| Trigger exposure | Pull request, issue, workflow dispatch, schedule, tag, release, workflow-run triggers |
| Token permissions | Explicit `permissions`; write scopes; contents, packages, deployments, id-token |
| Action integrity | Full-length SHA pinning; mutable tags; third-party action prevalence |
| Secret and environment use | Secret references; protected environments; deployment jobs; cloud-provider indicators |
| Runner exposure | Self-hosted labels; runner groups if observable; container or privileged execution indicators |
| OIDC and provenance | `id-token: write`; trusted publishing or provenance indicators |
| Supply-chain controls | Dependabot, Scorecard, artifact attestations, lockfile and checksum practices |
| Missingness | Repository private, archived, deleted, API failure, workflow unavailable |

GitHub’s security guidance explicitly treats permissions, secrets, untrusted triggers, third-party actions, OIDC, and runner type as distinct risk dimensions.[4] The feature extractor must not store secret values or private repository contents.

## Labels

Use a high-precision incident table with package, version range, event time, first public detection, removal time, incident family, source URLs, and confidence. Positive labels should be limited to documented targeted compromise or malicious publication when the source supports that interpretation. Ordinary vulnerabilities should be separate labels or excluded from the primary compromise task.

The 2025 Shai-Hulud campaign and 2026 Axios compromise are suitable case studies because government and maintainer sources provide dates and affected artifacts, but they should not be the only positive events.[5][6][7]

## Baselines

The benchmark should include:

1. random and prevalence-matched ranking;
2. package popularity and download-volume ranking;
3. direct and transitive dependent count;
4. depth-weighted reach and centrality measures;
5. maintainer out-degree and concentration;
6. workflow-presence and workflow-security rankings;
7. package weak-link metadata features from prior work;
8. logistic regression with regularization;
9. gradient-boosted trees or another interpretable tabular model;
10. homogeneous graph model;
11. heterogeneous graph model such as HAN/HGAT, only after the above are established.

All models should use the same candidate population, labels, observation dates, and evaluation windows where possible.

## Graph model design

If the heterogeneous model is retained, define package, maintainer, repository, and possibly incident node types and typed relations. Use reverse dependency edges where message passing requires both directions. Avoid using a single post-incident label on every node in a way that leaks the incident family or package identity.

The proposed architecture can begin with a PyG `HeteroData` representation and a relation-aware attention layer. However, the actual choice should be justified empirically against simpler message-passing and tabular alternatives. Hyperparameters, initialization, early stopping, negative sampling, and random seeds must be recorded.

## Evaluation metrics

Use ranking metrics as primary:

- Precision@K and Recall@K for operational review budgets;
- Average Precision and NDCG for full ranking quality;
- MRR for the earliest high-ranked positive;
- PR-AUC where class imbalance is severe;
- calibration error and reliability curves if scores are interpreted probabilistically;
- bootstrap or temporal confidence intervals;
- per-incident and per-stratum results;
- review-cost curves showing positives found per examined package.

ROC-AUC should not be the only metric in a rare-event ranking task. Report uncertainty and avoid claiming superiority from small absolute differences without a paired comparison.

## Ablation and sensitivity studies

At minimum, remove one feature family at a time: dependency graph, maintainer graph, workflow features, popularity controls, package metadata, and incident-adjacent variables. Compare directory presence with richer workflow features. Compare version-aware and simplified dependency graphs. Repeat with and without packages that lack public repositories. Repeat under multiple label-confidence thresholds.

## Reproducibility

Every run should save:

- code commit;
- data snapshot identifiers and checksums;
- feature cutoff date;
- population and sampling configuration;
- label version;
- model and hyperparameters;
- random seeds;
- metrics and confidence intervals;
- ranked output with feature provenance;
- known exclusions and failures.

## References

[1]: https://docs.deps.dev/ "Open Source Insights and deps.dev documentation"

[2]: https://google.github.io/osv.dev/ "OSV documentation"

[3]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142 "Dependency-tree resolution and propagation"

[4]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub Actions secure-use guidance"

[5]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA Shai-Hulud alert"

[6]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA Axios alert"

[7]: https://github.com/axios/axios/issues/10636 "Axios post-mortem"
