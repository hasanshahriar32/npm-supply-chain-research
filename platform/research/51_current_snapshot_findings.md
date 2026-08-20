# Current-Snapshot Structural-Leverage Audit

## Purpose and scope

This audit evaluates the project’s **committed current snapshot** of `25,228` package metrics. Its purpose is to establish what the existing deterministic measures actually describe before any temporal or predictive claim is made. It is a **cross-sectional descriptive analysis**, not a back-test and not evidence that any package will be compromised.

The source archive is `data/metrics_summary.csv.zip`, SHA-256 `43e1845a106719ef9fb8c7d72d174959cc25e6f8fe8a3c6bfcd6cb7ca8e90a35`. The reproducible analysis script is `scripts/analyze-structural-leverage.mjs`; the machine-readable output is `51_current_snapshot_structural_analysis.json`; and the top-50 legacy-score table is `51_current_snapshot_top_legacy_structural_scores.csv`.[1]

## Distributional findings

| Measure | Median | 90th percentile | 99th percentile | Maximum | Non-zero packages |
|---|---:|---:|---:|---:|---:|
| `wormability_max` | 32 | 327 | 967 | 967 | 22,147 |
| `wormability_sum` | 50 | 642 | 1,314 | 2,740 | 22,147 |
| `blast_radius` | 0 | 0 | 0 | 2 | 20 |
| Direct dependents | 1 | 6 | 46 | 1,150 | 20,331 |
| Direct dependents with observed public workflows | 0 | 0 | 0 | 2 | 15 |
| Transitive dependents | 4 | 120 | 1,833.57 | 4,615 | 20,328 |
| Legacy weighted structural score (`attacker_roi`) | 0.016546 | 0.169080 | 0.500000 | 0.794726 | 22,147 |

The practical result is that the current workflow-derived signal is **extremely sparse**: only `15 / 25,228` packages have a non-zero count of direct dependents with observed public workflow directories (`0.0594%`). Likewise, only `20 / 25,228` packages have a non-zero `blast_radius` (`0.0792%`). This means the present implementation does not supply a sufficiently rich CI/CD-exposure measure for an ecosystem-wide ranking study. It also means that the existing `blast_radius` feature should not be used as a stand-alone validation target.

## Confounding and queue-overlap findings

The original weighted field is kept as a **legacy structural score** for auditability, not as a measurement of attacker value. Its Spearman correlations with transitive dependents (`0.0825`), direct dependents (`0.1598`), workflow-bearing direct dependents (`0.0416`), and `wormability_max` versus transitive dependents (`0.0817`) are low in this snapshot. Low rank correlation does not demonstrate independent predictive information; it indicates only that these constructed fields form different orderings in the sampled data.

For a fixed top-1% review budget of `253` packages, the legacy-score and transitive-reach queues intersect on `16` packages (`6.3241%` of the budget). The legacy-score and workflow-bearing-dependent queues intersect on `12` packages (`4.7430%`), while all three intersect on `12`. The low overlap is a useful design finding: it supports evaluating separate queues rather than hiding incompatible signals inside a single “ROI” score.

| Queue comparison at top-1% budget | Shared packages | Interpretation |
|---|---:|---|
| Legacy structural score ∩ transitive reach | 16 | The score is not simply a reach ranking in this sample. |
| Legacy structural score ∩ workflow-bearing dependent count | 12 | The sparse workflow proxy changes the ordering but cannot yet be interpreted as public CI/CD exposure. |
| Transitive reach ∩ workflow-bearing dependent count | 15 | The existing workflow signal largely appears only among a narrow set of high-reach packages. |
| All three queues | 12 | A small common set should be reviewed descriptively, not presented as predicted targets. |

## What this resolves

The audit resolves one immediate research gap: it documents that existing metrics are useful as **feature candidates** and distinguishes them from validated outcomes. It also provides a reproducible empirical reason to replace the binary workflow-directory proxy with parsed configuration features and explicit missingness. Prior work establishes that dependency topology and maintainer concentration are meaningful systemic-risk descriptors, while GitHub Actions security research shows that workflow permissions, triggers, actions, and runners are semantically important beyond a directory flag.[2] [3] [4]

## What remains unresolved

The snapshot does not establish temporal validity, compromise likelihood, causal attack selection, workflow privilege, or HGAT utility. The next experiment must use an adjudicated incident registry, a dated feature-availability ledger, version-aware historical dependency resolution, and a strong baseline ladder. The selected protocol is specified in `50_gap_resolution_study_protocol.md`.

## References

[1]: https://github.com/ashik-hstu/npm-supply-chain-research "Repository metrics archive and analysis script"
[2]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., Small World with High Risks"
[3]: https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev "Koishybayev et al., Characterizing the Security of GitHub CI Workflows"
[4]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub, Secure use reference"
