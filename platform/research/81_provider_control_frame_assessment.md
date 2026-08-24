# Provider-Backed Control-Frame Assessment

**Status:** Completed feasibility assessment; **no primary controls created.**
**Prepared by:** Manus AI
**Assessment date:** 24 August 2026

## Decision

The review found one technically promising provider-backed source—Google Open Source Insights (deps.dev) BigQuery snapshots—but no source combination that presently supports a valid control frame for the project's **future confirmed compromise** or **future malicious publication** targets. The study therefore retains the explicit no-control and no-fit decision.

> A package-version absent from an advisory or a malicious-package catalogue is **not** thereby a benign temporal control. A control frame must define the sampled at-risk population, event-coverage source, horizon, cutoff, and exclusion rule before outcomes are inspected.

## Candidate comparison

| Candidate | Frozen population capability | Label/coverage capability | Access result | Primary-control decision |
| --- | --- | --- | --- | --- |
| deps.dev BigQuery public dataset | Its `Snapshots` table identifies full exports; `PackageVersions` has `SnapshotAt` and upstream publication time. [1] | Its advisory tables expose disclosure dates and affected/unaffected version fields, but cover disclosed vulnerabilities—not the project's malicious-publication or publisher-compromise target. [1] | Official documentation requires a Google Cloud account and BigQuery API. A no-credential metadata request returned HTTP 401; no rows were retrieved. | **Exclude.** Scientifically relevant future population source, but access and target-coverage gates fail. |
| Figshare/Mendeley *Malicious NPM Package Detection Dataset* | Versioned release with a DOI and a fixed publication date. [2] [3] | Description states malicious and benign source-code folders, but its landing records do not establish row-level package-version identities, collection cutoffs, incident coverage, or temporal review horizons. [2] [3] | Metadata was readable; no artifact is used. | **Exclude.** Static malware-classification corpus, not a cutoff-valid population for future compromise. |
| Amalfi explicit-label corpus | Exact package-version identities and explicit labels are available in the project’s previously frozen provenance ledger. [4] | No per-row review/outcome horizon or at-risk sampling frame for the primary incident target. [4] | Already assessed. | **Exclude from primary benchmark.** Retrospective sensitivity only. |

## deps.dev interpretation boundary

The official schema documents package-version snapshots and a provider-defined advisory relation. It also documents resolved dependency graph tables, making the dataset a potentially useful lower-volume route for a future **provider-snapshot sensitivity** once authorized access exists. [1] That technical value does not resolve the target-definition mismatch. Vulnerability advisories and their unaffected versions do not supply closed-world coverage for malicious publications or account compromises.

The current environment does not contain credentials for the BigQuery API. A metadata-only request to the official public-dataset endpoint returned `401 UNAUTHENTICATED`; no provider data was queried, copied, sampled, or attributed to the benchmark. The probe is recorded in `81_provider_control_frame_probe.json`.

## Required conditions before a control frame can be created

| Gate | Requirement |
| --- | --- |
| Population | Select one named deps.dev snapshot (or another provider snapshot) and store its timestamp, query text, source checksum/export identity, and eligibility rule. |
| Incident coverage | Pair that population with a frozen, dated source that explicitly covers malicious-package or compromise events—not only vulnerabilities. |
| Horizon | Define the post-cutoff observation interval and show that the coverage source was capable of recording relevant events over it. |
| Exclusions | Remove any package-version with unknown exposure, unresolved identity, post-cutoff publication, or ambiguity about incident coverage; do not relabel it benign. |
| Review | Freeze the sampled frame and event-coverage specification before computing a ranking or calibration statistic. |

Until all gates pass, the current cross-sectional, direct-declaration, and bounded registry-sensitivity artifacts remain descriptive only.

## References

[1] [Open Source Insights, “deps.dev BigQuery dataset”](https://docs.deps.dev/bigquery/v1/).

[2] [Figshare, “Malicious NPM Package Detection Dataset,” DOI 10.6084/m9.figshare.31451728](https://doi.org/10.6084/m9.figshare.31451728).

[3] [Mendeley Data, “Malicious NPM Package Detection Dataset,” Version 1](https://doi.org/10.17632/6tc8wrp62g.1).

[4] [Sejfia and Schäfer, “Practical Automated Detection of Malicious npm Packages,” ICSE 2022 artifact](https://github.com/githubnext/amalfi-artifact).
