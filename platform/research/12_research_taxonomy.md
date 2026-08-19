# Research Taxonomy

## Why a taxonomy is needed

The current draft uses terms such as “graph neural network,” “malicious package detection,” “blast radius,” and “attacker ROI” in ways that span several distinct research problems. The taxonomy below prevents false novelty claims and makes the evaluation target explicit.

| Research family | Typical question | Primary object | Typical labels | Representative methods | Relation to this project |
|---|---|---|---|---|---|
| Package-behavior detection | Is this package or update exhibiting malicious behavior? | Package code, manifest, update diff, runtime trace | Malicious/benign package or update | Static analysis, dynamic analysis, anomaly detection, behavior sequences, code graphs | Important detector baseline, but not the same task |
| Vulnerability propagation | Which packages or projects are exposed to a known vulnerability? | Version-resolved dependency tree | Vulnerable version and affected range | Dependency resolution, reachability, propagation lag analysis | Supplies graph and temporal methods |
| Ecosystem centrality | Which packages or maintainers are structurally central or fragile? | Package-maintainer dependency graph | Usually none or descriptive risk indicators | Degree, reachability, concentration, graph statistics | Closest foundation for Wormability and structural reach |
| Package weak-link analysis | Which metadata signals indicate elevated supply-chain weakness? | Package and maintainer metadata | Weak-link signal or survey agreement | Heuristics and large-scale empirical analysis | Strong baseline and feature source |
| CI/CD security analysis | Which workflows contain dangerous permissions, triggers, actions, or runner configurations? | Workflow files and execution settings | Misconfiguration or security weakness | Static workflow scanners, taint analysis, configuration analysis | Supplies richer infrastructure-exposure features |
| Incident attribution and threat intelligence | What happened in a known campaign and which artifacts were affected? | Incident, package, version, maintainer, time | Confirmed compromise and campaign family | Manual analysis, advisories, post-mortems | Supplies high-precision labels |
| Proposed structural target ranking | Which packages should defenders prioritize before a future incident? | Time-indexed cross-domain graph | Future compromise or high-leverage case | Interpretable scores, tabular models, heterogeneous GNNs | The intended contribution |

## Distinguishing prediction from detection

A detector often observes the package artifact or update and predicts whether it is malicious. A target-ranking model observes the ecosystem before a compromise and predicts which nodes will later be associated with a documented incident. The feature availability, label construction, and evaluation protocol are therefore different.

A behavior detector can legitimately use package code introduced in the candidate version. A pre-incident ranking model cannot use the malicious version, advisory publication, removal status, post-incident workflow changes, or incident-specific indicators that were unavailable at the prediction timestamp.

## Distinguishing reach from privilege

Dependency reach measures how many package or project nodes can be reached through a graph. CI/CD exposure measures properties of downstream build or release environments. Privilege is a further concept involving permissions, credentials, secrets, runner isolation, deployment access, and organizational controls. The project should not collapse these into one quantity without a validation study.

## Distinguishing structural leverage from compromise likelihood

A package can have high structural leverage but low compromise likelihood, and a package can be compromised without having unusually high structural leverage. The study should either model two separate outputs—structural leverage and incident likelihood—or explicitly treat structural leverage as a prioritization feature rather than as a complete risk probability.

## Recommended positioning statement

> This study evaluates whether a time-aligned, cross-domain ranking model can prioritize packages associated with later documented supply-chain compromises more effectively than established graph, metadata, behavior, and workflow-security baselines. It does not claim that a high score proves exploitability, attacker intent, or private infrastructure privilege.

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman

[2]: https://arxiv.org/abs/2112.10165

[3]: https://arxiv.org/abs/2202.13953

[4]: https://www.usenix.org/conference/usenixsecurity24/presentation/huang-cheng

[5]: https://dl.acm.org/doi/10.1145/3691620.3695492

[6]: https://ieeexplore.ieee.org/iel7/8858/4358699/10061526.pdf
