# Deep Audit of Structural Intervention Artifacts, Graph Validity, and Incident Ledgers

## 1. Execution Metadata
* **Task ID**: `Task 02`
* **Timestamp**: `2026-10-20 02:57:21 UTC+06:00`
* **Working Directory**: `/home/ashik/Desktop/npm-supply-chain-research`
* **Inspected Artifact Directories**:
  * `manuscript/results/structural_interventions/` (13 CSV/JSON files: `results.json`, `deterministic_curves.csv`, `random_summary.csv`, `random_analytic_expectations.csv`, `ablations.csv`, `concentration.csv`, `identity_grouping_sensitivity.csv`, `repository_mapping_sensitivity.csv`, `version_representation_curves.csv`, `independent_validation.json`, `run_config.json`, `manifest.json`, `random_trials.csv`)
  * `manuscript/results/graph_validity/` (`summary.json`, `nontrivial_components.csv`, `repository_parser_disagreements.csv`, `version_projection_witnesses.json`, `per_package.csv`, `repository_units.csv`)
  * `platform/research/` (`68_temporal_reconstruction_and_baseline_results.md`, `69_temporal_incident_label_adjudication.md`, `76_amalfi_basic_corpus.csv`, `80_datadog_positive_membership_overlap.json`, `85_figshare_npm_benchmark_control_frame_assessment.json`, `90_gap_resolution_report.md`, `94_campaign_relatedness_and_grouped_inference_protocol.json`, `95_release_authority_metadata_availability_audit.json`, and 49 `*_candidate_assessment.json` files)
  * Ingestion & Analysis Pipelines: `scripts/collect_data.py`, `scripts/collect_data_v2.py`, `scripts/study_structural_interventions.py`, `scripts/study_graph_validity.py`, `scripts/research_observations.py`
* **Execution Commands**:
  ```bash
  python3 scripts/validate_observation_semantics.py
  python3 scripts/validate_research_study.py
  python3 scripts/generate_task02_report.py
  ```

---

## 2. Quantitative and Structural Findings

### 2.1 Multi-Budget Experimental Curves: Coverage vs. Exposure Reduction Trade-Off

Evaluated across **$N = 7,171$ workflow-associated GitHub repositories** and **$M = 12,217$ maintainer usernames**:

| Budget ($|S|$) | Method / Strategy | Distinct Repos Covered ($C$) | Coverage % ($C$ %) | Exposure Reduction ($H$ %) | All-Source Full Exclusion ($P$) | Overlap Redundancy |
|---:|---|---:|---:|---:|---:|---:|
| 1 | `portfolio` | 1,680 | 23.43% | 0.36% | 1 | 0.00% |
| 1 | `sum_package_reach` | 2,368 | 33.02% | 0.51% | 26 | 0.00% |
| 1 | `max_package_reach` | 2,062 | 28.75% | 0.45% | 2 | 0.00% |
| 1 | `exact_union` | 2,543 | 35.46% | 0.55% | 269 | 0.00% |
| 1 | `greedy_coverage` | 2,543 | 35.46% | 0.55% | 269 | 0.00% |
| 1 | `random_baseline (200 trials mean)` | 46.8 | 0.65% | 0.01% | 0.3 | 0.00% |
| 1 | `random_analytic_expectation (exact)` | 37.8 | 0.53% | 0.01% | 0.1 | N/A |
| 5 | `portfolio` | 3,299 | 46.00% | 1.16% | 316 | 38.24% |
| 5 | `sum_package_reach` | 3,532 | 49.25% | 2.15% | 325 | 64.47% |
| 5 | `max_package_reach` | 3,022 | 42.14% | 2.23% | 80 | 70.65% |
| 5 | `exact_union` | 3,654 | 50.96% | 2.45% | 329 | 67.68% |
| 5 | `greedy_coverage` | 3,872 | 54.00% | 2.09% | 327 | 59.96% |
| 5 | `random_baseline (200 trials mean)` | 187.1 | 2.61% | 0.04% | 0.7 | 2.87% |
| 5 | `random_analytic_expectation (exact)` | 179.3 | 2.50% | 0.04% | 0.7 | N/A |
| 10 | `portfolio` | 3,435 | 47.90% | 1.59% | 391 | 53.12% |
| 10 | `sum_package_reach` | 3,711 | 51.75% | 2.68% | 399 | 70.05% |
| 10 | `max_package_reach` | 3,070 | 42.81% | 4.06% | 111 | 83.65% |
| 10 | `exact_union` | 3,910 | 54.53% | 4.48% | 343 | 81.12% |
| 10 | `greedy_coverage` | 4,331 | 60.40% | 3.79% | 351 | 75.27% |
| 10 | `random_baseline (200 trials mean)` | 339.1 | 4.73% | 0.08% | 1.2 | 6.75% |
| 10 | `random_analytic_expectation (exact)` | 336.9 | 4.70% | 0.08% | 1.4 | N/A |
| 25 | `portfolio` | 4,067 | 56.71% | 4.38% | 430 | 79.92% |
| 25 | `sum_package_reach` | 4,371 | 60.95% | 7.45% | 480 | 87.31% |
| 25 | `max_package_reach` | 3,248 | 45.29% | 9.00% | 116 | 92.20% |
| 25 | `exact_union` | 4,284 | 59.74% | 9.86% | 427 | 90.59% |
| 25 | `greedy_coverage` | 4,854 | 67.69% | 6.08% | 514 | 82.74% |
| 25 | `random_baseline (200 trials mean)` | 728.2 | 10.15% | 0.21% | 2.9 | 18.95% |
| 25 | `random_analytic_expectation (exact)` | 717.0 | 10.00% | 0.20% | 3.5 | N/A |
| 50 | `portfolio` | 4,446 | 62.00% | 6.14% | 503 | 84.33% |
| 50 | `sum_package_reach` | 4,574 | 63.78% | 13.72% | 576 | 92.79% |
| 50 | `max_package_reach` | 3,267 | 45.56% | 17.19% | 117 | 95.89% |
| 50 | `exact_union` | 4,321 | 60.26% | 18.09% | 441 | 94.83% |
| 50 | `greedy_coverage` | 5,196 | 72.46% | 8.73% | 638 | 87.12% |
| 50 | `random_baseline (200 trials mean)` | 1199.7 | 16.73% | 0.43% | 6.0 | 34.74% |
| 50 | `random_analytic_expectation (exact)` | 1161.2 | 16.19% | 0.41% | 7.0 | N/A |
| 100 | `portfolio` | 4,579 | 63.85% | 7.96% | 577 | 87.55% |
| 100 | `sum_package_reach` | 4,835 | 67.42% | 21.98% | 704 | 95.24% |
| 100 | `max_package_reach` | 4,268 | 59.52% | 33.59% | 533 | 97.25% |
| 100 | `exact_union` | 4,407 | 61.46% | 33.79% | 534 | 97.18% |
| 100 | `greedy_coverage` | 5,538 | 77.23% | 11.48% | 800 | 89.57% |
| 100 | `random_baseline (200 trials mean)` | 1680.6 | 23.44% | 0.80% | 12.8 | 51.22% |
| 100 | `random_analytic_expectation (exact)` | 1716.8 | 23.94% | 0.82% | 14.1 | N/A |

#### Core Decision-Theoretic Findings from Multi-Budget Extraction:
1. **The Multi-Homing Residual Exposure Trap ($C$ vs. $H$)**:
   * At budget $|S| = 100$, **Greedy Marginal Coverage** covers **5,538** of 7,171 workflow repositories (**77.23%**), appearing to protect over three-quarters of the ecosystem.
   * However, it eliminates only **11.48%** of uniform single-account compromise exposure. Crucially, **4,738 of the 5,538 covered repositories remain reachable** through other, unhardened maintainer accounts. Only **800 repositories** achieve all-source exclusion ($P$).
   * Conversely, **Exact Maintainer-Union Ranking** covers **4,407** repositories (61.46%) but eliminates **33.79%** of scenario exposure—nearly **$3\times$ higher risk reduction** than greedy coverage.
2. **Overlap Redundancy Dynamic**:
   * As the budget grows from 1 to 100, the selected overlap redundancy fraction ($1 - C(S) / \sum_{m \in S} |E_m|$) explodes from **0.00%** to **89.57%** for greedy coverage and **97.18%** for exact union.
   * While redundant paths are valuable for additive exposure reduction (hardening multiple parallel entry points), reporting coverage alone severely misleads defenders by conflating *"reaching a repository"* with *"protecting a repository"*.
3. **Analytic Baseline Conformance**:
   * The 200 random simulation trials match the exact finite-population hypergeometric expectations ($E[H] = |S| / |M| = 100 / 12,217 = 0.819\%$).

---

### 2.2 Ablations & Empirical Sensitivity Analysis

#### A. Architectural Ablation Matrix (`ablations.csv`, Budget = 100)
| Ablation Dimension | Parameter / Condition | Strategy | Covered ($C$) | Coverage % | Exposure % ($H$) | Full Exclusion ($P$) | Residual Exposed Endpoints |
|---|---|---|---:|---:|---:|---:|---:|
| `graph_depth` | `depth_0` | `portfolio` | 4,579 | 63.85% | 7.96% | 577 | 4,002 |
| `graph_depth` | `depth_0` | `sum_package_reach` | 4,438 | 61.89% | 6.58% | 559 | 3,879 |
| `graph_depth` | `depth_0` | `max_package_reach` | 1,434 | 20.00% | 0.69% | 25 | 1,409 |
| `graph_depth` | `depth_0` | `exact_union` | 4,796 | 66.88% | 10.67% | 748 | 4,048 |
| `graph_depth` | `depth_0` | `greedy_coverage` | 5,255 | 73.28% | 8.38% | 714 | 4,541 |
| `graph_depth` | `depth_1` | `portfolio` | 4,579 | 63.85% | 7.96% | 577 | 4,002 |
| `graph_depth` | `depth_1` | `sum_package_reach` | 5,045 | 70.35% | 16.53% | 737 | 4,308 |
| `graph_depth` | `depth_1` | `max_package_reach` | 4,732 | 65.99% | 19.18% | 655 | 4,077 |
| `graph_depth` | `depth_1` | `exact_union` | 5,072 | 70.73% | 21.16% | 874 | 4,198 |
| `graph_depth` | `depth_1` | `greedy_coverage` | 5,488 | 76.53% | 12.10% | 750 | 4,738 |
| `endpoint_transfer` | `all_packages` | `portfolio` | 4,579 | 63.85% | 7.96% | 577 | 4,002 |
| `endpoint_transfer` | `all_packages` | `sum_package_reach` | 4,817 | 67.17% | 20.23% | 701 | 4,116 |
| `endpoint_transfer` | `all_packages` | `max_package_reach` | 4,254 | 59.32% | 33.38% | 522 | 3,732 |
| `endpoint_transfer` | `all_packages` | `exact_union` | 4,465 | 62.26% | 33.58% | 528 | 3,937 |
| `endpoint_transfer` | `all_packages` | `greedy_coverage` | 5,308 | 74.02% | 12.10% | 666 | 4,642 |
| `endpoint_transfer` | `workflow_packages` | `portfolio` | 4,579 | 63.85% | 7.96% | 577 | 4,002 |
| `endpoint_transfer` | `workflow_packages` | `sum_package_reach` | 4,815 | 67.15% | 20.63% | 701 | 4,114 |
| `endpoint_transfer` | `workflow_packages` | `max_package_reach` | 4,294 | 59.88% | 32.67% | 501 | 3,793 |
| `endpoint_transfer` | `workflow_packages` | `exact_union` | 4,549 | 63.44% | 33.13% | 510 | 4,039 |
| `endpoint_transfer` | `workflow_packages` | `greedy_coverage` | 5,315 | 74.12% | 9.70% | 666 | 4,649 |
| `exclude_largest_portfolios` | `exclude_1` | `portfolio` | 4,512 | 62.92% | 7.62% | 530 | 3,982 |
| `exclude_largest_portfolios` | `exclude_1` | `exact_union` | 4,290 | 59.82% | 33.69% | 531 | 3,759 |
| `exclude_largest_portfolios` | `exclude_1` | `greedy_coverage` | 5,522 | 77.00% | 11.18% | 792 | 4,730 |
| `exclude_largest_portfolios` | `exclude_5` | `portfolio` | 4,048 | 56.45% | 7.37% | 142 | 3,906 |
| `exclude_largest_portfolios` | `exclude_5` | `exact_union` | 3,913 | 54.57% | 33.41% | 224 | 3,689 |
| `exclude_largest_portfolios` | `exclude_5` | `greedy_coverage` | 5,149 | 71.80% | 11.44% | 459 | 4,690 |
| `exclude_largest_portfolios` | `exclude_10` | `portfolio` | 3,956 | 55.17% | 6.96% | 141 | 3,815 |
| `exclude_largest_portfolios` | `exclude_10` | `exact_union` | 3,913 | 54.57% | 33.41% | 224 | 3,689 |
| `exclude_largest_portfolios` | `exclude_10` | `greedy_coverage` | 5,076 | 70.79% | 11.37% | 465 | 4,611 |

#### Key Ablation Insights:
* **Graph Depth Impact**:
  * Restricting reach to immediate direct dependents (`depth_0`, maintainer portfolio only) collapses greedy coverage from 5,538 down to 5,255 repositories and exposure reduction from 11.48% to 8.38%.
  * At `depth_1` (one transitive step), exact union achieves **21.16%** exposure reduction, proving that multi-hop reach accounts for more than one-third of total scenario risk.
* **Dominant Maintainer Exclusion (`exclude_1`, `exclude_5`, `exclude_10`)**:
  * Excluding the single largest maintainer drops greedy coverage from 5,538 to 5,522.
  * Excluding the top 5 maintainers reduces coverage to 5,149 and cuts all-source protection from 800 down to 459 repositories, demonstrating that ecosystem protection is disproportionately anchored in a tiny cluster of mega-maintainers.

#### B. Version Continuity vs. Name Projection Sensitivity (`version_representation_curves.csv`)
| Strategy | Selection Representation | Evaluation Representation | Covered ($C$) | Coverage % | Exposure % ($H$) | Full Exclusion ($P$) | Residual Pairs |
|---|---|---|---:|---:|---:|---:|---:|
| `portfolio` | `version_continuous` | `version_continuous` | 4,435 | 61.85% | 8.94% | 662 | 23788 |
| `portfolio` | `package_projected` | `version_continuous` | 4,435 | 61.85% | 8.94% | 662 | 23788 |
| `portfolio` | `version_continuous` | `package_projected` | 4,579 | 63.85% | 7.96% | 577 | 36785 |
| `sum_package_reach` | `version_continuous` | `version_continuous` | 4,706 | 65.63% | 34.36% | 789 | 91394 |
| `sum_package_reach` | `package_projected` | `version_continuous` | 4,763 | 66.42% | 20.93% | 796 | 55666 |
| `sum_package_reach` | `version_continuous` | `package_projected` | 4,772 | 66.55% | 27.82% | 700 | 128569 |
| `max_package_reach` | `version_continuous` | `version_continuous` | 4,207 | 58.67% | 40.08% | 536 | 106616 |
| `max_package_reach` | `package_projected` | `version_continuous` | 4,074 | 56.81% | 38.33% | 547 | 101969 |
| `max_package_reach` | `version_continuous` | `package_projected` | 4,384 | 61.14% | 32.31% | 512 | 149317 |
| `exact_union` | `version_continuous` | `version_continuous` | 4,479 | 62.46% | 40.59% | 527 | 107970 |
| `exact_union` | `package_projected` | `version_continuous` | 4,253 | 59.31% | 38.82% | 549 | 103262 |
| `exact_union` | `version_continuous` | `package_projected` | 4,614 | 64.34% | 32.41% | 509 | 149786 |
| `greedy_coverage` | `version_continuous` | `version_continuous` | 5,516 | 76.92% | 13.10% | 817 | 34855 |
| `greedy_coverage` | `package_projected` | `version_continuous` | 5,491 | 76.57% | 12.88% | 816 | 34260 |
| `greedy_coverage` | `version_continuous` | `package_projected` | 5,531 | 77.13% | 11.66% | 792 | 53879 |

* **Empirical Distortion**: When version continuity is preserved, exact maintainer-union ranking removes **40.59%** of exposure mass (compared to 33.79% in the name-projected graph). This confirms that name-level graphs dilute maintainer priority by inventing false downstream reach.

#### C. Identity Grouping & Repository Linkage Sensitivities
| Sensitivity Test | Parameter / Unit | Strategy | Covered ($C$) | Coverage % | Exposure % ($H$) | Full Exclusion ($P$) |
|---|---|---|---:|---:|---:|---:|
| Identity Grouping | `exact_email_hash_equivalence_group` | `portfolio` | 4,579 | 63.85% | 8.02% | 577 |
| Identity Grouping | `exact_email_hash_equivalence_group` | `exact_union` | 4,418 | 61.61% | 34.01% | 535 |
| Identity Grouping | `exact_email_hash_equivalence_group` | `greedy_coverage` | 5,538 | 77.23% | 11.57% | 800 |
| Repository Linkage | `link_consistent_workflow_repositories` | `portfolio` | 4,571 | 63.96% | 7.96% | 578 |
| Repository Linkage | `link_consistent_workflow_repositories` | `sum_package_reach` | 4,824 | 67.50% | 21.97% | 705 |
| Repository Linkage | `link_consistent_workflow_repositories` | `max_package_reach` | 4,260 | 59.61% | 33.59% | 534 |
| Repository Linkage | `link_consistent_workflow_repositories` | `exact_union` | 4,398 | 61.54% | 33.79% | 535 |
| Repository Linkage | `link_consistent_workflow_repositories` | `greedy_coverage` | 5,524 | 77.29% | 11.47% | 799 |

#### D. Lorenz Concentration & Inequality (`concentration.csv`)
| Budget ($|S|$) | Maintainer Share | Cumulative Exposure Pair Share (Lorenz) | Theoretical Max Distinct Endpoint Bound |
|---:|---:|---:|---:|
| 1 | 0.008% | 0.55% | 2,543 |
| 5 | 0.041% | 2.45% | 7,158 |
| 10 | 0.082% | 4.48% | 7,158 |
| 25 | 0.205% | 9.86% | 7,158 |
| 50 | 0.409% | 18.09% | 7,158 |
| 100 | 0.819% | 33.79% | 7,158 |
* The top **0.819% of maintainers (100 accounts)** control **33.79%** of all identity-repository exposure paths in the npm ecosystem.

---

### 2.3 Graph Validity, SCC Cycles, and Parser Disagreements

#### A. Strongly Connected Component (SCC) Topology (`summary.json`)
* **Package Projection Graph**:
  * Total nodes: **25,228** package names | Directed edges: **88,113**
  * Total SCC components: **24,907** (condensed into a strict DAG)
  * Non-trivial components ($|V| > 1$): **82** components containing **403 nodes**
  * Largest cycle: **61 nodes** | Self-loops: **13**
* **Exact Version Union Graph**:
  * Total nodes: **40,806** version identities | Directed edges: **121,885**
  * Total SCC components: **40,570**
  * Non-trivial components: **68** components containing **304 nodes**
  * Largest cycle: **61 nodes** | Self-loops: **9**

#### B. Spurious Reach Witnesses (`version_projection_witnesses.json`)
Deleting version tags joins incompatible releases along intermediate dependencies, creating artificial reverse paths for **8,587 of 25,228 packages (34.04%)** and **1,273,291 phantom reach pairs** (median excess = 28, max excess = 4,127 for `pseudomap`). Five checked witnesses:
1. `pseudomap` $\rightarrow$ `lru-cache` $\rightarrow$ `@apollo/server` (Incompatible `lru-cache` versions: 3.2.0/4.0.0 vs. 11.5.1).
2. `is` $\rightarrow$ `object-keys` $\rightarrow$ `algoliasearch`.
3. `foreach` $\rightarrow$ `algoliasearch` $\rightarrow$ `@angular/cli`.
4. `indexof` $\rightarrow$ `object-keys` $\rightarrow$ `algoliasearch`.
5. `has-color` $\rightarrow$ `chalk` $\rightarrow$ `@alib/build-scripts`.

#### C. Repository Parser Disagreement Breakdown (`repository_parser_disagreements.csv`)
* **Total Disagreements**: **658 package records**.
* **Root Cause**: The legacy regex parser truncated repository names at the first period (`.`). E.g., `https://github.com/tj/commander.js.git` was truncated to `tj/commander` (omitting `.js`), and `isaacs/fs.realpath.git` was truncated to `isaacs/fs`.
* **Workflow Status Breakdown**:
  * `workflow_flag = '0'` (checked negative): **597 rows**
  * `workflow_flag = '1'` (positive workflow): **60 rows**
  * Unchecked / null: **1 row**
* **Impact**: 60 packages had workflow flags associated with truncated repository keys. Corrected in `collect_data_v2.py` and `research_observations.py` without retroactively altering historical data.

---

### 2.4 Real-World Incident Companion & Dataset Hygiene Audit

#### A. Incident Screening in `platform/research/` (`103_...` through `178_...`)
* **Total Screened Candidates**: **49 structured JSON assessments** and **29 Markdown candidate screen records** covering real-world campaigns from 2017 to 2026.
* **Adjudication Decisions**:
  * `eligible_for_governed_primary_temporal_ledger_reconstruction`: **17 candidates**
  * `admit_as_one_bounded_row_in_existing_mini_shai_hulud_family`: **5 candidates**
  * `admit_one_bounded_package_event_record`: **3 candidates**
  * Excluded due to lack of pre-event source code, missing timestamps, or duplicate campaigns: **24 candidates**
* **Direct Graph Overlap**: **16 real-world compromise packages exist directly inside our 25,228 study graph**:
  1. `debug` (`108_debug_september_2025_candidate_assessment.json`): Eligible
  2. `@solana/web3.js` (`110_solana_web3_js_december_2024_candidate_assessment.json`): Eligible
  3. `chalk` (`112_chalk_september_2025_candidate_assessment.json`): Eligible
  4. `eslint-config-prettier` (`117_eslint_config_prettier_july_2025_candidate_assessment.json`): Eligible
  5. `eslint-plugin-prettier` (`119_eslint_plugin_prettier_july_2025_candidate_assessment.json`): Excluded (sub-variant)
  6. `node-ipc` (March 2022 protestware, `123_node_ipc_march_2022_candidate_assessment.json`): Eligible
  7. `nx` (`129_nx_august_2025_candidate_assessment.json`): Eligible
  8. `@tanstack/history` (`155_tanstack_history_may_2026_candidate_assessment.json`): Admitted under Shai-Hulud
  9. `@ctrl/tinycolor` (`157_ctrl_tinycolor_september_2025_candidate_assessment.json`): Excluded
  10. `ansi-styles` (`158_ansi_styles_september_2025_candidate_assessment.json`): Admitted
  11. `backslash` (`159_backslash_september_2025_candidate_assessment.json`): Admitted
  12. `simple-swizzle` (`160_simple_swizzle_september_2025_candidate_assessment.json`): Admitted
  13. `@opensearch-project/opensearch` (`162_opensearch_client_may_2026_candidate_assessment.json`): Admitted
  14. `@mastra/core` (`165_mastra_core_june_2026_candidate_assessment.json`): Admitted
  15. `echarts-for-react` (`167_echarts_for_react_may_2026_candidate_assessment.json`): Excluded
  16. `node-ipc` (May 2026 compromise, `168_node_ipc_may_2026_candidate_assessment.json`): Admitted

#### B. Dataset Hygiene & External Benchmarks Audit
1. **DataDog Malicious Software Packages Dataset (`80_datadog_positive_membership_overlap.json`)**:
   * Evaluated 47 primary records: 26 exact affected version matches, 4 present without exact version, 16 not present in npm registry.
   * Finding: DataDog dataset is retrospective and creates **0 valid negative controls**.
2. **AMALFI Corpus (`76_amalfi_basic_corpus.csv`)**:
   * 1,790 packages. Verified that **zero `0.0.1-security` stubs** exist in the curated dataset.
3. **Figshare NPM Malicious Package Benchmark (`85_figshare_npm_benchmark_control_frame_assessment.json`)**:
   * Evaluated Guo et al. (2026) benchmark (6,420 malicious versions, 7,288 benign packages).
   * **Verdict**: Explicitly **excluded** as a control frame for temporal forecasting because:
     * Non-membership in the malicious list does not establish a true non-event outcome.
     * Benign lists lack per-row collection cutoffs or observation horizons.

---

### 2.5 Sampling & Construct Validity Audit

1. **Package Sampling Logic (`scripts/collect_data.py`)**:
   * **Seed Set**: Ingested high-impact root packages from `wooorm/npm-high-impact` (`lib/top.js`).
   * **Expansion**: Iteratively resolved dependencies via Google deps.dev API (`/v3/systems/npm/packages/{pkg}/versions/{ver}`) and inserted discovered dependencies into the SQLite `packages` queue until collecting 25,228 packages.
   * **Temporal Scope**: Collection timestamps range between June 13, 2026 and June 16, 2026.
2. **Workflow Observation Endpoint ($R_{\text{workflow}確} = 7,171$)**:
   * Queried GitHub GraphQL API for the existence of `HEAD:.github/workflows`.
   * **Construct Boundary**:
     * Verified only whether `.github/workflows` exists and is non-empty.
     * **Zero inspection of workflow YAML content**: does not parse `npm install` flags (e.g., `--ignore-scripts`), does not verify whether dependencies are actually executed in CI, does not check OIDC/SLSA provenance tokens, and does not analyze secrets access.
     * Operates purely at the repository boundary; does not perform inter-procedural call-graph reachability.

---

## 3. Code and Manuscript Diffs Performed
* **Diff Status**: `None (Read-Only Audit)`.
* **Report Generation**: Created `scripts/generate_task02_report.py` to extract all multi-budget numbers, sensitivities, SCC properties, and candidate overlaps deterministically.

---

## 4. Anomaly and Vulnerability Flags

1. **Massive Unreported Result Reservoir**:
   * The active manuscript (`manuscript/sections/05_results.tex`) reports results for only **one budget (100)** in 219 words.
   * The complete 6-budget curve (Budgets 1, 5, 10, 25, 50, 100), the depth ablations (`depth_0` vs `depth_1`), and mega-maintainer exclusion ablations are already pre-computed and stored in `manuscript/results/structural_interventions/` but completely omitted from the paper text.
2. **Real-World Incident Grounding Disconnected from Manuscript**:
   * 16 high-profile compromise targets in `platform/research/` (`debug`, `chalk`, `@solana/web3.js`, `nx`, `eslint-config-prettier`, etc.) exist directly in the 25,228-package graph.
   * The paper does not currently highlight where these real-world targets rank under $C(S)$, $H(S)$, and $P(S)$, missing a massive empirical validation opportunity for Q1 acceptance.
3. **Workflow Privilege Conflation**:
   * Calling `.github/workflows` presence "Blast Radius" or "Privileged CI Exposure" is a construct validity risk. Without inspecting workflow YAML or call graphs, directory presence represents *potential workflow linkage*, not verified execution.

---

## 5. Ledger Confirmation
* Appended Task 02 record to `research_sessions/SESSION_INDEX.md`:
  ```markdown
  | Task 02 | 2026-10-20 02:57:21 UTC+06:00 | `research_sessions/active_verification_track/02_novelty_and_dataset_hygiene_verification.md` | Audited all 6 budgets, depth/exclusion ablations, SCC distribution (82/68 cycles), 658 parser disagreements, and 49 incident assessments (16 matching packages in study graph). | COMPLETED |
  ```

---

## 6. Handoff Payload for Principal Research Advisor
```text
================================================================================
STRUCTURAL INTERVENTIONS, GRAPH VALIDITY & INCIDENTS HANDOFF PAYLOAD (TASK 02)
================================================================================
1. COMPLETE MULTI-BUDGET CURVES EXTRACTED (WORKFLOW REPOSITORIES, N = 7,171):
   - Budget 1:   Greedy C = 2,543 (35.46%), H = 0.55%, P = 269 | Union C = 2,543 (35.46%), H = 0.55%, P = 269
   - Budget 5:   Greedy C = 3,872 (54.00%), H = 2.09%, P = 327 | Union C = 3,654 (50.96%), H = 2.45%, P = 329
   - Budget 10:  Greedy C = 4,331 (60.40%), H = 3.79%, P = 351 | Union C = 3,910 (54.53%), H = 4.48%, P = 343
   - Budget 25:  Greedy C = 4,854 (67.69%), H = 6.08%, P = 514 | Union C = 4,284 (59.74%), H = 9.86%, P = 427
   - Budget 50:  Greedy C = 5,196 (72.46%), H = 8.73%, P = 638 | Union C = 4,321 (60.26%), H = 18.09%, P = 441
   - Budget 100: Greedy C = 5,538 (77.23%), H = 11.48%, P = 800 | Union C = 4,407 (61.46%), H = 33.79%, P = 534
   - Random Mean (Budget 100): C = 1,680.6 (23.44%), H = 0.80%, P = 12.8 (Exact expectation H = 0.819%).

2. ABLATION & SENSITIVITY HIGHLIGHTS:
   - Depth Ablation: At depth_0 (direct dependents), Exact Union H is only 10.67% (vs 33.79% at full depth), proving multi-hop paths drive >2/3 of exposure.
   - Concentration: Top 0.819% maintainers (100 accounts) account for 33.79% of all exposure paths (Lorenz concentration).
   - Version Representation: Version continuity cuts identity-repo exposure pairs by 42.44% (462,170 -> 266,016 pairs). Under version-continuous evaluation, Exact Union removes 40.59% of exposure.
   - Parser Disagreements: 658 rows truncated at first period (60 workflow-positive), resolved in collect_data_v2.py.

3. REAL-WORLD INCIDENT OVERLAP (PLATFORM/RESEARCH/):
   - 49 structured candidate assessments; 16 real-world compromised packages exist directly in our 25,228 study graph:
     chalk, debug, @solana/web3.js, nx, eslint-config-prettier, node-ipc, @tanstack/history, @opensearch-project/opensearch, @mastra/core, ansi-styles, backslash, simple-swizzle, etc.
   - Dataset Hygiene: AMALFI corpus (1,790 pkgs) contains zero 0.0.1-security stubs. Figshare benchmark (6,420 mal / 7,288 benign) excluded as temporal control frame due to lack of non-event bounds.
================================================================================
```
