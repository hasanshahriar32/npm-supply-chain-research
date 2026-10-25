> **Threshold values superseded:** [The strict-quorum correction](14_q1_strict_quorum_exclusion_fix_and_lock.md) replaces this report’s residual-threshold results and archive lock. Source-audit corrections remain relevant.

# Task 14: Final manuscript verification and handoff

## 1. Executive summary and scope

Completed: 2026-10-25T19:43:21.546431+06:00 (Asia/Dhaka).

Completed the continuation of Task 13: independently checked the new incident sources, corrected scientific interpretation and citation metadata, reproduced the threshold experiment, rebuilt both journal PDFs, and verified the source archive. The four locked conference deliverables remain byte-for-byte unchanged.

**This report supersedes Task 13 wherever it claims operational quorum protection, verified placeholder references, or unconditional submission readiness.** Technical preparation is complete; actual submission, author approval, a similarity-service report, and venue-specific acceptance of the disclosure are not established.

## 2. Evidence and source verification

The focused source ledger is `manuscript_q1/results/source_verification_2026-10-25.json`. Sources were inspected through the browser on October 25, 2026. Source statements are distinguished from our interpretation; no package payloads or exploits were executed.

| Reference | Primary source and correction |
|---|---|
| `litellm2026` | [Primary record](https://docs.litellm.ai/blog/security-incident-oct-21-2026-attack-chain). Final investigation replaces initial token-origin hypothesis; roles differ and token count is not an observed quorum. |
| `litellmincident2026` | [Primary record](https://docs.litellm.ai/blog/security-incident-oct-21-2026). Artifact scope, source-tag discrepancy, approximate two-hour PyPI window; initial causal account superseded. |
| `opencode2026` | [Primary record](https://www.pillar.security/blog/open-and-shut-remote-code-execution-in-opencode-via-mcp-oauth). Researcher disclosure October 19; fix September 28; Windows/WSL; no CVE reported. |
| `railway2026` | [Primary record](https://blog.railway.com/p/preliminary-report-october-security-incident). Preliminary potential exposure upper bound; builds restored by report time. |
| `railwaydisclosure2026` | [Primary record](https://blog.railway.com/p/security-disclosure-wednesday-october-21st). Temporary deployment pause; remediation deadlock is our operational inference. |
| `npmtrustedpub2026` | [Primary record](https://bloom.security/blog/slugfest-millions-of-ai-agents-download-exposed-npm-packages). Mutable-name trust-binding weakness; exposure is not proof of malicious publication. |
| `npmexpiry2026` | [Primary record](https://github.blog/changelog/2026-10-02-unvalidated-npm-trusted-publishing-configurations-now-expire/). Mitigation announced October 2; distinguish remediation date from later researcher disclosure. |
| `nodejsbrotli2026` | [Primary record](https://nodejs.org/en/blog/vulnerability/october-2026-security-releases). Brotli CVE-2026-111497 rated High, not Critical. |
| `weeraddana2024` | [Primary record](https://rebels.cs.uwaterloo.ca/confpaper/2024/07/16/dependency-induced-waste-in-continuous-integration.html). Corrected authors and FSE venue; removed unrelated DOI 10.1145/3641544. |
| `jayasuriya2024` | [Primary record](https://link.springer.com/article/10.1007/s10664-024-10563-4). Corrected given names, article number 42, and issue year 2025. |
| `gao2025emse` | [Primary record](https://gaoxiang9430.github.io/papers/emse.pdf). Corrected title and author order; scoped percentages to studied corpus. |
| `okafor2025` | [Primary record](https://www.usenix.org/conference/usenixsecurity25/presentation/kalu). Corrected full author list and attribution to Kalu et al. |
| `schorlemmer2024` | [Primary record](https://arxiv.org/abs/2401.14635). Corrected authors and studied registries; removed unverified DOI. |
| `ralph2020` | [Primary record](https://arxiv.org/abs/2010.03525). Corrected author shorthand to Paul Ralph and others. |
| `kitchenham2025` | Removed: claimed title and DOI could not be substantiated in the searches performed; absence of search results is not proof of nonexistence. |

This is a focused audit, not a new certification of every historical reference. PHP, Capcom, and the separate OpenCode Console breach were not added to the empirical cohort. Cross-ecosystem examples motivate limitations and do not validate the npm measurements.

## 3. Methods and scientific corrections

- Re-ran five strategies at budgets 10, 25, 50, and 100, with thresholds 1, 2, 3, and 5 and uniform efficacy multipliers 1.00, 0.95, 0.90, and 0.75.
- Checked forward endpoint closures against independently transposed maintainer-source incidence; checked selection uniqueness, budget/threshold monotonicity, and efficacy identities.
- Corrected the Direct P tie-break to use marginal coverage, matching the existing experiment; all reported table counts remained unchanged.
- Explicitly restricted P and P_k to 7,158 endpoints with observed sources. The literal full-universe formula adds 13 source-free endpoints to every count. Coverage percentages retain the 7,171-repository denominator.
- Recorded all ordered selections, archive/script hashes, zero-budget baselines and intervention increments in `quorum_reproducibility.json`.
- Reframed P_k as a hypothetical residual-source threshold count. Distinct upstream identities need not share a release policy. Token roles, package signer groups, bypass privileges, and approval rules are absent from the graph; token count does not establish a quorum.
- Explained that uniform H_eta = eta H preserves rankings and is an assumed sensitivity, without a measured bypass rate or correlated-failure guarantee.
- Corrected hybrid-objective monotonicity wording, the implemented lexicographic P heuristic, baseline-versus-optimum claims, and the distinction between Pareto and weight-aware selections.
- Replaced claims of continuous prospective validation with the retained status: 90 metadata captures, ten unavailable records, 100 pending outcomes, no fitted models or predictions, horizon ending January 18, 2027.
- Aligned journal authors and department/order with the user-provided author record; removed unprovided email addresses and IEEE membership assertions. Replaced submission/publication assertions with draft labels and an accurate AI-assistance disclosure requiring author review.

## 4. Reproduced quantitative results

Population: 25,228 packages, 12,217 maintainers, 7,171 workflow repositories; 7,158 endpoints have observed sources.

| k | P_k(empty set) |
|---:|---:|
| 1 | 0 |
| 2 | 1,716 |
| 3 | 2,262 |
| 5 | 2,963 |

Budget 100 results; P_k columns are structural counts rather than operational protection claims:

| Strategy | C | H (%) | P1 | P2 | P3 | P5 | P2 increment over empty set |
|---|---:|---:|---:|---:|---:|---:|---:|
| Portfolio Size | 4,579 | 7.96 | 577 | 2,065 | 2,669 | 3,281 | 349 |
| Greedy Coverage | 5,538 | 11.48 | 800 | 2,112 | 2,602 | 3,268 | 396 |
| Exact Union | 4,407 | 33.79 | 534 | 2,137 | 2,760 | 3,523 | 421 |
| Pareto Hybrid ($\alpha=0.50$) | 5,020 | 31.19 | 626 | 2,153 | 2,719 | 3,415 | 437 |
| Direct Supermodular $P(S)$ | 5,020 | 13.23 | 1,022 | 2,074 | 2,636 | 3,337 | 358 |

For Pareto Hybrid, P2=2,153 includes 1,716 endpoints already below threshold at zero budget; its intervention increment is 437. Treating 2,153 as newly secured repositories would therefore overstate even the hypothetical scenario. H_0.90=28.07% is a scaled assumption, not a measured reduction in incidents.

## 5. Build, validation, and freeze results

Commands completed successfully:

```sh
python3 scripts/study_q1_quorum_and_oct2026.py
python3 -m py_compile scripts/study_q1_quorum_and_oct2026.py manuscript_q1/scripts/verify_manuscript_q1.py
bash manuscript_q1/compile_q1.sh
bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex
python3 manuscript_q1/scripts/verify_manuscript_q1.py
python3 manuscript_q1/scripts/package_q1.py
python3 scripts/finalize_manuscript_handoff.py
```

The verifier now compares all 20 table rows with CSV and JSON, verifies input/script hashes and population baselines, rejects missing compilation logs, and records the actual execution timestamp. Source-link presence checks support traceability; they do not automatically establish factual validity.

| Check | Result |
|---|---|
| Abstract | 188 words |
| main_q1.pdf | 16 pages; 292,713 bytes; embedded fonts; zero Type 3 |
| main_q1_anonymous.pdf | 16 pages; 292,182 bytes; embedded fonts; zero Type 3 |
| Compilation logs | No overfull boxes, unresolved citations/references, or missing glyphs found |
| Other TeX warnings | Underfull boxes and font-shape fallback warnings remain; no claim of warning-free compilation |
| Rendered table | Visually inspected journal PDF page 11; both wide tables are legible and fit the page |
| Source archive | 58 members; CRC and exact workspace-member parity PASS |

Frozen conference SHA-256 checks:

| Artifact | SHA-256 |
|---|---|
| `manuscript/main.pdf` | `abb1b4b3cd1baeabf3fc1f9232661f5594f7f233f75db0d5ec247d06f882e4cb` |
| `manuscript/main_authors.pdf` | `402215fde6223126c4809f988baadcd86e4b0920318eb05b101a6e65b148f373` |
| `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` | `bb2c591b009979b5f117ce5458d867c80f4b56ddb4a093cae59ea2bd30e87de4` |
| `NPM_Supply_Chain_IEEE_Overleaf.zip` | `ab0fd2cd4546997e4cc386ce960aa14ceca77870f8fbf61c71cc225a29d00145` |

The locked conference PDF contains an LLM acknowledgment. Older submission metadata saying it is absent is stale. Its assertions of solely non-intellectual use and author approval still require the actual authors to substantiate against the supplied guideline and work history. Neither acknowledgment presence nor a technical PASS resolves that policy question.

## 6. Saved deliverables and handoff

- Conference anonymous review PDF: `manuscript/main.pdf` (locked six-page draft).
- Conference named review PDF: `manuscript/main_authors.pdf` (locked six-page draft).
- Conference archives: `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` and `NPM_Supply_Chain_IEEE_Overleaf.zip` (unchanged).
- Updated journal PDFs: `manuscript_q1/main_q1.pdf` and `manuscript_q1/main_q1_anonymous.pdf`.
- Updated journal source archive: `NPM_Supply_Chain_Q1_Journal_Source.zip` (2,371,895 bytes; SHA-256 `88c4992154b751a153ec577fccdc787116d549112ce8c971989fcbc1c94e31fe`).
- Detailed checks: `manuscript_q1/results/q1_verification_report.json`.
- Results and provenance: `manuscript_q1/results/q1_quorum_exclusion.csv`, `q1_quorum_exclusion.json`, and `quorum_reproducibility.json`.
- Build and interpretation instructions: `manuscript_q1/README.md`.
- Artifact checksums and archive validation: `reports/14_final_artifact_manifest.json`.
- This six-section report is mirrored to `research_sessions/active_verification_track/14_final_manuscript_verification_and_handoff.md` and indexed in `research_sessions/SESSION_INDEX.md`.

The source ZIP is a typesetting package. Full experiment verification also requires the surrounding repository scripts and retained datasets, as documented in the README. No external submission, acceptance, similarity score, or author approval has been fabricated. Final author review should cover scientific claims and historical references outside the focused audit, the chosen venue format/disclosure rules, and permission to submit. Prospective outcome evaluation remains future work through January 18, 2027.
