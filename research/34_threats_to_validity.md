# Threats to Validity

## Construct validity

### “Wormability” is not credential control

A maintainer-to-package relationship does not prove that one credential controls every package, that a maintainer can publish today, or that package ownership is actively used. Mitigate by calling the feature shared-maintainer reach, tracking relationship type and recency, and testing alternative aggregations.

### “Blast Radius” is not infrastructure privilege

A downstream repository with a public workflow may have no secrets, read-only permissions, ephemeral runners, or strong environment protections. Conversely, a private repository may have significant privilege but be unobservable. Mitigate by expanding workflow features, including missingness, and interpreting results as public CI/CD exposure.

### “Attacker ROI” is not observed attacker utility

The score is a proxy for defensive prioritization. Without attacker decision logs or a causal design, it cannot prove that adversaries optimize the score. Use structural leverage or target-prioritization language unless validation justifies a stronger interpretation.

## Internal validity

### Temporal leakage

Current dependency graphs, workflow states, advisories, package removals, or popularity can leak future information. Apply the feature cutoff protocol and publish the availability ledger.

### Resolution error

Approximating semver ranges with the latest version can create false edges and incorrect reach. Use version-aware resolution, compare against simplified graphs, and report resolution confidence.

### Label contamination

OSV keyword filters may mix ordinary vulnerabilities with targeted compromise and may miss incidents described without selected words. Use manual evidence review, confidence classes, and sensitivity analyses.

### Correlated observations

Packages may share maintainers, repositories, campaign artifacts, or dependency subgraphs. Random splits can inflate performance. Use temporal, package-family, maintainer-group, and incident-family grouping.

### Model selection bias

Trying many feature sets or splits and presenting the best result produces optimistic estimates. Predefine the primary protocol, keep a final holdout, and report all major variants.

### Implementation errors

Graph direction, duplicate edges, self-loops, missing nodes, and normalization choices can change rankings. Add unit tests for graph traversal, compare small hand-verified graphs, and store intermediate counts.

## External validity

### Public-repository bias

The project observes GitHub repositories and public workflows. Enterprises using private repositories, internal registries, or other CI platforms may be underrepresented. Report public-visibility strata and avoid claiming enterprise-wide risk.

### npm-only scope

Findings may not transfer to PyPI, Maven, Cargo, or private ecosystems because registry governance, identity models, and dependency resolution differ. Multi-ecosystem validation is future work, not an assumed generalization.

### Incident-selection bias

Well-documented incidents are more likely to be included than silent compromises. Report the label discovery process and consider a negative-control or retrospective prevalence analysis.

### Ecosystem drift

Registry size, maintainer practices, CI/CD platforms, and attacker behavior change over time. Use rolling evaluation, report performance by period, and avoid treating 2025–2026 incidents as permanent ecosystem structure.

## Statistical conclusion validity

### Rare positives

A small number of confirmed compromise incidents can make top-K results unstable. Report confidence intervals, bootstrap at the incident level, and avoid relying on a single percentage without denominators.

### Popularity confounding

Dependent count, maintainer reach, and workflow prevalence are likely correlated with popularity. Include downloads, dependent count, age, and activity controls, and report partial or matched comparisons.

### Metric mismatch

ROC-AUC can look strong under extreme class imbalance while the review budget is poorly served. Use Precision@K, Recall@K, Average Precision, NDCG, MRR, calibration, and cost curves.

### Neural-model variance

GNN results may vary with seed, sampling, negative construction, and graph truncation. Report repeated runs, variance, training cost, and simpler baselines.

## Ethical validity

Package names, maintainer identifiers, repository mappings, and incident labels can expose individuals or invite targeting. Minimize personal data, avoid publishing credential-related details, do not release exploit artifacts, and coordinate responsibly when discovering new security issues.
