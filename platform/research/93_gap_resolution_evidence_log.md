# Gap-Resolution Evidence Log

## Scope and decision rule

This log records the evidence used to decide which research gaps can support a defensible contribution. It distinguishes **repository-supported descriptive evidence**, **externally documented prior work**, and **new analyses**. No entry should be interpreted as evidence that a predictive model already works unless it has a dated feature cutoff, an independently documented later outcome, an evaluation protocol, and reproducible output artifacts.

## Inventory checkpoint — 2026-08-20

The repository supplies a real, deterministic npm ecosystem snapshot containing 25,228 package metrics, dependency and maintainer structure, mapped public repositories, workflow-directory observations, and an archive-backed chart summary. It therefore supports present-tense descriptive structural analysis. It does **not** yet contain a temporal snapshot builder, an adjudicated multi-incident label set, a baseline runner, a leakage-controlled evaluation, or a graph-learning implementation. Consequently, its current “blast radius,” “wormability,” and weighted ranking are defensible as structural feature candidates rather than validated compromise forecasts.

| Gap | Current status | Evidence needed to resolve it | Research priority |
|---|---|---|---|
| Pre-incident prioritization | Plausible but unvalidated | Dated pre-event snapshots, later documented incident outcomes, rank baselines, uncertainty | High |
| CI/CD exposure linkage | Binary workflow-directory proxy only | Parsed public workflow security features, missingness ledger, conservative interpretation | High |
| Structural leverage versus compromise likelihood | Concepts conflated by the historic “ROI” name | Separate targets and decision uses; calibration and stratified analyses | High |
| Temporal validity | Protocol exists; historical data pipeline absent | Feature-availability ledger and strict/reconstructed fidelity regimes | Critical |
| HGAT incremental value | Architecture proposed; no experiment | Matched baselines, ablations, time-based evaluation, compute accounting | Medium, conditional |
| Incident-label quality | Protocol exists; broad evaluated label set absent | Reviewable version-level incident registry with confidence and source dates | Critical |

## Preliminary contribution decision

The most defensible primary contribution is a **time-aware, reproducible defensive prioritization benchmark** rather than an assertion that an HGAT forecasts attacker return on investment. Its novel component, if supported after related-work review, is the explicit separation of (a) structural dependency and maintainer leverage, (b) narrowly defined public CI/CD observability, and (c) future documented compromise labels under information-availability constraints. The graph model remains a secondary, falsifiable comparison rather than the claimed result.

## Operational notes

The managed production deployment packaging mismatch was repaired and a successful managed deployment is now available at `https://supplyhub-mfhdnapy.manus.space`. This operational event is not research evidence; it is recorded so that subsequent research artifacts can be surfaced in the platform after scholarly review.

## Related-work checkpoint A — structural risk, weak links, labels, and release authority

| Source | What it establishes | Consequence for this project |
|---|---|---|
| Zimmermann et al. (2019) | Dependency topology and maintainer concentration can create ecosystem-wide single points of failure. | Dependency reach and maintainer control are credible baseline features, not sufficient novelty. |
| Zahan et al. (2022) | Large-scale npm metadata can identify several proactive weak-link signals, including install scripts, inactive ownership, and expired maintainer domains. | A structural model must compare against hygiene and account-risk signals; it cannot claim the first proactive npm prioritization task. |
| Ohm et al. (2020) | Manually collected malicious-package records across registries can support defensive research, but the dataset concerns documented attacks rather than an automatic “ground truth.” | Version- and campaign-aware adjudication is feasible and necessary for labels. |
| Santos-Grueiro (2026) | Public release-authority discontinuities form a practical pre-payload review queue, but the study explicitly reports zero overlap with exact malicious versions in its cohort. | Release-authority change is a complementary review surface, not a substitute for compromise prediction; the present study must not merge the two targets. |

The current closest-new-work collision is **release-authority measurement**. It strengthens rather than eliminates the project’s remaining opportunity: a defensible study must focus on the *decision relationship* among stable structural leverage, public CI/CD observability, and release-path discontinuity under fixed historical cutoffs. It should report distinct queues and their overlap, not promise a single universal score.

### Sources retained

1. Zimmermann et al., *Small World with High Risks*, 2019: <https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman>.
2. Zahan et al., *What are Weak Links in the npm Supply Chain?*, 2022: <https://arxiv.org/abs/2112.10165>.
3. Ohm et al., *Backstabber’s Knife Collection*, 2020: <https://arxiv.org/abs/2005.09535>.
4. Santos-Grueiro, *On Good Authority*, 2026: <https://arxiv.org/abs/2606.22593>.

## Related-work checkpoint B — public CI/CD observability

Public workflow files are a meaningful but bounded source of evidence. Koishybayev et al. characterize CI/CD as privileged code that can access secrets and infrastructure; their large-scale measurements show prevalent overprivilege and widespread third-party action use. ARGUS further demonstrates that workflow and action code can contain security-relevant injection paths that simple pattern checks miss. GitHub’s own secure-use guidance identifies least-privilege token permissions, risky privileged triggers, immutable action pinning, environment review gates, OIDC, and self-hosted runners as operationally relevant controls. [5][6][7]

This evidence changes the research design in three ways. First, replace the binary `has_workflows` proxy with *publicly observable configuration families* rather than an inferred infrastructure-privilege score. Second, preserve `unknown` when a repository is private, unlinked, absent, or historically unavailable; do not treat missing public YAML as evidence of lower operational risk. Third, treat configuration state as time-varying: a large longitudinal workflow study reports frequent small changes, which makes a current workflow snapshot unsuitable for strict historical claims without commit-level reconstruction. [8]

| Publicly observable feature | Conservative interpretation | Not observable from public workflow YAML alone |
|---|---|---|
| `permissions` declaration and write scopes | Declared token-permission configuration | Actual run-time token use or organization defaults not encoded in the file |
| `pull_request_target`, `workflow_run`, and checkout patterns | Potential privileged-trigger review surface | Whether an untrusted pull request is actually processed in a vulnerable path |
| Third-party action references and full-SHA pins | Dependency immutability and action-sourcing posture | Whether a pinned revision is benign or a reviewed action is safe |
| `id-token: write`, environment use, deployment steps | Public indication of cloud/deployment-oriented configuration | Actual cloud role scope, secrets, account permissions, or business impact |
| `runs-on` and self-hosted labels | Public indication of runner configuration | Runner isolation, network access, co-tenancy, or host-resident credentials |
| Workflow creation/change history | Configuration churn and historical availability | Semantic intent or successful execution outcomes |

### Sources retained

5. Koishybayev et al., *Characterizing the Security of GitHub CI Workflows*, 2022: <https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev>.
6. Muralee et al., *ARGUS*, 2023: <https://www.usenix.org/conference/usenixsecurity23/presentation/muralee>.
7. GitHub, *Secure use reference*: <https://docs.github.com/en/actions/reference/security/secure-use>.
8. Rostami Mazrae et al., *An Empirical Study of the Evolution of GitHub Actions Workflows*, 2026: <https://arxiv.org/html/2602.14572v3>.

Browser verification on 2026-08-20 confirmed the official GitHub guidance on least-privilege tokens, OIDC, and self-hosted-runner limitations, and the USENIX study’s four CI/CD security properties and large-scale workflow findings. These sources support feature *definitions* and defensive interpretations; they do not supply package-compromise labels or establish causal exposure.

## Related-work checkpoint C — temporal labels and evaluation boundaries

Existing research confirms that dependency exposure can be measured over time, and that public advisory data can provide affected-version information. Zerouali et al. analyze when vulnerabilities are disclosed and fixed and distinguish package dependents from external GitHub projects. OSV similarly aggregates adopted vulnerability databases and supports affected-version representation. Neither source makes a keyword-derived advisory stream a complete or temporally clean compromise label set. [9][10]

The recent NPM malicious-package benchmark is a valuable **payload-detection** comparator: it curates malicious and benign package versions and evaluates code, metadata, dynamic, ML, and LLM detectors. Its central task is distinguishing malicious package content from benign content, often after package acquisition or removal. That task should remain explicitly separate from this project’s proposed **pre-incident defensive prioritization** task. The studies may share confirmed version-level incident records, but they should not share labels without a source-time and event-time audit. [11]

SynthChain reinforces the methodological point that no single telemetry source reconstructs an entire compromise chain. It is useful as an observability caution and a reproducible runtime-defense resource, but it is not a population-level npm package-ranking benchmark. [12]

| Evidence source | Appropriate use in the proposed work | Inappropriate use |
|---|---|---|
| OSV and advisory feeds | Candidate discovery, affected-version checks, source URLs, publication timestamps | Automatic “confirmed compromise” labels or pre-cutoff predictive features without review |
| Malicious-package benchmark | Compare scope with payload-detection literature; discover reviewed package/version candidates | Claim that a structural score detects malicious code or reproduce its headline metrics |
| Dependency-vulnerability propagation study | Define version-aware exposure and remediation baseline analyses | Infer intentional attack likelihood from ordinary vulnerabilities |
| Runtime attack testbed | State observability limits and future multi-source evaluation directions | Substitute for npm registry population or historical package labels |

### Sources retained

9. Zerouali et al., *On the Impact of Security Vulnerabilities in the npm and RubyGems Dependency Networks*, 2022: <https://link.springer.com/article/10.1007/s10664-022-10154-1>.
10. OSV, *Introduction to OSV*: <https://google.github.io/osv.dev/>.
11. Guo et al., *Understanding NPM Malicious Package Detection*, 2026: <https://arxiv.org/html/2603.27549v1>.
12. Tan et al., *SynthChain*, 2026: <https://arxiv.org/abs/2603.16694>.

Browser verification on 2026-08-20 confirmed the two most consequential novelty boundaries: the 2026 malicious-package benchmark evaluates package-content detection, whereas the release-authority paper constructs a public control-plane discontinuity queue and explicitly reports no overlap with exact malicious versions in its cohort. The proposed contribution must therefore evaluate related but separate defensive queues, rather than claiming one score predicts both control-plane change and malicious payloads.

## Related-work checkpoint D — historical dependency resolution

Browser review of **CHRONO-RESOLUTION** confirmed that it provides resolution-at-release-point data for npm, PyPI, and crates.io, enriched with OSV vulnerability data. This substantially reduces the novelty of merely reconstructing historical dependency graphs and creates an opportunity to make the project’s evaluation more reproducible. The contribution should use or compare against this artifact where its release-point sampling meets the required observation dates, then add what it does not provide: maintainer-structure history, public workflow configuration history, adjudicated compromise-event labels, cross-family leakage controls, and decision-oriented ranking evaluation. [13]

### Source retained

13. Rahman et al., *CHRONO-RESOLUTION*, 2026: <https://arxiv.org/abs/2607.15315>.

## Authoritative incident-evidence checkpoint

CISA’s 2025 Shai-Hulud alert establishes a high-impact credential-theft and automated npm-republication campaign affecting more than 500 packages; CERT/CC preserves the campaign’s disclosure chronology, propagation mechanism, and references to evolving affected-version lists. CISA’s 2026 Axios alert identifies a specific event date (31 March 2026), two affected Axios versions (`1.14.1` and `0.30.4`), and the injected dependency `plain-crypto-js@4.2.1`. [14][15][16]

These incidents support a **seed label registry**, not a finished prediction benchmark. The Axios record supplies a package and version but public feature cutoffs must precede the event; Shai-Hulud supplies campaign confirmation but its scope evolved, so package/version inclusion must point to an archived affected-version source and record retrieval date. Both incidents demonstrate that credential compromise and CI/CD context matter, but neither proves that public workflow configuration or network centrality predicts compromise.

| Incident family | Event timing usable for labels | Inclusion level | Labeling caution |
|---|---|---|---|
| Shai-Hulud | Public disclosures beginning 15 September 2025; CISA alert 23 September 2025 | Campaign confirmed; package/version membership requires a dated corroborating list | Do not assign every mentioned package an identical event timestamp or causal role |
| Axios | Malicious versions published 31 March 2026; CISA alert 20 April 2026 | Version-specific: `axios@1.14.1`, `axios@0.30.4`, and injected `plain-crypto-js@4.2.1` | Distinguish the compromised publisher target from a malicious transitive dependency and downstream exposure |

### Sources retained

14. CISA, *Widespread Supply Chain Compromise Impacting npm Ecosystem*, 2025: <https://www.cisa.gov/news-events/alerts/2025/09/23/widespread-supply-chain-compromise-impacting-npm-ecosystem>.
15. CISA, *Supply Chain Compromise Impacts Axios Node Package Manager*, 2026: <https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager>.
16. CERT/CC, *VU#534320*, 2025: <https://kb.cert.org/vuls/id/534320>.

## Temporal reconstruction checkpoint — 2026-08-24

The temporal reconstruction work located the public CHRONO-RESOLUTION release by Rahman, Marley, Paramitha, and Williams (Zenodo DOI: 10.5281/zenodo.17576373). The accompanying paper reports that the npm relations table records release-point dependency intervals, including resolved dependency versions and the highest available dependency versions. It also documents a public archive containing the raw and filtered datasets, construction scripts, and example queries. The dataset is therefore a high-value candidate source for a future **version-resolved** reconstruction stage. [13][17]

The release was not misrepresented as already ingested. Its single compressed archive is 10.2 GB, the paper reports 245,307,373 npm package-dependency interval relationships, and its registry snapshot is dated August 2024. Accordingly, it cannot cover the 2026 Axios family and must be selectively acquired and validated before use. The completed current artifact remains limited to exact, cutoff-valid source version declarations from official npm registry metadata; target-version resolution and transitive reach remain explicitly unavailable.

| Evidence item | Provenance | Use permitted now | Use not permitted now |
|---|---|---|---|
| npm package metadata and version-time maps | Official `registry.npmjs.org/<package>` response, SHA-256 recorded in `65_package_temporal_companion_diagnostics.json` | Select strict pre-event source versions and retain their declared direct dependencies | Infer which dependency version a historical install selected or any transitive reach |
| CHRONO-RESOLUTION paper | arXiv:2607.15315 | Document the availability and intended semantics of release-point resolution | Treat reported aggregate coverage as event-specific graph evidence |
| CHRONO-RESOLUTION release | Zenodo DOI 10.5281/zenodo.17576373 | Plan a source-acquisition and validation gate | Claim the archive has been queried, merged, or validated for the pilot |

### Source retained

17. Rahman et al., *CHRONO-RESOLUTION* data release, Zenodo DOI 10.5281/zenodo.17576373: <https://doi.org/10.5281/zenodo.17576373>.

## Isolated range-resolution checkpoint — 2026-08-24

The direct-declaration ledger was extended with a strictly limited target-version approximation. For each of its 20 direct runtime dependency ranges, the maintained `semver` implementation selected the highest non-prerelease target version that both satisfied the recorded range and carried an official registry timestamp at or before that row's cutoff. All 20 direct ranges produced a target approximation; no target was selected after its cutoff. [18]

This result is not represented as a reconstructed historical installation. It is an **isolated cutoff-valid SemVer approximation** and excludes package-lock state, package-manager-version behavior, peer, optional, bundled, workspace, override, nested, cache, and transitive-resolution semantics. The diagnostic stores zero transitive-reach values and keeps model ranking, calibration, and blast-radius inference blocked.

18. npm, *node-semver* reference implementation: <https://github.com/npm/node-semver>.

## Selective resolver-archive validation — 2026-08-24

The official CHRONO-RESOLUTION ZIP64 central directory was inspected with a 65,557-byte HTTP range request, and no data-member payload was downloaded. The inventory confirms that the archive has only four members and that its sole relation-data member, `data-relations.sql`, is 10,228,591,413 bytes compressed and 138,731,381,476 bytes uncompressed. It is therefore not a package-selectable or streaming-friendly public source for the current constrained worktree. [17]

A separate 1,508-byte range was used solely to extract and validate `schema-relations.sql` (SHA-256 `57db2833e311390250d1d292247f89573bd320917c4c301b44acb32839294c69`). The schema confirms direct relation fields for package and dependency versions plus interval start/end, supporting the conclusion that the dataset is semantically relevant for future interval-aware resolution. No relations rows were ingested, no historical resolver outputs were attributed to the pilot, and no transitive graph was produced.

## Bounded monolithic-stream attempt — 2026-08-24

To test whether the relation payload could be used without full extraction, the project streamed the archive member directly into a raw-deflate scanner that retained only pre-registered source package-version candidates. The transfer was stopped by its 1,500-second network bound after 783,198,932 of 10,228,591,413 compressed bytes (7.6569%) had arrived. Because a compressed stream cannot be interpreted as complete after timeout, the scanner retained no candidate rows and all incomplete output was deleted. The operational attempt is recorded in `73_chrono_resolution_streaming_attempt.json`.

The result narrows the next actionable data gate to an approved bulk-compute environment, a provider-side filter, or an upstream filtered export. It does not lower the fidelity threshold or justify use of a current graph as a historical substitute.

## Historical control-population source boundary — 2026-08-24

The npm-follower authors report a continuously collected archive of package metadata and code that retains later-deleted versions, with more than 35 million versions reported in 2023. The public project page characterizes the full ecosystem replica as 20+ TB. [19] [20] That scale makes the resource relevant for future event coverage and at-risk-population work, but unsuitable for acquisition in the current bounded sandbox without an official query, a frozen filtered export, or bulk-compute access.

The project therefore retains the no-control conclusion. It does not convert registry rows with no known incident into benign labels. A valid control population must be defined against a frozen incident-coverage source, a documented horizon, and an explicit source population before any temporal ranking or calibration experiment proceeds.

19. Pinckney et al., *npm-follower: A Complete Dataset Tracking the NPM Ecosystem*, arXiv:2308.12545: <https://arxiv.org/abs/2308.12545>.
20. Pinckney, *npm-follower project page*: <https://donaldpinckney.com/publication/npm-follower/>.

## Registry-only recursive graph sensitivity path — 2026-08-24

Official npm documentation states that a `package-lock.json` describes the exact dependency tree generated by an npm operation, while the SemVer reference treats a declared range as a set of satisfying versions and documents `maxSatisfying` over a provided version list. [21] [22] These statements support a narrowly bounded sensitivity graph in which retained registry versions are selected by cutoff-valid SemVer rules, but they also exclude calling that graph a historical installation tree.

The project added a depth-three, runtime-`dependencies`-only recursive reconstruction for the seven exact source snapshots. It excludes peer, optional, bundled, workspace, override, link, git, tarball, cache, and package-manager-version behavior, and it never supplies global graph metrics or prediction results. Every non-root node is labeled `registry_reconstructed_cutoff_semver_approximation`.

21. npm, *package-lock.json*: <https://docs.npmjs.com/cli/v11/configuring-npm/package-lock-json/>.
22. npm, *semver*: <https://docs.npmjs.com/cli/v6/using-npm/semver/>.

## Explicit benign-label sensitivity corpus — 2026-08-24

The public Amalfi artifact accompanying the ICSE 2022 malicious npm detection study contains `data/basic-corpus.csv`. The published schema is `package`, `version`, `hash`, and `analysis`, where the analysis field assigns `malicious` or `benign` labels. Its README distinguishes this manually labelled basic corpus from daily new-release files where unreviewed rows are labelled `not triaged`. [23]

This provides explicit package-version negatives for a separate retrospective release-classification sensitivity study; it is not evidence that arbitrary registry versions without an incident are benign. The corpus has no per-row review or horizon timestamps in the exposed CSV, and its case-centred construction is not a population frame for the primary future-compromise target. Any use is therefore isolated from the incident-family temporal benchmark and labelled non-primary.

23. Sejfia and Schäfer, *Amalfi ICSE 2022 artifact*: <https://github.com/githubnext/amalfi-artifact>.

## Human-vetted positive catalogue boundary — 2026-08-24

The DataDog Malicious Software Packages Dataset exposes an npm manifest of known malicious package names with explicit version arrays where available. Its repository says sample-file dates are discovery dates rather than publication dates, and the manifest has no row-level dates, campaign family, evidence URL, or negative labels. [24]

The manifest is consequently admissible only as a frozen positive-membership corroboration source. It cannot set a primary temporal event cutoff, turn an absent manifest entry into a benign label, or form a control population. The project will retain only candidate-overlap outputs and will not ingest samples or execute package content.

24. DataDog, *Malicious Software Packages Dataset*: <https://github.com/DataDog/malicious-software-packages-dataset>.

## Dated OSV and independent-report expansion — 2026-08-24

OpenSSF report `MAL-2026-3744` records `node-ipc` versions `9.1.6`, `9.2.3`, and `12.0.1` as malicious, with `published` set to `2026-05-14T16:53:17Z`, package-integrity evidence, and source-origin timestamps. [25] SafeDep's independently published incident report names the same three versions, characterizes a compromised maintainer account, and reports registry times including `12.0.1` at `2026-05-14T14:25:30.311Z`. [26]

The project admits this as one new `node_ipc_2026` incident family. Its strict feature cutoff is the earliest reported malicious publication timestamp, one millisecond before `12.0.1`; the selected exact pre-event source object is `node-ipc@12.0.0`. No report publication, discovery, remediation, payload, or current registry information enters the feature snapshot. The record increases the adjudicated ledger to nine package-event records and five families, but it does not create controls or permit model fitting.

25. OpenSSF Malicious Packages, *MAL-2026-3744: Malicious code in node-ipc (npm)*: <https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/node-ipc/MAL-2026-3744.json>.
26. SafeDep, *Compromised node-ipc on npm: Credential Stealer via DNS Exfiltration*, 14 May 2026: <https://safedep.io/malicious-node-ipc-npm-compromise/>.

## Dated dependency-confusion expansion — 2026-08-24

SafeDep's `oob.moika.tech` campaign report documents the June 2026 `@emcd-vue` wave and identifies `@emcd-vue/auth` versions `6.4.8` and `6.4.9`. [27] OpenSSF report `MAL-2026-5163` independently records `@emcd-vue/auth` as malicious, supplies package-integrity evidence and a GHSA alias, and lists versions `6.4.5`, `7.0.0`, `6.4.8`, and `6.4.9`. [28] The official npm registry response provides the exact `6.4.8` publication timestamp of `2026-06-01T07:04:12.358Z`.

The record is admitted as one distinct `moika_dependency_confusion_2026` family and uses that earliest documented malicious publication as its strict cutoff. The retained registry response does not provide a usable pre-cutoff version object, so this is intentionally a label-only event: it increases the ledger to ten package-event records and six families but does not increase exact source snapshots, direct edges, isolated range targets, or bounded graph roots. The ten-record count now meets the pre-registered positive-record floor; calibration and ranking remain blocked because no cutoff-valid control population exists and only eight exact feature snapshots are reconstructable.

27. SafeDep, *183 npm Packages Target Cloud and Finance via oob.moika.tech*, 28 May 2026: <https://safedep.io/oob-moika-tech-dependency-confusion-campaign/>.
28. OpenSSF Malicious Packages, *MAL-2026-5163: Malicious code in @emcd-vue/auth (npm)*: <https://github.com/ossf/malicious-packages/blob/main/osv/malicious/npm/%40emcd-vue/auth/MAL-2026-5163.json>.

## Provider-backed control-frame assessment — 2026-08-24

Open Source Insights documents the deps.dev BigQuery public dataset as a provider-backed source with full-snapshot timestamps, package-version export timestamps, upstream publication times, and advisory disclosure plus affected/unaffected-version fields. [29] This makes it a plausible future source for freezing an npm package-version population, but it does not by itself provide closed-world coverage for the project's malicious-publication or compromise targets: its documented advisory relation is vulnerability-oriented.

The provider documents a Google Cloud account and enabled BigQuery API as prerequisites. A metadata-only no-credential request to the official dataset endpoint returned `401 UNAUTHENTICATED`; no tables, rows, sample, or population were retrieved. The companion `81_provider_control_frame_probe.json` records the endpoint, status, zero rows, and no secrets. The assessment also excludes a versioned Figshare/Mendeley malicious/benign source-code dataset from the primary control frame because the published landing metadata does not establish row-level package-version identity, collection cutoff, coverage, or outcome horizon. [30] [31]

The valid next step remains provider-authorized snapshot access paired with a separately frozen malicious-package or compromise coverage source. Until then, an advisory absence or catalogue absence is not treated as a benign control.

29. Open Source Insights, *deps.dev BigQuery dataset*: <https://docs.deps.dev/bigquery/v1/>.
30. Figshare, *Malicious NPM Package Detection Dataset*, DOI 10.6084/m9.figshare.31451728: <https://doi.org/10.6084/m9.figshare.31451728>.
31. Mendeley Data, *Malicious NPM Package Detection Dataset*, Version 1: <https://doi.org/10.17632/6tc8wrp62g.1>.

## Shai-Hulud temporal-label candidate screen — 2026-08-24

The official CISA alert establishes that the September 2025 Shai-Hulud incident was a credential-theft and automated npm-republication campaign affecting more than 500 packages, and recommends pinning releases produced before 16 September 2025. [14] The alert itself does not provide package-version identifiers. The CISA-referenced Unit 42 technical report provides operational detail about the campaign and maintains an evolving scope discussion, but the retrieved public page did not supply a frozen, machine-readable affected package-version list in the reviewed material. [32]

This is a **candidate screen only**, not a ledger expansion. Campaign-level confirmation and a broad event window are insufficient for a package-event record under the frozen protocol. Admission would require a dated affected package-version list, independent corroboration of the selected package/version, an earliest malicious publication time from the official registry or primary evidence, and family-level grouping. No labels, controls, source snapshots, dependency edges, or model metrics were added by this screen.

32. Palo Alto Networks Unit 42, *“Shai-Hulud” Worm Compromises npm Ecosystem in Supply Chain Attack*: <https://unit42.paloaltonetworks.com/npm-supply-chain-attack/>.

## Bounded Shai-Hulud second-wave expansion — 2026-08-24

The candidate screen found a compact, version-specific path for one November 2025 second-wave package event without inferring campaign completeness. OpenSSF record `MAL-2025-191155` lists `wenk` versions `1.0.9` and `1.0.10`, was published on 24 November 2025, and retains references to Aikido, Wiz, and StepSecurity campaign reporting. [33] A frozen Wiz IOC CSV at commit `22752e7cc55ece6a053e3277b60b914e0260e65d` independently contains the exact `wenk,= 1.0.10 || = 1.0.9` row; its response SHA-256 is stored by the bounded assessment. [34]

The official registry provides `wenk@1.0.9` at `2025-11-24T10:06:12.376Z`, `wenk@1.0.10` at `2025-11-24T10:23:35.925Z`, and the prior `wenk@1.0.8` at `2018-11-08T06:39:02.210Z`. The ledger therefore admits one `shai_hulud_second_coming_2025` record with the earliest selected malicious publication as cutoff and `wenk@1.0.8` as the exact source snapshot. It does not ingest the 795-row Wiz IOC list as 795 independent events, assert campaign-wide completeness, create controls, or compute predictive metrics. The reproducible `82_shai_hulud_second_coming_candidate_assessment.json` records the frozen identities, cross-source checks, cutoff, and exclusions.

33. OpenSSF Malicious Packages, *MAL-2025-191155: Malicious code in wenk (npm)*: <https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/wenk/MAL-2025-191155.json>.
34. Wiz Research IOCs, *shai-hulud-2-packages.csv*, commit `22752e7`: <https://github.com/wiz-sec-public/wiz-research-iocs/blob/22752e7cc55ece6a053e3277b60b914e0260e65d/reports/shai-hulud-2-packages.csv>.

## Control-frame access-path preliminary screen — 2026-08-24

The next investigation is constrained by a five-part contract: a named cutoff population, row-level package-version identity, an independently documented malicious-publication or compromise coverage source, a post-cutoff observation horizon, and an exclusion rule that does not treat missing coverage as benign. A preliminary source screen reaffirms three known paths. deps.dev documents useful snapshot and package-version fields but requires access and does not itself close the target-coverage gap. [29] npm-follower documents historical retention but remains a 20+ TB archive without a bounded public query or filtered export in this environment. [19] [20] npm documents a public registry/CouchDB mirror, but a current or incrementally updated registry endpoint is not a historical frozen population and cannot establish a past non-event horizon by itself. [35]

No control rows, negative labels, or model metrics were created by this screen. The next step is to inspect whether any public provider exposes a compact, frozen, row-addressable export that can satisfy the population side of the contract and can be paired with a separately frozen event-coverage source.

The documented BigQuery sandbox route was also checked directly in the available browser session. The Google Cloud console redirected to the Google Account sign-in page before any project, query, or dataset operation; therefore, no authenticated sandbox or API access exists in this session. This confirms the earlier HTTP 401 API observation and does not justify a retry, a query, or a claimed provider extraction without a separately configured Google Cloud identity and project.

35. npm, *Registry documentation*: <https://docs.npmjs.com/cli/v9/using-npm/registry>.

The Libraries.io public-data route was also screened. Its own documentation characterizes the service as scraped public package metadata, not validated or curated for accuracy, and exposes a current aggregate npm package count rather than a dated release-level snapshot or an outcome-coverage horizon. [36] This is insufficient for a historical non-event denominator and is excluded as a primary temporal control source.

36. Libraries.io, *Data and service description*: <https://libraries.io/data>.

## Mini Shai-Hulud atool candidate screen — 2026-08-24

SafeDep reports that the npm account `atool` was compromised on 19 May 2026 and describes a 22-minute burst that published malicious versions across hundreds of npm packages. Its rendered table contains 318 package rows with version-level entries, including `amapcn` versions `0.2.2` and `0.3.2`. [37] OpenSSF `MAL-2026-4127` independently records the same `amapcn` pair, identifies the event as part of the Mini Shai-Hulud campaign, and preserves independently ingested Amazon Inspector and Google Open Source Security provenance records for those versions. [38]

Socket independently reports a 19 May Mini Shai-Hulud wave with hundreds of affected npm package versions, a timed publication window, and an affected-package table with package-version publication and detection timestamps. [39] This candidate is materially more specific than a campaign headline, but it is not admitted until the official npm registry confirms the earliest selected malicious version timestamp and an exact pre-event source object. The campaign will be treated as one incident family; the SafeDep/Socket lists will not be converted into hundreds of independent families or controls.

The official npm registry returned `amapcn@0.2.2` at `2026-05-19T01:56:40.925Z` and `amapcn@0.3.2` at `2026-05-19T02:05:59.265Z`; `amapcn@0.1.2`, published at `2026-05-18T14:23:03.053Z`, is the latest retained version strictly before the earliest selected affected release. The candidate therefore passed the frozen adjudication protocol and is admitted as **one** `mini_shai_hulud_atool_2026` record with `amapcn@0.1.2` as an exact pre-event source snapshot. The reproducible `84_mini_shai_hulud_atool_candidate_assessment.json` stores source response hashes, version agreement, cutoff, and exclusions. The 318 SafeDep table rows and Socket’s broader campaign list are not converted into independent families, controls, completeness claims, or predictive inputs.

## Figshare NPM malicious-package benchmark screen — 2026-08-24

Guo et al. release a versioned Figshare replication package for a 2026 npm malicious-package detector study. The landing record describes 6,420 malicious package versions and 7,288 benign packages, while the version-1 archive is 87,885,991 bytes and supports HTTP byte ranges. [40] [41] A bounded central-directory retrieval and two metadata-only member extractions were performed; no package source member was extracted or executed.

The extracted `malware_time.csv` contains 6,420 package-version rows. It has 6,149 nonblank timestamps after line-ending normalization, ranging from 2011-05-12T08:43:03.953Z to 2025-05-17T07:07:29.508Z, and 271 blank timestamps. The companion `selected_benign_packages.txt` contains 1,000 unique package/version strings but no per-row timestamp, collection cutoff, observation horizon, or documented relationship to the 7,288-benign count in the later public landing description. The archive’s filename inventory contains only those two top-level CSV files and package-code directories; it does not expose a compact benign temporal-label table.

The source is therefore **not eligible as a primary future-compromise control frame**: it is a retrospective detector-evaluation benchmark assembled from academic datasets and public advisories, not a documented cutoff population followed under a closed-world malicious-publication or compromise coverage protocol. Its explicitly labelled samples may be preserved as a future release-classification sensitivity lead only after separate sampling and retention checks. No rows, controls, benign labels, calibration, ranking, or prediction metrics were added to the current benchmark.

40. W. Guo et al., *How Effective Are NPM Malicious Package Detectors? A Large-Scale Empirical Study*, arXiv:2603.27549v2, 2026: <https://arxiv.org/html/2603.27549v2>.
41. W. Guo, *How Effective Are NPM Malicious Package Detectors? A Large-Scale Empirical Study*, Figshare Version 6, DOI 10.6084/m9.figshare.31869370: <https://doi.org/10.6084/m9.figshare.31869370>.

## GitHub Advisory Database malware-path screen — 2026-08-24

GitHub announced that its malware-advisory importer validates OpenSSF OSV records, preserves each upstream record as a snapshot, drops records without usable affected versions, and supports later withdrawal or retraction handling. [42] GitHub’s public Advisory Database repository documents a broader, community-curated vulnerability-advisory corpus in OSV format, including npm, with advisory updates sourced from multiple inputs and merge decisions reviewed by its curation team. [43]

This is a potentially useful **positive-advisory provenance and snapshot lead**, but it is not a temporal control frame. The public documentation defines an advisory database rather than an enumerated at-risk npm package-version population; it supplies no closed-world malicious-publication or maintainer-compromise coverage statement, no pre-registered non-event horizon, and no basis for interpreting a package/version absent from an advisory as benign. The new GitHub path therefore creates zero rows, controls, labels, family assignments, calibration results, or ranking metrics in the temporal benchmark. It may only be reconsidered as a frozen positive corroboration source, under the existing ledger protocol, if a candidate record requires it.

42. GitHub Blog, “How we took malware advisories beyond npm,” 6 August 2026: <https://github.blog/security/supply-chain-security/how-we-took-malware-advisories-beyond-npm/>.
43. GitHub, “GitHub Advisory Database” repository documentation: <https://github.com/github/advisory-database>.

## npm-follower historical-population access screen — 2026-08-24

The npm-follower project documents a real-time replica of the entire npm ecosystem, including package metadata and code, with a stated size of more than 20 TB. [44] This makes it conceptually relevant to historical package-version population reconstruction, including versions no longer retained by the current registry. However, the public `dependencies.science` repository is only the static website source: it lists no release, package, compact data artifact, filtered export, query API, or row-addressable historical package-version snapshot. [45]

The path is consequently excluded from the current control-frame pipeline. It fails the bounded reproducible-access requirement, and it does not itself define closed-world malicious-publication or maintainer-compromise coverage, a non-event horizon, or a benign label contract. No download, data rows, controls, labels, calibration results, or model metrics were created. Authorized access to a defined filtered export would still require a separately frozen incident-coverage and outcome-horizon source before control extraction could begin.

44. D. Pinckney et al., “npm-follower: A Complete Dataset Tracking the NPM Ecosystem,” project publication page, 2023: <https://donaldpinckney.com/publication/npm-follower/>.
45. D. Pinckney, `dependencies.science` repository: <https://github.com/donald-pinckney/dependencies.science>.

## SupplyTGN temporal benchmark screen — 2026-08-24

The SupplyTGN preprint describes a reproducible, leakage-audited temporal benchmark with explicit 30- and 90-day horizons, cutoff-safe feature materialization, and released per-instance predictions. [46] Its disclosed build, however, is based on **PyPI/OSV** component–cutoff instances rather than npm package versions. [46] The public abstract and release description therefore make it a useful methodological reference for pre-registering horizons, leakage audits, and per-instance artifacts, but not a population or outcome source for this npm benchmark.

SupplyTGN creates zero npm rows, controls, labels, incident families, calibration results, or model metrics. Transferring its reported PyPI/OSV performance to npm, or treating its PyPI non-events as npm benign controls, is prohibited. Its role is limited to benchmark-design comparison until an npm-specific source satisfies the frozen population, outcome-coverage, and non-event-horizon contract.

46. T. P. Tran Truong, S. Ha, and X.-B. Le, “SupplyTGN: A Reproducible Leakage-Safe Benchmark for Temporal Software Supply-Chain Risk,” SSRN preprint, 28 July 2026: <https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7194447>.

37. SafeDep, *Mini Shai-Hulud Strikes Again: 317 npm Packages Compromised*, 19 May 2026: <https://safedep.io/mini-shai-hulud-strikes-again-314-npm-packages-compromised/>.
38. OpenSSF Malicious Packages, *MAL-2026-4127: Malicious code in amapcn (npm)*: <https://github.com/ossf/malicious-packages/blob/c04e75e38121768f82fef0495de77b68b7054d7c/osv/malicious/npm/amapcn/MAL-2026-4127.json>.
39. Socket Research, *Mini Shai-Hulud Hits @antv Ecosystem, 639 Compromised npm Package Versions*, 19 May 2026: <https://socket.dev/blog/antv-packages-compromised>.
