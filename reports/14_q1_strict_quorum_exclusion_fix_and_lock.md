> **Artifact lock superseded by Task 15:** [The authorized conference rebuild](15_conference_manuscript_oct2026_modernization_and_rebuild.md) replaces the conference hashes and journal source ZIP recorded here. The strict metric and journal PDFs remain unchanged.

# Task 14: Strict quorum exclusion correction and artifact lock

## 1. Executive summary

Completed 2026-10-25T19:53:09.252670+06:00 (Asia/Dhaka). Implemented the advisor’s explicit strict definition, regenerated all 20 strategy/budget rows, updated Sections 4 and 6.3, and rebuilt both journal PDFs and the source ZIP. Technical verification is **PASS**. The four frozen conference deliverables are unchanged.

This correction supersedes the residual-threshold values in the earlier Task 14 handoff; that report remains as a historical record. The strict rule removes zero-budget credit but does not establish real package-approval enforcement.

## 2. Mathematical definition and boundary checks

For nonempty source sets, let n = |Sources(r)| and t = |Sources(r) \ S|. Count an endpoint exactly when:

```text
t = 0 OR (n >= k AND t < k)
```

All 13 source-free workflow endpoints are excluded. Consequently P_k(empty set)=0 for k in {1,2,3,5}, P_1=P, and every credited endpoint has at least one hardened source. If n<k, all its sources must be hardened.

Two advisor statements required correction: the compact expression t < min(k,n) is not equivalent, and strict counts need not increase with k. For n=2 and t=1, the explicit rule counts the endpoint at k=2 but excludes it at k=3. The manuscript and tests use the explicit rule. Counts remain monotone in the hardening set for each fixed k. Zero anchoring alone does not make source cardinality an observed release quorum.

Four tests passed, including an independent set-based oracle over 16,384 source/selection/threshold cases, single-source and empty-source boundaries, the compact-form counterexample, and the nonmonotone-k counterexample.

## 3. Source-cardinality census

| Observed upstream sources | Workflow repositories |
|---|---:|
| 0 | 13 |
| 1 | 1,716 |
| 2 | 546 |
| 3 | 354 |
| 4 | 347 |
| >=5 | 4,195 |

Total: 7,171 workflow repositories, of which 7,158 have nonempty sources. The census uses workflow-repository indices; other linked repositories are excluded. All four strict zero-budget counts equal zero.

## 4. Corrected results

The same five ordered selections and four budgets are reused. C, H, and efficacy-scaled H are unchanged. The original budget-100 P1 counts remain 800 for Greedy, 534 for Exact Union, 626 for Pareto, and 1,022 for Direct P.

| Strategy | Budget | P1 | P2 | P3 | P5 |
|---|---:|---:|---:|---:|---:|
| Portfolio Size | 10 | 391 | 512 | 488 | 521 |
| Portfolio Size | 25 | 430 | 602 | 657 | 661 |
| Portfolio Size | 50 | 503 | 718 | 777 | 784 |
| Portfolio Size | 100 | 577 | 774 | 858 | 892 |
| Greedy Coverage | 10 | 351 | 477 | 495 | 468 |
| Greedy Coverage | 25 | 514 | 756 | 732 | 727 |
| Greedy Coverage | 50 | 638 | 936 | 921 | 907 |
| Greedy Coverage | 100 | 800 | 1,145 | 1,125 | 1,105 |
| Exact Union | 10 | 343 | 440 | 466 | 485 |
| Exact Union | 25 | 427 | 637 | 719 | 694 |
| Exact Union | 50 | 441 | 655 | 734 | 787 |
| Exact Union | 100 | 534 | 793 | 901 | 1,022 |
| Pareto Hybrid (alpha=0.50) | 10 | 351 | 477 | 495 | 468 |
| Pareto Hybrid (alpha=0.50) | 25 | 498 | 706 | 734 | 729 |
| Pareto Hybrid (alpha=0.50) | 50 | 605 | 907 | 985 | 1,019 |
| Pareto Hybrid (alpha=0.50) | 100 | 626 | 961 | 1,018 | 1,063 |
| Direct Supermodular P(S) | 10 | 479 | 614 | 609 | 586 |
| Direct Supermodular P(S) | 25 | 618 | 743 | 774 | 779 |
| Direct Supermodular P(S) | 50 | 803 | 948 | 998 | 1,016 |
| Direct Supermodular P(S) | 100 | 1,022 | 1,169 | 1,286 | 1,383 |

These are hypothetical structural threshold counts, not measured numbers of secure repositories. Package-level signer groups, approval roles, and bypass privileges remain unobserved. The compiled manuscript numbers this table as Table 6; “Table 10” was the earlier advisor/session label.

## 5. Build, verification, and conference freeze

| Check | Result |
|---|---|
| Strict boundary tests | 4 passed; 16,384 exhaustive cases |
| Data parity | All 20 CSV/JSON/TeX rows match; workspace copies match |
| Independent count check | Recomputed strict counts from retained (total, remaining) cardinality histograms |
| Zero budget and P1 invariants | PASS |
| Retired Budget-10 values | Absent from active manuscript text/results and extracted text of both PDFs |
| Abstract | 188 words |
| main_q1.pdf | 16 pages; 296,408 bytes; embedded fonts; zero Type 3 |
| main_q1_anonymous.pdf | 16 pages; 295,517 bytes; embedded fonts; zero Type 3 |
| Compilation | Zero overfull boxes, undefined citations/references, or missing glyphs |
| Render review | Table visually inspected on page 11; fits the page |
| ZIP validation | CRC and exact member/workspace parity PASS; 58 files |
| Conference freeze | All four original SHA-256 hashes match |

Frozen files: `manuscript/main.pdf`, `manuscript/main_authors.pdf`, `NPM_Supply_Chain_IEEE_Anonymous_Source.zip`, and `NPM_Supply_Chain_IEEE_Overleaf.zip`. Full checksums are retained in `reports/14_strict_quorum_artifact_manifest.json`. Underfull boxes and font-shape fallback warnings remain; compilation is not claimed to be warning-free.

## 6. Saved deliverables and handoff

- Report: `reports/14_q1_strict_quorum_exclusion_fix_and_lock.md`.
- Mirrored report: `research_sessions/active_verification_track/14_q1_strict_quorum_exclusion_fix_and_lock.md`; session ledger updated.
- PDFs: `manuscript_q1/main_q1.pdf` and `manuscript_q1/main_q1_anonymous.pdf`.
- Results: `manuscript/results/q1_journal/q1_quorum_exclusion.csv`, `.json`, and `_table.tex`, with synchronized journal copies.
- Provenance and census: `manuscript_q1/results/quorum_reproducibility.json`.
- Verification: `manuscript_q1/results/q1_verification_report.json`.
- Tests: `scripts/tests/test_strict_quorum.py`.
- Source archive: `NPM_Supply_Chain_Q1_Journal_Source.zip` (2,506,074 bytes).
- Archive SHA-256: `26369ae951dcac9c12d5cc9b9465987a90a016ae1a5b4098225a88a939524fb4`.

Author review, venue-policy review, similarity checking, and submission approval remain separate from the technical lock. No external submission was performed.
