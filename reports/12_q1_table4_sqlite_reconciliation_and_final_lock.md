# Active Verification Session 12: Purge of Hardcoded Table 4 Metadata, 100% Programmatic SQLite Extraction, and Final Q1 Journal Deliverable Lock

## 1. Executive Summary & Session Objectives
* **Session Identifier**: `12_q1_table4_sqlite_reconciliation_and_final_lock`
* **Date & Timestamp**: 2026-10-21T17:30:00+06:00
* **Target Publication Venues**:
  * *IEEE Transactions on Software Engineering (TSE)* (Primary target; strict 100–200 word abstract limit, double-column IEEEtran journal format)
  * *ACM Transactions on Software Engineering and Methodology (TOSEM)* (Double-anonymous review)
  * *IEEE Transactions on Dependable and Secure Computing (TDSC)*
  * *Springer Empirical Software Engineering (EMSE)*
* **Author Affiliation**: Department of Computer Science and Engineering, Hajee Mohammad Danesh Science and Technology University (HSTU), Dinajpur 5200, Bangladesh
* **Compilation Toolchain**: Native `tectonic` 0.17.0 (`~/.local/bin/tectonic` invoking XeTeX engine with automatic BibTeX and font package caching)
* **Conference Deliverables Invariant (Track 1)**: `manuscript/main.pdf` (179,471 bytes, exactly 6.0 A4 pages), `manuscript/main_authors.pdf` (180,875 bytes, exactly 6.0 A4 pages), `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes), and `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes) remain **100% frozen with zero byte changes** and verified against cryptographic SHA-256 hashes.
* **Core Objectives Achieved**:
  1. **Hardcoded Metadata Purged from Table 4 Generation**: Completely rewrote `extract_incident_case_study()` in `scripts/extract_q1_temporal_and_authority_tables.py`. Removed all hardcoded dictionaries for maintainer names, maintainer counts, dependent counts, and strategy ranks.
  2. **100% Programmatic SQLite & CSV Extraction**:
     * Queried `package_metrics` from `data/npm_ecosystem.db.zip` for exact direct and transitive dependents (`541 / 3,525` for `debug`, `544 / 3,416` for `chalk`, `25 / 4,052` for `ansi-styles`, `1 / 357` for `simple-swizzle`, `14 / 15` for `eslint-config-prettier`, etc.).
     * Queried `package_maintainers` from `data/npm_ecosystem.db.zip` for total maintainer count $|M(p)|$ (`debug`: 2, `chalk`: 1, `ansi-styles`: 1, `eslint-config-prettier`: 3, `eslint-plugin-prettier`: 6, `@solana/web3.js`: 1, `nx`: 8, `node-ipc`: 12, `@tanstack/history`: 5, `@opensearch-project/opensearch`: 3, `@mastra/core`: 9).
     * Extracted exact workflow reach ($R_{\text{wf}}$) from `manuscript/results/graph_validity/per_package.csv`.
     * Computed 1-indexed maintainer strategy ranks directly on the 12,217-maintainer graph across Portfolio Size, Greedy Coverage (budget 100), Exact Union, and Pareto Hybrid ($\alpha=0.50$ via full scalarized greedy).
  3. **Section 5 Narrative Reconciled**: Updated `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex` to report maintainer `qix`'s true version-continuous 3-package portfolio union reach of **$1{,}476$ repositories** ($20.58\%$), replacing the stale back-calculation of $2{,}362$. Also confirmed `qix`'s Pareto Hybrid ($\alpha=0.50$) rank of **#48**.
  4. **Strict SQLite-to-Table-4 Parity Gate**: Upgraded `manuscript_q1/scripts/verify_manuscript_q1.py` with rigorous regex assertions validating every single row of Table 4 against SQLite and `per_package.csv`, while guaranteeing that no stale back-calculated values appear in the narrative text.
  5. **Dual PDF Compilation & Zero Protrusion**:
     * Integrated `\resizebox{\textwidth}{!}{% ... }%` into `q1_incident_case_study_table.tex`, guaranteeing 0 overfull `\hbox` protrusions across the entire table.
     * Recompiled Named version `manuscript_q1/main_q1.pdf` (15 pages, 278,629 bytes) and Double-Anonymous version `manuscript_q1/main_q1_anonymous.pdf` (14 pages, 276,717 bytes). Both have 0 overfull `\hbox` warnings and 0 Type 3 fonts.
  6. **Packaging and Verification Report Lock**: Re-ran verification suite producing `manuscript_q1/results/q1_verification_report.json` (`status: "PASS"`), and rebuilt `NPM_Supply_Chain_Q1_Journal_Source.zip` (52 files, 2,313,404 bytes, SHA-256: `9c139f3b20d00341cbb3d989d6853e40f963156d5ef2524d5d5c22e5c3256baf`).

---

## 2. Artifacts and Datasets Audited

### 2.1 Audited Datasets and Extraction Scripts
1. `data/npm_ecosystem.db.zip`: Canonical SQLite ecosystem database (tables `package_maintainers`, `package_metrics`, `maintainers`, `dependencies`, `package_versions`).
2. `manuscript/results/graph_validity/per_package.csv`: Canonical per-package ground-truth data file containing version-continuous and name-collapsed reaches across 25,228 packages.
3. `scripts/generate_task04_incident_validation.py`: Task 04 retrospective validation script establishing baseline SQLite rankings.
4. `scripts/extract_q1_temporal_and_authority_tables.py`: Extraction script generating journal Tables 4, 8, and 9. Fully rewritten to extract metadata dynamically.
5. `manuscript/results/q1_journal/q1_incident_case_study.csv` & `q1_incident_case_study_table.tex`: Corrected case study table.
6. `manuscript_q1/tables/q1_incident_case_study_table.tex`: Active manuscript table synchronized with resizebox wrapper.
7. `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex`: Section narrative cross-checked and aligned.
8. `manuscript_q1/scripts/verify_manuscript_q1.py`: Upgraded verification suite with SQLite parity gate.

### 2.2 Track 1 Conference Deliverables Frozen
Cryptographic verification confirmed 100% byte-for-byte consistency across all Track 1 conference files:
* `manuscript/main.pdf` (179,471 bytes): SHA-256 `abb1b4b3cd1baeabf3fc1f9232661f5594f7f233f75db0d5ec247d06f882e4cb`
* `manuscript/main_authors.pdf` (180,875 bytes): SHA-256 `402215fde6223126c4809f988baadcd86e4b0920318eb05b101a6e65b148f373`
* `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes): SHA-256 `bb2c591b009979b5f117ce5458d867c80f4b56ddb4a093cae59ea2bd30e87de4`
* `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes): SHA-256 `ab0fd2cd4546997e4cc386ce960aa14ceca77870f8fbf61c71cc225a29d00145`

Result: **0 byte modifications. 100% frozen.**

---

## 3. Methodological and Analytical Procedures

### 3.1 Forensic Parity Analysis: SQLite Ground Truth vs. Task 11 Metadata
A forensic audit comparing Task 11 outputs against `npm_ecosystem.db` identified that while the reach columns had been corrected in Task 11, the maintainer usernames, dependent counts, and strategy ranks were still populated from a static dictionary originating in Task 09. Specifically:
* `@solana/web3.js`: Listed `lorisleiva` with 160 dependents, whereas in SQLite `package_maintainers` lists `solana-devs` (1 maintainer total) with direct/transitive dependents of `6 / 31`, Portfolio Rank `#181`, Greedy `>100`, Exact Union Rank `#1,385`, and Pareto Rank `#562`.
* `nx`: Listed `frozenpandaman` with 123 dependents, whereas in SQLite `nx` is governed by 8 maintainers (`jameshenry`, `nrwlowner`, etc.) with direct/transitive dependents of `5 / 52`, and lead maintainer `jameshenry` ranks `#31` (Portfolio), `>100` (Greedy), `#899` (Union), and `#1,529` (Pareto).
* `eslint-config-prettier` & `eslint-plugin-prettier`: Listed `lydell` with 0 & 2 dependents and ranks `#741 / >100 / #35 / #20`. In SQLite, `lydell` has direct/transitive dependents `14 / 15` and `6 / 7`, Portfolio Rank `#561`, Greedy Rank `#35` (captured inside Budget 100!), Exact Union Rank `#39`, and Pareto Rank `#29`.
* `chalk` & `ansi-styles`: Listed `sindresorhus` with 0 dependents and Portfolio Rank `#1`. In SQLite, `sindresorhus` is Portfolio Rank `#2` (570 packages, behind only bot/aggregator accounts), Greedy Rank `#1`, Exact Union Rank `#1`, and Pareto Rank `#1`, with direct/transitive dependents `544 / 3,416` and `25 / 4,052`.
* `debug`: Listed only `qix` with 3 dependents, omitting co-maintainer `tootallnate` and true direct/transitive dependents `541 / 3,525`. Co-maintainer `tootallnate` ranks `#199` (Portfolio), `#8` (Greedy), `#6` (Union), and `#8` (Pareto), which explains why Greedy skips `qix`.
* `node-ipc`: Listed `riaevangelist` with 14 dependents and ranks `#482 / #112`. In SQLite, `node-ipc` has 12 maintainers, direct/transitive dependents `2 / 4`, Portfolio Rank `#2,562`, Greedy `>100`, Exact Union Rank `#2,560`, and Pareto Rank `#454`.

### 3.2 Dynamic SQLite Graph Extraction Implementation
Rewrote `extract_incident_case_study()` in `scripts/extract_q1_temporal_and_authority_tables.py` to perform full programmatic extraction:
1. Load `data/npm_ecosystem.db.zip` and initialize `study_structural_interventions.py` graph propagation structures.
2. Propagate endpoint bitsets through Kosaraju condensation to compute maintainer-level workflow repository closures.
3. Compute exact 1-indexed ranks for all 12,217 maintainers across Portfolio Size, Exact Union, Lazy Greedy Coverage (budget 100), and full Pareto Hybrid ($\alpha=0.50$).
4. Query `package_metrics` for `direct_dependents` and `transitive_dependents`.
5. Query `package_maintainers` for maintainer count $|M(p)|$.
6. Format maintainer column as `\texttt{maintainer} (|M(p)|)` and dependents as `direct / transitive`.
7. Wrap tabular output with `\resizebox{\textwidth}{!}{% ... }%` to eliminate any possible overfull `\hbox`.

### 3.3 Verification Suite Hardening
Upgraded `manuscript_q1/scripts/verify_manuscript_q1.py`:
* Programmatically parses `q1_incident_case_study_table.tex` and validates all 16 rows against expected SQLite values.
* Asserts that `qix`'s version-continuous union reach is reported as `1,476` (and verifies that the corrupted back-calculated value `2,362` does not exist anywhere in Section 5).
* Validates PDF font embedding, zero Type 3 fonts, zero undefined citations, zero overfull `\hbox` protrusions, and conference freeze invariants.

---

## 4. Empirical Results and Quantitative Findings

### 4.1 Programmatic SQLite & CSV Incident Case Study (Table 4)

| Package Name | Maintainer ($|M(p)|$) | Pre-Event Ver. | Dependents (Dir / Trans) | Workflow Reach ($R_{\text{wf}}$ Name) | Workflow Reach ($R_{\text{wf}}$ Ver.) | Phantom Inflation | Portfolio Rank | Greedy Rank ($|S|=100$) | Exact Union Rank | Pareto Rank ($\alpha=0.5$) |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| **`debug`** | `qix` (2) | 4.4.1 | 541 / 3,525 | 1,462 | 1,162 | **+25.8%** | #2,298 | #>100 | #8 | #48 |
| **`chalk`** | `sindresorhus` (1) | 5.6.0 | 544 / 3,416 | 1,125 | 587 | **+91.7%** | #2 | #1 | #1 | #1 |
| **`ansi-styles`** | `sindresorhus` (1) | 6.2.1 | 25 / 4,052 | 1,376 | 740 | **+85.9%** | #2 | #1 | #1 | #1 |
| **`simple-swizzle`** | `qix` (1) | 0.2.2 | 1 / 357 | 120 | 31 | **+287.1%** | #2,298 | #>100 | #8 | #48 |
| **`backslash`** | `qix` (1) | 0.2.0 | 1 / 1 | 0 | 0 | **0.0%** | #2,298 | #>100 | #8 | #48 |
| **`eslint-config-prettier`** | `lydell` (3) | 10.1.5 | 14 / 15 | 10 | 10 | **0.0%** | #561 | #35 | #39 | #29 |
| **`eslint-plugin-prettier`** | `lydell` (6) | 5.2.3 | 6 / 7 | 5 | 5 | **0.0%** | #561 | #35 | #39 | #29 |
| **`@solana/web3.js`** | `solana-devs` (1) | 2.1.0* | 6 / 31 | 4 | 4 | **0.0%** | #181 | #>100 | #1,385 | #562 |
| **`nx`** | `jameshenry` (8) | 21.5.0* | 5 / 52 | 2 | 2 | **0.0%** | #31 | #>100 | #899 | #1,529 |
| **`node-ipc (v12)`** | `riaevangelist` (12) | 12.0.0 | 2 / 4 | 4 | 4 | **0.0%** | #2,562 | #>100 | #2,560 | #454 |
| **`node-ipc (v10)`** | `riaevangelist` (12) | 10.1.0 | 2 / 4 | 4 | 4 | **0.0%** | #2,562 | #>100 | #2,560 | #454 |
| **`@tanstack/history`** | `tannerlinsley` (5) | 1.114.15 | 3 / 13 | 1 | 1 | **0.0%** | #163 | #>100 | #1,694 | #443 |
| **`@ctrl/tinycolor`** | `scttcper` (1) | 4.1.0 | 7 / 455 | 10 | 9 | **+11.1%** | #5,765 | #>100 | #366 | #490 |
| **`@opensearch-project/opensearch`** | `peterzhuamazon` (3) | 3.6.0 | 0 / 0 | 0 | 0 | **0.0%** | #2,548 | #>100 | #1,754 | #3,299 |
| **`@mastra/core`** | `tylerbarnes` (9) | 0.0.0* | 0 / 0 | 0 | 0 | **0.0%** | #416 | #>100 | #5,387 | #6,334 |
| **`echarts-for-react`** | `atool` (1) | 3.0.0 | 0 / 0 | 0 | 0 | **0.0%** | #398 | #>100 | #1,971 | #744 |

*Note*: For co-maintained packages, $|M(p)|$ is shown in parentheses; `debug` is co-maintained by `tootallnate` (#199 Portfolio, #8 Greedy, #6 Union, #8 Pareto) and phished account `qix` (#2,298 Portfolio, >100 Greedy, #8 Union, #48 Pareto).

### 4.2 Reconciled Section 5 Narrative Text
The empirical narrative in `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex` (lines 96–99) now reads:
> "\item \textbf{Co-Maintenance Masking:} Maintainer \texttt{qix} (governing \texttt{debug}, \texttt{simple-swizzle}, and \texttt{backslash}) reaches $2{,}971$ workflow repositories across their 3-package portfolio in the name-collapsed graph ($|E_{\text{qix}}| = 2{,}971$, $41.43\%$) and $1{,}476$ repositories in the version-continuous graph ($20.58\%$). However, \texttt{qix} is excluded by unweighted Greedy Coverage beyond budget 100 (rank $\#>100$) because co-maintainers with broader portfolios (\texttt{sindresorhus} and \texttt{tootallnate}) satisfy marginal coverage first, leaving all $2{,}971$ repositories residually exposed. Under Exact Union and Pareto Hybrid ($\alpha=0.50$), \texttt{qix} is correctly prioritized at rank \textbf{$\#8$} and \textbf{$\#48$}, respectively (rising to \textbf{$\#5$} in the version-continuous graph)."

---

## 5. Invariants, Validations, and Integrity Checks

### 5.1 Verification Test Suite Output Summary
The automated verification script `manuscript_q1/scripts/verify_manuscript_q1.py` ran with zero errors:

```json
{
  "status": "PASS",
  "checks": {
    "abstract": {
      "check": "abstract_word_count",
      "word_count": 188,
      "min_allowed": 100,
      "max_allowed": 200,
      "passed": true
    },
    "named_pdf": {
      "pdf_name": "main_q1.pdf",
      "exists": true,
      "passed": true,
      "pages": 15,
      "file_bytes": 278629,
      "fonts_embedded": true,
      "zero_type_3": true,
      "zero_overfull_hbox": true,
      "zero_undefined_citations": true,
      "zero_missing_glyphs": true,
      "total_fonts": 36,
      "type_3_count": 0,
      "unembedded_count": 0
    },
    "anonymous_pdf": {
      "pdf_name": "main_q1_anonymous.pdf",
      "exists": true,
      "passed": true,
      "pages": 14,
      "file_bytes": 276717,
      "fonts_embedded": true,
      "zero_type_3": true,
      "zero_overfull_hbox": true,
      "zero_undefined_citations": true,
      "zero_missing_glyphs": true,
      "total_fonts": 36,
      "type_3_count": 0,
      "unembedded_count": 0
    },
    "numerical_consistency": {
      "check": "numerical_consistency",
      "passed": true,
      "errors": []
    },
    "conference_freeze": {
      "check": "conference_freeze_invariants",
      "passed": true,
      "errors": []
    }
  }
}
```

### 5.2 PDF Font and Geometry Invariants

| Invariant Metric | Named Journal PDF (`main_q1.pdf`) | Anonymous Journal PDF (`main_q1_anonymous.pdf`) | Status |
|---|---|---|---|
| **Page Count** | 15 pages (IEEE Transactions standard) | 14 pages (Title/author metadata suppressed) | **PASS** |
| **Page Format** | Letter (8.5 × 11 in) | Letter (8.5 × 11 in) | **PASS** |
| **Overfull Boxes > 1 pt** | 0 | 0 | **PASS** |
| **Undefined Citations (`?`)** | 0 | 0 | **PASS** |
| **Undefined References (`??`)** | 0 | 0 | **PASS** |
| **Missing Glyphs** | 0 | 0 | **PASS** |
| **Total Fonts Embedded** | 36 / 36 (100%) | 36 / 36 (100%) | **PASS** |
| **Type 3 Fonts** | 0 | 0 | **PASS** |
| **Abstract Word Count** | 188 words ($\le 200$) | 188 words ($\le 200$) | **PASS** |
| **Table 4 Parity Gate** | 16/16 rows verified against SQLite & CSV | 16/16 rows verified against SQLite & CSV | **PASS** |

---

## 6. Deliverables, File Manifest, and Next Steps

### 6.1 Generated Deliverables Manifest
1. **Named Journal PDF**: [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) (278,629 bytes, 15 pages, 0 overfull boxes, 0 Type 3 fonts).
2. **Double-Anonymous Journal PDF**: [`manuscript_q1/main_q1_anonymous.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1_anonymous.pdf) (276,717 bytes, 14 pages, 0 overfull boxes, 0 Type 3 fonts).
3. **Q1 Source Zip Archive**: [`NPM_Supply_Chain_Q1_Journal_Source.zip`](file:///home/ashik/Desktop/npm-supply-chain-research/NPM_Supply_Chain_Q1_Journal_Source.zip) (2,313,404 bytes, SHA-256: `9c139f3b20d00341cbb3d989d6853e40f963156d5ef2524d5d5c22e5c3256baf`, 52 files).
4. **Verification Report**: [`manuscript_q1/results/q1_verification_report.json`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/results/q1_verification_report.json).
5. **Programmatic Case Study Outputs**:
   - CSV: [`manuscript/results/q1_journal/q1_incident_case_study.csv`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/results/q1_journal/q1_incident_case_study.csv)
   - LaTeX: [`manuscript/results/q1_journal/q1_incident_case_study_table.tex`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/results/q1_journal/q1_incident_case_study_table.tex)
   - Active Manuscript Table: [`manuscript_q1/tables/q1_incident_case_study_table.tex`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/tables/q1_incident_case_study_table.tex)
6. **Dynamic Table Generator**: [`scripts/extract_q1_temporal_and_authority_tables.py`](file:///home/ashik/Desktop/npm-supply-chain-research/scripts/extract_q1_temporal_and_authority_tables.py).
7. **Verification & Packaging Automation**:
   - [`manuscript_q1/scripts/verify_manuscript_q1.py`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/scripts/verify_manuscript_q1.py)
   - [`manuscript_q1/scripts/package_q1.py`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/scripts/package_q1.py)

### 6.2 Submission Readiness Summary
* **Track 1 (IEEE Conference — ICEEICT 2027)**: Completely locked and ready for immediate submission with [`manuscript/main.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/main.pdf) / [`manuscript/main_authors.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/main_authors.pdf) and `NPM_Supply_Chain_IEEE_Anonymous_Source.zip`.
* **Track 2 (Q1 Journal Submission)**:
  * **IEEE TSE / IEEE TDSC**: Ready for submission with [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) and [`NPM_Supply_Chain_Q1_Journal_Source.zip`](file:///home/ashik/Desktop/npm-supply-chain-research/NPM_Supply_Chain_Q1_Journal_Source.zip). Abstract (188 words) satisfies ScholarOne's 200-word constraint.
  * **ACM TOSEM / Springer EMSE**: Ready for submission with [`manuscript_q1/main_q1_anonymous.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1_anonymous.pdf) for double-anonymous peer review.
