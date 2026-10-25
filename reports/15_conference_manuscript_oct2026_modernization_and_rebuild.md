# Task 15: Conference manuscript October 2026 modernization and rebuild

## 1. Executive summary and authorization

Completed 2026-10-25T20:17:07.997047+06:00 (Asia/Dhaka). The user explicitly lifted the conference freeze. Both conference PDFs were modernized and rebuilt to **exactly six A4 pages**; both conference ZIPs and the journal source ZIP were regenerated. Conference and journal technical verification pass. No external submission was performed.

Pre-update conference PDFs and ZIPs, with their hashes, are preserved in `research_sessions/active_verification_track/task15_before/`. The Task 15 lock replaces the old conference checksums; earlier reports remain historical records. Both journal PDFs remain byte-for-byte identical to the strict Task 14 versions (16 pages each).

## 2. Literature and manuscript integration

Imported 12 corrected bibliography entries from the focused journal source audit. The conference now cites **24 references**, including npm SlugFest and binding expiry, OpenCode’s September fix/October disclosure, LiteLLM’s final attack-chain and artifact records, Railway’s preliminary report and deployment pause, and the High-severity Node.js Brotli boundary. Added Shen et al. (EMSE 2025), Kalu et al. (USENIX Security 2025), Weeraddana et al. (FSE 2024), and Jayasuriya et al. (EMSE 2025). Source URLs and identifying metadata are retained.

The source evidence was imported from the previously inspected records in `manuscript_q1/results/source_verification_2026-10-25.json`; this task did not independently repeat the full literature audit. Contextual incidents are not added as npm validation observations, and the 81.26% finding is qualified to the cited study’s corpus.

Shortened repeated collection, motivation, and validation prose to meet the page limit. Retained standard IEEE conference A4/10-point settings, all four figures, core C/H/P results, 200-seed MCSE values, the 39.50 s three-run profile, and the qix example (2,971 name-graph and 1,476 version-graph repositories). No margin or font compression was introduced.

## 3. Threshold definitions and reproduced sensitivities

The requested earlier increments use the unguarded residual-source count, now named **T_k**, while **P_k(strict)** retains the explicit zero-anchored definition from the preceding correction. These are different metrics. On 7,158 nonempty-source endpoints, T2(empty)=1,716, whereas P2(strict, empty)=0. All 13 source-free endpoints are excluded.

| Budget-100 selection | C | H (%) | P1 | T2 | Delta T2 | Strict P2 | H at eta=0.90 (%) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Greedy Coverage | 5,538 | 11.48 | 800 | 2,112 | 396 | 1,145 | 10.34 |
| Exact Union | 4,407 | 33.79 | 534 | 2,137 | 421 | 793 | 30.41 |
| Pareto Hybrid (alpha=0.50) | 5,020 | 31.19 | 626 | 2,153 | 437 | 961 | 28.07 |
| Direct Supermodular P(S) | 5,020 | 13.23 | 1,022 | 2,074 | 358 | 1,169 | 11.90 |

`scripts/generate_conference_modernization.py` independently reconstructs residual and strict counts from the retained total/remaining-source histograms, checks strict-count parity, and records source hashes in `manuscript/results/conference_modernization.json`. Neither definition establishes an enforced multisigner policy. Uniform efficacy is hypothetical and preserves H rankings; no bypass rate or control efficacy is estimated.

## 4. Build, validation, and package results

Completed the requested conference suite: `package_overleaf.py`, `verify_manuscript.py`, `check_author_versions.py`, `check_submission.py`, `validate_packages.py`, and `audit_artifacts.py`. Also compiled the extracted anonymous package independently, checked its text against the delivered PDF, ran the journal verifier, and rebuilt the journal ZIP.

| Deliverable/check | Result |
|---|---|
| main.pdf | 6 A4 pages; 187,181 bytes; 28 embedded fonts |
| main_authors.pdf | 6 A4 pages; 188,726 bytes; 29 embedded fonts |
| Conference logs | Zero overfull boxes, Type 3 fonts, undefined citations/references, or missing glyphs |
| Research consistency | 68 hashes; 150 deterministic and 6,000 random rows; generated values and prospective timing pass |
| Bibliography | 24 active citations; all 12 imported entries cited |
| Anonymous package | Standalone compilation, PDF-text parity, identity exclusions, and references pass |
| All three ZIPs | CRC and exact workspace-member parity pass (anonymous README is generated) |
| Journal verification | PASS; 188-word abstract; both PDFs remain 16 pages |

The final reference pages were rendered and visually inspected; content fits. Underfull boxes and font-shape fallback warnings remain. The data audit recomputes legacy fields offline; no new live collection or prospective outcome labeling was performed.

## 5. Artifact lock and saved reports

The reviewed replacement conference lock is `manuscript_q1/config/conference_lock.json`; the journal verifier reads that explicit lock rather than accepting arbitrary current files. Full prior/new hashes and all validation reports are indexed in `reports/15_conference_modernization_artifact_manifest.json`.

| Archive | Files | Bytes |
|---|---:|---:|
| `NPM_Supply_Chain_IEEE_Overleaf.zip` | 150 | 3,555,126 |
| `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` | 48 | 1,449,794 |
| `NPM_Supply_Chain_Q1_Journal_Source.zip` | 59 | 2,506,828 |

This six-section report is saved as `reports/15_conference_manuscript_oct2026_modernization_and_rebuild.md` and mirrored to `research_sessions/active_verification_track/15_conference_manuscript_oct2026_modernization_and_rebuild.md`. The reports index and session ledger are updated.

## 6. Handoff and remaining author actions

Use `manuscript/main.pdf` for anonymous conference review and `manuscript/main_authors.pdf` for named author review. Both conference archives contain the current PDFs and typesetting inputs. The journal PDFs retain the strict threshold analysis; its refreshed source ZIP contains the current cross-track lock and verification report. Full numerical reproduction requires the surrounding repository and retained data, beyond the typesetting ZIPs.

The conference acknowledgment now accurately describes LLM drafting, code revision, analysis checking, and source verification; it does not assert solely non-intellectual use or completed author approval. Older metadata claiming disclosure absence was corrected. The supplied venue guideline restricts LLM use to non-intellectual purposes, so that policy mismatch remains unresolved despite technical checks passing. Authors must review scientific claims, determine venue eligibility, finalize the disclosure, obtain the required similarity report, check indirect anonymity, and approve submission. No approval, originality declaration, similarity score, acceptance, or submission has been fabricated.
