# Final Research Report

## Predicting the Blast Radius in Software Supply Chains

**Assessment date:** 20 August 2026  
**Repository:** [ashik-hstu/npm-supply-chain-research][1]

## Executive conclusion

This research is **worthy of pursuing**, especially as a thesis or empirical security-engineering study, but its central claim must be narrowed. The strongest defensible contribution is not simply “an HGAT that predicts attacker ROI.” Graphs, maintainer concentration, package weak links, malicious-package behavior, vulnerability propagation, and CI/CD security have all been studied separately. The credible opportunity is to build a **time-aligned, reproducible defensive-ranking benchmark** that tests whether combining these domains improves the prioritization of packages associated with later documented supply-chain compromises.

The existing repository provides a useful foundation: it collects npm, deps.dev, GitHub GraphQL, and OSV data; stores dependency, maintainer, repository, workflow, and advisory records; and computes deterministic graph-based metrics. It does not yet contain the HGAT implementation, temporal benchmark, high-precision incident-label registry, baseline suite, calibration analysis, ablations, or reproducible experiment runner required to support the thesis’s strongest claims.[2][3]

The recommended decision is therefore **go, with a staged redesign**. First establish an interpretable benchmark and leakage-safe labels. Then test whether a heterogeneous graph model adds value. If a simpler model performs as well as HGAT, that is an important and potentially more reproducible result rather than a failure.

## 1. Research proposal and current implementation

The supplied draft proposes a heterogeneous graph spanning npm packages, maintainers, dependencies, GitHub repositories, and CI/CD workflow evidence. It calls the proposed maintainer-mediated reach “Wormability” and downstream workflow exposure “Blast Radius,” then combines normalized quantities into an Attacker ROI score. The intended task is to rank packages that may be strategically valuable for a self-propagating supply-chain campaign.[4]

The current repository implements a substantial subset of the data and metric pipeline. It creates SQLite tables for packages, package versions, maintainers, package-maintainer relationships, dependencies, advisories, and workflow flags. It uses npm Registry metadata, deps.dev dependency data, GitHub GraphQL workflow-directory checks, and OSV advisories. Its metric script computes maintainer package counts, reverse dependency traversal, workflow-bearing downstream dependents, normalized wormability and blast-radius values, and a weighted ranking.[2]

A read-only inspection of the committed database archive found approximately 25,228 packages, 22,340 package versions, 12,217 maintainers, 121,885 dependency edges, 21,527 repository mappings, 21,523 workflow checks, 15,300 positive workflow detections, 153,488 advisory rows, and 25,228 package-metric rows. These numbers describe the current snapshot; they are not evidence that the proposed ecosystem-wide or predictive HGAT experiment has been completed.

The supplied papers and Notion draft describe HGAT, temporal back-testing, baseline comparisons, and incident results, but those parts are not present as executable research artifacts in the current checkout. The repository therefore represents a **data-collection and deterministic-ranking prototype**, not yet the full thesis implementation.[3][4]

## 2. What similar research has already established

Prior work makes the problem important. Zimmermann et al. show that npm has package and maintainer single points of failure: individual packages can affect large parts of the ecosystem, and a small number of maintainer accounts may be able to inject code into many packages.[5] Zahan et al. analyze 1.63 million npm packages and propose six weak-link signals, including install scripts, expired maintainer domains, and inactive package or maintainer behavior.[6] These studies establish that maintainer and package structure are meaningful security variables, but they also mean that “using npm graphs and maintainers” is not sufficient novelty.

Ohm et al. provide a manually analyzed dataset of 174 malicious package artifacts across npm, PyPI, and RubyGems and organize attack techniques into attack trees.[7] This is valuable for incident taxonomy and label construction, but it is descriptive rather than a prospective target-ranking system. Garrett et al. study suspicious npm updates using unsupervised anomaly detection and security-relevant package-change features.[8] Amalfi combines classifiers, source reproducibility checks, and clone detection for malicious npm packages.[9] DONAPI, Cerebro, and SpiderScan further advance behavior-based detection through static and dynamic analysis, behavior sequences, cross-ecosystem modeling, and code-behavior graphs.[10][11][12]

Dependency-impact work also overlaps strongly with the proposed Blast Radius concept. Liu et al. show that npm-specific version resolution matters: simple reachability can construct the wrong dependency tree, so precise propagation analysis needs package-manager-aware resolution.[13] Zerouali et al. study direct and indirect exposure in npm and RubyGems, while Chinthanet et al. analyze release adoption and propagation lags across more than 1.5 million npm releases.[14][15] These studies support downstream impact analysis, but they focus primarily on vulnerabilities and remediation rather than intentional compromise or CI/CD privilege.

CI/CD research fills another part of the picture. Pan et al. measure more than 320,000 workflow-configured GitHub repositories and analyze security-critical usages and attack surfaces.[16] Riggio and Pautasso analyze more than 200,000 workflow specification files and nine security misconfigurations, while Fares et al. compare nine GitHub Actions workflow scanners on 2,722 workflows.[17][18] GitHub’s own guidance treats token permissions, secrets, untrusted triggers, third-party action integrity, OIDC, environment protections, and runner type as separate security dimensions.[19]

The literature therefore supports the importance of the proposed ingredients but also reveals the main challenge: **the project must prove incremental value across research traditions that already have strong specialized methods**.

## 3. The genuine research gap

The most credible gap is the combination of four elements:

1. **Pre-incident prioritization:** rank packages before a documented compromise rather than detect malicious code after publication.
2. **Cross-domain graph structure:** connect package dependencies, maintainers, and repositories rather than using only package metadata or source behavior.
3. **Infrastructure-aware downstream exposure:** enrich dependent count with observable workflow-security properties rather than treating all dependents as equivalent.
4. **Temporal and reproducible evaluation:** freeze features before the prediction window and compare against strong baselines.

This gap is plausible but conditional. The project must demonstrate that the combination predicts or prioritizes something not already captured by package popularity, direct/transitive dependent count, maintainer out-degree, package weak-link metadata, or workflow security scores.

The term “Blast Radius” should be carefully scoped. A public `.github/workflows` directory proves only that workflows are publicly observable. It does not prove that a downstream project has secrets, write permissions, deployment access, OIDC trust, or a reachable privileged runner. The initial binary feature should therefore be called **public workflow observability** and extended with permission, trigger, action-pinning, deployment, OIDC, runner, and missingness features.[19]

The term “Wormability” also requires qualification. A shared maintainer record does not prove shared credential control, current publishing access, or the ability to propagate to every associated package. It is best defined as **shared-maintainer reach**, with alternative aggregations and identity-quality indicators.

## 4. Main methodological gaps to fix

| Gap | Why it threatens the thesis | Required remedy |
|---|---|---|
| No executable HGAT or experiment suite | Draft model claims cannot be reproduced | Implement a model only after the benchmark and baselines |
| No strict temporal snapshot builder | Current data can leak post-incident information | Freeze every feature at the observation date |
| Keyword-only advisory filtering | Ordinary vulnerabilities can be mislabeled as targeted compromises | Build a reviewed version-level incident registry |
| Approximate dependency graph risk | Latest-version links can misrepresent npm resolution | Use version-aware resolution and compare projections |
| Workflow directory as privilege proxy | Observability is not privilege | Parse permissions, triggers, actions, OIDC, deployments, runners, and missingness |
| Popularity confounding | Centrality may simply rediscover popular packages | Include popularity controls and matched baselines |
| Small positive set | Top-K results may be unstable or anecdotal | Use multiple incidents, confidence intervals, and incident-level resampling |
| Public GitHub bias | Private enterprise CI/CD is underobserved | Report visibility strata and avoid enterprise-wide claims |
| Neural complexity assumed | HGAT may not beat simpler models | Require ablations against interpretable baselines |
| Ambiguous task definition | Detection, exploitability, leverage, and compromise are conflated | Separate structural leverage from compromise likelihood |

## 5. Recommended research design

The primary task should be defined as follows:

> At observation date \(t\), rank package nodes using only information available by \(t\), then test whether high-ranked packages are overrepresented among high-confidence compromise events beginning in a subsequent window.

The benchmark should use rolling-origin temporal evaluation. Every run must record the feature cutoff, label window, source snapshot, code commit, population, label version, model configuration, seed, outputs, and checksums.

The initial feature families should include resolved dependency reach, direct and transitive dependents, depth-weighted reach, maintainer reach and concentration, package popularity and activity, weak-link metadata, public workflow observability, workflow permissions, action pinning, deployment indicators, OIDC indicators, runner type, and explicit missingness.

The baseline sequence should be: random and prevalence-matched ranking, popularity, dependency centrality, maintainer reach, workflow exposure, weak-link metadata, regularized logistic regression, gradient-boosted trees, homogeneous graph learning, and finally a heterogeneous graph model. The model that best supports the data and the defensive use case should win, regardless of whether it is HGAT.

Primary evaluation metrics should be Precision@K, Recall@K, Average Precision, NDCG, MRR, calibration, confidence intervals, and review-cost curves. ROC-AUC may be reported but should not be the sole metric for a rare-event ranking task.

## 6. Label strategy

Use CISA, registry, maintainer, and high-quality incident sources to create a high-precision label table. The 2025 Shai-Hulud campaign is documented by CISA as a widespread npm compromise involving more than 500 packages and automated propagation through compromised developer credentials.[20] The 2026 Axios incident is documented by CISA and the Axios maintainer: `axios@1.14.1` and `axios@0.30.4` injected `plain-crypto-js@4.2.1`, with a short publication window.[21][22]

These are valuable anchors, but they are not sufficient for an ecosystem-wide model. Shai-Hulud is a multi-package campaign whose package-level involvement must be reconstructed carefully. Axios is a version-specific compromise with a short exposure period. Every label should contain package, version or range, event time, first public detection, removal time if known, incident family, evidence URLs, confidence, and whether the package was directly or indirectly involved.

OSV is useful because it aggregates vulnerability databases and represents affected versions, but an OSV record is not automatically a targeted-compromise label.[23]

## 7. Safety and ethics

The project should remain defensive. Static analysis should operate on archived artifacts without executing lifecycle scripts. Any dynamic research should use synthetic packages or a formally approved isolated environment with no network access, no host secrets, resource limits, pinned images, and disposable state. Do not publish payloads, credentials, private repository content, raw maintainer emails, or operational instructions for compromise. Report new findings through coordinated disclosure.

## 8. Final recommendation

Proceed with the research under this title or a safer refinement such as:

> **Pre-Incident Defensive Prioritization of High-Leverage npm Packages Using Dependency, Maintainer, and CI/CD Exposure Graphs**

The first publishable milestone should be a benchmark and gap-aware empirical study, not a neural architecture demonstration. The thesis becomes strong if it can show, under strict temporal validation, that the proposed cross-domain features improve defensive ranking over established baselines and that the result remains useful after controlling for popularity, public-repository bias, resolution error, and label uncertainty.

If HGAT adds measurable value, include it as the relation-aware model. If it does not, report the simpler model and explain why interpretability and reproducibility are preferable. Either outcome can be scientifically valuable; the weak outcome would be claiming successful prediction before the evidence exists.

## References

[1]: https://github.com/ashik-hstu/npm-supply-chain-research "Project repository"

[2]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/scripts/collect_data.py "Collection implementation"

[3]: https://github.com/ashik-hstu/npm-supply-chain-research/blob/master/scripts/calculate_metrics.py "Metric implementation"

[4]: https://www.notion.so/ha5an/Predicting-the-Blast-Radius-Forecasting-High-ROI-Attack-Entry-Points-in-Software-Supply-Chains-via--340379c3555d80fb8da0e0463e750c75 "Supplied thesis draft"

[5]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al."

[6]: https://arxiv.org/abs/2112.10165 "Zahan et al."

[7]: https://arxiv.org/abs/2005.09535 "Ohm et al."

[8]: https://www.cs.cmu.edu/~gferreir/pre-prints/icse2019-detecting-suspicious-package-updates.pdf "Garrett et al."

[9]: https://arxiv.org/abs/2202.13953 "Amalfi"

[10]: https://www.usenix.org/conference/usenixsecurity24/presentation/huang-cheng "DONAPI"

[11]: https://arxiv.org/html/2309.02637v2 "Cerebro"

[12]: https://dl.acm.org/doi/10.1145/3691620.3695492 "SpiderScan"

[13]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142 "Liu et al."

[14]: https://link.springer.com/article/10.1007/s10664-022-10154-1 "Zerouali et al."

[15]: https://link.springer.com/article/10.1007/s10664-021-09951-x "Chinthanet et al."

[16]: https://ieeexplore.ieee.org/iel7/8858/4358699/10061526.pdf "Pan et al."

[17]: https://link.springer.com/chapter/10.1007/978-3-032-12089-2_14 "Riggio and Pautasso"

[18]: https://arxiv.org/abs/2601.14455 "Fares et al."

[19]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub Actions secure-use guidance"

[20]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA Shai-Hulud alert"

[21]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA Axios alert"

[22]: https://github.com/axios/axios/issues/10636 "Axios post-mortem"

[23]: https://google.github.io/osv.dev/ "OSV documentation"
