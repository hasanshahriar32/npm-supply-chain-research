# Temporal Reconstruction and Baseline-Eligibility Results

**Status:** Completed feasibility and reconstruction stage; **no predictive model has been fitted.**  
**Scope:** Pre-registered package-event records, official npm registry metadata, and independently adjudicated incident evidence.  
**Prepared by:** Manus AI  
**Artifact date:** 24 August 2026

## Executive finding

This extension successfully reconstructs **eighteen exact pre-event package-version metadata snapshots** from twenty pre-registered npm package-event records spanning **fourteen incident families**. It produces a reproducible ledger of **51 cutoff-valid direct dependency declarations** and, for every declared range, one **isolated cutoff-valid SemVer target approximation**. A separate, depth-three registry-only sensitivity artifact expands those approximations to **259 bounded edges** across twelve roots with runtime dependencies. Neither artifact is a lockfile or a package-manager execution trace. No transitive reach is computed, and therefore no historical blast-radius or attack-return quantity is estimated.

The evidence permits a negative but important methodological conclusion. The present data cannot support ranking, logistic-regression, PR-AUC, Recall@K, probability-calibration, or uncertainty estimates. The twenty-record and fourteen-family totals are not an independently sampled training cohort; the pilot still has no cutoff-valid adjudicated non-event population and only eighteen exact source snapshots because two high-confidence label-only events lack usable pre-event registry objects. The correct result is a transparent **no-fit decision**, not a weakly powered model claim.

> **Historical-fidelity definition.** `registry_reconstructed_exact_direct_declaration` means that the source package version was selected strictly before the event cutoff from the official npm registry's version-time map and that version object's declared `dependencies` map was retained verbatim. It does **not** mean that a declared range was resolved to a target version, installed by npm, or expanded transitively.

## Evidence and reconstruction design

The package-event ledger contains independently sourced, high-confidence incidents: the 2021 `ua-parser-js` / `coa` / `rc` compromise family, the 2018 `event-stream` incident, the 2018 ESLint incident, the 2025 `is` compromise, and the 2026 Axios-, `node-ipc`-, `oob.moika.tech`-, Mini Shai-Hulud-`atool`-, and Keyv/Cacheable-related families. Primary or authoritative incident sources identify the affected releases and event anchors, while the registry provides the temporal version objects. CISA's public alerts identify the `ua-parser-js` and Axios-related affected versions; Mandiant documents the 2021 Node.js compromise campaign; npm's incident post documents the `event-stream` response; ESLint's postmortem records its publication timeline; and independently published SafeDep and OpenSSF records corroborate the `node-ipc`, `@emcd-vue/auth`, and `amapcn` release sets and event timing. Frozen OpenSSF `MAL-2025-6020`, a dated StepSecurity report, and the `is` maintainer’s remediation commit agree that `is@3.3.1` and `5.0.0` were malware-bearing releases from a hijacked account. Frozen OpenSSF `MAL-2026-11524`, the frozen Wiz Keyv IOC list, and independent Snyk research agree on `keyv@6.0.0`; the official registry timestamp provides the feature cutoff and selects `keyv@6.0.0-rc.1` as the source object. Wiz reports payload descent from Mini Shai-Hulud, so the separate Keyv/Cacheable campaign family is not treated as statistically independent of the May 2026 `atool` family. [1] [2] [3] [4] [5] [6] [7] [8] [9] [22] [23] [32] [33] [34] [35] [36] [37] [38]

For each record, the builder sets the feature cutoff to one millisecond before the recorded event start, selects the latest registry version timestamp at or before that cutoff, and reads only that selected version object's runtime `dependencies`. A SHA-256 digest of the raw registry response is stored with each reconstructed source record. This arrangement prevents the event release itself or later metadata from becoming a feature.

| Reconstruction component | Result | Fidelity and interpretation |
|---|---:|---|
| Pre-registered package-event records | 19 | Package-level observations; not nineteen independent attacks. |
| Incident families | 13 | The earlier twelve families plus `solana_web3_js_publish_access_compromise_2024`. `colors` and `faker` remain one related family; Keyv/Cacheable remains non-independent of the `atool` family for any future uncertainty design because only payload ancestry—not statistical independence—is documented. |
| Exact source snapshots | 17 | Source package version object selected strictly before its cutoff. |
| Source snapshot unavailable | 2 | `plain-crypto-js` and `@emcd-vue/auth`; no qualifying pre-event version object was retained by the current registry response. |
| Declared direct edges | 48 | Exact source declarations, each retaining the original SemVer range. |
| Isolated target-range approximations | 48 | Highest valid SemVer version within the declared range and published by the cutoff; not an observed installation result. |
| Transitive-reach values | 0 | Intentionally not computed. |

The reproducible inputs and outputs are `64_temporal_package_event_ledger.csv`, `65_package_temporal_companion_snapshots.csv`, `65_package_temporal_companion_declared_edges.csv`, `66_temporal_baseline_and_calibration_gate.json`, `67_cutoff_direct_dependency_graph_edges.csv`, `67_cutoff_direct_dependency_graph_manifest.json`, `70_cutoff_direct_dependency_range_resolution.csv`, `71_direct_range_resolution_diagnostic.json`, `74_bounded_recursive_registry_semver_graph_edges.csv`, and `75_bounded_recursive_registry_graph_diagnostic.json`. The relevant build scripts are `build-package-temporal-companion.mjs`, `build-cutoff-direct-dependency-graphs.mjs`, `build-cutoff-direct-dependency-range-resolution.mjs`, `analyze-direct-range-resolution-diagnostic.mjs`, `build-bounded-recursive-registry-graph.mjs`, and `analyze-bounded-recursive-registry-graph.mjs`.

## Direct-dependency reconstruction result

The graph artifact begins as a **declared-edge ledger**, not an implied package-manager installation tree. Every edge records the source package-version node, dependency package name, declared range, cutoff, response checksum, and three fidelity fields: source snapshot fidelity, target-version fidelity, and transitive-reach fidelity. A second ledger (`70_cutoff_direct_dependency_range_resolution.csv`) uses the maintained `semver` implementation to select the highest non-prerelease target version satisfying each direct declaration among versions whose registry timestamps are at or before the cutoff. All 29 ranges resolved under that deliberately narrow procedure. [12]

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
| `is-2025-07-19` | 3.3.0 | 0 | Exact direct declaration | No runtime dependency declarations in the selected version. |
| `keyv-2026-08-04` | 6.0.0-rc.1 | 1 | Exact source declaration + 1 isolated target approximation | No install trace or transitive traversal. |
| `colors-2022-01-08` | 1.4.0 | 0 | Exact direct declaration | Related to `faker`; no runtime dependency declarations in the selected version. |
| `faker-2022-01-05` | 5.5.3 | 0 | Exact direct declaration | Related to `colors`; no runtime dependency declarations in the selected version. |
| `debug-2025-09-08` | 4.4.1 | 1 | Exact source declaration + 1 isolated target approximation | One bounded Qix-related family record; no install trace or transitive traversal. |
| `solana-web3-js-2024-12-03` | 2.1.0-canary-20241203100809 | 18 | Exact source declaration + 18 isolated target approximations | All-stream time-map selection; no same-branch substitution, install trace, or transitive traversal. |

The selected sixteen exact source snapshots have a mean of **3.0** declared runtime dependencies, a median of **1.5**, a minimum of **0**, and a maximum of **18**. These are descriptive properties of the reconstructed pilot records only. They do not measure dependency reach, downstream consumers, package importance, or attack impact.

## Bounded recursive registry-graph sensitivity

Official npm documentation defines `package-lock.json` as the exact dependency tree generated by an npm operation, while the SemVer reference defines a range as a set of satisfying versions and documents highest-satisfying selection over a supplied version list. [11] [12] The study therefore uses the current registry only for a **bounded sensitivity graph**: it recursively selects the highest retained, non-prerelease package version satisfying each runtime `dependencies` range and published by the root's frozen cutoff. It excludes `devDependencies`, peers, optional and bundled relations, workspaces, overrides, links, git and tarball specifications, as well as all package-manager installation behavior.

The resulting artifact contains **225 edges** and **107 bounded nodes across the eleven root graphs with runtime dependencies**. The sixteen-root exact-snapshot design also retains `ua-parser-js@0.7.28`, `wenk@1.0.8`, `is@3.3.0`, `colors@1.4.0`, and `faker@5.5.3`, each with no runtime dependencies, while `plain-crypto-js` and `@emcd-vue/auth` remain unavailable as exact source snapshots. The 225 edges distribute as 48 at depth one, 108 at depth two, and 69 at depth three; every selected target range resolved under the stated cutoff-valid SemVer method.

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
| `keyv@6.0.0-rc.1` | 1 | 2 | 1 / 0 / 0 | Range-selected registry sensitivity only. |
| `debug@4.4.1` | 1 | 2 | 1 / 0 / 0 | Range-selected registry sensitivity only. |
| `@solana/web3.js@2.1.0-canary-20241203100809` | 160 | 38 | 18 / 90 / 52 | Range-selected registry sensitivity only; no reach or blast-radius interpretation. |

> **Interpretation limit.** These counts are neither historical installed-tree sizes nor transitive dependency reach. The graph is not a package-lock reconstruction and must not be compared across roots as a security score, centrality measure, blast-radius quantity, or input to any ranking, calibration, PR-AUC, Recall@K, or attack-return calculation.

## Temporal baseline and calibration gate

The gate computed descriptive feature summaries rather than a model. Across the sixteen exact snapshots, package age ranges from 5 to 5,032 days (median 3,358); prior version count ranges from 4 to 1,945 (median 40); and the direct-dependency count ranges from 0 to 18 (median 1.5). All sixteen retained source versions include registry integrity metadata and none expose an install-script indicator in the retained snapshot. These facts are not evidence of protective or harmful effects because the data contain no comparison population.

| Requested analysis | Decision | Evidence-grounded reason |
|---|---|---|
| Direct-dependency-count ranking | Not evaluable | No cutoff-valid controls against which to rank. |
| Package-age ranking | Not evaluable | No cutoff-valid controls against which to rank. |
| Multivariable logistic regression | Blocked | Retained records are incident records, not positive/negative outcomes in a sampling frame. |
| Probability calibration | Blocked | No cutoff-valid evaluation population; two label-only events also lack exact feature snapshots. |
| PR-AUC or Recall@K | Blocked | Requires positives and a defensible non-event population. |
| Historical structural/workflow features | Excluded | Current graph, maintainer, workflow, download, and popularity data cannot be backdated without an auditable historical source. |

The strict positive-count and family-count floors are met. The remaining gate is to pre-register a cutoff-valid control design and ensure that exact historical feature coverage is adequate for the records being evaluated before fitting or calibrating a model. The 2021 `ua-parser-js`, `coa`, and `rc` observations must remain grouped as one family rather than treated as three independent attack instances.

## Campaign relatedness and future grouped-inference protocol

`94_campaign_relatedness_and_grouped_inference_protocol.json` freezes a **non-executed** inference safeguard from the strict seventeen-record ledger. It inventories twelve campaign families, keeps the shared-family `unc3379_2021`, Axios, ESLint, and colors/faker records intact, and defines eleven validation units after clustering the documented Mini Shai-Hulud `atool` and Keyv/Cacheable payload-lineage families. The latter remain separately dated observations, but payload descent is not evidence of statistical independence. The colors/faker shared-maintainer event remains a single family rather than two independent units; the bounded Qix-related Debug family is also a single unit and does not establish campaign completeness. The artifact records source checksums, group memberships, and the exact statement retained from the frozen Keyv assessment.

| Protocol layer | Pre-registered rule | Current result |
|---|---|---|
| Split unit | Assign connected components of the documented family-relatedness graph, not package-event rows, to a single temporal partition. | Ten validation units defined; **zero splits generated**. |
| Temporal order | Use forward-only development, validation, and final-test cutoffs; exclude any split whose evaluation partition is structurally ineligible. | No control frame or model-eligible dataset exists. |
| Related family handling | Keep `mini_shai_hulud_atool_2026` and `keyv_cacheable_august_2026` in one validation cluster. | Required for any future eligible split or resampling design. |
| Uncertainty design | If the eligibility gate later opens, resample validation units rather than package-event rows and report degenerate replicates. | **Zero intervals** and no resampling output. |

The implementation references group-aware validation only as a future technical pattern: GroupKFold documents non-overlapping groups; GroupShuffleSplit documents randomized group partitions and fixed seeds; and the cross-validation guide states that time-dependent and grouped processes warrant time-aware and group-wise validation. [39] [40] [41] No library splitter was run. The protocol does not supply controls, a train/test split, model fit, uncertainty interval, rank, or predictive metric; it makes future inference more auditable if and only if the separate frozen-population and target-matched outcome gate is later satisfied.

## Strict pre-event release-authority metadata availability

`95_release_authority_metadata_availability_audit.json` performs a bounded **availability audit**, not a release-authority feature extraction. It reads only the official-registry version object already selected strictly before each incident cutoff and its immediate earlier retained version object. The root package document, current dist-tags, current maintainer lists, current repository and workflow state, downloads, and dependency graphs are excluded. The two label-only records remain out of scope because no exact source object exists.

| Availability condition | Exact pre-event source snapshots | Permitted reading |
|---|---:|---|
| Immediate earlier retained version object | 14 / 14 | A predecessor object is currently retained for comparison availability only. |
| Repository-descriptor comparison available | 13 / 14 | Both frozen version objects retain a repository descriptor; no descriptor value or difference is emitted. |
| `gitHead` comparison available | 11 / 14 | Both frozen version objects retain a `gitHead`; no hash, equality result, or change classification is emitted. |
| `publishConfig` comparison available | 0 / 14 | No paired retained `publishConfig` field is available under this narrow rule. |
| Selected `dist.integrity` retained | 14 / 14 | Integrity presence is retained as metadata availability only, not provenance quality or risk evidence. |

The artifact emits booleans, selected/predecessor version identifiers, and registry-response checksums only. It extracts **zero metadata values**, classifies **zero deltas**, computes **zero release-authority scores**, and creates **zero controls, effects, rankings, models, or predictive metrics**. A retained field is not evidence of authority integrity, compromise likelihood, or benign status; a missing field is not a hygiene or outcome label. The audit therefore identifies a future data-availability gate without retroactively reconstructing publisher transitions, repository transfers, provenance changes, or workflow changes.

## Future-only release-authority delta semantics

`96_release_authority_delta_semantics_protocol.json` converts the preceding availability audit into a **future-only eligibility contract**, not an observed-delta analysis. It defines six possible review-surface families: repository links, source-revision references, release-manifest publication intent, verifiable provenance attestations, release mediation or publisher authority, and release-bound workflow authority. Each can enter a future benchmark only after a frozen control frame, target-matched horizon, version-specific raw evidence, field semantics, canonicalization policy, source checksums, and the campaign-relatedness registry are all frozen before outcomes are inspected.

| Future comparison type | Minimum evidence boundary | Never infer |
|---|---|---|
| Repository or source-revision reference | Two retained version objects, opaque values, versioned canonicalization, and time-valid checksums. | Current repository ownership, code differences, or hostile transfer. |
| Manifest publication intent | Two immutable release-manifest fragments and a pre-registered allowlist. | Build workflow, actor identity, or attestation status from a missing field. |
| Provenance attestation | Release-specific signed attestation, verification policy, and immutable transparency-log reference. | Absence of malicious code or a benign outcome. |
| Publisher/mediation or workflow authority | Version-specific evidence with documented retention and semantics; workflow state must be bound to the release revision. | Account takeover, secrets, cloud scope, or malicious intent. |

The protocol makes `not_eligible_missing_or_ambiguous_evidence` and `not_applicable_to_release_regime` explicit states; neither may fall back to unchanged, safe, benign, or no-known-event. It records **zero raw values, observed comparisons, classified deltas, scores, controls, models, ranks, or predictive metrics**. The design uses Santos-Grueiro’s predecessor-aware release-authority record only as methodological context, retains npm’s explicit warning that provenance does not guarantee malicious-code absence, and does not access provenance data from npm or deps.dev. [42] [43] [44]

## Official npm provenance-attestation access screen

`97_official_npm_provenance_attestation_access_assessment.json` evaluates whether the fifteen exact pre-event source versions can be checked for provenance attestations **without package download, installation, or undocumented endpoint guessing**. Official npm documentation describes `npm audit signatures` as the verification mechanism for downloaded dependency sets, while the public Registry API reference reviewed here does not document a public unauthenticated metadata-only endpoint for an arbitrary version’s attestation bundle. Therefore the assessment makes **zero version-specific endpoint requests**, downloads **zero package payloads**, runs **zero signature verifications**, retrieves **zero bundles**, and classifies **zero attestation states**.

| Access question | Bounded result | Inference limit |
|---|---|---|
| Candidate pre-event versions | 15 exact source objects could be screened in a future documented or authorized path. | Candidate availability is not an attestation result. |
| Official metadata-only retrieval path | Not established by the reviewed documentation. | Do not guess an endpoint or convert access uncertainty to attestation absence. |
| Documented verification mechanism | `npm audit signatures` for downloaded dependency sets. | Not invoked; it would exceed the metadata-only/no-payload access policy. |
| Provenance meaning | A verifiable link to source/build information. | It does not guarantee absence of malicious code and does not create a benign label. |

The decision is an **access-contract exclusion**, not a provenance-state result for any package version. It creates **zero comparisons, controls, release-authority scores, rankings, models, or predictive metrics**. Current badges, current provenance views, current repository state, and current transparency-log search results remain unusable as historical evidence. [45] [46] [47]

## Full-ledger source-object retention census

`98_full_ledger_source_object_retention_census.json` separates the **current registry’s retention of reconstructable source objects** from historical package evidence across every pre-registered ledger record. All seventeen records have a checksum-identified current registry response. Fifteen retain a selected pre-cutoff version object that satisfies the strict source-object requirement; two remain label-only exceptions. This is a census of reconstruction eligibility, not a measurement of historical package state.

| Retention state | Records | Consequence |
|---|---:|---|
| Current response retains selected pre-event version object | 15 | Eligible for the existing strict source-object reconstruction only. |
| Time map selects a pre-cutoff version but the selected object fails strict retention | 1 (`plain-crypto-js`) | Remains label-only; no substitute source object, feature, or delta is created. |
| Current response has no retained pre-cutoff version selection | 1 (`@emcd-vue/auth`) | Remains label-only; no absent-history or benign inference is permitted. |

The census stores only record identifiers, selected version identifiers and timestamps, retention states, and current response provenance. It extracts **zero package metadata, maintainer, publisher, repository, workflow, provenance, or attestation values**; derives **zero features**; and creates **zero controls, scores, models, rankings, or predictive metrics**. Current retention differences do not make campaign rows independent and cannot stand in for any release-time package, authority, dependency, or workflow observation.

## Future raw-evidence capture contract for release-authority deltas

`99_release_authority_raw_evidence_capture_contract.json` operationalizes the existing future-only delta ontology without observing a new authority value. It defines the collection envelope that must exist **before** a future eligible comparison: a frozen field-specific plan; access-controlled, immutable raw-evidence storage; append-only chain-of-custody records; source-time validity checks; and offline canonicalization that writes only opaque, access-controlled commitments to a public-safe ledger.

| Contract element | Required future safeguard | Explicitly not produced now |
|---|---|---|
| Raw evidence integrity | Exact received bytes, byte digest, length, media type, retrieval protocol, and transformation lineage reside in controlled storage. | No evidence object, endpoint contact, package payload, installation, or execution. |
| Opaque canonicalization | Versioned offline function plus keyed, non-public commitments prevent raw value publication and low-entropy dictionary recovery. | No raw value, canonicalization run, commitment, equality result, or delta classification. |
| Source-time validity | Pairwise release/predecessor binding, field semantics, historical retention, and release-time relation must be documented before collection. | No current registry, maintainer, repository, VCS, workflow, or provenance state is substituted. |
| Six field schemas | Repository link, source revision, manifest intent, provenance, publisher/mediation, and workflow evidence each have a narrow allowable source class. | No authority feature, control, outcome, score, rank, interval, model, calibration, or metric. |

The contract is deliberately **pre-activation**. A capture run remains prohibited unless a frozen package-version population and independently adjudicated, target-matched, horizon-covered outcome manifest satisfy the primary control-frame gate, and the collector is insulated from outcomes until quality control is sealed. Missing, redacted, malformed, current-only, or time-ambiguous evidence remains a reason code—not `unchanged`, safe, benign, trusted, or no-known-event.

## Future independently adjudicated outcome-manifest sealing protocol

`100_future_outcome_manifest_sealing_protocol.json` defines the complementary future process for outcomes: it requires a target/horizon contract, versioned source inventory, independent candidate dockets, full-horizon coverage records, conflict and retraction history, checksum and Merkle-root sealing, and strict blinding from feature collection. It does not inspect an incident source or create a target record.

| Protocol layer | Future requirement | Explicit boundary |
|---|---|---|
| Target and horizon | Freeze `(feature cutoff, horizon end]`, target definition, lag policy, censoring rule, and exclusions before opening an outcome source. | A later discovery cannot move an event time without independently documented time evidence. |
| Source and adjudication | Preserve scoped source objects; use independent adjudicators, pre-registered reconciliation, exact package-version identity, and event-time support. | Advisory absence, registry survival, remediation, deletion, and current state never become a target decision. |
| Non-event decision | Require source-specific completeness across the entire row horizon and explicit exclusions. | Incomplete coverage, ambiguity, or absence remains unknown or right-censored—not a control. |
| Sealing and blinding | Seal source inventory, dockets, coverage, and decision ledgers with immutable revisions; keep adjudicators blind to features, priority, controls, and performance. | No manifest, outcome row, positive, non-event, join, split, score, model, interval, or metric exists now. |

The protocol inherits the frozen related-family rule: Mini Shai-Hulud `atool` and Keyv/Cacheable remain one documented related-family cluster in any future eligible join, while colors and faker remain one shared-maintainer family. The bounded Qix-related Debug record remains one separate family and validation unit, not a campaign-complete census. A sealed manifest is **integrity metadata**, not proof that a package version is positive, unaffected, safe, benign, or trusted. Existing seventeen incident records remain positive evidence only and do not establish closed-world coverage or a non-event population.

## Future public-safe aggregate-release policy

`101_future_public_safe_aggregate_release_policy.json` specifies how a future eligible study must separate public governance metadata from restricted evidence. It defines four release classes, but currently enables only protocol metadata. It does not inspect a source or compute an aggregate.

| Release class | Future content boundary | Current state |
|---|---|---|
| P0 — protocol metadata | Versioned schemas, gates, policy identifiers, and prohibited-field rules only. | The only class represented by this policy itself; it contains no observed values or counts. |
| P1 — sealed integrity metadata | Opaque manifest-level commitments and gate status only, subject to source terms and disclosure review. | Not activated; raw values, source references, row commitments, and identifiers remain restricted. |
| P2 — screened descriptive aggregates | Broad, pre-registered aggregates only after population/outcome seals, disclosure review, small-cell suppression, complementary suppression, differencing review, linkage review, and relatedness controls. | Not activated; any aggregate using the current 17 records, 12 families, or 11 future validation units is non-releasable. |
| P3 — aggregate benchmark results | Model-result release would require a separate future amendment and independently eligible benchmark. | Explicitly disabled: no performance, calibration, ranking, interval, cohort, or feature-effect result may be released. |

The policy permanently restricts raw source objects, exact protected package/version identities, outcome and control rows, authority values and commitments, reviewer material, feature rows, split membership, scores, rankings, intervals, and predictive metrics. Even a permitted future aggregate must preserve documented related-family clusters, avoid direct and complementary small-cell reconstruction, resist temporal and cross-release differencing, and carry immutable revision and revocation lineage. A release class, digest, gate decision, or suppression decision remains **governance metadata**, not evidence of benignness, coverage, independence, historical fidelity, or model eligibility.

## Future aggregate-plan parameter-sealing contract

`102_future_aggregate_plan_parameter_sealing_contract.json` resolves the release policy’s remaining precondition without choosing a threshold. It specifies how a future, independent disclosure authority must select a complete secure parameter set **before** it receives protected data, preview counts, outcomes, controls, score distributions, rankings, or model results.

| Contract element | Future requirement | Explicit boundary |
|---|---|---|
| Secure record | Holds 12 secure-only parameter categories for cell and validation-unit protection, broad strata, rounding, suppression, coarsening, linkage review, relatedness, iteration, and revocation. | No parameter value, threshold, stratum, rule, record, or commitment is set now. |
| Public commitment | Allows only a keyed, non-reversible, non-dictionary-attackable commitment plus process status after secure sealing. | No value, deterministic hash, stable identifier, raw timestamp, data-derived digest, row, label, outcome, control, or aggregate may be public. |
| Role separation | Parameter authority, disclosure reviewer, implementation operator, and audit observer must be distinct from outcome, source, feature, population, and model roles. | A passing verification is not a data-access approval, safe-disclosure proof, or release authorization. |
| Amendment | Before protected-data access, replace the complete record with a new immutable revision and fresh attestations; afterward, abort and restart a new protocol instance. | No threshold tuning after a cell, suppression outcome, prevalence, score, rank, or model result. |

The contract contains zero secure records, parameter values, commitments, attestations, access-control reviews, verifications, amendments, plans, cells, releases, outcomes, controls, authority values, scores, rankings, intervals, or metrics. A withheld or revoked parameter is not evidence about a package, incident, coverage gap, non-event, safe release, or model conclusion.

## Bounded crossenv typosquatting screen

The 2017 `crossenv` typosquatting incident is independently corroborated but **excluded** from the 17-record primary temporal ledger. npm’s incident notice identifies deliberate malicious `hacktask` typosquatting beginning 19 July 2017, environment-variable exfiltration through `crossenv`, and registry removal of the actor’s packages. [48] An independent contemporaneous account and Snyk’s advisory both identify `crossenv@6.1.1`. [49] [50]

| Eligibility check | Bounded evidence | Strict result |
|---|---|---|
| Exact candidate release | Independent reports identify `crossenv@6.1.1`. | Satisfied for a candidate screen only. |
| Official event-time anchor | The official registry time map retains `6.1.1` at `2017-07-19T06:49:52.698Z`; the strict cutoff is one millisecond earlier. [51] | Satisfied. |
| Time-mapped predecessor | The same official time map selects `6.0.7` at `2017-07-19T06:32:58.946Z`. [51] | Satisfied only as a timestamp selection. |
| Exact retained pre-event source object | The bounded current registry response retains only `0.0.1-security`, `0.0.2-security`, `1.0.0`, and `1.0.1` version objects; it does not retain the selected `6.0.7` object. | **Failed.** No strict snapshot can be reconstructed. |

`103_crossenv_typosquatting_candidate_assessment.json` preserves the source checksums, exact time-map decision, and retention exception. It adds **zero** primary-ledger records or families, source snapshots, declarations, range approximations, graph edges, validation units, controls, labels, historical installs, reach values, scores, models, rankings, intervals, or metrics. The exclusion does not deny the incident, and it does not turn the unretained predecessor into benign, safe, unchanged, no-known-event, or a control.

## Bounded flatmap-stream package-event screen

The historic `flatmap-stream` package event is independently corroborated but **excluded** from the 17-record primary ledger. npm identifies `flatmap-stream@0.1.1` as the malicious package associated with `event-stream@3.3.6`; Snyk independently records the injected `0.1.1` release timeline; and Microsoft independently identifies `flatmap-stream` as malicious while blocking `0.1.0`, `0.1.1`, and `0.1.2`. [52] [53] [54]

| Eligibility check | Bounded evidence | Strict result |
|---|---|---|
| Exact candidate release | npm and Snyk identify `flatmap-stream@0.1.1`; Microsoft’s mitigation includes that version. | Satisfied for candidate screening. |
| Relatedness | Primary and independent reports connect the package to `event-stream@3.3.6`. | Any future eligible record remains within the existing `event_stream_2018` family; it cannot create a new independent family or validation unit. |
| Official affected-release time | Current bounded registry metadata has no `0.1.1` time-map entry and no `0.1.x` time-map entries. [55] | **Failed.** No official exact event cutoff exists. |
| Exact retained pre-event source object | The response retains only unrelated `0.0.1-security` package metadata; none of the relevant `0.1.x` version objects remains. [55] | **Failed.** No source snapshot can be reconstructed. |

`104_flatmap_stream_candidate_assessment.json` preserves source checksums, the related-family boundary, and the dual registry-retention exception. It adds **zero** ledger records, families, validation units, snapshots, declarations, range approximations, graph edges, controls, labels, historical installs, reach values, scores, models, rankings, intervals, or metrics. The exclusion neither disputes the incident nor converts the missing registry history into a benign, safe, unchanged, no-known-event, or control state.

## Bounded colors and faker related package-event family

The 2022 `colors` and `faker` publications satisfy the frozen admission rule and add two **related** strict ledger records under the single `colors_faker_protestware_2022` family. Snyk identifies the breaking `colors@1.4.1` and `1.4.44-liberty-2` publications plus `faker@6.6.6`; Sonatype independently identifies anomalous colors releases `1.4.1`, `1.4.2`, and `1.4.44-liberty-2`, the faker functional-code purge, and a common maintainer; Russ Cox independently documents intentional sabotage of both packages. [56] [57] [58]

| Record | Official earliest assessed release time | Strict selected source object | Family rule |
|---|---|---|---|
| `colors-2022-01-08` | `colors@1.4.44-liberty-2`, `2022-01-08T04:24:16.448Z` [59] | `colors@1.4.0` | Shares one related family and future validation unit with faker. |
| `faker-2022-01-05` | `faker@6.6.6`, `2022-01-05T01:38:36.409Z` [60] | `faker@5.5.3` | Shares one related family and future validation unit with colors. |

`105_colors_faker_protestware_candidate_assessment.json` records source checksums, exact official cutoffs, and the two strict predecessor selections. The admission adds two records, one family, one future validation unit, and two exact source snapshots, but **zero controls, historical installation traces, reach or blast-radius values, authority comparisons, scores, models, rankings, intervals, or predictive metrics**. Shared-maintainer and coordinated-disruption evidence does not license two independent observations, a campaign-complete census, or a causal claim beyond the bounded source descriptions.

## Bounded Debug September 2025 package-event family

The September 2025 `debug` compromise satisfies the frozen admission rule and adds one strict record under the one `qix_npm_phishing_september_2025` family. The Debug maintainer’s incident issue identifies `debug@4.4.2` among phishing-driven npm-account-compromise releases. Wiz and StepSecurity independently list the same exact affected version and document the compromise context. [65] [66] [67]

| Record | Official affected-release time | Strict selected source object | Family rule |
|---|---|---|---|
| `debug-2025-09-08` | `debug@4.4.2`, `2025-09-08T13:12:39.973Z` [68] | `debug@4.4.1` | One bounded Qix-related family and future validation unit; neither campaign completeness nor statistical independence from unadjudicated packages is inferred. |

`108_debug_september_2025_candidate_assessment.json` records cross-source corroboration, the strict registry cutoff, and the retained predecessor selection. The admission adds one record, one family, one future validation unit, one exact source snapshot, one direct declaration, one isolated range approximation, and one bounded registry-only sensitivity edge. It adds **zero controls, historical installation traces, reach or blast-radius values, authority comparisons, scores, models, rankings, intervals, calibration results, or predictive metrics**.

## Bounded peacenotwar protestware package-event screen

The historic `peacenotwar` incident is independently corroborated but **excluded** from the 16-record primary ledger. Snyk reports that the maintainer published `peacenotwar` on 8 March 2022 before adding it to `node-ipc`; its dedicated advisory marks all `peacenotwar` versions affected. The CNCF TAG Security compromise catalogue independently characterizes the node-ipc/peacenotwar event as malicious-maintainer behavior. [61] [62] [63]

| Eligibility check | Bounded evidence | Strict result |
|---|---|---|
| Finite exact candidate release set | The dedicated Snyk advisory uses an all-versions (`*`) scope; no inspected independent source identifies a finite event-specific `peacenotwar` release set. [61] [62] | **Failed.** An all-version advisory cannot be collapsed into a finite exact target without version-specific evidence. |
| Relatedness | The reports establish a potentially related node-ipc protestware context. [61] [63] | No family or validation unit is created from this excluded candidate. |
| Official registry cutoff | The first retained registry publication is `9.1.1` at `2022-03-08T16:38:45.767Z`. [64] | The strict cutoff is one millisecond earlier. |
| Exact retained pre-event source object | The official registry begins with `9.1.1`; no retained version exists strictly earlier than the cutoff. [64] | **Failed.** No strict source snapshot can be reconstructed. |

`106_peacenotwar_protestware_candidate_assessment.json` preserves source checksums, the all-version advisory boundary, and the first-publication registry exception. It adds **zero** ledger records, campaign families, future validation units, source snapshots, declarations, range approximations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, scores, models, rankings, intervals, or metrics. The exclusion neither disputes the documented behavior nor converts this candidate, an advisory omission, or unavailable pre-event state into benign, safe, unchanged, no-known-event, or a control.

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

GitHub’s public malware-advisory path is similarly a **positive-provenance lead only**. GitHub documents an importer that validates OpenSSF OSV records, preserves upstream records as snapshots, drops entries without usable affected versions, and handles later retractions; its Advisory Database repository documents OSV-formatted advisories, curation, and npm support. [26] [27] Those properties can support future corroboration of an individually adjudicated positive record, but the documentation defines an advisory database rather than a frozen at-risk npm package-version population. It provides no closed-world malicious-publication or maintainer-compromise coverage statement and no paired non-event horizon. Advisory absence remains unknown, not benign; the path creates **zero controls**.

The `npm-follower` archive is a more promising historical-population concept but not an accessible control source. Its project documents real-time archiving of npm metadata and code, including deleted versions, at a stated scale above 20 TB. [28] The linked public `dependencies.science` repository is only static website source and exposes no compact release, filtered export, query API, or row-addressable historical snapshot. [29] More importantly, the archive itself does not supply matched malicious-publication or maintainer-compromise outcome coverage or a non-event horizon. It is therefore excluded under the bounded-access and outcome-contract gates; no data rows or controls were created.

SupplyTGN supplies a useful **benchmark-design reference**, not npm control data. Its preprint documents cutoff-safe feature materialization, leakage audits, explicit 30- and 90-day horizons, and released per-instance predictions, but the disclosed benchmark is constructed from PyPI/OSV component–cutoff instances. [30] Its outcomes are therefore outside the npm malicious-publication and maintainer-compromise target contract. The study may inform future npm pre-registration of horizons and leakage checks, but creates **zero npm rows or controls** and cannot transfer PyPI/OSV performance claims to npm.

The 2026 **Original Sin of npm** study is an npm-specific vulnerability-lifecycle and propagation reference, not a matched compromise-control frame. It reports a 5 September 2023 npm-follower snapshot, random package-name sampling, subsequent live-registry filtering, and a custom 1,077,946-parent-package database combining current/default dependency resolution with OSV/NVD vulnerability information. [31] Its target is disclosed vulnerability propagation rather than closed-world malicious publication or maintainer compromise; its post-sample live filtering means the final population is not a frozen cutoff-valid at-risk denominator; it provides no named downloadable custom-database release or query endpoint; and it specifies no future non-event horizon. The candidate creates **zero controls, labels, model fits, or metrics**. Its discussion of vulnerability introduction, fixing, publication, and right-censoring is retained only as methodology context.

To make a future authorized population study reproducible without pretending that access or outcomes already exist, `90_authorized_npm_control_frame_access_specification.json` now defines a non-executed extraction contract. The documented deps.dev tables can identify a named full snapshot (`Snapshots.Time`) and package-version rows (`PackageVersions.SnapshotAt`, canonical npm identifiers, and `UpstreamPublishedAt`), but the specification explicitly prohibits `Latest` views and advisory absence as historical or non-event evidence. [16] It requires an independent frozen manifest covering malicious publication or maintainer compromise throughout a pre-registered interval, plus exact query text, parameters, deterministic output order, job metadata, and checksums. No authorized query was run; **zero package-version rows, joined outcomes, controls, labels, model fits, or metrics** were created.

| Candidate source | Population property | Outcome-coverage and horizon | Bounded access | Primary-control decision |
|---|---|---|---|---|
| Zenodo NPM Registry Dataset 2025 | Named 20 February 2025 GitHub-repository subset | No paired malicious-publication/compromise coverage or horizon | One 22.3 GB gzip / 108 GB expanded stream | Excluded. |
| deps.dev BigQuery | Snapshot and package-version fields documented | Advisories are vulnerability-oriented; no authenticated access | Google Cloud account and BigQuery API required | Excluded pending both access and target match. |
| Libraries.io public metadata | Current scraped package metadata | No frozen historical outcome contract | Public page, but no documented temporal denominator | Excluded. |
| Guo et al. Figshare detector benchmark | Versioned package/version labels and partial malware timestamps | Retrospective detector corpus; benign list lacks timestamp, cutoff, and horizon | Bounded metadata-only ZIP access works | Excluded as primary temporal control frame. |
| GitHub Advisory Database malware path | OSV positive-advisory provenance and update/retraction handling | No frozen at-risk population, closed-world compromise coverage, or non-event horizon | Public repository and announcement | Excluded as primary temporal control frame. |
| npm-follower archive | Real-time historical npm metadata and code archive, including deleted versions | No matched malicious-publication/compromise coverage or non-event horizon | More than 20 TB; no public filtered export or query path documented | Excluded under bounded-access and outcome-contract gates. |
| SupplyTGN | PyPI/OSV component–cutoff benchmark with explicit horizons and leakage audits | PyPI/OSV vulnerability target, not npm compromise/malicious-publication coverage | Public preprint and described release | Methodology-only; excluded from npm controls. |
| Original Sin of npm | 2023 npm-follower-derived random package-name sample with later live filtering | OSV/NVD vulnerability lifecycle, not closed-world malicious-publication/compromise coverage; no non-event horizon | Paper describes custom database but no row-level release, filtered export, or query endpoint | Methodology-only; excluded from npm controls. |
| Authorized access specification | Future named deps.dev snapshot plus independently frozen external positive-coverage manifest | Explicitly requires target-matched coverage and a pre-registered horizon; neither is currently available | Template only; no BigQuery query or data export executed | Reproducibility contract only; zero controls. |

## What the discovered version-resolved dataset changes—and does not change

CHRONO-RESOLUTION is a public, citable dataset designed for dependency resolution at release points. Its authors report 146,651 npm packages and 245,307,373 npm package-dependency interval relationships, and document that the release includes raw and filtered data, scripts, and query examples. [10] [11] It is the appropriate **next source candidate** for target-version and interval-aware direct-edge reconstruction.

However, its supplied archive is a single 10.2 GB compressed release, while its underlying npm relation table is much larger when imported. It also has an August 2024 registry snapshot date, so it cannot cover the 2026 Axios-family record. The archive was therefore recorded as an acquisition and validation gate, not silently treated as ingested evidence. Before using it, the study must validate package coverage, temporal interval semantics, resolver behavior, and the mapping between the dataset's release-point intervals and each frozen event cutoff. Only after that validation may any resolved-target or transitive graph carry an **approximate/version-resolved** fidelity label distinct from the exact declared-edge fidelity used here.

## Implications for the proposed research contribution

The result narrows a defensible contribution. Rather than claiming that blast radius can currently be forecast from a small current-snapshot feature set, the study can contribute a **leakage-resistant temporal evaluation protocol** and an auditable staged reconstruction pipeline. The pipeline separates: (1) incident adjudication, (2) exact source-version reconstruction, (3) declared direct edges, (4) externally resolved historical dependencies, and only then (5) transitive blast-radius measurement and predictive evaluation.

This boundary is scientifically useful. It prevents a present-day dependency graph or repository workflow feature from being presented as evidence about a prior compromise, and it prevents multiple packages from the same campaign from inflating apparent sample size. A future predictive study should retain this fidelity vocabulary, preserve raw checksums and event-family identifiers, and report results only after its controls, time splits, and historical feature availability have passed the stated gate.

## Current strict-cohort amendment — 26 August 2026

The bounded March 2022 `node-ipc` event is now admitted as a record distinct from the separately adjudicated May 2026 `node-ipc` compromise. GitHub’s reviewed advisory and Snyk’s contemporaneous technical report identify `node-ipc@10.1.1` and `10.1.2` as the finite destructive maintainer publications; NVD records the same affected range. Official registry metadata places the earliest selected affected release at `2022-03-07T11:03:59.179Z`, fixes the strict cutoff at `2022-03-07T11:03:59.178Z`, and selects retained `node-ipc@10.1.0` as the exact source object.[61] [69] [70] [71]

| Governed artifact | Current result | Interpretation boundary |
|---|---:|---|
| Strict package-event ledger | 23 records in 17 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 21 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 69 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 322 edges across 14 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 16 | Related-family safeguards remain mandatory; no split or model was generated. |

The admission adds one family and one future validation unit while preserving **zero controls, benign labels, historical installations, dependency reach values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics**. The no-control/no-model gate remains blocked.

## Lottie Player October 2024 admission — 26 August 2026

The bounded `@lottiefiles/lottie-player` account-takeover screen satisfies the frozen admission rule. LottieFiles’ incident resolution identifies unauthorized versions `2.0.5`, `2.0.6`, and `2.0.7`; Sonatype and Snyk independently identify the same finite release set and the compromised publishing-access context.[72] [73] [74] Official npm registry metadata places the earliest affected release, `2.0.5`, at `2024-10-30T20:12:15.375Z`. The one-millisecond cutoff is `2024-10-30T20:12:15.374Z`, selecting retained `@lottiefiles/lottie-player@2.0.4` as the exact source object.[75]

| Governed artifact | Current result | Interpretation boundary |
|---|---:|---|
| Strict package-event ledger | 24 records in 18 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 22 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 74 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 335 edges across 15 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 17 | Related-family safeguards remain mandatory; no split or model was generated. |

This creates one separate family and future validation unit. It creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. The retained source object is a temporal reconstruction input only; it does not license inferences about current maintainers, repository state, downstream use, or causal impact.

## Nx S1ngularity August 2025 admission — 26 August 2026

The bounded `nx` screen satisfies the frozen admission rule. The Nx postmortem and reviewed GitHub advisory identify eight unauthorized `nx` publications after publishing-token theft; independent Snyk and StepSecurity reports retain the same finite release set.[76] [77] [78] [79] Official npm registry metadata places the earliest affected release, `21.5.0`, at `2025-08-26T22:32:25.482Z`. The one-millisecond cutoff is `2025-08-26T22:32:25.481Z`, and the all-stream time map selects retained `nx@21.5.0-canary.20250826-af44608` rather than a same-branch substitute.[80]

| Governed artifact | Current result | Interpretation boundary |
|---|---:|---|
| Strict package-event ledger | 25 records in 19 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 23 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 109 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 458 edges across 16 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 18 | Related-family safeguards remain mandatory; no split or model was generated. |

This creates one separate family and future validation unit. It creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. The selected canary object is a strict timing result only and does not permit same-branch substitution, installation, reach, causality, or prediction claims.

## Amendment: bounded country-currency-map March 2025 package-hijack admission

Sonatype reported `country-currency-map@2.1.8` as a hijacked malicious release in its March 2025 crypto-package campaign, while contemporaneous BleepingComputer coverage independently names the same deprecated `2.1.8` version. [81] [82] The bounded official npm registry metadata response timestamps `2.1.8` at `2025-03-25T09:03:00.518Z`; strict subtraction yields cutoff `2025-03-25T09:03:00.517Z`, which selects retained `country-currency-map@2.1.7` as the exact pre-event source object. [83]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 26 records in 20 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 24 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 110 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 459 edges across 17 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 19 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded March 2025 family and future validation unit. It creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded html-to-gutenberg May 2026 hijacked-publication admission

GitHub’s reviewed malware advisory identifies `html-to-gutenberg@4.2.11` and `4.2.14`, and JFrog independently identifies the hijacked `4.2.11` release and the May 2026 upload timing; The Hacker News independently corroborates the package-level event and its upload date. [84] [85] [86] The bounded official npm registry metadata response timestamps `4.2.11` at `2026-05-25T19:19:47.408Z`; strict subtraction yields cutoff `2026-05-25T19:19:47.407Z`, which selects retained `html-to-gutenberg@4.2.10` as the exact pre-event source object. [87]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 27 records in 21 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 25 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 124 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 721 edges across 18 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 20 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded May 2026 family and future validation unit. It creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded common-stack generate-plugin May 2026 hijacked-publication admission

Sonatype identifies `@common-stack/generate-plugin@9.0.2-alpha.21` and `9.0.2-alpha.22` as hijacked malicious releases. GitHub’s reviewed malware advisory independently includes the same two versions in its package-specific affected-version set. [88] [89] The strict ledger target is their two-version intersection only: it does not add additional advisory-only releases by inference. Bounded official npm registry metadata timestamps `9.0.2-alpha.21` at `2026-05-21T15:54:08.581Z`; strict subtraction yields cutoff `2026-05-21T15:54:08.580Z`, selecting retained `@common-stack/generate-plugin@9.0.2-alpha.18` as the exact pre-event source object. [90]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 28 records in 22 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 26 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 126 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 760 edges across 19 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 21 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded May 2026 family and future validation unit. It creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality. No relationship to another governed family is asserted.

## Exclusion: bounded sbx-mask March 2026 source-retention screen

Sonatype reports `sbx-mask` as a malicious npm package in a suspected trusted-maintainer-account compromise, while GitHub’s reviewed malware advisory independently identifies the finite affected-version set `1.0.0`, `1.0.1`, and `1.0.2`. [91] [92] Official npm registry metadata timestamps the earliest listed release, `1.0.0`, at `2026-03-19T14:46:00.636Z`; strict subtraction yields cutoff `2026-03-19T14:46:00.635Z`. The current response retains only `0.0.1-security`, which is not before that cutoff, so there is no selected strict pre-event version or retained source object. [93]

| Governing decision | Result | Boundary retained |
|---|---|---|
| Primary ledger admission | Excluded | No retained source object can be substituted or inferred. |
| Cohort totals | Unchanged: 28 records, 22 families, 26 exact snapshots, 126 declarations/approximations, 760 bounded edges, 21 validation units | No new record, family, snapshot, declaration, range selection, or graph edge. |
| Permitted interpretation | Current retention eligibility only | Not evidence of historical installation, downstream reach, current publisher state, benignness, a non-event, or causality. |

This strict exclusion creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. It does not dispute the independently documented incident and does not assert any relationship to another governed family.

## Amendment: bounded Bitwarden CLI April 2026 npm-distribution compromise admission

Bitwarden’s public incident statement identifies malicious npm distribution of `@bitwarden/cli@2026.4.0` during a limited 22 April 2026 window. StepSecurity independently identifies the same exact npm release as compromised, while the NVD-sourced public CVE record corroborates the release and the documented Checkmarx incident context. [94] [95] [96] The bounded official npm registry metadata response timestamps `2026.4.0` at `2026-04-22T21:22:59.021Z`; strict subtraction yields cutoff `2026-04-22T21:22:59.020Z`, selecting retained `@bitwarden/cli@2026.3.0` as the exact pre-event source object. [97]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 29 records in 23 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 27 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 153 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 974 edges across 20 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 22 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded separate family and future validation unit. The documented broader Checkmarx context does **not** expand this row into additional package records, authorize assignment to another governed family, or establish statistical independence. The admission creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded React Native country-select March 2026 malicious-publication admission

StepSecurity and Aikido independently identify `react-native-country-select@0.3.91` as a malicious npm release published on 16 March 2026. [98] [99] The target is limited to their finite exact-version intersection, `0.3.91`; later releases reported only by StepSecurity are not inferred into the row. The bounded official npm registry metadata response timestamps `0.3.91` at `2026-03-16T10:54:18.512Z`; strict subtraction yields cutoff `2026-03-16T10:54:18.511Z`, selecting retained `react-native-country-select@0.3.9` as the exact pre-event source object. [100]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 30 records in 24 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 28 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 153 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 974 edges across 20 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 23 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded family and one future validation unit. The sources’ same-day shared-publisher context with a separately named package does **not** authorize expansion into that package, assignment to an existing governed family, campaign completeness, or statistical independence. The admission creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded rand-user-agent April–May 2025 unauthorized-publication admission

Aikido and BleepingComputer independently identify `rand-user-agent@2.0.83`, `@2.0.84`, and `@1.0.110` as malicious unauthorized npm releases. BleepingComputer records direct developer confirmation of the three unauthorized versions. [101] [102] The governed target is limited to that exact three-version intersection. The bounded official npm registry metadata response timestamps earliest affected `2.0.83` at `2025-04-26T15:25:00.992Z`; strict subtraction yields cutoff `2025-04-26T15:25:00.991Z`, selecting retained `rand-user-agent@2.0.82` as the exact pre-event source object. [103]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 31 records in 25 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 29 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 153 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 974 edges across 20 edge-bearing roots | Not dependency reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 24 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded separate family, one exact source snapshot, and one future validation unit. The retained source object declares no runtime dependencies, so this admission adds no direct declaration, isolated range approximation, or bounded sensitivity edge. The documented unauthorized-publication context does **not** authorize expansion into another package, assignment to an existing governed family, campaign completeness, or statistical independence. The admission creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded Joyfill July 2026 relatedness exclusion

StepSecurity identifies three malicious `@joyfill/components` beta releases, and Socket independently identifies `@joyfill/components@4.0.0-rc24-2773-beta.4`, producing a strict one-version source intersection. [104] [105] Socket explicitly links that release to the ongoing PolinRider supply-chain attack, already represented by the governed `common_stack_generate_plugin_polinrider_hijack_2026` family. [105] This screen is restricted to genuinely separate candidates, so it excludes the Joyfill lead before registry access rather than infer a new family, another package row, an existing-family expansion, campaign completeness, or statistical independence.

| Governed quantity after exclusion | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | Unchanged: 31 records in 25 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | Unchanged: 29 | No registry request or source-object selection occurred. |
| Direct declarations and isolated SemVer approximations | Unchanged: 153 each | No dependency data was acquired. |
| Depth-three registry-only sensitivity graph | Unchanged: 974 edges across 20 edge-bearing roots | No reach, centrality, blast-radius, or predictive interpretation. |
| Future validation units | Unchanged: 24 | No independent unit was created. |

This exclusion creates **zero** ledger records, families, validation units, source snapshots, declarations, range approximations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. It does not dispute the reported malicious version or establish a complete campaign, current publisher state, downstream exposure, causal effect, or statistical-independence conclusion.

## Amendment: bounded AsyncAPI generator July 2026 GitHub Actions release-pipeline-compromise admission

Aikido and Microsoft Security independently identify `@asyncapi/generator@3.3.1` as an affected AsyncAPI npm release.[106] [107] The target is limited to their exact one-version intersection; other AsyncAPI packages in the reports are not inferred into this row. The bounded official npm registry metadata response timestamps `3.3.1` at `2026-07-14T07:10:48.853Z`; strict subtraction yields cutoff `2026-07-14T07:10:48.852Z`, selecting retained `@asyncapi/generator@3.3.0` as the exact pre-event source object.[108]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 32 records in 26 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 30 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 179 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 1,408 edges across 21 edge-bearing roots | Bounded descriptor only; not reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 25 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded separate family, one exact source snapshot, 26 direct declarations, 26 isolated range approximations, 434 bounded sensitivity edges, and one future validation unit. The bounded graph retains two unresolved edges and one capped root; neither condition is interpreted as installation, reach, completeness, or exposure. Reported Miasma-branding and `prt-scan` overlap and unresolved attribution do **not** establish a relationship to an existing governed family, campaign completeness, causality, or statistical independence. The admission creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

## Amendment: bounded dYdX v4 client January–February 2026 cross-ecosystem malicious-publication admission

Socket and The Hacker News independently identify `@dydxprotocol/v4-client-js@3.4.1`, `@1.22.1`, `@1.15.2`, and `@1.0.31` as compromised npm releases.[109] [110] The target is limited to that exact four-version intersection; the reported PyPI release, all other npm versions, and the earlier dYdX-related incident are not inferred into this row. The bounded official npm registry metadata response timestamps earliest affected `1.0.31` at `2026-01-27T13:22:18.888Z`; strict subtraction yields cutoff `2026-01-27T13:22:18.887Z`, selecting retained `@dydxprotocol/v4-client-js@3.4.0` as the exact pre-event source object.[111]

| Governed quantity after admission | Value | Boundary retained |
|---|---:|---|
| Strict package-event ledger | 33 records in 27 families | Positive evidence only; not a control frame. |
| Exact retained pre-event snapshots | 31 | Two label-only exceptions remain. |
| Direct declarations and isolated SemVer approximations | 200 each | Declarations and cutoff-valid approximations, not installations or locks. |
| Depth-three registry-only sensitivity graph | 1,553 edges across 22 edge-bearing roots | Bounded descriptor only; not reach, centrality, blast radius, or a predictive feature set. |
| Future validation units | 26 | Related-family safeguards remain mandatory; no split or model was generated. |

This adds one bounded separate family, one exact source snapshot, 21 direct declarations, 21 isolated range approximations, 145 bounded sensitivity edges, and one future validation unit. The preserved graph-wide two unresolved edges and one capped root do not establish installation, reach, exposure, or completeness. The reports characterize the maintainer-compromise attribution as unconfirmed; neither that characterization, the cross-ecosystem context, nor a reference to a prior dYdX-related event establishes a relationship to an existing governed family, campaign completeness, causality, or statistical independence. The admission creates **zero** controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, model fits, or predictive metrics. Registry metadata establishes time-map selection and retained-object availability only; it is not evidence of historical installation, downstream reach, current maintainer state, or causality.

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

[26] [GitHub Blog, “How we took malware advisories beyond npm,” 6 August 2026](https://github.blog/security/supply-chain-security/how-we-took-malware-advisories-beyond-npm/).

[27] [GitHub, “GitHub Advisory Database” repository documentation](https://github.com/github/advisory-database).

[28] [D. Pinckney et al., “npm-follower: A Complete Dataset Tracking the NPM Ecosystem,” project publication page, 2023](https://donaldpinckney.com/publication/npm-follower/).

[29] [D. Pinckney, `dependencies.science` repository](https://github.com/donald-pinckney/dependencies.science).

[30] [T. P. Tran Truong, S. Ha, and X.-B. Le, “SupplyTGN: A Reproducible Leakage-Safe Benchmark for Temporal Software Supply-Chain Risk,” SSRN preprint, 2026](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7194447).

[31] [M. Robinson et al., “Original Sin of npm: A Study on Vulnerability Propagation in JavaScript Dependency Networks,” ASIA CCS 2026 / arXiv:2604.17668v1, 19 April 2026](https://arxiv.org/html/2604.17668v1).

[32] [OpenSSF Malicious Packages, “MAL-2025-6020: Malicious code in is (npm),” frozen at commit `063a778`](https://github.com/ossf/malicious-packages/blob/063a778886548231828c8e476eecdb5c5c04fbcb/osv/malicious/npm/is/MAL-2025-6020.json).

[33] [StepSecurity, “Another npm Supply Chain Attack: The 'is' Package Compromise,” 22 July 2025](https://www.stepsecurity.io/blog/another-npm-supply-chain-attack-the-is-package-compromise).

[34] [enricomarino/is, “v3.3.2” remediation commit `0fe137a`](https://github.com/enricomarino/is/commit/0fe137a5946e4ecb0e649bd7dea48d5415a242fc).

[35] [OpenSSF Malicious Packages, “MAL-2026-11524: Malicious code in keyv (npm),” frozen at commit `88b1340754`](https://github.com/ossf/malicious-packages/blob/88b1340754c17c3d9ae43642c9b2de22b1bbfc10/osv/malicious/npm/keyv/MAL-2026-11524.json).

[36] [Wiz Research IOCs, frozen `keyv-packages.csv` at commit `22752e7`](https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/keyv-packages.csv).

[37] [Wiz Research, “keyv and cacheable npm Package Hijacked in Supply Chain Attack,” 4 August 2026](https://www.wiz.io/blog/keyv-and-cacheable-npm-supply-chain-attack).

[38] [Snyk, “Inside the keyv npm Compromise: preinstall Malware, Trusted Provenance, and IDE Hooks,” 4 August 2026](https://snyk.io/blog/inside-keyv-npm-compromise-preinstall-malware-trusted-provenance-ide-hooks/).

[39] [scikit-learn, “GroupKFold” documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html).

[40] [scikit-learn, “GroupShuffleSplit” documentation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupShuffleSplit.html).

[41] [scikit-learn, “Cross-validation: evaluating estimator performance”](https://scikit-learn.org/stable/modules/cross_validation.html).

[42] [I. Santos-Grueiro, “On Good Authority: Release-Authority Measurement for Registry-Mediated Package Ecosystems,” arXiv:2606.22593, 2026](https://arxiv.org/abs/2606.22593).

[43] [npm Docs, “Generating provenance statements”](https://docs.npmjs.com/generating-provenance-statements).

[44] [Open Source Insights, “Introducing npm package SLSA provenance support”](https://blog.deps.dev/npm-provenance/).

[45] [npm Docs, “Generating provenance statements”](https://docs.npmjs.com/generating-provenance-statements).

[46] [npm, “npm Registry API”](https://api-docs.npmjs.com/).

[47] [GitHub, “Introducing npm package provenance”](https://github.blog/security/supply-chain-security/introducing-npm-package-provenance/).

[48] [npm, “crossenv malware on the npm registry,” 2 August 2017](https://blog.npmjs.org/post/163723642530/crossenv-malware-on-the-npm-registry).

[49] [Ivan Akulov, “Malicious packages in npm. Here’s what to do,” 2 August 2017](https://iamakulov.com/notes/npm-malicious-packages/).

[50] [Snyk Vulnerability Database, “Malicious Package Affecting crossenv package,” `npm:crossenv:20170802`](https://security.snyk.io/vuln/npm:crossenv:20170802).

[51] [npm registry metadata, `crossenv`](https://registry.npmjs.org/crossenv).

[52] [npm, “Details about the event-stream incident,” 27 November 2018](https://blog.npmjs.org/post/180565383195/details-about-the-event-stream-incident).

[53] [Snyk, “A post-mortem of the malicious event-stream backdoor,” 6 December 2018](https://snyk.io/blog/a-post-mortem-of-the-malicious-event-stream-backdoor/).

[54] [Microsoft Azure DevOps Blog, “Blocking malicious versions of event-stream and flatmap-stream packages,” 28 November 2018](https://devblogs.microsoft.com/devops/blocking-malicious-versions-of-event-stream-and-flatmap-stream-packages/).

[55] [npm registry metadata, `flatmap-stream`](https://registry.npmjs.org/flatmap-stream).

[56] [Snyk, “Open source maintainer pulls the plug on npm packages colors and faker, now what?”, 9 January 2022](https://snyk.io/blog/open-source-npm-packages-colors-faker/).

[57] [Sonatype, “npm Libraries ‘colors’ and ‘faker’ Sabotaged in Protest by Their Maintainer,” 10 January 2022](https://www.sonatype.com/blog/npm-libraries-colors-and-faker-sabotaged-in-protest-by-their-maintainer-what-to-do-now).

[58] [Russ Cox, “What NPM Should Do Today To Stop A New Colors Attack Tomorrow,” 10 January 2022](https://research.swtch.com/npm-colors).

[59] [npm registry metadata, `colors`](https://registry.npmjs.org/colors).
[60] [npm registry metadata, `faker`](https://registry.npmjs.org/faker).
[61] [Snyk, “Malicious npm package peacenotwar had a destructive payload,” 16 March 2022](https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/).
[62] [Snyk vulnerability database, `SNYK-JS-PEACENOTWAR-2426724`](https://security.snyk.io/vuln/SNYK-JS-PEACENOTWAR-2426724).
[63] [CNCF TAG Security, “node-ipc/peacenotwar” compromise catalogue](https://tag-security.cncf.io/community/catalog/compromises/2022/node-ipc-peacenotwar/).
[64] [npm registry metadata, `peacenotwar`](https://registry.npmjs.org/peacenotwar).
[65] [Debug project, “Version 4.4.2 published to npm is compromised,” Issue #1005, 8 September 2025](https://github.com/debug-js/debug/issues/1005).
[66] [Wiz, “Widespread npm Supply Chain Attack: Breaking Down Impact & Scope Across Debug, Chalk, and Beyond,” 9 September 2025](https://www.wiz.io/blog/widespread-npm-supply-chain-attack-breaking-down-impact-scope-across-debug-chalk).
[67] [StepSecurity, “20+ Popular NPM Packages Compromised,” 8 September 2025](https://www.stepsecurity.io/blog/20-popular-npm-packages-compromised-chalk-debug-strip-ansi-color-convert-wrap-ansi).
[68] [npm registry metadata, `debug`](https://registry.npmjs.org/debug).

[69] [GitHub Advisory Database, “Embedded Malicious Code in node-ipc,” GHSA-97m3-w2cp-4xx6](https://github.com/advisories/GHSA-97m3-w2cp-4xx6).

[70] [NVD, “CVE-2022-23812 Detail”](https://nvd.nist.gov/vuln/detail/CVE-2022-23812).

[71] [npm registry metadata, `node-ipc`](https://registry.npmjs.org/node-ipc).

[72] [LottieFiles, “Resolution of Security Incident with @lottiefiles/lottie-player Package,” 2 November 2024](https://lottiefiles.com/blog/inside-lottiefiles/resolution-of-security-incident-with-lottiefiles-lottie-player-package).

[73] [Sonatype, “Lottie Player Compromised in Supply Chain Attack,” 31 October 2024](https://www.sonatype.com/blog/lottie-player-compromised-in-supply-chain-attack-all-you-need-to-know).

[74] [Snyk, “Lottie Player npm package compromised for crypto wallet theft,” 31 October 2024](https://snyk.io/blog/lottie-player-npm-package-compromised-crypto-wallet-theft/).

[75] [npm registry metadata, `@lottiefiles/lottie-player`](https://registry.npmjs.org/%40lottiefiles%2Flottie-player).

[76] [Nx, “S1ngularity - What Happened, How We Responded, What We Learned,” 5 September 2025](https://nx.dev/blog/s1ngularity-postmortem).

[77] [GitHub Security Advisory, “Malicious versions of Nx and some supporting plugins were published,” GHSA-cxm3-wv7p-598c](https://github.com/nrwl/nx/security/advisories/GHSA-cxm3-wv7p-598c).

[78] [Snyk, “Weaponizing AI Coding Agents for Malware in the Nx Malicious Package Security Incident,” 27 August 2025](https://snyk.io/blog/weaponizing-ai-coding-agents-for-malware-in-the-nx-malicious-package/).

[79] [StepSecurity, “s1ngularity: Popular Nx Build System Package Compromised with Data-Stealing Malware,” 27 August 2025](https://www.stepsecurity.io/blog/supply-chain-security-alert-popular-nx-build-system-package-compromised-with-data-stealing-malware).

[80] [npm registry metadata, `nx`](https://registry.npmjs.org/nx).

[81] [Sonatype, “Multiple Crypto Packages Hijacked, Turned Into Info-Stealers,” 27 March 2025](https://www.sonatype.com/blog/multiple-crypto-packages-hijacked-turned-into-info-stealers).

[82] [BleepingComputer, “Infostealer campaign compromises 10 npm packages, targets devs,” 27 March 2025](https://www.bleepingcomputer.com/news/security/infostealer-campaign-compromises-10-npm-packages-targets-devs/).

[83] [npm registry metadata, `country-currency-map`](https://registry.npmjs.org/country-currency-map).

[84] [GitHub Advisory Database, “Malware in html-to-gutenberg,” GHSA-2gqj-wrf5-35w8](https://github.com/advisories/GHSA-2gqj-wrf5-35w8).

[85] [JFrog Security Research, “Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops to Deploy a Credential/Crypto Stealer,” 24 June 2026](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/).

[86] [The Hacker News, “Hijacked npm and Go Packages Use VS Code Tasks to Deploy Python Infostealer,” 29 June 2026](https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html).

[87] [npm registry metadata, `html-to-gutenberg`](https://registry.npmjs.org/html-to-gutenberg).

[88] [Sonatype, “Hijacked npm Package Attempts to Deliver PolinRider-Linked RAT,” 21 May 2026](https://www.sonatype.com/blog/hijacked-npm-package-attempts-to-deliver-polinrider-linked-rat).

[89] [GitHub Advisory Database, “Malware in @common-stack/generate-plugin,” GHSA-6p55-6hvr-3xmg](https://github.com/advisories/GHSA-6p55-6hvr-3xmg).

[90] [npm registry metadata, `@common-stack/generate-plugin`](https://registry.npmjs.org/%40common-stack%2Fgenerate-plugin).

[91] [Sonatype, “Sonatype Discovers Two Malicious npm Packages,” 19 March 2026](https://www.sonatype.com/blog/sonatype-discovers-two-malicious-npm-packages).

[92] [GitHub Advisory Database, “Malware in sbx-mask,” GHSA-r934-qgg3-v7fg](https://github.com/advisories/GHSA-r934-qgg3-v7fg).

[93] [npm registry metadata, `sbx-mask`](https://registry.npmjs.org/sbx-mask).

[94] [Bitwarden, “Bitwarden Statement on Checkmarx Supply Chain Incident,” 23 April 2026](https://community.bitwarden.com/t/bitwarden-statement-on-checkmarx-supply-chain-incident/96127).

[95] [StepSecurity, “Bitwarden CLI Hijacked on npm,” 23 April 2026](https://www.stepsecurity.io/blog/bitwarden-cli-hijacked-on-npm-bun-staged-credential-stealer-targets-developers-github-actions-and-ai-tools).

[96] [GitHub Advisory Database, CVE-2026-42994](https://github.com/advisories/GHSA-999x-2wm3-jfx8).

[97] [npm registry metadata, `@bitwarden/cli`](https://registry.npmjs.org/%40bitwarden%2Fcli).

[98] [StepSecurity, “Malicious npm Releases Found in Popular React Native Packages,” 16 March 2026](https://www.stepsecurity.io/blog/malicious-npm-releases-found-in-popular-react-native-packages---130k-monthly-downloads-compromised).

[99] [Aikido, “Glassworm Strikes Popular React Native Phone Number Packages,” 18 March 2026](https://www.aikido.dev/blog/glassworm-strikes-react-packages-phone-numbers).

[100] [npm registry metadata, `react-native-country-select`](https://registry.npmjs.org/react-native-country-select).

[101] [Aikido, “RATatouille: A Malicious Recipe Hidden in rand-user-agent,” 6 May 2025](https://www.aikido.dev/blog/catching-a-rat-remote-access-trojian-rand-user-agent-supply-chain-compromise).

[102] [BleepingComputer, “Supply chain attack hits npm package with 45,000 weekly downloads,” 8 May 2025](https://www.bleepingcomputer.com/news/security/supply-chain-attack-hits-npm-package-with-45-000-weekly-downloads/).

[103] [npm registry metadata, `rand-user-agent`](https://registry.npmjs.org/rand-user-agent).

[104] [StepSecurity, “Compromised npm Packages: @joyfill/components and @joyfill/layouts Ship an Obfuscated Remote Access Trojan,” 28 July 2026](https://www.stepsecurity.io/blog/joyfill-npm-supply-chain-compromise).

[105] [Socket, “Two Joyfill npm Beta Releases Compromised to Deliver DEV#POPPER Remote Access Trojan,” 28 July 2026](https://socket.dev/blog/joyfill-npm-beta-releases-compromised).

[106] [Aikido, “AsyncAPI npm packages backdoored via GitHub Actions,” 14 July 2026](https://www.aikido.dev/blog/asyncapi-npm-packages-backdoored-via-github-actions).

[107] [Microsoft Security, “Unpacking the AsyncAPI npm supply chain compromise and import-time payload delivery,” 15 July 2026](https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/).

[108] [npm registry metadata, `@asyncapi/generator`](https://registry.npmjs.org/%40asyncapi%2Fgenerator).

[109] [Socket, “Malicious dYdX Packages Published to npm and PyPI After Maintainer Compromise,” 6 February 2026](https://socket.dev/blog/malicious-dydx-packages-published-to-npm-and-pypi).

[110] [The Hacker News, “Compromised dYdX npm and PyPI Packages Deliver Wallet Stealers and RAT Malware,” 6 February 2026](https://thehackernews.com/2026/02/compromised-dydx-npm-and-pypi-packages.html).

[111] [npm registry metadata, `@dydxprotocol/v4-client-js`](https://registry.npmjs.org/%40dydxprotocol%2Fv4-client-js).

## Bounded dYdX Solo September 2022 npm account-compromise admission

GitHub’s reviewed advisory and BleepingComputer independently converge on `@dydxprotocol/solo@0.41.1` and `0.41.2`.[112] [113] Official registry metadata fixes the earliest release at `2022-09-23T10:39:42.987Z`; the strict cutoff selects retained `0.41.0`.[114] This bounded addition brings the cohort to **34 records, 28 families, 32 snapshots, 211 declarations and approximations, 1,643 sensitivity edges, and 27 validation units**. No companion packages, relatedness, independence, controls, installations, reach, blast-radius values, scores, models, calibration, ranking, intervals, or predictive metrics are created.

[112] [GitHub Advisory Database, “Malware in @dydxprotocol/solo”](https://github.com/advisories/GHSA-xjr5-5w2w-3233).
[113] [BleepingComputer, “npm packages used by crypto exchanges compromised”](https://www.bleepingcomputer.com/news/security/npm-packages-used-by-crypto-exchanges-compromised/).
[114] [npm registry metadata, `@dydxprotocol/solo`](https://registry.npmjs.org/%40dydxprotocol%2Fsolo).
