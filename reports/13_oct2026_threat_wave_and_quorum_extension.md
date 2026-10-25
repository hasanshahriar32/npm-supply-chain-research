# Active Verification Session 13: Integration of October 2026 Supply-Chain Threat Wave & Generalized $k$-of-$n$ Quorum Exclusion Extension

## 1. Executive Summary & Session Objectives
* **Session Identifier**: `13_oct2026_threat_wave_and_quorum_extension`
* **Date & Timestamp**: 2026-10-25T19:34:00+06:00
* **Target Publication Venues**:
  * *IEEE Transactions on Software Engineering (TSE)* (Primary target; strict 100–200 word abstract limit, double-column IEEEtran journal format)
  * *ACM Transactions on Software Engineering and Methodology (TOSEM)* (Double-anonymous review)
  * *IEEE Transactions on Dependable and Secure Computing (TDSC)*
  * *Springer Empirical Software Engineering (EMSE)*
* **Author Affiliation**: Department of Computer Science and Engineering, Hajee Mohammad Danesh Science and Technology University (HSTU), Dinajpur 5200, Bangladesh
* **Compilation Toolchain**: Native `tectonic` 0.17.0 (`~/.local/bin/tectonic` invoking XeTeX engine with automatic BibTeX and font package caching)
* **Conference Deliverables Invariant (Track 1)**: `manuscript/main.pdf` (179,471 bytes, exactly 6.0 A4 pages), `manuscript/main_authors.pdf` (180,875 bytes, exactly 6.0 A4 pages), `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes), and `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes) remain **100% frozen with zero byte changes** and verified against cryptographic SHA-256 hashes.
* **Core Objectives Achieved**:
  1. **Empirical Grounding in the October 17–22, 2026 Supply-Chain Wave**: Analyzed the multi-layer security incidents across four software supply chain strata:
     * *Multi-Token Quorum Breach & Build Artifact Injection* (`LiteLLM 1.107.0`, Oct 21): 3 stolen developer GitHub CLI OAuth tokens bypassed branch protections and injected malicious payloads (`cook.pth`/`sitecustomize.py`) directly into release wheels while preserving a clean GitHub tag.
     * *Transitive Version Lag & Silent Remediation* (`OpenCode` MCP Sign-In RCE, Oct 17–19): Passing unescaped OAuth URLs to an outdated version of the npm `open` package (maintained by `sindresorhus`, Rank #1 in Table 4) enabled arbitrary execution, patched silently in v1.18.33 without a CVE.
     * *CI/CD Secret Decryption & Remediation Deadlock* (`Railway` & `OpenCode Console`, Oct 20–22): Compromised CI credentials exposed environment secrets across ~100,000 workspaces, while pausing builds created an operational deadlock that prevented developers from rolling out rotated secrets.
     * *OIDC Flaws & Runtime C Boundaries*: npm Trusted Publishing validation bypass (Oct 13, exposing 1,500 packages / 10M downloads) and Node.js bundled C Brotli decompressor memory corruption (`CVE-2026-111497`, Oct 21).
  2. **Mathematical Formulation & Execution of Generalized $k$-of-$n$ Quorum Exclusion $P_k(S)$**:
     * Implemented $P_k(S) = \left| \left\{ r \in R_{\text{wf}} : |\text{Sources}(r) \setminus S| < k \right\} \right|$ for $k \in \{1, 2, 3, 5\}$ across budgets $|S| \in \{10, 25, 50, 100\}$ on the canonical 25,228-package / 12,217-maintainer / 7,171-workflow-repository graph.
     * Evaluated five prioritization strategies: `Portfolio Size`, `Greedy Coverage`, `Exact Union`, `Pareto Hybrid (\alpha=0.50)`, and `Direct Supermodular P(S)`.
     * Evaluated imperfect control efficacy $H_\eta(S) = \eta \cdot H(S)$ for $\eta \in \{1.00, 0.95, 0.90, 0.75\}$ to model residual CI credential leaks and OIDC token bypasses.
  3. **Integration into Manuscript Sections**:
     * Updated `01_introduction.tex` with modern motivation and a dedicated 6th contribution bullet on $k$-quorum multi-token defense.
     * Updated `02_related_work.tex` with contemporary CI/CD exfiltration and OIDC signing circumvention analyses.
     * Added Subsection 6.3 and Table 10 (`tab:q1_quorum_exclusion`) to `06_pareto_and_heterogeneous_results_rq4.tex`.
     * Expanded Construct Validity in `08_threats_to_validity_and_ethics.tex` to cover imperfect control efficacy and native runtime C boundaries.
     * Updated actionable DevSecOps recommendations in `09_conclusion.tex` (dependency cooldown periods and out-of-band secret rotation pathways).
     * Added 5 primary-source verified references to `references_q1.bib` (`litellm2026`, `opencode2026`, `railway2026`, `npmtrustedpub2026`, `nodejsbrotli2026`).
  4. **Compilation, Verification, and Packaging**:
     * Maintained strict 188-word abstract compliance in `00_abstract.tex`.
     * Recompiled `main_q1.pdf` (16 pages, 291,738 bytes) and `main_q1_anonymous.pdf` (16 pages, 290,233 bytes) with native Tectonic: 0 Type 3 fonts, 0 overfull boxes > 1 pt, 0 undefined citations.
     * Upgraded automated test suite `verify_manuscript_q1.py` with regex verification for Table 10, passing all checks (`status: "PASS"`).
     * Rebuilt source archive `NPM_Supply_Chain_Q1_Journal_Source.zip` (53 files, 2,345,195 bytes, SHA-256: `d2fbad2cc5327f3d4745dfa67b115208365f216dc77126083e09d744d3a680cf`).

---

## 2. Artifacts and Datasets Audited

### 2.1 Audited Datasets and Extraction Scripts
1. `data/npm_ecosystem.db.zip`: Canonical SQLite ecosystem database (tables `package_maintainers`, `package_metrics`, `dependencies`, `package_versions`).
2. `scripts/study_q1_quorum_and_oct2026.py`: Standalone analysis script executing the generalized $k$-quorum and imperfect hardening experiments across 12,217 maintainers and 7,171 workflow repositories.
3. `manuscript/results/q1_journal/q1_quorum_exclusion.csv` & `q1_quorum_exclusion.json`: Machine-readable results containing complete $P_k(S)$, $C(S)$, $H(S)$, and $H_\eta(S)$ metrics.
4. `manuscript/results/q1_journal/q1_quorum_exclusion_table.tex` & `manuscript_q1/tables/q1_quorum_exclusion_table.tex`: Formatted publication LaTeX table.
5. `manuscript_q1/bibliography/references_q1.bib`: Verified BibTeX database updated with primary incident entries.
6. `manuscript_q1/scripts/verify_manuscript_q1.py`: Upgraded verification suite with automated regex assertions for Table 10.
7. `manuscript_q1/results/q1_verification_report.json`: Updated automated verification report.

### 2.2 Track 1 Conference Deliverables Frozen
Cryptographic verification confirmed 100% byte-for-byte consistency across all Track 1 conference files:
* `manuscript/main.pdf` (179,471 bytes): SHA-256 `abb1b4b3cd1baeabf3fc1f9232661f5594f7f233f75db0d5ec247d06f882e4cb`
* `manuscript/main_authors.pdf` (180,875 bytes): SHA-256 `402215fde6223126c4809f988baadcd86e4b0920318eb05b101a6e65b148f373`
* `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (1,441,736 bytes): SHA-256 `bb2c591b009979b5f117ce5458d867c80f4b56ddb4a093cae59ea2bd30e87de4`
* `NPM_Supply_Chain_IEEE_Overleaf.zip` (3,520,168 bytes): SHA-256 `ab0fd2cd4546997e4cc386ce960aa14ceca77870f8fbf61c71cc225a29d00145`

Result: **0 byte modifications. 100% frozen.**

---

## 3. Methodological and Analytical Procedures

### 3.1 Mathematical Definition of Generalized $k$-of-$n$ Quorum Exclusion
Under standard all-source exclusion ($P(S)$), an endpoint $r \in R_{\text{wf}}$ is considered defended if and only if all upstream maintainers are in the hardened cohort:
$$\text{Sources}(r) \subseteq S \iff |\text{Sources}(r) \setminus S| = 0$$
While this represents absolute immunity against single-account takeover ($k=1$), it overstates risk for organizations enforcing multi-maintainer review policies or dual-custody publishing gates. Conversely, it understates adversary capacity when attackers compromise multiple credentials (such as the 3-token exfiltration in `LiteLLM 1.107.0`).

We define **$k$-Quorum Exclusion** $P_k(S)$ as:
$$P_k(S) = \left| \left\{ r \in R_{\text{wf}} : |\text{Sources}(r) \setminus S| < k \right\} \right|$$
* **$k=1$ (Strict Single-Account All-Source Exclusion)**: Exactly requires $\text{Sources}(r) \subseteq S$. A repository is protected only if zero unhardened maintainers remain.
* **$k=2$ (Two-Maintainer Review Quorum)**: Requires $|\text{Sources}(r) \setminus S| \le 1$. If an endpoint enforces a 2-person code review or dual-signature release gate, an attacker who compromises only a single unhardened account cannot bypass the review barrier.
* **$k=3$ (Three-Token Compromise Threshold)**: Requires $|\text{Sources}(r) \setminus S| \le 2$. Models resilience against an adversary possessing two compromised tokens attempting to subvert multi-stage release pipelines.
* **$k=5$ (Enterprise Quorum Threshold)**: Requires $|\text{Sources}(r) \setminus S| \le 4$.

### 3.2 Imperfect Hardening Efficacy $\eta$
Prior models assume perfect control enforcement: hardening maintainer $m$ eliminates $100\%$ of their compromise contribution. In reality, stolen CI tokens (Railway), developer OAuth leakage via agent logs (LiteLLM), or OIDC token validation flaws (npm Trusted Publishing) allow adversaries to publish malicious releases despite maintainer-level 2FA.

We parameterize effective exposure reduction as:
$$H_\eta(S) = \eta \cdot H(S) = \eta \cdot \frac{\sum_{m \in S} w_m |E_m|}{\sum_{v \in M} w_v |E_v|}, \quad \eta \in (0, 1]$$
where $\eta$ represents the residual integrity rate of the hardening mechanism ($\eta=0.95$ models a 5% failure/bypass rate, $\eta=0.90$ models a 10% rate, and $\eta=0.75$ models a 25% bypass rate).

---

## 4. Empirical Results and Quantitative Findings

### 4.1 Complete $k$-Quorum Exclusion Results (Table 10)

The empirical evaluation executed on `npm_ecosystem.db` across all 7,158 reachable workflow endpoints yielded the exact counts below:

| Prioritization Strategy | Budget $|S|$ | Covered $C(S)$ | Coverage $C$ (%) | Exposure $H(S)$ (%) | $P_1(S)$ ($k=1$) | $P_2(S)$ ($k=2$) | $P_3(S)$ ($k=3$) | $P_5(S)$ ($k=5$) | Effective $H_{0.90}$ (%) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Portfolio Size** | 10 | 3,435 | 47.90% | 1.59% | 391 | 1,915 | 2,433 | 3,093 | 1.43% |
| | 25 | 4,067 | 56.71% | 4.38% | 430 | 1,974 | 2,563 | 3,194 | 3.94% |
| | 50 | 4,446 | 62.00% | 6.14% | 503 | 2,025 | 2,613 | 3,244 | 5.53% |
| | 100 | 4,579 | 63.85% | 7.96% | 577 | 2,065 | 2,669 | 3,281 | 7.16% |
| **Greedy Coverage** | 10 | 4,331 | 60.40% | 3.79% | 351 | 1,846 | 2,406 | 3,080 | 3.41% |
| | 25 | 4,854 | 67.69% | 6.08% | 514 | 1,976 | 2,487 | 3,176 | 5.47% |
| | 50 | 5,196 | 72.46% | 8.73% | 638 | 2,039 | 2,552 | 3,232 | 7.86% |
| | 100 | **5,538** | **77.23%** | 11.48% | 800 | 2,112 | 2,602 | 3,268 | 10.33% |
| **Exact Union** | 10 | 3,910 | 54.53% | 4.48% | 343 | 1,825 | 2,385 | 3,105 | 4.03% |
| | 25 | 4,284 | 59.74% | 9.86% | 427 | 1,995 | 2,596 | 3,244 | 8.87% |
| | 50 | 4,321 | 60.26% | 18.09% | 441 | 2,011 | 2,609 | 3,324 | 16.28% |
| | 100 | 4,407 | 61.46% | **33.79%** | 534 | 2,137 | **2,760** | **3,523** | 30.41% |
| **Pareto Hybrid ($\alpha=0.50$)** | 10 | 4,331 | 60.40% | 3.79% | 351 | 1,846 | 2,406 | 3,080 | 3.41% |
| | 25 | 4,795 | 66.87% | 7.68% | 498 | 1,948 | 2,505 | 3,194 | 6.91% |
| | 50 | 5,001 | 69.74% | 14.96% | 605 | 2,102 | 2,689 | 3,390 | 13.46% |
| | 100 | **5,020** | **70.00%** | **31.19%** | 626 | **2,153** | **2,719** | 3,415 | **28.07%** |
| **Direct Supermodular $P(S)$** | 10 | 3,976 | 55.45% | 2.58% | 479 | 1,856 | 2,392 | 3,070 | 2.32% |
| | 25 | 4,239 | 59.11% | 4.15% | 618 | 1,880 | 2,424 | 3,124 | 3.74% |
| | 50 | 4,604 | 64.20% | 6.55% | 803 | 1,983 | 2,517 | 3,177 | 5.90% |
| | 100 | 5,020 | 70.00% | 13.23% | **1,022** | 2,074 | 2,636 | 3,337 | 11.91% |

### 4.2 Key Quantitative Findings
1. **Quorum Expansion Effect**: Relaxing the single-maintainer bottleneck to a 2-maintainer review quorum ($k=2$) expands protected repositories under Pareto Hybrid ($\alpha=0.50$) from **$626$ to $2{,}153$** ($+243.9\%$, a $3.44\times$ multiplier). Under Greedy Coverage, protection expands from $800$ to $2{,}112$.
2. **Strategy Crossover Dynamics**: Under strict single-account exclusion ($k=1$), Direct Supermodular optimization dominates ($P_1 = 1{,}022$ vs.\ $800$ for Greedy and $626$ for Pareto). However, under multi-account review quorums ($k \ge 2$), **Pareto Hybrid ($\alpha=0.50$) achieves the highest protection ($P_2 = 2{,}153$)**, overtaking Direct $P(S)$ ($2{,}074$). For $k=3$ and $k=5$, Exact Union achieves $P_3 = 2{,}760$ and $P_5 = 3{,}523$.
3. **Resilience to Imperfect Controls ($\eta < 1$)**: Under a 10% residual failure rate ($\eta = 0.90$), Pareto Hybrid preserves **$H_{0.90} = 28.07\%$** exposure reduction, which is still **$2.44\times$ greater** than the exposure reduction of perfect Greedy Coverage ($\eta = 1.00$, $H=11.48\%$).

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
      "pages": 16,
      "file_bytes": 291738,
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
      "pages": 16,
      "file_bytes": 290233,
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

### 5.2 PDF Font, Geometry, and Gate Compliance Ledger

| Invariant Metric | Named Journal PDF (`main_q1.pdf`) | Anonymous Journal PDF (`main_q1_anonymous.pdf`) | Status |
|---|---|---|---|
| **Page Count** | 16 pages (IEEE Transactions standard) | 16 pages (Title/author metadata suppressed) | **PASS** |
| **Page Format** | Letter (8.5 × 11 in) | Letter (8.5 × 11 in) | **PASS** |
| **Overfull Boxes > 1 pt** | 0 | 0 | **PASS** |
| **Undefined Citations (`?`)** | 0 | 0 | **PASS** |
| **Undefined References (`??`)** | 0 | 0 | **PASS** |
| **Missing Glyphs** | 0 | 0 | **PASS** |
| **Total Fonts Embedded** | 36 / 36 (100%) | 36 / 36 (100%) | **PASS** |
| **Type 3 Fonts** | 0 | 0 | **PASS** |
| **Abstract Word Count** | 188 words ($\le 200$) | 188 words ($\le 200$) | **PASS** |
| **Table 4 Parity Gate** | 16/16 rows verified against SQLite & CSV | 16/16 rows verified against SQLite & CSV | **PASS** |
| **Table 10 Quorum Parity** | Verified across all strategies & $k \in \{1, 2, 3, 5\}$ | Verified across all strategies & $k \in \{1, 2, 3, 5\}$ | **PASS** |

---

## 6. Deliverables, File Manifest, and Next Steps

### 6.1 Generated Deliverables Manifest
1. **Named Journal PDF**: [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) (291,738 bytes, 16 pages, 0 overfull boxes, 0 Type 3 fonts).
2. **Double-Anonymous Journal PDF**: [`manuscript_q1/main_q1_anonymous.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1_anonymous.pdf) (290,233 bytes, 16 pages, 0 overfull boxes, 0 Type 3 fonts).
3. **Q1 Source Zip Archive**: [`NPM_Supply_Chain_Q1_Journal_Source.zip`](file:///home/ashik/Desktop/npm-supply-chain-research/NPM_Supply_Chain_Q1_Journal_Source.zip) (2,345,195 bytes, SHA-256: `d2fbad2cc5327f3d4745dfa67b115208365f216dc77126083e09d744d3a680cf`, 53 files).
4. **Verification Report**: [`manuscript_q1/results/q1_verification_report.json`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/results/q1_verification_report.json).
5. **Programmatic Quorum Outputs**:
   - CSV: [`manuscript/results/q1_journal/q1_quorum_exclusion.csv`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/results/q1_journal/q1_quorum_exclusion.csv)
   - JSON: [`manuscript/results/q1_journal/q1_quorum_exclusion.json`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/results/q1_journal/q1_quorum_exclusion.json)
   - LaTeX: [`manuscript/results/q1_journal/q1_quorum_exclusion_table.tex`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/results/q1_journal/q1_quorum_exclusion_table.tex)
   - Active Manuscript Table: [`manuscript_q1/tables/q1_quorum_exclusion_table.tex`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/tables/q1_quorum_exclusion_table.tex)
6. **Execution Script**: [`scripts/study_q1_quorum_and_oct2026.py`](file:///home/ashik/Desktop/npm-supply-chain-research/scripts/study_q1_quorum_and_oct2026.py).

### 6.2 Submission Readiness Summary
* **Track 1 (IEEE Conference — ICEEICT 2027)**: Completely locked and ready for immediate submission with [`manuscript/main.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/main.pdf) / [`manuscript/main_authors.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript/main_authors.pdf) and `NPM_Supply_Chain_IEEE_Anonymous_Source.zip`.
* **Track 2 (Q1 Journal Submission)**:
  * **IEEE TSE / IEEE TDSC**: Ready for submission with [`manuscript_q1/main_q1.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1.pdf) and [`NPM_Supply_Chain_Q1_Journal_Source.zip`](file:///home/ashik/Desktop/npm-supply-chain-research/NPM_Supply_Chain_Q1_Journal_Source.zip). Abstract (188 words) satisfies ScholarOne's 200-word constraint.
  * **ACM TOSEM / Springer EMSE**: Ready for submission with [`manuscript_q1/main_q1_anonymous.pdf`](file:///home/ashik/Desktop/npm-supply-chain-research/manuscript_q1/main_q1_anonymous.pdf) for double-anonymous peer review.
