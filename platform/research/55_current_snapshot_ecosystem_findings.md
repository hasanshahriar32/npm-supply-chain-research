# Current-Snapshot Ecosystem Structure and Observability

## Provenance and analytical boundary

This memo profiles the committed SQLite archive `data/npm_ecosystem.db.zip`, SHA-256 `ab45439cf94cf43f3133b0aaff644557d55e86e99430a0a7937bfd0ce5266315`. It reports aggregate current-snapshot structure only. The raw archive is not placed in the deployable web project; the reproduction script is `scripts/analyze_ecosystem_structure.py`, the aggregate output is `55_current_snapshot_ecosystem_structure.json`, and the top-50 maintainer portfolio table is `55_top_maintainer_portfolios.csv`.[1]

The archive has `25,228` packages, `22,340` package-version rows, `121,885` dependency rows, `12,217` maintainer records, `79,405` package–maintainer relationships, and `153,488` advisory rows. It does **not** record a publication timestamp for package versions or a version-level advisory relation. Consequently, it cannot by itself support a strict historical compromise-prediction evaluation.

## What the archive makes observable

| Observable quantity | Count | Denominator | Share | Interpretation |
|---|---:|---:|---:|---|
| Version rows with a repository URL | 21,664 | 22,340 | 96.9740% | Repository linkage is broadly available in this snapshot. |
| Version rows with GitHub owner/repository fields | 21,527 | 22,340 | 96.3607% | Public GitHub linkage makes later workflow-history reconstruction feasible for much of the snapshot. |
| Version rows with fetched GitHub workflows present | 15,300 | 22,340 | 68.4870% | Workflow **presence** is common enough to justify a parsed-CI/CD work package. |
| Version rows with successful workflow fetch but no workflow present | 6,223 | 22,340 | 27.8568% | No public workflow is an observable state, not a safety label. |
| Version rows with no successful workflow fetch | 817 | 22,340 | 3.6571% | Missingness must be retained as unknown rather than coerced to zero. |

The contrast with the existing `direct_dependents_with_workflows` metric is important. That aggregate is non-zero for only 15 packages, while the version-level table shows 15,300 rows with a fetched public workflow. The current aggregate therefore loses most of the useful configuration surface. The next research iteration should parse workflow YAML at a historical commit rather than count whether a dependent has a workflow directory.

## Maintainer concentration findings

The largest observed maintainer portfolio contains `967` package relationships. The top 1% of observed maintainers (`123` accounts) hold `18,027 / 79,405` package–maintainer relationships (`22.7026%`). This is a descriptive concentration result, compatible with prior work showing that a small set of maintainers can represent systemic ecosystem risk; it is not proof that any particular maintainer is compromised or likely to be compromised.[2]

| Association | Spearman correlation | Reading |
|---|---:|---|
| Transitive dependents vs. package maintainer count | -0.1361 | More maintainers on a package do not correspond to greater downstream reach in this snapshot. |
| Transitive dependents vs. largest attached maintainer portfolio | 0.0817 | Ecosystem reach and portfolio concentration form largely different rankings here. |
| Direct dependents vs. package maintainer count | 0.0367 | Package co-maintenance count is not a meaningful direct-dependent proxy in this dataset. |

These low correlations strengthen the protocol’s choice to retain **structural leverage** and **maintainer/control concentration** as separately inspectable components. They do not establish incremental predictive value; that requires dated features and high-confidence future incident labels.

## Implications for resolving the research gap

The archive supports an actionable next step: build a public CI/CD configuration extractor for the linked GitHub repositories, retaining explicit `unknown` states for inaccessible history. GitHub documents permissions, privileged triggers, third-party action pinning, OIDC, environments, and runner choice as security-relevant controls, and empirical research demonstrates that the semantics of workflow configuration matter beyond repository-level presence.[3] [4]

The archive’s two deficiencies are equally valuable findings. First, advisory rows lack affected-version linkage, so natural-language advisory keywords must not become primary compromise labels. Second, package-version rows lack release time, so current repository and workflow state cannot be retroactively treated as pre-incident evidence. The study protocol’s external label registry and historical feature ledger are mandatory, not optional polish.

## Advisory-label readiness audit

The archive contains `153,488` advisory rows, spanning `153,009` distinct package names from `2025-09-01` to `2026-04-30`. Only `164` of those package names overlap the current metric population. More importantly, `153,422` rows carry the broad classification `compromise`, with only `50` classified as `account_takeover` and `16` as `dependency_confusion`.

This distribution is not plausible as a manually adjudicated package-version ground truth for the study’s narrow target. It appears suitable for broad candidate discovery or an upstream classification output, but not for a primary label set because the table has no affected-version column, no event-start field distinct from publication, and no incident-family identifier. The correct research response is therefore to retain it as a discovery source, preserve the result as a negative data-quality finding, and use the evidence hierarchy in `52_seed_incident_registry.csv` for primary positives.

## References

[1]: https://github.com/ashik-hstu/npm-supply-chain-research "Repository data archive and reproducible analysis scripts"
[2]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., Small World with High Risks"
[3]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub, Secure use reference"
[4]: https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev "Koishybayev et al., Characterizing the Security of GitHub CI Workflows"
