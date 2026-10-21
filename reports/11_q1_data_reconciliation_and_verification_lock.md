# Active Verification Session 11: Q1 Journal Data Reconciliation, IEEE TSE Abstract Enforcement, and Automated Verification Suite Lock

## 1. Executive Summary & Session Objectives
* **Session Identifier**: `11_q1_data_reconciliation_and_verification_lock`
* **Date & Timestamp**: 2026-10-21T16:00:00+06:00
* **Target Publication Venues**:
  * *IEEE Transactions on Software Engineering (TSE)* (Primary target; strict 100–200 word abstract limit, double-column IEEEtran journal format)
  * *ACM Transactions on Software Engineering and Methodology (TOSEM)* (Double-anonymous review)
  * *IEEE Transactions on Dependable and Secure Computing (TDSC)*
  * *Springer Empirical Software Engineering (EMSE)*
* **Author Affiliation**: Department of Computer Science and Engineering, Hajee Mohammad Danesh Science and Technology University (HSTU), Dinajpur 5200, Bangladesh
* **Compilation Toolchain**: Native `tectonic` 0.17.0 (`~/.local/bin/tectonic` invoking XeTeX engine with automatic BibTeX and font package caching)
* **Conference Deliverables Invariant (Track 1)**: `manuscript/main.pdf` (179,471 bytes, exactly 6.0 A4 pages), `manuscript/main_authors.pdf` (180,875 bytes, exactly 6.0 A4 pages), `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes), and `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes) remain **100% frozen with zero byte changes** and verified against cryptographic SHA-256 hashes.
* **Core Objectives Achieved**:
  1. **Table 4 Data Bug Fixed**: Corrected `scripts/extract_q1_temporal_and_authority_tables.py` to extract ground-truth package-level workflow reach ($R_{\text{wf}}$) directly from `manuscript/results/graph_validity/per_package.csv`, eliminating the maintainer-union reach conflation. Regenerated `manuscript/results/q1_journal/q1_incident_case_study.csv`, `manuscript/results/q1_journal/q1_incident_case_study_table.tex`, and `manuscript_q1/tables/q1_incident_case_study_table.tex`.
  2. **Narrative Text Reconciled**: Updated `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex` to report exact ground-truth values (`debug`: 1,462 vs 1,162; `chalk`: 1,125 vs 587; `ansi-styles`: 1,376 vs 740; `simple-swizzle`: 120 vs 31), while explicitly disambiguating maintainer `qix`'s 3-package portfolio union reach ($|E_{\text{qix}}| = 2,971$).
  3. **Strict IEEE TSE Abstract Word Limit Enforced**: Tightened `manuscript_q1/sections/00_abstract.tex` from 212 words down to **exactly 188 words** (within the strict 100–200 word TSE limit) while preserving every core quantitative invariant ($N=25,228$, $M=12,217$, $R_{\text{wf}}=7,171$, $\alpha=0.50$ sweet spot at $70.0\%$ coverage and $31.2\%$ exposure reduction, supermodular $P(S)=1,022$, package-level sole-maintainer bottleneck $67.37\%$ vs $27.32\%$, and the 45-snapshot release-authority / 1,848 SemVer edge audit).
  4. **BibTeX Author Completeness Enforced**: Audited `manuscript_q1/bibliography/references_q1.bib` and `.bbl`; verified all entries have full author lists, resolving truncated author lists for `gao2025emse` (Gao, Xiang and Shen, Yijun and Sun, Hailong and Guo, Yu), `guo2026`, and `ralph2020`.
  5. **Type 3 Font Elimination in Figures**: Created `manuscript_q1/scripts/render_q1_figures.py` setting `pdf.fonttype = 42` and `ps.fonttype = 42`, re-rendering `q1_pareto_frontier.pdf` and `q1_supermodular_p_and_weights.pdf` to eliminate all 7 Type 3 bitmap fonts and enforce 100% TrueType font embedding.
  6. **Dual PDF Compilation**: Compiled both Named (`manuscript_q1/main_q1.pdf`, 15 pages, 277,683 bytes) and Double-Anonymous (`manuscript_q1/main_q1_anonymous.pdf`, 14 pages, 275,784 bytes) journal manuscripts with 0 overfull `\hbox` protrusions $> 1\text{ pt}$, 0 undefined citations, and 0 missing glyphs.
  7. **Automated Q1 Verification Suite**: Developed and executed `manuscript_q1/scripts/verify_manuscript_q1.py`, writing `manuscript_q1/results/q1_verification_report.json` with status `PASS`.
  8. **Source Packaging**: Created `manuscript_q1/scripts/package_q1.py` and generated `NPM_Supply_Chain_Q1_Journal_Source.zip` (52 files, 2,310,376 bytes).

---

## 2. Artifacts and Datasets Audited

### 2.1 Audited Datasets and Extraction Scripts
1. `scripts/generate_task04_incident_validation.py`: Ground-truth incident extraction script defining canonical per-package metrics.
2. `manuscript/results/graph_validity/per_package.csv`: Canonical per-package ground-truth data file containing version-continuous and name-collapsed reaches across 25,228 packages.
3. `scripts/extract_q1_temporal_and_authority_tables.py`: Extraction script generating journal Tables 4, 8, and 9. Modified to pull exact package-level reach.
4. `manuscript/results/q1_journal/q1_incident_case_study.csv` & `q1_incident_case_study_table.tex`: Corrected case study table.
5. `manuscript_q1/sections/00_abstract.tex`: Verbatim abstract inspected and trimmed to 188 words.
6. `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex`: Section narrative cross-checked and aligned.
7. `manuscript_q1/bibliography/references_q1.bib`: Bibliographic database inspected and verified.
8. `manuscript/results/experiments/q1_journal_experiments.json`: Verification of Pareto, supermodular, and heterogeneous optimization outputs.

### 2.2 Track 1 Conference Deliverables Frozen
The following Track 1 conference files were checked against their expected cryptographic checksums:
* `manuscript/main.pdf` (179,471 bytes): SHA-256 `abb1b4b3cd1baeabf3fc1f9232661f5594f7f233f75db0d5ec247d06f882e4cb`
* `manuscript/main_authors.pdf` (180,875 bytes): SHA-256 `402215fde6223126c4809f988baadcd86e4b0920318eb05b101a6e65b148f373`
* `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes): SHA-256 `bb2c591b009979b5f117ce5458d867c80f4b56ddb4a093cae59ea2bd30e87de4`
* `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes): SHA-256 `ab0fd2cd4546997e4cc386ce960aa14ceca77870f8fbf61c71cc225a29d00145`

Result: **0 byte modifications. 100% frozen.**

---

## 3. Methodological and Analytical Procedures

### 3.1 Forensic Reconciliation of Table 4 Reach Bug
* **Root Cause Analysis**: In Task 09, `scripts/extract_q1_temporal_and_authority_tables.py` inadvertently reported maintainer-portfolio union reach values rather than single-package reach values for packages maintained by `qix` and `sindresorhus`, then back-calculated version-continuous reach using percentage inflation ratios. For example:
  * Maintainer `qix` maintains 3 packages in the ecosystem (`debug`, `simple-swizzle`, `backslash`), whose combined union reach is 2,971 repositories. Task 09 reported `2,971` as the reach of `debug` itself, and `2,969` for `simple-swizzle`, despite `simple-swizzle` having only 357 total transitive package dependents.
  * In addition, raw unescaped `%` symbols in LaTeX generation caused TeX parser line trunction, creating an overfull `\hbox` of 34.66 pt.
* **Surgical Fix**:
  1. Updated `extract_incident_case_study()` in `scripts/extract_q1_temporal_and_authority_tables.py` to index `manuscript/results/graph_validity/per_package.csv` by package name and read `reach_name` and `reach_version` directly.
  2. For zero-reach packages (`backslash`, `@opensearch-project/opensearch`, `@mastra/core`, `echarts-for-react`), set inflation to `0.0\%` rather than `NaN`.
  3. Properly escaped all `%` signs as `\%`.
  4. Adjusted table formatting with `\setlength{\tabcolsep}{0.5pt}` in `q1_incident_case_study_table.tex` to ensure zero column overflow in two-column format.
  5. Synchronized files across `manuscript/results/q1_journal/` and `manuscript_q1/tables/`.

### 3.2 IEEE TSE Abstract Enforcement (100–200 Words)
* *IEEE TSE* submission guidelines mandate an abstract of no more than 200 words. ScholarOne enforces this cutoff strictly upon submission.
* The draft in Task 10 stood at 212 words.
* We condensed the text to **188 words** without dropping any empirical invariant:
  * Ecosystem scale: $N = 25,228$, $M = 12,217$, $R_{\text{wf}} = 7,171$.
  * Three competing objectives: $C(S)$ coverage, $H(S)$ exposure, $P(S)$ supermodular exclusion.
  * Budget-100 greedy vs. exact-union dilemma: $77.2\%$ coverage leaving $85.6\%$ exposed vs. eliminating $33.8\%$ exposure at $-1,131$ repos.
  * Hybrid scalarization Pareto sweet spot: $\alpha = 0.50$ ($70.0\%$ coverage, $31.2\%$ exposure reduction).
  * Direct supermodular optimization: $P(S) = 1,022$ (+27.8% over greedy).
  * Sole-maintainer bottleneck resolution: $+40.05\text{ pp}$ gain ($27.32\% \rightarrow 67.37\%$).
  * Temporal release-authority audit: 45 snapshots, 1,848 SemVer edges.

### 3.3 Type 3 Font Elimination in Vector Figures
* An inspection of `pdffonts` on `main_q1.pdf` revealed 7 Type 3 bitmap fonts originating from Matplotlib's default text rendering in `q1_pareto_frontier.pdf` and `q1_supermodular_p_and_weights.pdf`.
* Created `manuscript_q1/scripts/render_q1_figures.py` with:
  ```python
  import matplotlib
  matplotlib.rcParams['pdf.fonttype'] = 42
  matplotlib.rcParams['ps.fonttype'] = 42
  ```
* Re-rendered both figures with TrueType embedding and recompiled the PDF. Resulting PDF contains **0 Type 3 fonts** across all 36 embedded fonts.

### 3.4 Automated Verification and Packaging Architecture
* Implemented `manuscript_q1/scripts/verify_manuscript_q1.py` executing 5 distinct test suites:
  1. Abstract word count (100–200 words).
  2. Named PDF geometry, font embedding, overfull boxes, undefined citations.
  3. Anonymous PDF geometry, font embedding, overfull boxes, undefined citations.
  4. Numerical consistency between LaTeX source, generated tables, and ground truth files.
  5. Cryptographic hash check for Track 1 conference files.
* Implemented `manuscript_q1/scripts/package_q1.py` packaging all clean sources, tables, figures, scripts, and documentation into `NPM_Supply_Chain_Q1_Journal_Source.zip`.

---

## 4. Empirical Results and Quantitative Findings

### 4.1 Reconciled Ground Truth vs. Corrupted Task 09 Output (Table 4)

| Compromised Package | Maintainer | Deps | Task 04 / Canonical Ground Truth ($R_{\text{wf}}$ Name vs. Version) | Task 09 Corrupted Output | Phantom Inflation | Maintainer Prioritization Ranks (Portfolio / Greedy / Union / Pareto) |
|---|---|---:|---|---|---:|---|
| **`debug`** | `qix` | 3 | **1,462 vs. 1,162** (+300 repos) | 2,971 vs. 2,362 | **+25.8%** | #2,298 / #>100 / #8 / #4 |
| **`chalk`** | `sindresorhus` | 0 | **1,125 vs. 587** (+538 repos) | 5,293 vs. 2,761 | **+91.7%** | #1 / #1 / #1 / #1 |
| **`ansi-styles`** | `sindresorhus` | 0 | **1,376 vs. 740** (+636 repos) | 5,133 vs. 2,761 | **+85.9%** | #1 / #1 / #1 / #1 |
| **`simple-swizzle`** | `qix` | 1 | **120 vs. 31** (+89 repos) | 2,969 vs. 767 | **+287.1%** | #2,298 / #>100 / #8 / #4 |
| **`backslash`** | `qix` | 0 | **0 vs. 0** | 0 vs. 0 | **0.0%** | #2,298 / #>100 / #8 / #4 |
| **`eslint-config-prettier`** | `lydell` | 0 | **10 vs. 10** | 10 vs. 10 | **0.0%** | #741 / #>100 / #35 / #20 |
| **`eslint-plugin-prettier`** | `lydell` | 2 | **5 vs. 5** | 5 vs. 5 | **0.0%** | #741 / #>100 / #35 / #20 |
| **`@solana/web3.js`** | `lorisleiva` | 160 | **4 vs. 4** | 4 vs. 4 | **0.0%** | #1,834 / #>100 / #342 / #248 |
| **`nx`** | `frozenpandaman` | 123 | **2 vs. 2** | 2 vs. 2 | **0.0%** | #652 / #>100 / #215 / #162 |
| **`node-ipc (v12)`** | `riaevangelist` | 14 | **4 vs. 4** | 4 vs. 4 | **0.0%** | #482 / #>100 / #112 / #82 |
| **`node-ipc (v10)`** | `riaevangelist` | 14 | **4 vs. 4** | 4 vs. 4 | **0.0%** | #482 / #>100 / #112 / #82 |
| **`@tanstack/history`** | `tannerlinsley` | 1 | **1 vs. 1** | 1 vs. 1 | **0.0%** | #514 / #>100 / #148 / #108 |
| **`@ctrl/tinycolor`** | `scttcper` | 0 | **10 vs. 9** | 10 vs. 9 | **+11.1%** | #921 / #>100 / #280 / #215 |
| **`@opensearch-project/opensearch`** | `peterzhuamazon` | 0 | **0 vs. 0** | 0 vs. 0 | **0.0%** | #2,548 / #>100 / #1754 / #1420 |
| **`@mastra/core`** | `tylerbarnes` | 0 | **0 vs. 0** | 0 vs. 0 | **0.0%** | #416 / #>100 / #5387 / #4120 |
| **`echarts-for-react`** | `atool` | 0 | **0 vs. 0** | 0 vs. 0 | **0.0%** | #398 / #>100 / #1971 / #1680 |

### 4.2 Narrative Reconciliation in Section 5
The empirical narrative in `manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex` now clearly distinguishes between maintainer-level portfolio union reach and single-package reach:
> "Crucially, maintainer-level reach must not be confused with single-package blast radius: maintainer \texttt{qix}'s complete 3-package portfolio reaches $|E_{\text{qix}}| = 2{,}971$ workflow repositories in the name graph and $2{,}362$ in the version graph, but individual packages within that portfolio exhibit starkly divergent reach ($1{,}462$ vs. $1{,}162$ for \texttt{debug}, $120$ vs. $31$ for \texttt{simple-swizzle}, and $0$ for \texttt{backslash})."

### 4.3 Verbatim IEEE TSE-Compliant Abstract (188 Words)
```latex
\begin{abstract}
Centralized package registries rely on maintainer accounts as root authorities for software publication. However, prioritizing maintainers for proactive security interventions faces fundamental structural tensions. We present an empirical study of maintainer prioritization across $N = 25{,}228$ npm packages, $M = 12{,}217$ maintainer accounts, and $R_{\text{wf}} = 7{,}171$ continuous-integration workflow repositories. We formalize maintainer selection across three competing objectives: submodular coverage $C(S)$, modular scenario exposure reduction $H(S)$, and supermodular all-source exclusion $P(S)$. We prove that greedy coverage and exact-union ranking optimize opposing properties: at budget 100, greedy coverage achieves $77.2\%$ coverage but leaves $85.6\%$ of endpoints exposed, whereas exact union eliminates $33.8\%$ of exposure mass but covers $1{,}131$ fewer repositories. To resolve this conflict, we formulate a hybrid scalarization $J_\alpha(S)$. The Pareto frontier reveals an empirical sweet spot at $\alpha = 0.50$, achieving $70.0\%$ coverage and $31.2\%$ exposure reduction. Directly optimizing supermodular exclusion secures $P(S) = 1{,}022$ fully defended endpoints (+27.8\% over greedy). Furthermore, incorporating heterogeneous maintainer priors resolves a package-level sole-maintainer bottleneck, raising captured exposure mass from $27.32\%$ to $67.37\%$. Finally, an audit across 45 historical pre-compromise snapshots and 1,848 reconstructed SemVer edges validates pre-event release-authority metadata availability.
\end{abstract}
```

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
      "file_bytes": 277683,
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
      "file_bytes": 275784,
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

---

## 6. Deliverables, File Manifest, and Next Steps

### 6.1 Generated Deliverables Manifest
1. **Named Journal PDF**: [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) (277,683 bytes, 15 pages).
2. **Double-Anonymous Journal PDF**: [`manuscript_q1/main_q1_anonymous.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1_anonymous.pdf) (275,784 bytes, 14 pages).
3. **Q1 Source Zip Archive**: [`NPM_Supply_Chain_Q1_Journal_Source.zip`](file:///home/ashik/Desktop/npm-supply-chain-research/NPM_Supply_Chain_Q1_Journal_Source.zip) (2,310,376 bytes, SHA-256: `8c8cea363db12751dd99fca5f37f418a38d4c3b4be948d6d96038bdc3519aa0e`, 52 files).
4. **Verification Report**: [`manuscript_q1/results/q1_verification_report.json`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/results/q1_verification_report.json).
5. **Reconciled Case Study Table**:
   - CSV: `manuscript/results/q1_journal/q1_incident_case_study.csv`
   - LaTeX: `manuscript/results/q1_journal/q1_incident_case_study_table.tex`
   - Active Manuscript Table: `manuscript_q1/tables/q1_incident_case_study_table.tex`
6. **Vector Figure Generation Script**: `manuscript_q1/scripts/render_q1_figures.py`.
7. **Verification & Packaging Scripts**:
   - `manuscript_q1/scripts/verify_manuscript_q1.py`
   - `manuscript_q1/scripts/package_q1.py`

### 6.2 Next Steps
* **Track 1 (IEEE Conference — ICEEICT 2027)**: Ready for immediate submission using `manuscript/main.pdf` (or `manuscript/main_authors.pdf`) and `NPM_Supply_Chain_IEEE_Anonymous_Source.zip`.
* **Track 2 (Q1 Journal — IEEE TSE / ACM TOSEM / IEEE TDSC / EMSE)**:
  * For *IEEE TSE* / *IEEE TDSC*: Submit `manuscript_q1/main_q1.pdf` and upload `NPM_Supply_Chain_Q1_Journal_Source.zip`. Form abstract matches the 188-word limit.
  * For *ACM TOSEM* / *Springer EMSE*: Submit `manuscript_q1/main_q1_anonymous.pdf` for double-anonymous peer review.
