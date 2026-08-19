# Related-Work Review

## Review question

The review asks: **What has already been studied about software-supply-chain package risk, dependency impact, maintainer concentration, malicious-package detection, and CI/CD exposure, and what remains open for a pre-incident defensive ranking model?**

The literature separates into several research traditions. This distinction is essential because a detector that identifies malicious code after publication is solving a different problem from a model that ranks structurally high-leverage packages before compromise.

## Research traditions

### Ecosystem structure and single points of failure

Zimmermann et al. study npm package dependencies, maintainers, and public security issues at ecosystem scale. They find that individual packages can affect large parts of the ecosystem and that a small number of maintainer accounts could inject code into a majority of packages. This is the closest prior support for the proposed maintainer-mediated reach feature, but it does not establish a CI/CD-aware pre-incident ranking model.[1]

Zahan et al. analyze metadata from 1.63 million npm packages and propose six weak-link signals, including install scripts, expired maintainer email domains, and inactive packages or maintainers. Their work is large-scale and practitioner-informed, but its focus is package weakness signals rather than downstream infrastructure exposure or incident-time target ranking.[2]

Ohm et al. contribute a manually analyzed dataset of 174 malicious packages used in real-world attacks across npm, PyPI, and RubyGems, together with attack trees. Their contribution is valuable for label construction and threat taxonomy, but it is descriptive and not a learned pre-incident ranking system.[3]

### Dependency propagation and impact analysis

Dependency-network studies analyze how vulnerabilities propagate through direct and transitive dependencies. Liu et al. show that npm-specific dependency-resolution rules matter: simply using reachability can resolve the wrong dependency tree, leading to incorrect propagation analysis. Their DVGraph contains more than 10 million library versions and 60 million resolved dependency relations, illustrating the scale and precision required for ecosystem-wide claims.[4]

Zerouali et al. study how vulnerabilities affect direct and indirect dependents in npm and RubyGems, including both package releases and external GitHub projects. Chinthanet et al. analyze adoption and propagation lags over a network of 1,553,325 npm releases. These studies support the importance of downstream reach but focus on vulnerability exposure and remediation dynamics, not intentional compromise or CI/CD privilege.[5][6]

### Malicious-package and suspicious-update detection

Garrett et al. use unsupervised anomaly detection over security-relevant features of npm package updates. Their approach aims to reduce manual review effort and detect suspicious changes, including a confirmed malicious update. The unit of analysis is a package update and the objective is behavioral or change anomaly, not ecosystem target prioritization.[7]

Sejfia and Schäfer’s Amalfi combines machine-learning classifiers, source reproducibility checking, and clone detection to find potentially malicious npm packages. DONAPI combines static and dynamic analysis with a behavior knowledge base and reports a large local package cache and manually confirmed samples. Cerebro extends behavior-sequence modeling across NPM and PyPI. SpiderScan models suspicious behavior as graphs using control-flow and data-dependence relationships, then matches target packages to known malicious behavior graphs.[8][9][10][11]

These systems are highly relevant competitors for the phrase “graph-based malicious-package detection,” but they do not solve the same task as the proposed structural ranking problem. They are primarily concerned with whether package behavior is malicious, whereas the proposed work asks which package should receive defensive attention because of its potential downstream leverage.

### CI/CD and infrastructure exposure

CI/CD studies show why a workflow-presence feature is potentially valuable but also why a directory-level binary is insufficient. Pan et al. measure more than 320,000 GitHub repositories with CI/CD pipelines and identify security-critical usage patterns and attack surfaces. Riggio and Pautasso study more than 200,000 GitHub workflow specification files and report widespread security misconfigurations. Fares et al. compare nine workflow security scanners on 2,722 workflows and find major differences in coverage and reported weaknesses.[12][13][14]

GitHub’s own security guidance identifies least-privilege token permissions, secrets handling, untrusted triggers, third-party action pinning, OIDC, environment protections, and self-hosted runner exposure as important dimensions. Therefore, the current repository’s `has_github_workflows` variable should be treated as a coarse observability signal, not as a measurement of infrastructure privilege.[15]

## Comparison matrix

| Study | Primary objective | Main data or unit | Method | Main value to this project | Important limitation for the proposed question |
|---|---|---|---|---|---|
| Zimmermann et al. [1] | Measure npm structural security threats | Packages, dependencies, maintainers | Ecosystem measurement | Establishes maintainer and package single points of failure | Does not model CI/CD exposure or prospective target ranking |
| Zahan et al. [2] | Identify npm weak-link signals | 1.63M package metadata records | Large-scale empirical analysis and developer survey | Strong metadata baselines and signal taxonomy | Weakness signals are not attacker-leverage labels or out-of-time predictions |
| Ohm et al. [3] | Characterize real-world malicious packages | 174 package artifacts across ecosystems | Manual analysis and attack trees | Provides incident taxonomy and label candidates | Small, historical, manually collected, descriptive dataset |
| Garrett et al. [7] | Detect suspicious npm updates | Package versions and update features | Unsupervised clustering | Strong update-anomaly baseline | Detects suspicious changes, not structural downstream impact |
| Liu et al. [4] | Analyze vulnerability propagation precisely | 10M+ versions and resolved dependency relations | Knowledge graph and dependency-tree resolution | Demonstrates need for npm-accurate resolution | Focuses on vulnerabilities, not intentional compromise or workflows |
| Zerouali et al. [5] | Measure vulnerability exposure | npm and RubyGems dependency networks | Empirical propagation analysis | Supports downstream-impact evaluation | Does not model CI/CD privilege or attacker targeting |
| Chinthanet et al. [6] | Study fix adoption and propagation lag | 1.55M npm releases | Longitudinal empirical study | Supports temporal evaluation and snapshot discipline | Studies remediation rather than pre-incident target ranking |
| Amalfi [8] | Detect malicious npm packages | Published package versions | ML plus source reproducibility and clone detection | Practical maliciousness baseline | Package-behavior classification, not ecosystem leverage |
| DONAPI [9] | Detect malicious npm behavior | Large npm cache and behavior sequences | Static/dynamic analysis and behavior knowledge base | Strong behavior-based detector comparison | Requires code analysis and labels; different prediction task |
| Cerebro [10] | Cross-ecosystem malicious behavior detection | NPM and PyPI packages | Behavior sequences and language-model classifier | Shows current state of package-behavior modeling | Does not rank infrastructure leverage or use maintainers/dependents |
| SpiderScan [11] | Detect malicious packages via behavior graphs | NPM code and suspicious behavior graphs | Control/data-dependence graph matching with dynamic confirmation | Closest “graph + malicious package” prior art | Graphs describe code behavior, not ecosystem relations |
| Pan et al. [12] | Measure CI/CD attack surfaces | 320K+ GitHub repositories | Workflow parsing and security analysis | Supports richer infrastructure features | Does not link workflow risk to package-level incident prediction |
| Riggio and Pautasso [13] | Measure GitHub workflow misconfiguration | 200K+ workflow files | Static misconfiguration detectors | Provides workflow-risk feature taxonomy | Not a package-impact ranking model |
| Fares et al. [14] | Compare workflow scanners | 2,722 workflows and nine scanners | Scanner coverage/performance comparison | Shows observable workflow security is multidimensional | Scanner benchmarking, not cross-domain package ranking |

## Synthesis

The closest prior work establishes four facts relevant to this proposal:

1. npm’s package and maintainer graph contains structural concentration and single points of failure.[1]
2. Package metadata and update behavior can provide weak-link or anomaly signals at ecosystem scale.[2][7]
3. Downstream reach and dependency resolution materially affect ecosystem-wide impact.[4][5]
4. CI/CD workflow security depends on detailed permissions, triggers, actions, secrets, and runner properties, not merely workflow existence.[12][13][15]

No reviewed source directly establishes the full proposed combination: **time-aligned package dependency structure + maintainer-mediated reach + downstream CI/CD security observables + pre-incident ranking of later compromised packages**. That combination is a plausible research gap, but the novelty claim remains conditional. The study must show that the combination predicts something that simpler combinations do not, and it must distinguish structural leverage from maliciousness detection.

## Implications for study design

The literature suggests that the project should not begin with HGAT. It should first build a benchmark in which the following baselines are hard to beat: dependent count, resolved transitive reach, maintainer out-degree, package popularity, age and activity, weak-link metadata, workflow security features, and a regularized tabular model. Only after those baselines are established should the project test a heterogeneous graph model.

The most valuable empirical contribution may be a carefully time-split benchmark and feature-ablation study rather than the use of a particular neural architecture. If the neural model does not improve ranking, calibration, or transfer to later incidents, that negative result is informative and should be reported.

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman

[2]: https://arxiv.org/abs/2112.10165

[3]: https://arxiv.org/abs/2005.09535

[4]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142

[5]: https://link.springer.com/article/10.1007/s10664-022-10154-1

[6]: https://link.springer.com/article/10.1007/s10664-021-09951-x

[7]: https://www.cs.cmu.edu/~gferreir/pre-prints/icse2019-detecting-suspicious-package-updates.pdf

[8]: https://arxiv.org/abs/2202.13953

[9]: https://www.usenix.org/conference/usenixsecurity24/presentation/huang-cheng

[10]: https://arxiv.org/html/2309.02637v2

[11]: https://dl.acm.org/doi/10.1145/3691620.3695492

[12]: https://ieeexplore.ieee.org/iel7/8858/4358699/10061526.pdf

[13]: https://link.springer.com/chapter/10.1007/978-3-032-12089-2_14

[14]: https://arxiv.org/abs/2601.14455

[15]: https://docs.github.com/en/actions/reference/security/secure-use
