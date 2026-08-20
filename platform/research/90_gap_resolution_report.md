# From “Attack-ROI Prediction” to an Auditable npm Defense Benchmark

**Author:** Manus AI  
**Research status:** Evidence-backed redesign and reproducible current-snapshot audit  
**Scope:** npm package ecosystem, public repository configuration, and documented supply-chain incidents

## Executive assessment

The original question—whether software-supply-chain blast radius can be used to forecast high-return attack entry points—is **research-worthy**, but not in its original form. A claim that a graph model predicts an attacker’s return is not currently defensible: attacker utility is unobserved, public package data omit decisive private controls, the available snapshot is not temporally reconstructed, and verified future compromise labels are sparse and heterogeneous. Presenting a weighted structural score as attacker ROI would overstate what the data measure.

The review instead identifies a publishable and operationally useful contribution: a **time-aware, multi-queue benchmark for defensive prioritization**. The study compares three distinct review surfaces—structural leverage, public CI/CD configuration, and release-authority discontinuity—against separately adjudicated package-version incidents. It asks what each queue is useful for, where they overlap, whether any signal improves ranking beyond transparent baselines, and when public evidence is insufficient. This contribution is novel only if it releases the time-indexed join, preserves missingness and provenance, uses grouped temporal evaluation, and publishes negative results as readily as positive ones.

> **Core conclusion:** dependency reach is a credible exposure descriptor, public workflow configuration is a meaningful but incomplete security surface, and release-authority change is a distinct review signal. None is, alone or in combination, a validated proxy for attacker ROI or a guarantee of compromise prediction.

## What prior work establishes—and what it leaves open

| Research stream | Established contribution | Remaining opening for this project |
|---|---|---|
| npm ecosystem concentration | A small number of packages and maintainers can have broad downstream influence; unmaintained dependencies create systemic exposure.[1] | Evaluate structural leverage as a *review queue* under dated, version-aware conditions rather than claiming a causal attack score. |
| npm weak links | Metadata signals such as install scripts, inactive ownership, and expired maintainer domains can surface proactive concerns in a large npm corpus.[2] | Compare structural and public-CI/CD features against hygiene baselines instead of treating them as new. |
| Supply-chain incident corpora | Documented malicious packages and attack trees support defensive research but require careful source and label interpretation.[3] | Build a version-specific, evidence-graded label registry with distinct event and disclosure times. |
| GitHub CI/CD security | Workflow permissions, triggers, third-party actions, and access to secrets are security-relevant; broad measurements reveal widespread risky configurations.[4] | Parse public configuration history rather than using a binary “workflow exists” proxy. |
| Workflow vulnerability analysis | Static analysis can find workflow vulnerabilities that pattern checks miss.[5] | Do not equate static workflow features with compromise probability; retain a review-surface target. |
| Release-authority records | Public release-path discontinuities can produce a pre-payload review queue; the reviewed cohort reported zero overlap with exact malicious versions.[6] | Compare authority discontinuity against other queues, rather than claiming it detects malicious payloads. |
| Historical dependency resolution | Release-point dependency resolution can be reconstructed and released for npm, PyPI, and crates.io research.[7] | Reuse it where possible; contribute label linkage, authority/workflow history, and decision evaluation rather than graph reconstruction alone. |
| Malicious-package detection | Recent benchmarking evaluates code-, metadata-, dynamic-, ML-, and LLM-based detection of malicious package content.[8] | Keep post-publication payload detection distinct from pre-incident prioritization. |

The new work changes the novelty boundary substantially. Structural leverage, weak-link signals, public workflow security, malicious-content detection, release-authority review, and historical dependency resolution all have active research bases. The credible gap lies at their boundary: **a provenance-complete, time-aware comparison of defensively actionable but semantically distinct queues**.

## Real-data audit: what the current repository actually supports

Two reproducible analyses were performed directly on the committed private-repository archives. The CSV audit uses `data/metrics_summary.csv.zip`, SHA-256 `43e1845a106719ef9fb8c7d72d174959cc25e6f8fe8a3c6bfcd6cb7ca8e90a35`. The database audit uses `data/npm_ecosystem.db.zip`, SHA-256 `ab45439cf94cf43f3133b0aaff644557d55e86e99430a0a7937bfd0ce5266315`. Scripts and machine-readable outputs are included alongside this report: `scripts/analyze-structural-leverage.mjs`, `scripts/analyze_ecosystem_structure.py`, `51_current_snapshot_structural_analysis.json`, and `55_current_snapshot_ecosystem_structure.json`.

| Finding | Observed result | Interpretation |
|---|---:|---|
| Current metric population | 25,228 packages | This is a repository snapshot, not an npm census. |
| Non-zero `blast_radius` | 20 packages (0.0792%) | The existing discrete field is too sparse to serve as a stand-alone outcome or broad ranking feature. |
| Non-zero workflow-bearing-direct-dependent count | 15 packages (0.0594%) | The present aggregate workflow proxy discards nearly all available workflow information. |
| Package-version rows with public GitHub linkage | 21,527 / 22,340 (96.3607%) | Public workflow-history reconstruction is feasible for much of the snapshot. |
| Package-version rows with fetched workflows present | 15,300 / 22,340 (68.4870%) | Parsed public CI/CD features are a viable work package. |
| Top 1% maintainers’ share of package–maintainer relations | 18,027 / 79,405 (22.7026%) | Current data show meaningful ownership concentration, but not compromise risk. |
| Legacy score ∩ transitive-reach queue, top-1% budget | 16 / 253 packages | The legacy score is not simply a transitive-reach ranking. |
| Advisory package-name overlap with metrics | 164 packages | The archive advisory table cannot form a broad primary label cohort for this snapshot. |

The database analysis also reveals why the task must not jump to a graph model. The archive stores no package-version publication time and no advisory-to-version mapping. Its `153,488` advisory rows cover `153,009` package names, with `153,422` broadly classified as `compromise`; this is unsuitable as manually adjudicated package-version ground truth. The correct response is not to train on it anyway, but to treat it as candidate discovery and construct an evidence-graded seed registry.

## High-confidence incident anchors

The project now contains `52_seed_incident_registry.csv`, a deliberately small registry designed to make label quality visible. CISA reports that Axios versions `1.14.1` and `0.30.4` injected the malicious `plain-crypto-js@4.2.1` dependency on 31 March 2026.[9] The registry preserves the event date separately from CISA’s later public alert date. It also records Shai-Hulud as a confirmed campaign but deliberately excludes it from package-version primary positives until each package/version can be corroborated with a dated affected-version list. CISA described Shai-Hulud as a credential-harvesting, automated publication campaign that compromised more than 500 packages; CERT/CC further documents the propagation context.[10] [11]

This distinction matters. A compromised maintainer target, an injected malicious dependency, a campaign-associated package, an ordinary vulnerability, and a public authority-path change are all different objects. Collapsing them into a single binary label creates a benchmark that cannot answer a coherent research question.

## The selected study: three queues, separate targets

The research program is formalized in `50_gap_resolution_study_protocol.md`. Each package-version observation has a cutoff time \(t\), and only facts public or reconstructed at or before \(t\) may be used. The study uses three transparent queues.

| Queue | Primary components | Appropriate decision | Prohibited inference |
|---|---|---|---|
| **S — Structural leverage** | Version-aware downstream reach; maintainer/control concentration | Where a compromise could have broad downstream impact | Which package an attacker will choose |
| **W — Public workflow observability** | Declared permissions, privileged triggers, action pinning, OIDC, runner labels, workflow churn | Which public automation configurations merit review | Actual secret scope, cloud privilege, or deployment impact |
| **A — Release authority** | Predecessor-aware publisher, repository, workflow, provenance, signing, and mediation changes | Which releases merit control-plane review | Malicious payload detection |

The primary outcome is `future_confirmed_compromise`: a reviewed package/version incident whose event begins within a stated horizon after the cutoff. A secondary outcome is `future_malicious_publication`. A `review_surface` is **not** an outcome; it is a queue membership result. This design preserves the fact that recent release-authority work defines a useful review surface but does not claim it overlaps exact malicious versions.[6]

## Evaluation design that can survive review

The benchmark must use rolling-origin splits, retain an untouched final period, and group incident families so related package releases cannot leak across training and test. Every feature requires a source, effective date, cutoff rule, historical-fidelity grade, missingness reason, and immutable reference; the machine-readable initial ledger is `53_feature_availability_ledger.csv`.

The model ladder starts with review-budget baselines, direct/transitive dependents, dated popularity, package age, and weak-link metadata. It then adds an interpretable regularized model and a nonlinear tabular comparator. A homogeneous graph model and then an HGAT are optional **only** if they add stable out-of-time value under exactly the same feature availability and grouped splits. Attention weights must never be interpreted as causal explanations.

| Measure | Why it is required |
|---|---|
| Recall@K and Precision@K | Defenders work with finite review capacity. |
| PR-AUC and enrichment over prevalence | Positives are rare; ordinary accuracy is misleading. |
| NDCG | Ranking position matters when a queue is inspected in order. |
| Brier score and calibration slope | A probability claim requires calibration, not only ranking. |
| Family-clustered bootstrap intervals | Related campaign records violate naïve independent-row assumptions. |
| Label-shuffle sanity check | Confirms the pipeline does not obtain performance from leakage or a coding artifact. |

## Staged implementation roadmap

| Stage | Deliverable | Decision gate |
|---|---|---|
| 1. Preserve current evidence | Snapshot audit, schema profile, source checksums, seed incident registry | Complete in this revision. |
| 2. Reconstruct dated features | Release-point dependency views, package ownership history, GitHub workflow commit snapshots | Stop if cutoff-valid history cannot be established for a usable cohort. |
| 3. Expand and adjudicate labels | Version-level registry with event time, evidence hierarchy, reviewer rationale, and campaign-family key | Stop if high-confidence positives remain too sparse for uncertainty-qualified temporal evaluation. |
| 4. Run queue-overlap pilot | S/W/A candidate volume, stability, overlap, and a reviewer sample | Publish as a review-surface study if no valid outcome cohort exists. |
| 5. Run temporal baseline ladder | Transparent scores, regularized model, boosted trees, then optional graph model | Retain complex model only on stable incremental out-of-time value. |
| 6. Release artifacts | Data dictionary, code, split manifest, feature ledger, result tables, limitations | Do not release raw tokens, private repository data, or inferred secrets. |

## Research value and limitation statement

The project is now strongest as a **security engineering and empirical-software-engineering benchmark**. It can produce useful evidence even if no model predicts compromise well: a negative result showing that public structure and workflow configuration do not outperform simple confounding baselines would be valuable and would discourage unsafe risk claims. A positive result would still be bounded—it would establish limited ranking utility in a stated cohort, not attacker intent, causality, or deploy-time safety.

The major remaining cost is data engineering and label review, not model architecture. Historical version resolution can be reused from modern tools and datasets, while public GitHub linkage makes workflow reconstruction technically feasible. However, public YAML cannot reveal secret values, organization defaults, cloud policy, private workflows, or whether a risky-looking path actually executed. GitHub’s secure-use guidance makes those limitations explicit.[12] The publication should therefore state that it ranks **publicly observable review surfaces**, not organizations or maintainers.

## Organized artifact map

| Artifact | Function |
|---|---|
| `93_gap_resolution_evidence_log.md` | Source-by-source evidence, novelty boundary, and incident provenance log |
| `50_gap_resolution_study_protocol.md` | Pre-registered target, feature, split, baseline, and evaluation design |
| `51_current_snapshot_findings.md` | Reproducible current metrics audit |
| `52_seed_incident_registry.csv` | High-confidence version/campaign anchor labels with review rationale |
| `53_feature_availability_ledger.csv` | Machine-readable historical-fidelity and leakage-control ledger |
| `54_ecosystem_archive_schema_profile.json` | Raw database schema and aggregate row-count profile |
| `55_current_snapshot_ecosystem_findings.md` | Maintainer concentration, repository/workflow observability, and advisory-data limitations |
| `scripts/analyze-structural-leverage.mjs` | CSV metrics analysis reproduction |
| `scripts/profile_ecosystem_archive.py` | SQLite archive schema profiling reproduction |
| `scripts/analyze_ecosystem_structure.py` | SQLite aggregate structure/observability analysis reproduction |

## References

[1]: https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman "Zimmermann et al., Small World with High Risks"
[2]: https://arxiv.org/abs/2112.10165 "Zahan et al., What are Weak Links in the npm Supply Chain?"
[3]: https://arxiv.org/abs/2005.09535 "Ohm et al., Backstabber’s Knife Collection"
[4]: https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev "Koishybayev et al., Characterizing the Security of GitHub CI Workflows"
[5]: https://www.usenix.org/conference/usenixsecurity23/presentation/muralee "Muralee et al., ARGUS"
[6]: https://arxiv.org/abs/2606.22593 "Santos-Grueiro, On Good Authority"
[7]: https://arxiv.org/abs/2607.15315 "Rahman et al., CHRONO-RESOLUTION"
[8]: https://arxiv.org/html/2603.27549v1 "Guo et al., Understanding NPM Malicious Package Detection"
[9]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA, Axios npm Supply Chain Compromise"
[10]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA, Widespread npm Supply Chain Compromise"
[11]: https://kb.cert.org/vuls/id/534320 "CERT/CC, VU#534320"
[12]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub, Secure use reference"
