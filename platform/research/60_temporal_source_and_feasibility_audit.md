# Historical Source and Temporal-Pilot Feasibility Audit

## Decision summary

The next study stage can execute a **small, exact direct-metadata temporal pilot** using the official npm registry and the project’s high-confidence Axios anchor labels. It cannot yet support a general claim about historical transitive reach, calibrated compromise probability, or a graph-learning comparison. The current private archive is a single cross-sectional ecosystem snapshot, not a dated series; the registry supports package-version publication times and version-scoped dependency declarations, but its current top-level package fields must not be projected backward without an explicit fidelity warning. [1]

> **Research decision.** The first temporal artifact will reconstruct only version records published at or before a frozen cutoff and will label direct dependency declarations as `registry-reconstructed`. It will treat transitive resolution, dated downloads, historical workflow state, and current maintainer fields as unavailable unless a dated source supplies them.

## Source inventory and admissibility

| Source | What it supplies | Temporal admissibility | Role in the pilot | Limitation |
|---|---|---|---|---|
| Existing private SQLite archive and metrics CSV | Current package, maintainer, repository, workflow, and structural summaries | **Cross-sectional only** | Scope-A descriptive reference | No dated snapshots or historical labels |
| npm registry package metadata endpoint | Package-version metadata, dependency declarations, and a `time` map of version publication timestamps | **Exact for version rows that remain in the endpoint** | Primary direct-metadata reconstruction input | Current top-level metadata and missing/deleted versions are not historical truth [1] |
| CISA Axios alert | Event date and exact affected Axios and injected dependency versions | **High-confidence label anchor** | Primary positive-label seed | Too few labels for population-level prediction [2] |
| CISA Shai-Hulud alert | Confirmed campaign date and ecosystem scope | **Campaign-level only** | Candidate-discovery and exclusion evidence | No package-version list in the alert; not a primary package-version label [3] |
| Datadog malicious package dataset | Human-triaged package samples and npm manifest entries, sometimes with versions | **Candidate source only** | Future label discovery | File dates are discovery dates, not publication dates; selection is rule-set biased [4] |
| npm-follower | Continuously archived package metadata and code, including later-deleted versions | **Potential high-fidelity external archive** | Future expansion source | Access and coverage must be frozen, versioned, and documented before use [5] |
| CHRONO-RESOLUTION | Release-point dependency-resolution dataset and construction methodology | **Schema validated; relation payload not locally acquirable** | Future version-resolved and transitive-resolution extension | The only relation-data ZIP member is 10.23 GB compressed and 138.73 GB uncompressed; it cannot be selectively queried from the published archive [6] [8] |
| Zenodo NPM Registry Dataset 2025 | A 2025 GitHub-repository subset of registry data | **One dated snapshot** | Optional sensitivity source | 22.3 GB compressed; not a practical default artifact for this platform [7] |

## Label readiness

The existing seed registry contains two exact affected Axios version labels, `axios@1.14.1` and `axios@0.30.4`, plus `plain-crypto-js@4.2.1`, with an event date of 31 March 2026. CISA’s alert names those versions and states that the affected Axios releases injected the malicious dependency; it is therefore strong evidence for a targeted-compromise target for Axios and a distinct malicious-publication/dependency-injection target for `plain-crypto-js`. [2] The Shai-Hulud row remains `campaign_only` because CISA confirms scale and timing but does not enumerate affected package versions. [3]

The Datadog repository is valuable candidate-discovery evidence because its samples are human triaged and its npm manifest can carry version information. However, its README explicitly describes the date encoded in sample filenames as a **discovery** date rather than a package-publication date. It cannot establish feature availability or event onset alone. [4]

## Feasibility gate

| Capability | Pilot status | Required rule |
|---|---|---|
| Version publication cutoff | Ready | Keep only versions whose npm `time[version]` is at or before cutoff |
| Direct dependency declarations | Ready | Read only the retained version objects; preserve raw semver range and source checksum |
| Affected-version labels | Ready, sparse | Restrict primary positives to CISA-supported Axios versions; retain `plain-crypto-js` as a separate target class |
| Negative observations | Ready only as **unlabeled controls** | Do not call them benign; report them as no-known-event observations |
| Isolated direct-range approximation | Ready with strict approximation label | Select the highest SemVer target satisfying each declared range among registry versions timestamped by the cutoff; never call this an observed install |
| Transitive dependency resolution | Not ready | Do not infer from current graph; the validated CHRONO-RESOLUTION schema has `dependency_version` and intervals, but its published relation payload is not selectively queryable [6] [8] |
| Historical workflow/CI exposure | Not ready | Do not use current GitHub workflow presence as a temporal feature |
| Calibration or learned ranking | Not ready for inference | Compute only feasibility diagnostics until multiple incident families and adequate positive count exist |

## Immediate pilot specification

The reproducible pilot will use the 31 March 2026 cutoff, registry responses for `axios` and `plain-crypto-js`, the CISA labels above, and a fixed 30-day lookback window. It will emit a package-version ledger containing exact publication time, pre-cutoff eligibility, dependency declarations, primary-label class, source retrieval time, and SHA-256 checksum. It will separately report why the sample cannot support calibrated probability estimates: there are too few independent incident families and no defensible labeled-negative population.

## CHRONO-RESOLUTION selective archive validation

On 24 August 2026, the project used an HTTP byte-range request against the official Zenodo archive to obtain the 65,557-byte ZIP64 tail and inspect its central directory without downloading the 10.2 GB release. The archive contains four members. `data-relations.sql` is the only relations-data member: **10,228,591,413 bytes compressed** and **138,731,381,476 bytes uncompressed**. The release is therefore a monolithic SQL dump rather than a partitioned, package-selectable artifact.

The project then retrieved only a 1,508-byte range containing the compressed `schema-relations.sql` member and extracted its 2,888-byte schema. The verified `relations_minified` definition contains `ecosystem`, `package`, `package_version`, `dependency`, `dependency_constraint`, `dependency_version`, `dependency_highest_version`, `interval_start`, and `interval_end`. This validates that the source could support interval-aware version-resolved direct-edge work if an approved bulk-compute environment or an upstream filtered export becomes available. It does not validate or ingest any relations rows, and it does not make transitive reach computable in this project.

The selective archive inventory is committed as `72_chrono_resolution_archive_inventory.json`; the extracted source schema is `72_chrono_resolution_schema_relations.sql`. Both artifacts record source provenance and avoid a full data download.

### Bounded full-stream acquisition attempt

The project also made one memory-bounded, single-pass attempt to stream the complete `data-relations.sql` raw-deflate member through a scanner that retained only the seven pre-registered package-version candidates. The HTTP transfer was capped at 1,500 seconds. It received **783,198,932 of 10,228,591,413 compressed bytes (7.6569%)** before the network timeout; the raw-deflate stream necessarily ended incomplete, and the scanner retained **zero** candidate rows. The incomplete output and stale diagnostics were removed rather than being presented as evidence. The committed `73_chrono_resolution_streaming_attempt.json` records this operational limit.

This bounded failure establishes a practical acquisition boundary, not a scientific negative finding about the source data. The remaining valid options are a sanctioned bulk-compute environment, an upstream package-filtered export, or a provider-side query. Until one is available, the project cannot construct a version-resolved transitive graph from this archive.

## npm-follower control-population feasibility

The npm-follower publication confirms that the project archives package metadata and code as packages and versions are published, retains later-deleted versions, and reported more than 35 million package versions in 2023. [5] Its public project page describes the replica as **20+ TB**. [9] This establishes npm-follower as a scientifically relevant source for a future at-risk population and deleted-version recovery, but not as a dataset that can be acquired or sampled defensibly from the present bounded environment without an official query interface, a versioned filtered export, or a bulk-compute allocation.

As a result, the project does not create “no-known-event” package rows from the current registry and label them benign. A cutoff-valid control population remains unassembled rather than fabricated. The next admissible control-design step is to obtain a frozen incident-coverage source and a matching, explicitly sampled at-risk package frame from an authoritative provider; only then may non-event observations be defined relative to documented coverage and horizon.

## Registry-only recursive graph admissibility

Official npm documentation distinguishes a package lockfile—an exact representation of the dependency tree that an npm operation generated—from a manifest range. [10] The SemVer reference defines a range as a set of satisfying versions and exposes `maxSatisfying` as a function over a supplied version list. [11] These semantics permit a bounded, reproducible **registry-only approximation** for the pre-registered roots: recursively select the highest retained non-prerelease version satisfying each runtime `dependencies` range among versions timestamped by the root cutoff.

This strategy is admissible only as a labeled sensitivity artifact. It cannot reproduce a historical `package-lock.json`, npm installation, hoisting arrangement, or resolved peer/optional/bundled/workspace/override behavior. The associated graph builder therefore excludes those relations, caps depth and node count, and prohibits use for global reach, centrality, blast-radius, ranking, calibration, or attack-return claims. Its valid descriptive outputs are bounded edge and node counts only.

## Version-labelled release-corpus sensitivity source

The public ICSE 2022 Amalfi artifact contains a compact `basic-corpus.csv` whose rows explicitly identify an npm package, exact version, content hash, and manually assigned `malicious` or `benign` analysis label. Its separate daily experiment CSVs are described as all new public npm versions for the day, with unreviewed samples marked `not triaged`. [12] This is materially stronger than a registry row with no known event: it supplies an explicit version-level negative label.

The corpus is nevertheless **not** a primary control population for the project's pre-registered future-compromise target. The basic corpus is a classifier training corpus, is concentrated around known malicious-package families, and its README does not provide per-row discovery, review, or outcome-horizon timestamps. It can support only a clearly named **retrospective release-classification sensitivity** after release timestamps and corpus version hashes are frozen. It cannot support the main incident-family ranking, calibration, or blast-radius claims, and it must not be merged with the independently adjudicated compromise ledger.

## Human-vetted positive-only catalogue

The DataDog Malicious Software Packages Dataset publishes an npm `manifest.json` whose values are either an explicit list of known malicious versions or `null` when the catalogue does not specify a version. Its repository documents the sample filename date as a **discovery date**, not necessarily a package publication date. [13] The manifest itself has no per-record discovery date, evidence URL, campaign-family identifier, or negative/control rows.

This makes the manifest useful only as a frozen, human-vetted **positive-membership corroboration** for existing or separately sourced package-version records. It cannot establish an event time for a new primary incident label, cannot distinguish a `null` value from a safe package version, and cannot create a control population. Any overlap is retained as candidate-level corroboration and never used to overwrite primary incident evidence or temporal cutoffs.

## Dated OSV-report validation: node-ipc

The OpenSSF Malicious Packages OSV report `MAL-2026-3744` supplies a published timestamp of 14 May 2026, exact npm versions `9.1.6`, `9.2.3`, and `12.0.1`, source provenance records, package-integrity evidence, and an alias to `GHSA-pvh2-rg5g-69v7`. [14] Its independent SafeDep report, published on the same date, names the same three versions and reports their official registry publication timestamps, including `12.0.1` at `2026-05-14T14:25:30.311Z`. [15]

This pair satisfies the pre-registered adjudication threshold for one new, independent maintainer-compromise family. The ledger uses the earliest reported malicious publication timestamp as the cutoff, reconstructs `node-ipc@12.0.0` immediately before that cutoff from official registry metadata, and retains the report publication time only as evidence provenance—not a feature.

## Dated OSV-report validation: `@emcd-vue/auth`

SafeDep documents the `oob.moika.tech` dependency-confusion campaign, including the `@emcd-vue` June 2026 wave and exact `@emcd-vue/auth` versions `6.4.8` and `6.4.9`. [16] OpenSSF report `MAL-2026-5163` independently identifies the package as malicious, records versions `6.4.5`, `7.0.0`, `6.4.8`, and `6.4.9`, exposes package-integrity evidence, and aliases `GHSA-gj65-7753-2q9f`. [17] The official registry time map confirms `6.4.8` at `2026-06-01T07:04:12.358Z`; this is the earliest documented malicious version and is used as the strict event anchor.

The retained current registry response does not contain a usable pre-anchor version object for this package. The record is therefore admitted as a high-confidence **label-only event** but contributes no source-package metadata, direct declaration, range approximation, or bounded graph root. This is an intentional fidelity result: the expanded ledger reaches ten package-event records and six incident families, while exact reconstruction remains eight source snapshots and the primary baseline remains blocked for lack of cutoff-valid controls.

## References

[1]: https://github.com/npm/registry/blob/main/docs/responses/package-metadata.md "npm Registry package metadata documentation"
[2]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA: Supply Chain Compromise Impacts Axios Node Package Manager"
[3]: https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem "CISA: Widespread Supply Chain Compromise Impacting npm Ecosystem"
[4]: https://github.com/datadog/malicious-software-packages-dataset "Datadog Malicious Software Packages Dataset"
[5]: https://arxiv.org/abs/2308.12545 "Pinckney et al., npm-follower"
[6]: https://arxiv.org/abs/2607.15315 "Rahman et al., CHRONO-RESOLUTION"
[7]: https://zenodo.org/records/14914149 "NPM Registry Dataset 2025 (GitHub Only)"
[8]: https://doi.org/10.5281/zenodo.17576373 "CHRONO-RESOLUTION Zenodo data release"
[9]: https://donaldpinckney.com/publication/npm-follower/ "npm-follower project page"
[10]: https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/ "npm package-lock documentation"
[11]: https://docs.npmjs.com/cli/v6/using-npm/semver/ "npm SemVer documentation"
[12]: https://github.com/githubnext/amalfi-artifact "Amalfi ICSE 2022 artifact repository"
[13]: https://github.com/DataDog/malicious-software-packages-dataset "DataDog Malicious Software Packages Dataset"
[14]: https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/node-ipc/MAL-2026-3744.json "OpenSSF MAL-2026-3744 node-ipc report"
[15]: https://safedep.io/malicious-node-ipc-npm-compromise/ "SafeDep node-ipc compromise report"
[16]: https://safedep.io/oob-moika-tech-dependency-confusion-campaign/ "SafeDep oob.moika.tech dependency-confusion campaign"
[17]: https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/%40emcd-vue/auth/MAL-2026-5163.json "OpenSSF MAL-2026-5163 @emcd-vue/auth report"
