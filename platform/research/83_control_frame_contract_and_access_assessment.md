# Temporal Control-Frame Contract and Access Assessment

**Status:** Evidence-gated access assessment; **zero control observations created.**
**Prepared by:** Manus AI
**Artifact date:** 24 August 2026

## Decision question

> Can a documented package-version population snapshot be paired with an independently documented malicious-publication or compromise coverage source to produce a cutoff-valid temporal control frame?

The answer remains **no** for the sources assessed here. A package absent from an event catalogue is not benign merely because a catalogue is incomplete, target-mismatched, or observed after the candidate cutoff. The contract below is therefore a precondition to data construction, not a retrospective justification for sampling.

## Required contract

| Contract element | Required evidence | Failure consequence |
|---|---|---|
| Frozen population | A named snapshot date, immutable source reference, and explicit inclusion rule | No denominator for an at-risk frame. |
| Row identity | Package and version identifiers, with enough release timing to apply the cutoff | No valid feature or observation join. |
| Target coverage | A separately frozen source whose stated scope covers malicious publications or publisher compromises, not only vulnerabilities | Absence cannot be interpreted as a non-event. |
| Observation horizon | A documented post-cutoff interval in which coverage applies | No future-outcome definition. |
| Exclusions | Pre-registered rules for deleted records, unobservable packages, ambiguous labels, and incomplete coverage | Leakage and selection bias cannot be audited. |
| Access and reproducibility | A bounded, repeatable extraction path or a reviewed provider query with output checksum | The population cannot be reproduced or independently verified. |

## Candidate: NPM Registry Dataset 2025 (GitHub Only)

Zenodo publishes a registry snapshot mined on **20 February 2025**, containing **1,900,347** package records that were filtered by the presence of a GitHub repository URL. The associated `npm-mine` documentation says this is a subset of **3,450,250** npm entries at collection time and that each retained row is a registry-style package record. [1] [2] This gives the candidate a named snapshot date, package-level identity, and a clear—though non-ecosystem-wide—inclusion rule.

However, the only released payload is `registry.json.gz`, reported as **22.3 GB compressed** and **108 GB uncompressed**. The documentation describes streaming the full JSON array, not a row-addressable query or pre-filtered export. [1] [2] Downloading or partially processing that monolithic payload would exceed the bounded-access policy used for the temporal program; no payload bytes were retrieved or parsed for this assessment.

Most importantly, the dataset has **no documented companion outcome-coverage contract** for malicious publications or maintainer compromises after 20 February 2025. The current primary ledger is deliberately adjudicated and non-exhaustive, while positive-only catalogues and vulnerability advisories cannot turn missing entries into benign outcomes. Thus neither a candidate control sample nor a horizon-specific non-event label can be formed from this snapshot.

| Requirement | Evidence | Decision |
|---|---|---|
| Frozen population | 20 February 2025 snapshot; GitHub-URL subset | Partially satisfied; valid only for the documented subset. |
| Row identity | Registry-style package records; version maps are expected inside each record | Plausible but not independently inspected because no payload was retrieved. |
| Target coverage | No companion closed-world malicious-publication or compromise coverage source | **Failed.** |
| Observation horizon | No linked event-coverage period or closed-world follow-up definition | **Failed.** |
| Bounded reproducibility | Single 22.3 GB gzip / 108 GB expanded payload; full-stream example only | **Failed in this environment.** |
| Primary control-frame eligibility | All required elements | **Excluded.** |

## Provider route: deps.dev BigQuery

The official deps.dev documentation confirms that the BigQuery dataset retains exported snapshot timestamps, package-version fields, dependency relations, and advisory fields. It also states that use requires a Google Cloud account with the BigQuery API enabled; the sandbox can support small queries but still sits behind a Google Cloud identity. [3] The available browser session redirected to Google sign-in before any dataset operation, and the earlier unauthenticated metadata request returned HTTP 401. No BigQuery project, query, preview, or row was created.

Even with authorized access, the documented advisory relation concerns disclosed vulnerabilities. This does not meet the separate target-coverage requirement for a closed-world malicious-publication or publisher-compromise outcome source. Therefore access is a necessary but insufficient future condition.

## Candidate: Libraries.io public metadata

Libraries.io describes its public service as scraped package metadata, explicitly says that the data are not validated, and presents its npm coverage as a current package count rather than an immutable historical snapshot with a version-level outcome horizon. [4] Its public page therefore does not establish a frozen cutoff population, release-level retention contract, malicious-publication or compromise coverage, or an auditable non-event denominator. It is **excluded** as a primary temporal control source. A separate commercial offering is outside the present public-evidence scope and would still require a documented outcome-coverage contract.

## Determination and next data gate

The 2025 Zenodo snapshot is recorded as a **useful population-source lead, excluded for the present benchmark**. Its public provenance does not overcome its monolithic access path or the absent outcome-coverage/horizon contract. deps.dev remains **technically promising but access- and target-incomplete**. The benchmark remains at **zero valid controls**, and no calibration, ranking, recall, PR-AUC, or probability claim is permitted.

The next admissible step is an authorized, bounded provider export or query that selects a named snapshot and is paired *before extraction* with a separately frozen event-coverage source whose documented scope includes the target event types and horizon. Until both sides exist, the correct deliverable is another exclusion—not a sampled benign set.

## References

[1] [Zenodo, “NPM Registry Dataset 2025 (GitHub Only),” Version 1.0.0](https://zenodo.org/records/14914149).

[2] [Brittany Reid, “npm-mine” repository and dataset documentation](https://github.com/Brittany-Reid/npm-mine).

[3] [Open Source Insights, “deps.dev BigQuery dataset”](https://docs.deps.dev/bigquery/v1/).

[4] [Libraries.io, “Data and service description”](https://libraries.io/data).
