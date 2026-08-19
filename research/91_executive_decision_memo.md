# Executive Decision Memo

## Decision

**Proceed, but narrow and reposition the research.** The problem is important, the existing repository contains a useful data and ranking prototype, and the combination of package topology, maintainer reach, and CI/CD exposure is plausibly differentiated. However, the current thesis draft overstates novelty and completion by presenting HGAT performance and incident back-testing that are not yet represented by reproducible code and artifacts.

## Recommended contribution

Build a **temporal benchmark for defensive prioritization of high-leverage npm packages**. Treat HGAT as one candidate model rather than the contribution itself. The benchmark should determine whether the cross-domain feature combination improves over popularity, dependency centrality, maintainer concentration, package weak-link metadata, workflow-security signals, and interpretable tabular models.

## Why it matters

Prior work shows that npm contains package and maintainer single points of failure, that package metadata can reveal weak-link signals, that dependency resolution affects downstream impact, and that GitHub Actions risk depends on detailed permissions and workflow configuration.[1][2][3][4] The proposed project can connect these strands in a defensive pre-incident ranking task.

## Must-fix issues

| Priority | Required change |
|---|---|
| Critical | Implement strict temporal snapshots and leakage checks |
| Critical | Replace keyword-only compromise labels with a reviewed version-level incident registry |
| Critical | Compare against strong non-neural baselines |
| Critical | Separate structural leverage from compromise likelihood |
| High | Replace workflow-directory presence with richer workflow-security features and missingness |
| High | Use npm-accurate version-aware dependency resolution |
| High | Report uncertainty, calibration, per-incident results, and review-cost curves |
| Medium | Add pinned dependencies, tests, manifests, and a reproducible experiment runner |

## Publication positioning

Avoid saying:

> “We predict the optimal attack entry points and prove that attackers target the most privileged packages.”

Prefer:

> “We evaluate whether time-aligned dependency, maintainer, and public CI/CD exposure features improve defensive prioritization of packages associated with later documented supply-chain compromises.”

## Go/no-go threshold

Continue toward publication if the team can assemble a high-confidence label set, reconstruct time-valid features, and obtain a meaningful comparison against popularity and graph baselines. If the dataset remains too sparse for predictive claims, pivot to a careful empirical study of structural leverage, workflow observability, and the limits of public supply-chain data.

## Immediate next actions

1. Freeze the research question and terminology.
2. Add a source-backed incident-label registry.
3. Build strict historical snapshot and feature-availability checks.
4. Implement the baseline ranking suite.
5. Evaluate feature-family ablations.
6. Add workflow security parsing and missingness analysis.
7. Implement HGAT only after the benchmark is stable.
8. Write the final results without hiding negative or null findings.

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman
[2]: https://arxiv.org/abs/2112.10165
[3]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142
[4]: https://docs.github.com/en/actions/reference/security/secure-use
