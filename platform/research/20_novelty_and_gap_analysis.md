# Novelty and Research-Gap Analysis

## Bottom-line assessment

The research is **worth pursuing**, but the strongest version is not “HGAT predicts attacker ROI.” That wording overclaims both novelty and evidence. A defensible contribution is:

> **A time-aligned, reproducible benchmark for defensive prioritization of structurally high-leverage npm packages, combining dependency reach, maintainer-sharing structure, and public CI/CD security observables, with rigorous comparisons against graph, metadata, behavior, and workflow baselines.**

An HGAT can be one candidate model in that benchmark. It should not define the contribution in advance.

## What is already established

| Established finding | Evidence | Consequence |
|---|---|---|
| npm has package and maintainer concentration that can create single points of failure | Zimmermann et al. [1] | Maintainer-mediated reach is a credible feature family, not a novel premise by itself |
| Metadata weak links exist at ecosystem scale | Zahan et al. [2] | Weak-link metadata must be included as a strong baseline |
| Malicious-package incidents can be cataloged and manually classified | Ohm et al. [3] | The project can build a label taxonomy, but labels require source provenance |
| Dependency resolution materially affects propagation results | Liu et al. [4] | Package-level reachability must not replace version-aware resolution without validation |
| Downstream exposure and remediation lags are measurable | Zerouali et al. and Chinthanet et al. [5][6] | Time alignment and exposure definitions are central to validity |
| Malicious-package behavior detection is an active and competitive area | Amalfi, DONAPI, Cerebro, SpiderScan [7][8][9][10] | The project must clearly separate structural target ranking from package-behavior detection |
| CI/CD risk is multidimensional | Pan et al., Riggio and Pautasso, Fares et al., GitHub guidance [11][12][13][14] | Workflow-directory presence is an intentionally coarse proxy, not a privilege measure |

## Candidate gaps

### Gap A: Pre-incident target prioritization across domains

The reviewed literature contains strong studies of ecosystem structure, malicious behavior, vulnerability propagation, and workflow security, but the combination of these domains into a **pre-incident package-ranking task** is less developed. The gap is plausible because the task differs from package-malware detection and vulnerability exposure analysis.

**What would close the gap:** build historical graph snapshots before documented incidents, produce rankings without post-incident information, and compare a cross-domain model with feature-family ablations.

### Gap B: Linking package reach to observable CI/CD exposure

Existing dependency studies measure downstream package or project reach, while CI/CD studies analyze workflows independently. A cross-domain link from package dependencies to workflow security properties could be useful for defenders. However, the current proposed link is weak because `has_workflows` is only a directory-presence flag.

**What would close the gap:** parse workflow files and record permissions, triggers, action pinning, deployment or release behavior, self-hosted runners, OIDC, environment protections, and workflow recency. The analysis should report private-repository missingness and avoid claiming that public workflows reveal actual secrets.

### Gap C: Distinguishing structural leverage from compromise likelihood

The draft treats “Attacker ROI” as if structural reach and compromise probability were one construct. Prior literature suggests these are distinct. A popular or highly connected package can be safe, well governed, and difficult to compromise; a low-centrality package can still be compromised through a targeted campaign.

**What would close the gap:** define separate targets for structural leverage and later documented compromise, or use a multi-task model with clearly separated outputs. Report whether the score is useful for defensive review even when it does not predict compromise likelihood.

### Gap D: Temporal validity under realistic information constraints

The draft proposes back-testing but does not yet provide a full leakage audit. Post-incident advisories, package removals, public compromise reports, later maintainer changes, and current workflow states can leak future information into historical rankings.

**What would close the gap:** freeze every feature at the observation date, construct time-specific dependency and maintainer snapshots, use publication-time rather than current advisory metadata, and retain an auditable feature-availability table.

### Gap E: Value of HGAT over interpretable models

The proposal assumes a heterogeneous attention model is appropriate because the data are heterogeneous. Heterogeneous data do not automatically imply that a neural model is necessary. If a regularized generalized linear model, gradient-boosted trees, or a weighted centrality score performs as well, the neural architecture adds complexity without evidence of value.

**What would close the gap:** compare models under matched features and time splits; report performance, calibration, variance, training cost, feature availability, and explanation quality. Use attention weights cautiously: attention is not automatically a causal or faithful explanation.

### Gap F: Label quality for targeted compromise

OSV and advisory databases are valuable but heterogeneous. A keyword filter over summary and details can include ordinary vulnerabilities and miss incidents described with different language. A package-level binary label can also hide version-level and campaign-level uncertainty.

**What would close the gap:** create a manually reviewed label set with affected versions, event times, incident family, evidence URLs, confidence, and exclusion reasons. Treat ambiguous cases as unknown or use confidence-weighted evaluation.

## Novelty claims that should be rejected or softened

The following claims are not defensible without new evidence:

- “No existing work maps supply-chain topology to attacker ROI.” Prior work already studies package centrality, maintainer concentration, vulnerability impact, and malicious package detection.
- “HGAT proves attackers target the most privileged packages.” Observational ranking cannot prove attacker optimization or causal privilege.
- “Workflow presence equals CI/CD blast radius.” It is a public observability proxy.
- “The model forecasts optimal entry points.” This requires out-of-time, multi-incident performance and comparison against popularity and centrality baselines.
- “A top-100 result demonstrates effectiveness.” Top-K results need uncertainty intervals, an appropriate candidate population, and comparison to random, popularity, centrality, and label-prevalence baselines.

## Recommended contribution hierarchy

| Priority | Contribution | Why it matters |
|---|---|---|
| 1 | Reproducible, version-aware cross-domain dataset and feature schema | Makes the study auditable and useful even if the model is modest |
| 2 | High-precision incident labels and temporal benchmark | Addresses the largest validity problem in predictive claims |
| 3 | Interpretable structural-leverage baselines and ablations | Establishes whether each feature family adds value |
| 4 | Workflow security feature extraction with missingness analysis | Converts coarse workflow presence into a defensible exposure proxy |
| 5 | HGAT or another heterogeneous model | Tests whether relation-aware learning improves generalization |
| 6 | Prospective monitoring prototype | Provides practical value after offline validity is established |

## Go/no-go recommendation

**Go**, with a narrower claim and a staged evaluation. The project is sufficiently important and plausibly differentiated for a thesis or empirical security paper. It is not ready to claim a novel predictive HGAT system. The first publication-quality milestone should be a benchmark and ablation study; the graph neural network should be an empirical question within that benchmark.

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman

[2]: https://arxiv.org/abs/2112.10165

[3]: https://arxiv.org/abs/2005.09535

[4]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142

[5]: https://link.springer.com/article/10.1007/s10664-022-10154-1

[6]: https://link.springer.com/article/10.1007/s10664-021-09951-x

[7]: https://arxiv.org/abs/2202.13953

[8]: https://www.usenix.org/conference/usenixsecurity24/presentation/huang-cheng

[9]: https://arxiv.org/html/2309.02637v2

[10]: https://dl.acm.org/doi/10.1145/3691620.3695492

[11]: https://ieeexplore.ieee.org/iel7/8858/4358699/10061526.pdf

[12]: https://link.springer.com/chapter/10.1007/978-3-032-12089-2_14

[13]: https://arxiv.org/abs/2601.14455

[14]: https://docs.github.com/en/actions/reference/security/secure-use
