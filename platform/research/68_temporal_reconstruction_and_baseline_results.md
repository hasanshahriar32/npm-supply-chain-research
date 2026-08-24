# Temporal Reconstruction and Baseline-Eligibility Results

**Status:** Completed feasibility and reconstruction stage; **no predictive model has been fitted.**  
**Scope:** Pre-registered package-event records, official npm registry metadata, and independently adjudicated incident evidence.  
**Prepared by:** Manus AI  
**Artifact date:** 24 August 2026

## Executive finding

This extension successfully reconstructs **ten exact pre-event package-version metadata snapshots** from twelve pre-registered npm package-event records spanning **eight incident families**. It produces a reproducible ledger of **28 cutoff-valid direct dependency declarations** and, for every declared range, one **isolated cutoff-valid SemVer target approximation**. A separate, depth-three registry-only sensitivity artifact expands those approximations to **63 bounded edges** across eight roots with runtime dependencies. Neither artifact is a lockfile or a package-manager execution trace. No transitive reach is computed, and therefore no historical blast-radius or attack-return quantity is estimated.

The evidence permits a negative but important methodological conclusion. The present data cannot support ranking, logistic-regression, PR-AUC, Recall@K, probability-calibration, or uncertainty estimates. The twelve-record and eight-family floors are now met, but the pilot has no cutoff-valid adjudicated non-event population and only ten exact source snapshots because two high-confidence label-only events lack usable pre-event registry objects. The correct result is a transparent **no-fit decision**, not a weakly powered model claim.

> **Historical-fidelity definition.** `registry_reconstructed_exact_direct_declaration` means that the source package version was selected strictly before the event cutoff from the official npm registry's version-time map and that version object's declared `dependencies` map was retained verbatim. It does **not** mean that a declared range was resolved to a target version, installed by npm, or expanded transitively.

## Evidence and reconstruction design

The package-event ledger contains independently sourced, high-confidence incidents: the 2021 `ua-parser-js` / `coa` / `rc` compromise family, the 2018 `event-stream` incident, the 2018 ESLint incident, and the 2026 Axios-, `node-ipc`-, `oob.moika.tech`-, and Mini Shai-Hulud-`atool`-related families. Primary or authoritative incident sources identify the affected releases and event anchors, while the registry provides the temporal version objects. CISA's public alerts identify the `ua-parser-js` and Axios-related affected versions; Mandiant documents the 2021 Node.js compromise campaign; npm's incident post documents the `event-stream` response; ESLint's postmortem records its publication timeline; and independently published SafeDep and OpenSSF records corroborate the `node-ipc`, `@emcd-vue/auth`, and `amapcn` release sets and event timing. [1] [2] [3] [4] [5] [6] [7] [8] [9] [22] [23]

For each record, the builder sets the feature cutoff to one millisecond before the recorded event start, selects the latest registry version timestamp at or before that cutoff, and reads only that selected version object's runtime `dependencies`. A SHA-256 digest of the raw registry response is stored with each reconstructed source record. This arrangement prevents the event release itself or later metadata from becoming a feature.

| Reconstruction component | Result | Fidelity and interpretation |
|---|---:|---|
| Pre-registered package-event records | 12 | Package-level observations; not twelve independent attacks. |
| Incident families | 8 | `unc3379_2021`, `event_stream_2018`, `eslint_2018`, `axios_2026`, `node_ipc_2026`, `moika_dependency_confusion_2026`, `shai_hulud_second_coming_2025`, and `mini_shai_hulud_atool_2026`. |
| Exact source snapshots | 10 | Source package version object selected strictly before its cutoff. |
| Source snapshot unavailable | 2 | `plain-crypto-js` and `@emcd-vue/auth`; no qualifying pre-event version object was retained by the current registry response. |
| Declared direct edges | 28 | Exact source declarations, each retaining the original SemVer range. |
| Isolated target-range approximations | 28 | Highest valid SemVer version within the declared range and published by the cutoff; not an observed installation result. |
| Transitive-reach values | 0 | Intentionally not computed. |

The reproducible inputs and outputs are `64_temporal_package_event_ledger.csv`, `65_package_temporal_companion_snapshots.csv`, `65_package_temporal_companion_declared_edges.csv`, `66_temporal_baseline_and_calibration_gate.json`, `67_cutoff_direct_dependency_graph_edges.csv`, `67_cutoff_direct_dependency_graph_manifest.json`, `70_cutoff_direct_dependency_range_resolution.csv`, `71_direct_range_resolution_diagnostic.json`, `74_bounded_recursive_registry_semver_graph_edges.csv`, and `75_bounded_recursive_registry_graph_diagnostic.json`. The relevant build scripts are `build-package-temporal-companion.mjs`, `build-cutoff-direct-dependency-graphs.mjs`, `build-cutoff-direct-dependency-range-resolution.mjs`, `analyze-direct-range-resolution-diagnostic.mjs`, `build-bounded-recursive-registry-graph.mjs`, and `analyze-bounded-recursive-registry-graph.mjs`.

## Direct-dependency reconstruction result

The graph artifact begins as a **declared-edge ledger**, not an implied package-manager installation tree. Every edge records the source package-version node, dependency package name, declared range, cutoff, response checksum, and three fidelity fields: source snapshot fidelity, target-version fidelity, and transitive-reach fidelity. A second ledger (`70_cutoff_direct_dependency_range_resolution.csv`) uses the maintained `semver` implementation to select the highest non-prerelease target version satisfying each direct declaration among versions whose registry timestamps are at or before the cutoff. All 28 ranges resolved under that deliberately narrow procedure. [12]

The resolved-target label is **`registry_reconstructed_cutoff_semver_approximation`**, not exact resolution. It does not reconstruct npm's historical installation state because peer, optional, bundled, workspace, override, nested, package-manager-version, cache, and lockfile behavior are not part of the calculation. The artifacts remain unsuitable for transitive graph traversal, centrality, dependency reach, blast radius, or attack-return estimates.

| Pre-event source record | Selected source version | Declared direct edges | Source fidelity | Boundary |
|---|---:|---:|---|---|
| `ua-parser-js-2021-10-22` | 0.7.28 | 0 | Exact direct declaration | No runtime dependency declarations in the selected version. |
| `coa-2021-11-04` | 2.0.2 | 3 | Exact source declaration + 3 isolated target approximations | No install trace or transitive traversal. |
| `rc-2021-11-04` | 1.2.8 | 4 | Exact source declaration + 4 isolated target approximations | No install trace or transitive traversal. |
| `axios-2026-03-31` | 1.14.0 | 3 | Exact source declaration + 3 isolated target approximations | No install trace or transitive traversal. |
| `plain-crypto-js-2026-03-31` | — | 0 | Not available | No cutoff-valid source object retained. |
| `event-stream-2018-11-26` | 4.0.1 | 7 | Exact source declaration + 7 isolated target approximations | No install trace or transitive traversal. |
| `eslint-scope-2018-07-12` | 4.0.0 | 2 | Exact source declaration + 2 isolated target approximations | No install trace or transitive traversal. |
| `eslint-config-eslint-2018-07-12` | 5.0.1 | 1 | Exact source declaration + 1 isolated target approximation | No install trace or transitive traversal. |
| `node-ipc-2026-05-14` | 12.0.0 | 4 | Exact source declaration + 4 isolated target approximations | No install trace or transitive traversal. |
| `wenk-2025-11-24` | 1.0.8 | 0 | Exact direct declaration | No runtime dependency declarations in the selected version. |
| `amapcn-2026-05-19` | 0.1.2 | 4 | Exact source declaration + 4 isolated target approximations | No install trace or transitive traversal. |

The selected ten exact source snapshots have a mean of **2.8** declared runtime dependencies, a median of **3**, a minimum of **0**, and a maximum of **7**. These are descriptive properties of the reconstructed pilot records only. They do not measure dependency reach, downstream consumers, package importance, or attack impact.

## Bounded recursive registry-graph sensitivity

Official npm documentation defines `package-lock.json` as the exact dependency tree generated by an npm operation, while the SemVer reference defines a range as a set of satisfying versions and documents highest-satisfying selection over a supplied version list. [11] [12] The study therefore uses the current registry only for a **bounded sensitivity graph**: it recursively selects the highest retained, non-prerelease package version satisfying each runtime `dependencies` range and published by the root's frozen cutoff. It excludes `devDependencies`, peers, optional and bundled relations, workspaces, overrides, links, git and tarball specifications, as well as all package-manager installation behavior.

The resulting artifact contains **63 edges** and **65 bounded nodes across the eight root graphs with runtime dependencies**. The ten-root exact-snapshot design also retains `ua-parser-js@0.7.28` and `wenk@1.0.8`, each with no runtime dependencies, while `plain-crypto-js` and `@emcd-vue/auth` remain unavailable as exact source snapshots. The 63 edges distribute as 28 at depth one, 18 at depth two, and 17 at depth three; every selected target range resolved under the stated cutoff-valid SemVer method.

| Pre-event source root | Bounded edges | Bounded nodes including root | Depth 1 / 2 / 3 edges | Interpretation boundary |
|---|---:|---:|---|---|
| `coa@2.0.2` | 8 | 9 | 3 / 3 / 2 | Range-selected registry sensitivity only. |
| `rc@1.2.8` | 4 | 5 | 4 / 0 / 0 | Range-selected registry sensitivity only. |
| `axios@1.14.0` | 15 | 15 | 3 / 5 / 7 | Range-selected registry sensitivity only. |
| `event-stream@4.0.1` | 11 | 8 | 7 / 4 / 0 | Range-selected registry sensitivity only; duplicate/cyclic selections can reduce unique-node count. |
| `eslint-scope@4.0.0` | 3 | 3 | 2 / 1 / 0 | Range-selected registry sensitivity only. |
| `eslint-config-eslint@5.0.1` | 4 | 5 | 1 / 2 / 1 | Range-selected registry sensitivity only. |
| `node-ipc@12.0.0` | 14 | 15 | 4 / 3 / 7 | Range-selected registry sensitivity only. |
| `amapcn@0.1.2` | 4 | 5 | 4 / 0 / 0 | Range-selected registry sensitivity only. |

> **Interpretation limit.** These counts are neither historical installed-tree sizes nor transitive dependency reach. The graph is not a package-lock reconstruction and must not be compared across roots as a security score, centrality measure, blast-radius quantity, or input to any ranking, calibration, PR-AUC, Recall@K, or attack-return calculation.

## Temporal baseline and calibration gate

The gate computed descriptive feature summaries rather than a model. Across the ten exact snapshots, package age ranges from 5 to 4,464 days (median 3,358); prior version count ranges from 4 to 130 (median 38.5); and the direct-dependency count ranges from 0 to 7 (median 3). All ten retained source versions include registry integrity metadata and none expose an install-script indicator in the retained snapshot. These facts are not evidence of protective or harmful effects because the data contain no comparison population.

| Requested analysis | Decision | Evidence-grounded reason |
|---|---|---|
| Direct-dependency-count ranking | Not evaluable | No cutoff-valid controls against which to rank. |
| Package-age ranking | Not evaluable | No cutoff-valid controls against which to rank. |
| Multivariable logistic regression | Blocked | Retained records are incident records, not positive/negative outcomes in a sampling frame. |
| Probability calibration | Blocked | No cutoff-valid evaluation population; two label-only events also lack exact feature snapshots. |
| PR-AUC or Recall@K | Blocked | Requires positives and a defensible non-event population. |
| Historical structural/workflow features | Excluded | Current graph, maintainer, workflow, download, and popularity data cannot be backdated without an auditable historical source. |

The strict positive-count and family-count floors are met. The remaining gate is to pre-register a cutoff-valid control design and ensure that exact historical feature coverage is adequate for the records being evaluated before fitting or calibrating a model. The 2021 `ua-parser-js`, `coa`, and `rc` observations must remain grouped as one family rather than treated as three independent attack instances.

## Explicit-label corpus control-frame review

The public Amalfi ICSE 2022 artifact provides a valuable distinction from generic “no-known-event” rows: its frozen 1,790-row basic corpus explicitly labels 643 package-version releases malicious and 1,147 benign. [11] However, it is a retrospective release-classification corpus rather than a documented future-outcome population. It does not disclose a per-row review time or outcome horizon, and it is concentrated around malicious-package detection cases rather than a population-sampled at-risk frame.

Registry provenance makes the mismatch more decisive. Of the 1,790 explicit labels, 1,102 version objects remain available from the current registry—but these comprise **9 malicious** and **1,093 benign** rows. The other 688 rows comprise 634 malicious and 54 benign rows. This extreme label-associated retention means that a classifier trained on retained rows would estimate registry survival, not a meaningful release-classification or future-compromise relationship. No imputation, class balancing, or performance metric is reported.

| Requested role | Decision | Evidence boundary |
|---|---|---|
| Explicit version-level negative labels | Provenanced | The source directly assigns labels; these are not inferred no-known-event rows. |
| Primary temporal controls | Blocked | No frozen outcome horizon or at-risk population frame. |
| Retained release-classification model | Blocked | 9 retained malicious versus 1,093 retained benign rows; retention is outcome-linked. |
| Primary PR-AUC, Recall@K, calibration, or ranking | Blocked | Target, sampling frame, and independent-family design remain unmatched. |

The corpus therefore strengthens the methodological conclusion rather than relaxing it: explicit benign labels alone are insufficient when source construction, timing, and post-publication retention do not support the target causal/temporal question. The provenance ledger and control-frame memorandum preserve the corpus for a future release-classification study in an archival environment, but no result transfers to this study's future-compromise benchmark.

## Provider-backed control-frame assessment

Open Source Insights documents the deps.dev BigQuery dataset as a provider-backed source with full-snapshot timestamps, package-version exports, upstream publication times, and advisory disclosure plus affected/unaffected-version fields. [16] Those fields are technically promising for a future frozen package-version population, but the documented advisory relation is vulnerability-oriented rather than a closed-world record of malicious publication or publisher compromise.

The provider requires a Google Cloud account and enabled BigQuery API. The recorded unauthenticated metadata probe returned HTTP 401 and retrieved no table metadata or rows; consequently, it created **zero controls**. A versioned Figshare/Mendeley malicious-NPM source-code release was also excluded: its public landing metadata does not establish row-level package-version identity, collection cutoff, population coverage, or an outcome horizon. [17] [18]

| Candidate source | Useful documented property | Primary-control decision | Reason |
|---|---|---|---|
| deps.dev BigQuery | Snapshot, version, publication, dependency, and advisory fields | Excluded pending authorized, matched access | No rows were accessible; advisory semantics do not cover the target malicious-publication/compromise outcome. |
| Figshare/Mendeley malicious-NPM source-code release | Versioned public release with labelled folders | Excluded | Landing metadata does not define a temporal package-version population or a valid non-event horizon. |

This assessment is a precise feasibility result, not evidence that either source contains no useful data. It preserves the no-fit gate: absence from an advisory or catalogue is not a benign temporal control. The reproducible assessment and HTTP probe record are `81_provider_control_frame_assessment.md` and `81_provider_control_frame_probe.json`.

## Control-frame contract and public snapshot access assessment

A valid control frame requires more than a package list. Before extraction, the study now requires a named frozen population, row-level package-version identity, a separately frozen event-coverage source whose documented target includes malicious publication or publisher compromise, a post-cutoff observation horizon, pre-registered exclusions, and a bounded reproducible access path. Missing entries in a source that fails any of these requirements remain **unknown**, not benign.

The Zenodo **NPM Registry Dataset 2025 (GitHub Only)** is a useful population-source lead: it documents a 20 February 2025 snapshot and an explicit GitHub-repository inclusion rule for 1,900,347 package records. [19] Its associated documentation describes registry-style records, but the only release payload is one 22.3 GB gzip file (108 GB uncompressed) with full-stream parsing rather than a row-addressable or filtered export. [19] [20] No payload bytes were retrieved. More decisively, no linked source supplies closed-world malicious-publication or compromise coverage and a horizon for the candidate population. The source is therefore excluded for the present temporal control frame.

Libraries.io is likewise excluded: its public documentation describes scraped, unvalidated package metadata and a current aggregate package count, not an immutable historical package-version population with a documented outcome horizon. [21] Its public data cannot supply a temporal non-event denominator. The new `83_control_frame_contract_and_access_assessment.md` preserves the contract, exact source boundaries, and zero-control decision.

The Figshare replication package for Guo et al.’s 2026 detector benchmark is a useful **release-classification sensitivity lead**, but it also fails the primary temporal-control contract. Its public description reports 6,420 malicious package versions and 7,288 benign packages. A bounded version-1 archive inspection retrieved only its ZIP directory plus three named text/CSV metadata members—not any package source—and confirmed 6,420 malware package-version rows, of which 271 have blank timestamps after normalization. Its selected-benign list contains 1,000 version-addressable strings but no per-row timestamp, collection cutoff, follow-up horizon, or documented relationship to the later 7,288-benign count. [24] [25] The release is a retrospective detector-evaluation corpus assembled from academic datasets and public advisories, rather than a frozen at-risk population followed under matched compromise coverage. It creates **zero controls**.

| Candidate source | Population property | Outcome-coverage and horizon | Bounded access | Primary-control decision |
|---|---|---|---|---|
| Zenodo NPM Registry Dataset 2025 | Named 20 February 2025 GitHub-repository subset | No paired malicious-publication/compromise coverage or horizon | One 22.3 GB gzip / 108 GB expanded stream | Excluded. |
| deps.dev BigQuery | Snapshot and package-version fields documented | Advisories are vulnerability-oriented; no authenticated access | Google Cloud account and BigQuery API required | Excluded pending both access and target match. |
| Libraries.io public metadata | Current scraped package metadata | No frozen historical outcome contract | Public page, but no documented temporal denominator | Excluded. |
| Guo et al. Figshare detector benchmark | Versioned package/version labels and partial malware timestamps | Retrospective detector corpus; benign list lacks timestamp, cutoff, and horizon | Bounded metadata-only ZIP access works | Excluded as primary temporal control frame. |

## What the discovered version-resolved dataset changes—and does not change

CHRONO-RESOLUTION is a public, citable dataset designed for dependency resolution at release points. Its authors report 146,651 npm packages and 245,307,373 npm package-dependency interval relationships, and document that the release includes raw and filtered data, scripts, and query examples. [10] [11] It is the appropriate **next source candidate** for target-version and interval-aware direct-edge reconstruction.

However, its supplied archive is a single 10.2 GB compressed release, while its underlying npm relation table is much larger when imported. It also has an August 2024 registry snapshot date, so it cannot cover the 2026 Axios-family record. The archive was therefore recorded as an acquisition and validation gate, not silently treated as ingested evidence. Before using it, the study must validate package coverage, temporal interval semantics, resolver behavior, and the mapping between the dataset's release-point intervals and each frozen event cutoff. Only after that validation may any resolved-target or transitive graph carry an **approximate/version-resolved** fidelity label distinct from the exact declared-edge fidelity used here.

## Implications for the proposed research contribution

The result narrows a defensible contribution. Rather than claiming that blast radius can currently be forecast from a small current-snapshot feature set, the study can contribute a **leakage-resistant temporal evaluation protocol** and an auditable staged reconstruction pipeline. The pipeline separates: (1) incident adjudication, (2) exact source-version reconstruction, (3) declared direct edges, (4) externally resolved historical dependencies, and only then (5) transitive blast-radius measurement and predictive evaluation.

This boundary is scientifically useful. It prevents a present-day dependency graph or repository workflow feature from being presented as evidence about a prior compromise, and it prevents multiple packages from the same campaign from inflating apparent sample size. A future predictive study should retain this fidelity vocabulary, preserve raw checksums and event-family identifiers, and report results only after its controls, time splits, and historical feature availability have passed the stated gate.

## References

[1] [CISA, “Malware Discovered in Popular npm Package ua-parser-js,” 22 October 2021](https://www.cisa.gov/news-events/alerts/2021/10/22/malware-discovered-popular-npm-package-ua-parser-js).

[2] [Mandiant, “Supply Chain Compromise Affects Node.js Package Manager,” 2021](https://cloud.google.com/blog/topics/threat-intelligence/supply-chain-node-js/).

[3] [CISA, “Supply Chain Compromise Impacts Axios Node Package Manager,” 20 April 2026](https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager).

[4] [npm, “Details about the event-stream incident,” 2018](https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident).

[5] [ESLint, “Postmortem for Malicious Package Publishes,” 2018](https://eslint.org/blog/2018/07/postmortem-for-malicious-package-publishes/).

[6] [SafeDep, “Compromised node-ipc on npm: Credential Stealer via DNS Exfiltration,” 14 May 2026](https://safedep.io/malicious-node-ipc-npm-compromise/).

[7] [OpenSSF Malicious Packages, “MAL-2026-3744: Malicious code in node-ipc (npm)”](https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/node-ipc/MAL-2026-3744.json).

[8] [SafeDep, “183 npm Packages Target Cloud and Finance via oob.moika.tech,” 28 May 2026](https://safedep.io/oob-moika-tech-dependency-confusion-campaign/).

[9] [OpenSSF Malicious Packages, “MAL-2026-5163: Malicious code in @emcd-vue/auth (npm)”](https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/%40emcd-vue/auth/MAL-2026-5163.json).

[10] [I. Rahman, J. Marley, R. Paramitha, and L. Williams, “chrono-resolution: A Dependency Resolution Dataset at Release Points for npm, PyPI, and crates.io Packages,” arXiv:2607.15315, 2026](https://arxiv.org/abs/2607.15315).

[11] [Rahman et al., “CHRONO-RESOLUTION” data release, Zenodo, DOI 10.5281/zenodo.17576373](https://doi.org/10.5281/zenodo.17576373).

[12] [npm, “node-semver” reference implementation](https://github.com/npm/node-semver).

[13] [npm, “package-lock.json” documentation](https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/).

[14] [npm, “semver” documentation](https://docs.npmjs.com/cli/v6/using-npm/semver/).

[15] [A. Sejfia and M. Schäfer, “Practical Automated Detection of Malicious npm Packages,” ICSE 2022 artifact repository](https://github.com/githubnext/amalfi-artifact).

[16] [Open Source Insights, “deps.dev BigQuery dataset”](https://docs.deps.dev/bigquery/v1/).

[17] [Figshare, “Malicious NPM Package Detection Dataset,” DOI 10.6084/m9.figshare.31451728](https://doi.org/10.6084/m9.figshare.31451728).

[18] [Mendeley Data, “Malicious NPM Package Detection Dataset,” Version 1](https://doi.org/10.17632/6tc8wrp62g.1).

[19] [Zenodo, “NPM Registry Dataset 2025 (GitHub Only),” Version 1.0.0](https://zenodo.org/records/14914149).

[20] [Brittany Reid, “npm-mine” repository and dataset documentation](https://github.com/Brittany-Reid/npm-mine).

[21] [Libraries.io, “Data and service description”](https://libraries.io/data).

[22] [SafeDep, “Mini Shai-Hulud Strikes Again: 317 npm Packages Compromised,” 19 May 2026](https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/).

[23] [OpenSSF Malicious Packages, “MAL-2026-4127: Malicious code in amapcn (npm)”](https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/amapcn/MAL-2026-4127.json).

[24] [W. Guo et al., “How Effective Are NPM Malicious Package Detectors? A Large-Scale Empirical Study,” arXiv:2603.27549v2, 2026](https://arxiv.org/html/2603.27549v2).

[25] [W. Guo, “How Effective Are NPM Malicious Package Detectors? A Large-Scale Empirical Study,” Figshare Version 6](https://doi.org/10.6084/m9.figshare.31869370).
