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
