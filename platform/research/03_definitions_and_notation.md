# Working Definitions and Notation

## Scope

The project should use precise defensive terminology. The proposed quantities are observable or derived proxies. They are not direct measurements of attacker intent, compromise probability, credential value, or private infrastructure impact.

## Graph

Let the time-indexed heterogeneous graph be:

\[
G_t = (V_t, E_t, \tau, \phi),
\]

where package nodes, maintainer nodes, and repository or infrastructure nodes are typed by \(\tau\), and dependency, ownership, hosting, workflow, and other relationships are typed by \(\phi\). Every feature and edge used to rank a target at time \(t\) must be available no later than \(t\).

The package dependency relation should be version-aware. A package-version node is preferable for resolution analysis, while a package-level projection may be used for ecosystem ranking if the projection rule is stated explicitly.

## Wormability proxy

For package \(v\), let \(M(v)\) be the set of maintainers associated with that package under the selected npm metadata snapshot. Let \(P(m,t)\) be the set of packages associated with maintainer \(m\) at time \(t\). Candidate measures include:

\[
W_{\max}(v,t) = \max_{m \in M(v)} |P(m,t)|
\]

and

\[
W_{\sum}(v,t) = \sum_{m \in M(v)} |P(m,t)|.
\]

These measures represent **shared-maintainer reach**. They should not be called a probability of lateral propagation. Maintainer records may be incomplete, usernames may be reused or aliased, and package ownership does not prove that a single credential controls every associated package.

## Blast Radius proxy

Let \(Dep_t(v)\) be the set of downstream package nodes that depend on \(v\) under a stated dependency-resolution and graph-projection procedure. Let \(C(d,t)\) indicate an observable CI/CD property of dependent \(d\). The simplest proposed proxy is:

\[
B_{\mathrm{workflow}}(v,t) = \sum_{d \in Dep_t(v)} C(d,t).
\]

Possible refinements include depth weighting, repository activity weighting, workflow recency, workflow permission scope, deployment indicators, OIDC or trusted-publishing indicators, and a separate missingness indicator for private or unavailable repositories.

A visible `.github/workflows` directory is only evidence of **public workflow observability**. It is not evidence that a workflow has cloud credentials, write permissions, deployment access, or an exploitable trust relationship.

## Defensive structural leverage score

The proposed score can be represented as:

\[
L(v,t) = \alpha f_W(W(v,t)) + \beta f_B(B(v,t)) + \gamma f_P(Pop(v,t)) + \delta f_H(H(v,t)),
\]

where \(f_W\) and \(f_B\) are documented normalization functions, \(Pop\) is a popularity or adoption control, and \(H\) denotes optional package-hygiene or known-risk features. The inclusion of popularity controls is essential because dependent count and maintainer reach can be strongly correlated with popularity.

For a neural model, the output should be named a **ranking score** or calibrated probability of the defined label, not an “attacker ROI” unless the label and interpretation justify that language.

## Label

A positive label must be tied to a dated, documented event and an affected package or version. Recommended labels are multi-class or confidence-weighted:

| Label | Meaning |
|---|---|
| `confirmed_targeted_compromise` | A reliable incident source documents malicious publication or compromise of a package or maintainer |
| `malicious_publication` | A package version is documented as intentionally malicious, but targeting or lateral movement is unclear |
| `dependency_confusion` | A documented name-resolution or namespace-confusion incident affected the package or consumer |
| `ordinary_vulnerability` | A security vulnerability without evidence of intentional compromise |
| `ambiguous` | The evidence is insufficient for a high-confidence class |

The final benchmark should not treat all OSV advisories or keyword matches as equivalent compromise labels.

## Prediction task

For an observation date \(t\) and horizon \(h\), the primary task is:

> Rank package nodes using only information available at or before \(t\), then evaluate whether packages receiving a confirmed positive label in \((t, t+h]\) are prioritized.

This formulation makes temporal leakage auditable and separates ranking utility from causal claims.

## Reference standards

The definitions are informed by prior findings that npm has maintainer and package single points of failure [1], that weak-link metadata signals can identify security-relevant exposure [2], and that accurate npm dependency resolution is necessary for ecosystem propagation analysis [3].

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., npm ecosystem security threats"

[2]: https://arxiv.org/abs/2112.10165 "Zahan et al., npm weak links"

[3]: https://dl.acm.org/doi/abs/10.1145/3510003.3510142 "Liu et al., dependency-tree vulnerability propagation"
