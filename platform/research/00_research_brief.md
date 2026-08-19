# Research Brief

## Executive assessment

**Preliminary judgment: the research is worthy, but the publishable contribution must be narrowed and empirically rebuilt.** The topic is important because prior work shows that npm’s dependency and maintainer structure creates ecosystem-wide single points of failure, while other studies show that malicious-package detection and vulnerability analysis mostly focus on package behavior, metadata, or propagation after a vulnerable package is known. The proposed study’s potentially distinctive contribution is a **defensive ranking problem** that combines dependency reach, shared-maintainer reach, and observable downstream CI/CD exposure before an incident is known.[1][2][3]

The proposal is not yet a demonstrated HGAT result. The current repository contains a substantial data-collection and deterministic metric pipeline, but no graph-learning model, temporal experiment runner, baseline suite, or reproducible back-test implementation. The thesis draft and methodology documents describe these components, but the claims of successful HGAT performance against named incidents remain **unverified until the experiments and labels are published**.[4][5]

## Proposed contribution

The proposal models the npm ecosystem as a heterogeneous graph containing package, maintainer, and repository or infrastructure entities. It defines two structural features:

- **Wormability:** intended lateral reach associated with maintainers who control multiple packages.
- **Blast Radius:** intended downstream infrastructure exposure, approximated through dependent packages whose public repositories contain CI/CD workflows.

The proposed Attacker ROI score combines normalized versions of these quantities. The research should frame this as a **defensive structural leverage or target-prioritization score**, because the current observables do not directly measure exploitability, attacker intent, credential value, or the probability that a package will actually be compromised.

## What is already supported

The current repository implements collection from the npm Registry, deps.dev, GitHub GraphQL, and OSV; stores package, maintainer, dependency, version, workflow, and advisory records in SQLite; and computes deterministic wormability, reverse dependency reachability, workflow-aware blast radius, and a weighted ROI score. The bundled snapshot contains approximately 25,000 packages, 22,000 package versions, 12,000 maintainers, 122,000 dependency edges, and more than 21,000 mapped repositories.[4]

Prior studies provide strong support for the general importance of the problem. Zimmermann et al. report that npm contains single points of failure associated with popular packages and a small number of maintainer accounts.[1] Zahan et al. analyze 1.63 million npm packages and identify metadata weak-link signals including install scripts, expired maintainer domains, and inactive packages.[2] Ohm et al. provide a manually analyzed dataset of 174 real-world malicious packages across npm, PyPI, and RubyGems.[3] Garrett et al. show the feasibility of anomaly detection for suspicious npm updates, while Liu et al. demonstrate that accurate dependency resolution matters for ecosystem-wide propagation analysis.[6][7]

## Early novelty assessment

The topic is **not novel merely because it uses npm graphs, maintainers, or machine learning**. Those elements already appear in prior work. A defensible novelty claim would instead require showing that a time-aligned, cross-domain ranking model incorporating public downstream CI/CD exposure adds predictive value beyond established baselines such as dependent count, maintainer out-degree, popularity, package-hygiene features, known-vulnerability scores, and behavior-based detection.

The strongest potential novelty is therefore the combination of:

1. a pre-incident ranking objective rather than post-compromise detection;
2. an explicit distinction between software reach and infrastructure exposure; and
3. a rigorous temporal evaluation that asks whether the ranking would have prioritized later compromised packages before their compromise dates.

These are hypotheses about contribution, not conclusions. The work must demonstrate incremental value through ablations, time-split evaluation, calibration, and incident-level analysis.

## Main methodological risks

The largest risks are temporal leakage, label scarcity, public-repository bias, incorrect npm dependency resolution, popularity confounding, maintainer identity ambiguity, and equating a visible workflow directory with privileged or reachable infrastructure. The current code also uses a limited seed-and-expansion strategy and checks workflow-directory presence rather than workflow permissions, secrets exposure, OIDC configuration, or actual downstream use. These limitations should be made explicit rather than hidden behind the term “ROI.”

The proposal should also avoid relying on a single named incident or a small positive set. A single-case demonstration cannot establish predictive validity, and an apparently successful ranking can arise because popularity, package age, or dependent count already identify the target. The minimum credible study needs multiple temporally separated incidents, carefully defined labels, strong non-neural baselines, and confidence intervals.

## Recommended research direction

Proceed with a **two-stage contribution**:

1. Build and validate an interpretable structural-risk ranking benchmark with versioned historical snapshots, precise dependency resolution, high-precision compromise labels, and publicly reproducible features.
2. Add an HGAT or other heterogeneous graph model only as a controlled comparison, with ablations showing whether relation-aware message passing improves ranking over simpler models.

If the graph model does not improve out-of-time ranking or calibration, the result should still be publishable as a careful empirical study of structural supply-chain leverage and the limits of public CI/CD observability. A simpler and more interpretable model is preferable if it performs comparably.

## Initial decision

| Decision dimension | Preliminary result |
|---|---|
| Importance | High: supply-chain compromise and maintainer concentration are established security concerns |
| Closest prior art | Strong: npm weak-link analysis, ecosystem centrality, malicious-package detection, and dependency-propagation studies |
| Potential novelty | Moderate and conditional: cross-domain pre-incident ranking with CI/CD exposure may be distinctive |
| Current implementation readiness | Partial: collection and deterministic metrics exist; HGAT and evaluation are absent |
| Main publication risk | Overclaiming predictive performance or novelty without temporal, multi-incident evidence |
| Recommendation | Proceed after narrowing the claim and designing the benchmark first |

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., Small World with High Risks"

[2]: https://arxiv.org/abs/2112.10165 "Zahan et al., What are Weak Links in the npm Supply Chain?"

[3]: https://arxiv.org/abs/2005.09535 "Ohm et al., Backstabber’s Knife Collection"

[4]: https://github.com/ashik-hstu/npm-supply-chain-research "Project repository and current implementation"

[5]: https://www.notion.so/ha5an/Predicting-the-Blast-Radius-Forecasting-High-ROI-Attack-Entry-Points-in-Software-Supply-Chains-via--340379c3555d80fb8da0e0463e750c75 "Supplied Notion thesis draft"

[6]: https://www.cs.cmu.edu/~gferreir/pre-prints/icse2019-detecting-suspicious-package-updates.pdf "Garrett et al., Detecting Suspicious Package Updates"

[7]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142 "Liu et al., Demystifying Vulnerability Propagation"
