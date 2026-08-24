# Exact Direct-Metadata Temporal Pilot Protocol

## Purpose and scope

This protocol implements the smallest defensible next experiment from the gap-resolution study. Its purpose is to validate provenance, cutoff enforcement, label adjudication, and diagnostic reporting for **package-version observations**. It is not an evaluation of compromise-prediction accuracy and does not claim that structural reach, current repository state, or graph attention predicts future compromise.

The pilot uses a frozen cutoff of **2026-03-31T00:00:00Z**, a 30-day outcome horizon, and the official npm registry’s version-level metadata. The cutoff matches the high-confidence event-start date in CISA’s Axios alert. [1]

> **Pre-registration.** No feature, positive label, or evaluation rule may be added after inspecting its association with the pilot’s outcomes. The output labels unobserved package-version rows as `no_known_event_in_registry`, not benign.

## Frozen inputs

| Input | Immutable source | Rule |
|---|---|---|
| Candidate packages | `axios`, `plain-crypto-js` | Chosen from the pre-existing seed registry, not registry search results |
| Positive-label anchors | `research/52_seed_incident_registry.csv` | Only rows with `confidence=high` and `primary_target_eligible=yes` can be primary positives |
| Registry metadata | `GET https://registry.npmjs.org/:package` | Store response SHA-256 and retrieval time; consume only per-version objects and `time[version]` [2] |
| Cutoff | `2026-03-31T00:00:00Z` | A version is eligible only when its registry publication timestamp is at or before the cutoff |
| Horizon | 30 days | A positive must have event-start time in `(cutoff, cutoff + 30 days]`; this pilot will instead report a temporal consistency failure when the event time equals the cutoff |

## Reconstruction rules

Each package response produces one row per version. The pilot retains the raw package name, version string, timestamp, dependency map, optional-dependency map, peer-dependency map, install-script indicator, and integrity/hash fields where present. Version rows have `historical_fidelity=registry_reconstructed_exact` only when the registry reports a timestamp and the object itself is retained; all other fields receive their own availability state.

The protocol deliberately excludes current `latest` tags, top-level maintainers, repository fields, current download counts, and workflow evidence from temporal model features. npm’s documentation explains that top-level fields are hoisted from the most recently published version, so they are not safe as of a past cutoff. [2]

Direct dependency declarations are not transitive dependency resolution. The pilot records the declared semver range only. It assigns `transitive_resolution=not_available` rather than resolving ranges against a current registry state. CHRONO-RESOLUTION is the future candidate for that extension because it targets resolution at release points. [3]

## Independent label adjudication

Two record-level questions are separated:

| Question | Allowed answer | Evidence requirement |
|---|---|---|
| Is the version tied to a documented event? | `confirmed`, `campaign_associated`, `ambiguous`, or `excluded` | Government alert, maintainer post-mortem, or independently corroborated technical record |
| Is it a primary temporal positive? | `yes` or `no` | Exact package and version, high confidence, event date strictly after the feature cutoff, and a target definition matching the event |

The Axios package releases are `confirmed_targeted_compromise` evidence. `plain-crypto-js@4.2.1` remains a separate `confirmed_malicious_publication` / injected-dependency record; it must not be merged into the maintainer-compromise target. CISA names the exact Axios and injected dependency versions but the event date equals the proposed cutoff. [1] The first execution therefore records a **boundary-case outcome**, not a valid future-prediction positive. This is an expected negative result about protocol feasibility, not an error to repair by moving the cutoff after observing data.

The Shai-Hulud campaign remains excluded from package-version primary labels until an authoritative, dated affected-version list is independently adjudicated. CISA establishes campaign-level compromise and timing only. [4]

## Analysis plan

The execution will compute descriptive diagnostics only:

1. Number of versions eligible before the cutoff by package.
2. Number of version rows with direct dependency declarations and install-script indicators.
3. Number of exact labels matched, boundary failures, and non-primary records.
4. Registry-response checksums, retrieval timestamps, and missingness counts.
5. Whether more than one independent incident family and at least ten temporally valid positive observations are available.

No PR-AUC, calibration curve, p-value, accuracy, or learned model will be reported unless the last condition holds and an independently specified unlabeled-control design is added. If it fails, the study will report a feasibility result and a preregistered path to the next data acquisition stage.

## Preservation and safety

Only metadata rows, hashes, and aggregate counts are saved in `research/`; no malicious payloads, credentials, or package tarballs are downloaded or executed. The collection script streams HTTP responses, limits requests to the named seed packages, and writes immutable response checksums.

## References

[1]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA: Supply Chain Compromise Impacts Axios Node Package Manager"
[2]: https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md "npm Registry package metadata documentation"
[3]: https://arxiv.org/abs/2607.15315 "Rahman et al., CHRONO-RESOLUTION"
[4]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA: Widespread Supply Chain Compromise Impacting npm Ecosystem"
