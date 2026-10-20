# Active Verification Session 10: Assembly, Multi-Budget Integration, and Tectonic Compilation of Standalone Q1 Journal Manuscript (`manuscript_q1/main_q1.pdf`)

## 1. Execution Metadata
* **Session Identifier**: `10_q1_journal_manuscript_build_and_audit`
* **Date & Timestamp**: 2026-10-21T03:57:30+06:00
* **Target Publication Venues**: *IEEE Transactions on Software Engineering (TSE)* / *ACM Transactions on Software Engineering and Methodology (TOSEM)* / *IEEE Transactions on Dependable and Secure Computing (TDSC)*
* **Author Affiliation**: Department of Computer Science and Engineering, Hajee Mohammad Danesh Science and Technology University (HSTU), Dinajpur 5200, Bangladesh
* **Compilation Toolchain**: Native `tectonic` 0.17.0 (`~/.local/bin/tectonic` invoking XeTeX engine with automatic BibTeX and font package caching)
* **Output Artifact**: `manuscript_q1/main_q1.pdf` (282,184 bytes, 15 pages, letter format, standard double-column `IEEEtran` `compsoc` journal class)
* **Word Count**: 9,367 words across 10 complete sections (spanning target range of 8,500–10,500 words)
* **Conference Freeze Verification**: `manuscript/main.pdf` (179,471 bytes, exactly 6.0 A4 pages) and `manuscript/main_authors.pdf` (180,875 bytes, exactly 6.0 A4 pages) remain 100% frozen with 13/13 compliance checks and 11/11 package validation checks passing.

---

## 2. Quantitative and Structural Findings

### 2.1 Complete Architectural Structure of the Q1 Journal Manuscript
The standalone journal repository (`manuscript_q1/`) was scaffolded and populated with 10 self-contained sections, 9 LaTeX tables, 6 vector figures, and 23 verified peer-reviewed literature citations:

1. `sections/00_abstract.tex`: IEEE TSE-compliant abstract (212 words) synthesizing the multi-objective formalization, the $\alpha=0.50$ Pareto knee ($70.0\%$ coverage, $31.2\%$ exposure reduction), the supermodular $P(S)=1,022$ breakthrough, the $+40.05\text{ pp}$ package-level sole-maintainer bottleneck gain ($67.37\%$ vs $27.32\%$), and the 45-snapshot release authority audit.
2. `sections/01_introduction.tex`: Extensive motivation contrasting registry-level versus organizational defenders, defining the five Research Questions (RQ1–RQ5), and stating our four primary contributions.
3. `sections/02_related_work.tex`: Deep literature synthesis positioning our work against topological concentration (Zimmermann, Zahan), malicious package detection and call graphs (AMALFI, Guo, Ohm, Weeraddana TOSEM 2024, Gao EMSE 2025), registry provenance (Okafor USENIX 2025, Schorlemmer S&P 2024, He PACMSE 2025), and temporal graph evaluation (Pinckney, Rahman). Includes Table 1 (Literature Positioning).
4. `sections/03_data_and_graph_construction.tex`: Complete accounting of the 25,228-package, 12,217-maintainer, and 7,171-workflow-repository ecosystem, detailing Kosaraju SCC cycle condensation (82 cyclic nodes in 68 SCCs on name graph; 68 cyclic components across 40,806 nodes on version graph), 658 repository URL disagreements, and the 5 verified phantom witnesses (`pseudomap`, `is`, `foreach`, `indexof`, `has-color`).
5. `sections/04_objectives_and_optimization_framework.tex`: Formal mathematical definitions of $C(S)$, $H(S)$, and $P(S)$; proof of Proposition 1 (monotone submodularity of $J_\alpha(S)$ and $(1-1/e)$ approximation guarantees); formalization of the Minimum-Remaining-Source heuristic; definitions of heterogeneous risk formulations ($w_m^{\text{sole}}$, $w_m^{\text{log}}$, and $H_{\text{pkg-sole}}$); and exact finite-population hypergeometric expectations with Monte Carlo standard errors ($\text{MCSE}_C = 37.5$ repos, $\text{MCSE}_H = 0.026\text{ pp}$).
6. `sections/05_empirical_results_rq1_to_rq3.tex`: Multi-budget trajectories across $|S| \in \{1, 5, 10, 25, 50, 100\}$ (Table 3), the fixed-graph descriptive divergence ($\Delta C = +1,131$ repos, $\Delta H = -22.31\text{ pp}$, $\Delta P = +266$ repos), the $42.44\%$ representation shrinkage ($462,170 \rightarrow 266,016$ identity-repository pairs), the $+13.43\text{ pp}$ cross-representation selection penalty on version graphs, and the complete 16-assessment case study across 15 real-world compromised packages (Table 4) with explicit non-forecast qualifications.
7. `sections/06_pareto_and_heterogeneous_results_rq4.tex`: Presentation of the Pareto frontier across scalarization weights $\alpha$ (Table 5, Fig. 4), analyzing the $\alpha=0.50$ sweet spot; the supermodular $P(S)=1,022$ breakthrough (Table 6, Fig. 5) delivering $+222$ repos over greedy and $+488$ repos over union; and the heterogeneous risk results (Table 7) showing that weight-aware package-sole optimization eliminates $67.37\%$ of sole-maintainer exposure mass ($+40.05\text{ pp}$ improvement over unweighted exact union).
8. `sections/07_temporal_authority_and_prospective_design_rq5.tex`: Integration of the 6-dimension ablation suite, the 1,848-edge bounded recursive SemVer cutoff reconstruction ($99.89\%$ completeness under $t_{\text{cutoff}} < t_{\text{incident}}$, Table 8), the 45-snapshot release authority and provenance audit (Table 9: $97.8\%$ predecessor availability, $93.3\%$ repository continuity, $0.0\%$ public Sigstore provenance), and the pre-registered 100-package prospective cohort protocol (horizon ending January 18, 2027).
9. `sections/08_threats_to_validity_and_ethics.tex`: Comprehensive 4-part ACM SIGSOFT Empirical Standards analysis addressing Construct, Internal, External/Observational, and Conclusion validity (grounded in Kitchenham et al. *IEEE TSE* 2025 guidelines on avoiding fixed-graph pseudo-replication), plus responsible disclosure and maintainer non-stigmatization.
10. `sections/09_conclusion.tex`: Synthesis of findings, future research directions, and actionable guidance for package registry operators (targeted WebAuthn/FIDO2 MFA, differential release-authority quarantine, $P(S)$ verification badges) and downstream DevSecOps organizations (3–7 day cooldowns, `--ignore-scripts`, lockfile pinning, SBOM co-maintenance auditing).

### 2.2 Compilation Metrics & Quality Invariants
* **Total Compiled Pages**: 15 pages in double-column IEEE Transactions journal format.
* **Overfull Boxes**: **0 (Zero)** overfull `\hbox` or `\vbox` warnings across the entire 15-page document.
* **Unresolved Citations / References**: **0 (Zero)** undefined citations (`?`) or cross-references.
* **Bibliographic Rigor**: 23 verified peer-reviewed literature entries; zero hallucinated citations.
* **Total Vector & Raster Assets**: 6 embedded PDF vector figures (`study_system.pdf`, `objective_tradeoff.pdf`, `representation_detail.pdf`, `q1_pareto_frontier.pdf`, `q1_supermodular_p_and_weights.pdf`, `artifact_comparison.pdf`).

---

## 3. Code and Manuscript Diffs Performed

### 3.1 Created Directory Structure and Core Files
* `manuscript_q1/main_q1.tex`: Primary driver document configured with `\documentclass[10pt,journal,compsoc]{IEEEtran}`.
* `manuscript_q1/config/preamble_q1.tex`: Package definitions, theorem environments (`\newtheorem{proposition}{Proposition}`), and title definitions.
* `manuscript_q1/compile_q1.sh`: Native build script invoking `tectonic --keep-logs --keep-intermediates --outdir build main_q1.tex`.
* `manuscript_q1/scripts/clean_tex.py`: Automated typography cleaner enforcing ASCII em-dashes and proper ampersand escaping.
* `manuscript_q1/sections/*.tex`: 10 newly written journal sections.
* `manuscript_q1/tables/*.tex`: 6 standalone LaTeX tables (`q1_pareto_table.tex`, `q1_supermodular_p_table.tex`, `q1_heterogeneous_weights_table.tex`, `q1_incident_case_study_table.tex`, `q1_release_authority_table.tex`, `q1_temporal_reconstruction_table.tex`).
* `manuscript_q1/bibliography/references_q1.bib`: Verified BibTeX database including peer-reviewed 2024–2025 literature.

### 3.2 Layout & Geometry Polishing Performed
* Converted wide multi-column tables (`q1_supermodular_p_table.tex`, `q1_release_authority_table.tex`, `q1_temporal_reconstruction_table.tex`) from `table` to `table*` to span double columns naturally.
* Balanced column spacing in `q1_incident_case_study_table.tex` (`\setlength{\tabcolsep}{2.2pt}`) and `multi_budget_comparison` (`\setlength{\tabcolsep}{4.5pt}`), eliminating 136 pt and 41 pt overfull margins.
* Split wide hypergeometric expectation equation (13) into an `align` environment to eliminate single-column margin protrusion.
* Escaped all percentage signs (`\%`) and ampersands (`\&`) across table cells and narrative text.

---

## 4. Anomaly and Vulnerability Flags

1. **`pplr8t` TeX Font Encoding Warning for Em-Dashes**:
   * *Diagnosis*: Standard Palatino font metrics (`pplr8t`) in classical TeX do not map Unicode `—` (0x2014) directly without `fontspec`.
   * *Resolution*: Converted all Unicode em-dashes (`—`) to standard LaTeX triple-hyphens (`---`) and en-dashes (`–`) to double-hyphens (`--`), completely eliminating the missing character font warnings.
2. **XeTeX Bell-Character Ingestion in Heterogeneous Table Header**:
   * *Diagnosis*: Python string generation in earlier scripts interpreted `\arg\max` as `\a` (ASCII bell 0x07) followed by `rg\max`.
   * *Resolution*: Corrected to `$\arg\max_S H_w(S)$` with proper escaping, ensuring valid syntax.
3. **Conference Freeze Invariant**:
   * *Diagnosis*: Strict requirement that conference files remain completely frozen.
   * *Resolution*: Verified that `manuscript/main.pdf`, `manuscript/main_authors.pdf`, and both conference zip archives remain 100% untouched and passing all 24 compliance and validation tests.

---

## 5. Ledger Confirmation
* Master Ledger `research_sessions/SESSION_INDEX.md`: Updated with Session 10 entry.
* Reports Overview `reports/README.md`: Updated with Session 10 summary.
* Working Directory Status: Clean and synchronized; `manuscript_q1/build/` intermediate build artifacts added to `.gitignore`.

---

## 6. Handoff Payload

* **Compiled Journal PDF**: [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) (15 pages, 282,184 bytes, 9,367 words, zero overfull boxes, zero unresolved citations).
* **Compilation Command**: `bash manuscript_q1/compile_q1.sh` (or `~/.local/bin/tectonic manuscript_q1/main_q1.tex`).
* **Source Tree**: Fully modular under `manuscript_q1/sections/`, `manuscript_q1/tables/`, `manuscript_q1/figures/`, and `manuscript_q1/bibliography/`.
* **Conference Paper Status**: Fully locked and ready for immediate submission to ICEEICT 2027 (`manuscript/main.pdf` and `manuscript/main_authors.pdf`, exactly 6.0 pages each).
