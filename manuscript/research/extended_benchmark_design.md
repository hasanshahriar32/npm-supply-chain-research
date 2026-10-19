# Completed structural study and prospective benchmark design

Updated **20 October 2026, Asia/Dhaka**. This author-side document separates executed experiments and collection from future outcome evaluation. It replaces the earlier generic protocol. No neural-model or compromise-forecast performance is implied.

## Completed structural experiments

`scripts/study_structural_interventions.py` compares portfolio size, summed package reach, exact portfolio-union reach, greedy marginal coverage and 200 seeded random baselines at budgets 1, 5, 10, 25, 50 and 100. It evaluates package/repository endpoints, observation depth, version continuity, repository-link consistency, dominant portfolios and hypothetical email-hash grouping. Results and source manifests are in `manuscript/results/structural_interventions/`.

Let `E_m` be the endpoints structurally reachable from an observed source identity `m`. Three estimands have different interpretations:

1. **Uniform scenario exposure share:** `H(S) = sum(m in S)|E_m| / sum(m)|E_m|`. This assumes mutually exclusive, equally weighted identity-loss scenarios and ideal prevention of selected source scenarios. It is not an estimated attack distribution.
2. **Distinct endpoint coverage:** `C(S) = |union(m in S) E_m|`. This is a review-coverage measure. Unselected identities can still reach a covered endpoint.
3. **All-source full protection:** define `A_e = {m : e in E_m}`; then `P(S) = |{e : A_e is nonempty and A_e is a subset of S}|`. This stronger graph-model condition remains conditional on observed completeness and idealized control.

These are established optimization objectives and baselines. The empirical contribution is their behavior under overlapping portfolios and measurement assumptions. None measures deployed security improvement or causal attack prevention.

`scripts/study_graph_validity.py` independently evaluates all 25,228 package roots. Version continuity changes reverse-reached name counts for 8,587 roots. The 15,233 workflow-positive package names map to 7,171 repository keys before mapping exclusions. The original URL parser has 658 mismatched targets, including 60 positive flags. Results are in `manuscript/results/graph_validity/`.

## Prospective cohort: collection completed, outcomes pending

The first acquisition-feasibility wave has actually been collected:

| Item | Frozen value or actual result |
|---|---|
| Sampling frame | All 25,228 package names in our immutable original archive |
| Selection | Uniform sample without replacement; seed 20261020; manifest written before requests |
| Selected names | 100 |
| Capture endpoint | Official npm `/latest`; sequential requests separated by at least 0.2 seconds |
| Successful responses | 90 HTTP 200 |
| Missing metadata | Eight HTTP 405 and two HTTP 404; no replacement |
| Feature cutoff | 20 October 2026, 00:48:38.569362 Asia/Dhaka |
| Follow-up | `(cutoff, cutoff + 90 days]` |
| Horizon end | 18 January 2027, 00:48:38.569362 Asia/Dhaka |
| Outcomes | All 100 pending; zero positive or negative labels |
| Models/performance | Zero fitted models; zero forecasting metrics |

The collector is `scripts/freeze_prospective_cohort.py`. In `manuscript/results/prospective_cohort/`, `selection_manifest.json` fixes sampling and target description before acquisition; `capture_records.jsonl` records times, HTTP statuses, successful-response hashes and allowlisted features; `cohort_status.json` fixes the final capture as the common availability cutoff. Existing manifests cannot be overwritten by a repeat run.

Maintainer usernames and the recorded version publisher have separate fields. Attestation-metadata presence is not cryptographic provenance verification. No email addresses, raw response bodies, install-script bodies or tarballs are retained. Joining the old graph later would supply **stale structural features available at the new cutoff**, not contemporaneous measurements or a reconstruction of old acquisition dates.

This 100-name wave demonstrates collection feasibility. It is not a powered or fully preregistered forecasting benchmark. The horizon may yield no eligible events; such an outcome cannot justify changing the target after follow-up.

## Fix the future target and ascertainment process

The intended target is **a publicly documented unauthorized publication or release-pipeline compromise affecting an established sampled package during follow-up**. Record affected versions, event and first-report times, incident role, evidence URLs, withdrawal/revision state, campaign linkage, adjudication and timing uncertainty. Ordinary accidental vulnerabilities, newly created malicious packages, unrelated typosquats, downstream exposure and deliberate maintainer protestware are separate classes.

Before reviewing future outcomes, freeze surveillance sources and versions, query/collection procedure, reporting-delay allowance, inclusion criteria, censoring rules and analysis plan. Successful source probes establish access to OSV package queries and OpenSSF records. Those sources mix attack classes and incomplete reporting; they are not a complete compromise census. No unattended surveillance or scheduled task has been activated.

Use three distinct observation states:

- **Documented target event:** evidence meets the registered role, timing and inclusion criteria.
- **No documented target event under specified ascertainment:** complete registered follow-up found no qualifying report. This is an outcome of a reporting process, not certified benignness.
- **Unknown/censored:** follow-up was incomplete, coverage failed, timing was unresolved or evidence did not support target classification.

Documented-event-versus-unlabeled and positive/unlabeled designs are legitimate when their assumptions are explicit. An impossible proof that every comparison package is benign is unnecessary. Silently turning unavailable or unreported cases into known uncompromised packages would still overstate the evidence. Metric denominators and sensitivity analyses must match the registered estimand.

Sampling comparisons after cases are known requires inclusion probabilities and a restricted inference target. A balanced case/control sample does not reveal population prevalence. Calibration requires representative ascertainment or valid corrections; otherwise claims must concern the sampled reporting process rather than true underlying compromise risk.

## Feature evidence and graph fidelity

| Observation | Supported interpretation |
|---|---|
| Name-projected edge union | Structural reach in merged package-name adjacency |
| Exact version-node union | Version-continuous paths in merged resolved adjacencies |
| Retained source manifest | Declarations associated with one identified version |
| Publication-time map | Retained reported publication times; incomplete deleted-version coverage |
| Cutoff SemVer selection | A bounded range-based approximation |
| Historical lockfile/resolver context | Project-specific resolution under documented settings |
| Dated workflow YAML | Visible configuration at the recorded revision |
| Public maintainer array | Account/package metadata membership at capture |
| Version publisher field | The recorded version actor, with registry-specific semantics |
| Verified authority/provenance | A particular verified release/build relationship; no harmlessness guarantee |

The version graph still merges resolution contexts and does not reconstruct an installation. The original collector omits query roots, response errors and acquisition times. Its DIRECT/INDIRECT field is target-node relation to the extraction root, so filtering it does not recover global direct edges. Future graph collection should retain root/context identifiers, timestamps, response hashes and resolver/error state.

The original workflow zeros conflate unavailable repositories and absent directories. Flags queried for truncated URLs cannot be transferred to corrected targets. New `scripts/research_observations.py` and `scripts/collect_data_v2.py` support corrected lexical parsing and conservative future workflow states. They do not repair the archive retroactively; no new live workflow observations have been collected.

Richer workflow features need commit-bound YAML, observable permissions, trigger/checkout combinations, action references and field-level missingness. Historical authority comparisons also need version-specific predecessor evidence and a validated release/build link.

## Forecast experiments that remain unexecuted

Start with frozen random, dependency-reach, maintainer-portfolio, release-activity and available-metadata baselines. Popularity needs a dated measurement window. With enough independent events, compare regularized logistic regression and a transparent tree-based model at matching cutoffs and feature availability. Graph learning is a later candidate; graph heterogeneity does not demonstrate that attention will help.

No universal incident-count floor substitutes for a power or precision assessment. Independent event/campaign counts, effect sizes, observation design and uncertainty determine what is estimable. Zero or very few events can support observability findings without a meaningful model comparison.

For repeated waves, use chronological training, validation and untouched test periods. Keep related campaign records together and test package-disjoint evaluation where possible. Handle overlapping horizons so the same event does not enter multiple partitions. Scaling, imputation, coefficients, thresholds and calibration use training/validation observations only.

Report budgeted ranking performance against the **registered documented-event outcome**, its observed base rate, censoring and ascertainment limitations. Random-queue simulation variability is distinct from uncertainty about future incidents. Use independent campaign/time units when estimating uncertainty rather than treating one campaign's packages as independent attacks. Calibrated true-compromise probabilities require an identification argument about reporting and prevalence.

A future evaluation manifest must bind sources, feature availability, observation units, outcome protocol, reporting/censoring, campaign groups, splits, ranking settings and code. Retain all eligible predictions and exclusions, including null or negative results.

## Current status

The structural decision experiments and graph-validity measurements are complete. The new prospective wave has 100 selected names, 90 successful current metadata captures and 100 pending outcomes. Historical incident artifacts remain candidate-discovery and development resources; they do not constitute evaluated publisher-compromise prediction.

Deployed hardening effects, historical credential/workflow authority and future forecasting performance remain unobserved. See [2026-10-20_research_status.json](2026-10-20_research_status.json) and [2026-10-20_groundwork_assessment.md](2026-10-20_groundwork_assessment.md).
