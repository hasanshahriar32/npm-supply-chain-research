# Task 01: Workspace Extraction, Manifest Inventory, and Manuscript Baseline

> **Context**: Executed in accordance with the Master System Directive and Task 01 instructions from `manuscript/review/NPM Research Verification and Workflow.docx`. All session logging rules and the mandatory 6-section schema are strictly applied.

# Workspace Extraction, Full Manifest Audit, and Manuscript Baseline

## 1. Execution Metadata
* **Timestamp**: `2026-10-20 01:41:32 UTC+06:00`
* **Working Directory**: `/home/ashik/Desktop/npm-supply-chain-research`
* **Inspected Artifacts and Archives**:
  * Root Archive: `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` (Size: `237,370` bytes, SHA-256: `4d6cc93fa2c74e73a9040cec967fb28a27bd8f7b42eea3b768273b12139d68b7`)
  * Unpacked Directory: `extracted_manuscript_source/` (17 LaTeX, BibTeX, figures, and results files)
  * Active Manuscript Workspace: `manuscript/` (containing updated LaTeX, precompiled PDFs `main.pdf` and `main_authors.pdf`, results directories `graph_validity/`, `structural_interventions/`, and `prospective_cohort/`)
  * Data Pipelines & Core Scripts: `scripts/study_structural_interventions.py`, `scripts/study_graph_validity.py`, `scripts/freeze_prospective_cohort.py`, `scripts/collect_data_v2.py`, `scripts/research_observations.py`, `scripts/validate_observation_semantics.py`, `scripts/validate_research_study.py`, `scripts/calculate_metrics.py`, `scripts/collect_data.py`
* **Exact Commands Run**:
  ```bash
  mkdir -p research_sessions/active_verification_track
  unzip -q NPM_Supply_Chain_IEEE_Anonymous_Source.zip -d extracted_manuscript_source/
  python3 scripts/validate_observation_semantics.py
  python3 scripts/validate_research_study.py
  python3 scripts/generate_task01_report.py
  ```

---

## 2. Quantitative and Structural Findings

### 2.1 Unpack Nested Archive Confirmation
* The nested anonymous source archive `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` was successfully verified and extracted into `extracted_manuscript_source/`.
* The archive preserves the standalone typesetting package including `main.tex`, `compile.sh`, `README.md`, `config/`, `sections/`, `tables/`, `figures/`, `results/`, and `bibliography/`.
* Original zip archive retained intact at workspace root with SHA-256: `4d6cc93fa2c74e73a9040cec967fb28a27bd8f7b42eea3b768273b12139d68b7`.

### 2.2 Full Workspace File Inventory
Total project files matching extensions (`.tex`, `.bib`, `.py`, `.js`, `.ts`, `.sh`, `.json`, `.csv`, `.md`): **373 files**.

| Relative File Path | Size (Bytes) | Line Count |
|---|---:|---:|
| `README.md` | 8,990 | 95 |
| `docs/work_summary.md` | 2,575 | 23 |
| `extracted_manuscript_source/README.md` | 645 | 11 |
| `extracted_manuscript_source/bibliography/references.bib` | 5,080 | 95 |
| `extracted_manuscript_source/compile.sh` | 1,242 | 27 |
| `extracted_manuscript_source/config/metadata.tex` | 586 | 11 |
| `extracted_manuscript_source/config/preamble.tex` | 592 | 19 |
| `extracted_manuscript_source/figures/evidence_pipeline.tex` | 1,147 | 18 |
| `extracted_manuscript_source/main.tex` | 892 | 27 |
| `extracted_manuscript_source/results/field_rows.tex` | 399 | 10 |
| `extracted_manuscript_source/results/numbers.tex` | 418 | 11 |
| `extracted_manuscript_source/sections/00_abstract.tex` | 1,492 | 3 |
| `extracted_manuscript_source/sections/01_introduction.tex` | 2,084 | 10 |
| `extracted_manuscript_source/sections/02_related_work.tex` | 1,915 | 10 |
| `extracted_manuscript_source/sections/03_problem_and_evidence.tex` | 2,285 | 34 |
| `extracted_manuscript_source/sections/04_audit_method.tex` | 2,585 | 24 |
| `extracted_manuscript_source/sections/05_results.tex` | 8,490 | 77 |
| `extracted_manuscript_source/sections/06_benchmark_design.tex` | 1,983 | 9 |
| `extracted_manuscript_source/sections/07_validity_and_ethics.tex` | 1,643 | 8 |
| `extracted_manuscript_source/sections/08_conclusion.tex` | 571 | 2 |
| `extracted_manuscript_source/sections/09_acknowledgment.tex` | 309 | 2 |
| `extracted_manuscript_source/tables/literature_positioning.tex` | 1,585 | 18 |
| `manuscript/README.md` | 10,696 | 104 |
| `manuscript/bibliography/references.bib` | 6,084 | 114 |
| `manuscript/compile.sh` | 1,353 | 32 |
| `manuscript/config/authors.tex` | 514 | 8 |
| `manuscript/config/metadata.tex` | 596 | 11 |
| `manuscript/config/preamble.tex` | 592 | 19 |
| `manuscript/figures/evidence_pipeline.tex` | 1,147 | 18 |
| `manuscript/guideline/guide.md` | 5,655 | 87 |
| `manuscript/main.tex` | 907 | 27 |
| `manuscript/main_authors.tex` | 195 | 4 |
| `manuscript/research/2026-10-20_groundwork_assessment.md` | 19,726 | 131 |
| `manuscript/research/2026-10-20_literature_extension.md` | 15,462 | 92 |
| `manuscript/research/2026-10-20_research_status.json` | 6,911 | 151 |
| `manuscript/research/2026-10-20_study_protocol.md` | 4,227 | 36 |
| `manuscript/research/2026-10-20_verified_sources.csv` | 6,722 | 18 |
| `manuscript/research/claim_evidence.csv` | 11,360 | 46 |
| `manuscript/research/extended_benchmark_design.md` | 11,028 | 96 |
| `manuscript/research/novelty_assessment.md` | 11,283 | 72 |
| `manuscript/research/repository_context.md` | 8,211 | 57 |
| `manuscript/research/structural_interventions_notes.md` | 13,485 | 92 |
| `manuscript/results/artifact_audit.json` | 9,207 | 333 |
| `manuscript/results/author_versions_validation.json` | 938 | 34 |
| `manuscript/results/field_comparison.csv` | 337 | 8 |
| `manuscript/results/field_rows.tex` | 399 | 10 |
| `manuscript/results/graph_validity/nontrivial_components.csv` | 19,309 | 151 |
| `manuscript/results/graph_validity/per_package.csv` | 2,758,916 | 25,229 |
| `manuscript/results/graph_validity/queue_membership.csv` | 115,489 | 2,278 |
| `manuscript/results/graph_validity/repository_parser_disagreements.csv` | 72,571 | 659 |
| `manuscript/results/graph_validity/repository_units.csv` | 454,894 | 12,744 |
| `manuscript/results/graph_validity/source_access/access_attempts.json` | 5,855 | 153 |
| `manuscript/results/graph_validity/source_access/chrono_resolution_release_metadata.json` | 5,774 | 1 |
| `manuscript/results/graph_validity/source_access/deps_dev_is_number.json` | 148 | 1 |
| `manuscript/results/graph_validity/source_access/npm_metadata_is_number.json` | 2,161 | 99 |
| `manuscript/results/graph_validity/source_access/osv_keyv_reported_outcomes.json` | 7,261 | 1 |
| `manuscript/results/graph_validity/source_access/sandbox_access_attempts.json` | 3,026 | 85 |
| `manuscript/results/graph_validity/summary.json` | 26,709 | 637 |
| `manuscript/results/graph_validity/version_projection_witnesses.json` | 3,794 | 170 |
| `manuscript/results/numbers.tex` | 418 | 11 |
| `manuscript/results/prospective_cohort/README.md` | 1,130 | 9 |
| `manuscript/results/prospective_cohort/cohort_status.json` | 1,855 | 39 |
| `manuscript/results/prospective_cohort/selection_manifest.json` | 4,732 | 125 |
| `manuscript/results/research_method_rows.tex` | 486 | 10 |
| `manuscript/results/research_numbers.tex` | 566 | 13 |
| `manuscript/results/structural_interventions/ablations.csv` | 77,409 | 379 |
| `manuscript/results/structural_interventions/concentration.csv` | 2,246 | 31 |
| `manuscript/results/structural_interventions/deterministic_curves.csv` | 27,125 | 151 |
| `manuscript/results/structural_interventions/identity_grouping_sensitivity.csv` | 7,897 | 37 |
| `manuscript/results/structural_interventions/independent_validation.json` | 363 | 10 |
| `manuscript/results/structural_interventions/manifest.json` | 5,171 | 60 |
| `manuscript/results/structural_interventions/random_analytic_expectations.csv` | 3,234 | 31 |
| `manuscript/results/structural_interventions/random_summary.csv` | 11,235 | 31 |
| `manuscript/results/structural_interventions/random_trials.csv` | 1,049,602 | 6,001 |
| `manuscript/results/structural_interventions/repository_mapping_sensitivity.csv` | 6,218 | 31 |
| `manuscript/results/structural_interventions/results.json` | 853,687 | 18,933 |
| `manuscript/results/structural_interventions/run_config.json` | 2,853 | 247 |
| `manuscript/results/structural_interventions/version_representation_curves.csv` | 57,827 | 271 |
| `manuscript/results/submission_compliance.json` | 4,041 | 157 |
| `manuscript/results/validation_report.md` | 3,521 | 33 |
| `manuscript/scripts/audit_artifacts.py` | 15,536 | 250 |
| `manuscript/scripts/check_submission.py` | 4,874 | 91 |
| `manuscript/scripts/package_overleaf.py` | 3,413 | 53 |
| `manuscript/scripts/render_figures.py` | 2,421 | 46 |
| `manuscript/scripts/render_research_figures.py` | 9,290 | 168 |
| `manuscript/scripts/verify_manuscript.py` | 3,484 | 59 |
| `manuscript/sections/00_abstract.tex` | 1,481 | 3 |
| `manuscript/sections/01_introduction.tex` | 2,880 | 10 |
| `manuscript/sections/02_related_work.tex` | 2,265 | 9 |
| `manuscript/sections/03_problem_and_evidence.tex` | 3,327 | 13 |
| `manuscript/sections/04_audit_method.tex` | 4,413 | 39 |
| `manuscript/sections/05_results.tex` | 4,666 | 45 |
| `manuscript/sections/06_benchmark_design.tex` | 2,971 | 12 |
| `manuscript/sections/07_validity_and_ethics.tex` | 1,871 | 8 |
| `manuscript/sections/08_conclusion.tex` | 748 | 2 |
| `manuscript/sections/09_acknowledgment.tex` | 347 | 2 |
| `manuscript/submission_files/author_details.md` | 1,802 | 26 |
| `manuscript/submission_files/authors.json` | 730 | 21 |
| `manuscript/submission_files/guideline_compliance.md` | 4,087 | 35 |
| `manuscript/submission_files/preparation_notes.md` | 1,844 | 11 |
| `manuscript/submission_files/requirements.json` | 1,552 | 30 |
| `manuscript/tables/literature_positioning.tex` | 1,585 | 18 |
| `platform/README.md` | 3,986 | 68 |
| `platform/client/public/__manus__/debug-collector.js` | 25,168 | 821 |
| `platform/client/src/_core/hooks/useAuth.ts` | 2,857 | 98 |
| `platform/client/src/const.ts` | 1,465 | 31 |
| `platform/client/src/hooks/useComposition.ts` | 2,333 | 81 |
| `platform/client/src/hooks/usePersistFn.ts` | 471 | 20 |
| `platform/client/src/lib/trpc.ts` | 162 | 4 |
| `platform/client/src/lib/utils.ts` | 169 | 6 |
| `platform/components.json` | 388 | 19 |
| `platform/docs/clerk_migration_notes.md` | 1,046 | 12 |
| `platform/docs/clerk_verification_notes.md` | 1,397 | 11 |
| `platform/docs/enhancement_verification.md` | 89,381 | 417 |
| `platform/drizzle/meta/0000_snapshot.json` | 2,593 | 110 |
| `platform/drizzle/meta/_journal.json` | 208 | 13 |
| `platform/drizzle/relations.ts` | 27 | 1 |
| `platform/drizzle/researchSchema.ts` | 4,232 | 90 |
| `platform/drizzle/schema.ts` | 1,195 | 28 |
| `platform/drizzle.config.ts` | 353 | 15 |
| `platform/drizzle.research.config.ts` | 261 | 10 |
| `platform/lib/trpc.ts` | 334 | 6 |
| `platform/next-env.d.ts` | 298 | 7 |
| `platform/package.json` | 4,372 | 126 |
| `platform/pages/api/cron/research-ingestion.ts` | 734 | 14 |
| `platform/pages/api/trpc/[trpc].ts` | 257 | 5 |
| `platform/proxy.ts` | 304 | 11 |
| `platform/research/00_research_brief.md` | 7,828 | 76 |
| `platform/research/01_claim_and_implementation_audit.md` | 7,038 | 59 |
| `platform/research/02_source_inventory.csv` | 7,282 | 29 |
| `platform/research/03_definitions_and_notation.md` | 4,989 | 91 |
| `platform/research/100_future_outcome_manifest_sealing_protocol.json` | 16,272 | 222 |
| `platform/research/101_future_public_safe_aggregate_release_policy.json` | 14,847 | 172 |
| `platform/research/102_future_aggregate_plan_parameter_sealing_contract.json` | 15,406 | 184 |
| `platform/research/103_crossenv_typosquatting_candidate_assessment.json` | 4,817 | 91 |
| `platform/research/104_flatmap_stream_candidate_assessment.json` | 5,175 | 93 |
| `platform/research/105_colors_faker_protestware_candidate_assessment.json` | 4,772 | 93 |
| `platform/research/106_peacenotwar_protestware_candidate_assessment.json` | 5,561 | 125 |
| `platform/research/107_debug_september_2025_candidate_screen_notes.md` | 2,638 | 28 |
| `platform/research/108_debug_september_2025_candidate_assessment.json` | 4,520 | 86 |
| `platform/research/109_solana_web3_js_december_2024_candidate_screen_notes.md` | 2,339 | 24 |
| `platform/research/10_literature_review.md` | 11,466 | 105 |
| `platform/research/110_solana_web3_js_december_2024_candidate_assessment.json` | 4,783 | 104 |
| `platform/research/111_chalk_september_2025_candidate_screen_notes.md` | 2,257 | 24 |
| `platform/research/112_chalk_september_2025_candidate_assessment.json` | 3,669 | 74 |
| `platform/research/113_ledger_connect_kit_december_2023_candidate_screen_notes.md` | 2,254 | 25 |
| `platform/research/114_ledger_connect_kit_december_2023_candidate_assessment.json` | 2,182 | 56 |
| `platform/research/115_eslint_config_prettier_july_2025_candidate_screen_notes.md` | 1,235 | 14 |
| `platform/research/116_eslint_config_prettier_registry_assessment_pending.md` | 714 | 5 |
| `platform/research/117_eslint_config_prettier_july_2025_candidate_assessment.json` | 1,290 | 38 |
| `platform/research/118_tanstack_may_2026_candidate_screen_notes.md` | 1,139 | 12 |
| `platform/research/119_eslint_plugin_prettier_july_2025_candidate_assessment.json` | 1,472 | 37 |
| `platform/research/11_literature_matrix.csv` | 5,837 | 16 |
| `platform/research/120_jscrambler_july_2026_candidate_screen_notes.md` | 1,521 | 16 |
| `platform/research/121_jscrambler_july_2026_candidate_assessment.json` | 1,511 | 41 |
| `platform/research/122_node_ipc_march_2022_candidate_screen_notes.md` | 2,153 | 24 |
| `platform/research/123_node_ipc_march_2022_candidate_assessment.json` | 1,482 | 39 |
| `platform/research/124_noblox_related_candidate_discovery_notes.md` | 2,190 | 20 |
| `platform/research/125_noblox_js_proxy_october_2021_candidate_assessment.json` | 5,062 | 106 |
| `platform/research/126_lottie_player_october_2024_candidate_screen_notes.md` | 1,484 | 16 |
| `platform/research/127_lottie_player_october_2024_candidate_assessment.json` | 5,717 | 165 |
| `platform/research/128_nx_august_2025_candidate_screen_notes.md` | 1,951 | 18 |
| `platform/research/129_nx_august_2025_candidate_assessment.json` | 81,880 | 2,780 |
| `platform/research/12_research_taxonomy.md` | 4,851 | 47 |
| `platform/research/130_country_currency_map_march_2025_candidate_screen_notes.md` | 1,620 | 14 |
| `platform/research/131_country_currency_map_march_2025_candidate_assessment.json` | 4,478 | 118 |
| `platform/research/132_html_to_gutenberg_may_2026_candidate_screen_notes.md` | 2,978 | 30 |
| `platform/research/133_html_to_gutenberg_may_2026_candidate_assessment.json` | 4,630 | 121 |
| `platform/research/134_opensearch_may_2026_discovery_screen_notes.md` | 1,996 | 17 |
| `platform/research/135_common_stack_generate_plugin_may_2026_candidate_screen_notes.md` | 2,259 | 19 |
| `platform/research/136_common_stack_generate_plugin_may_2026_candidate_assessment.json` | 18,615 | 656 |
| `platform/research/137_sbx_mask_march_2026_candidate_screen_notes.md` | 3,039 | 30 |
| `platform/research/138_sbx_mask_march_2026_candidate_assessment.json` | 4,041 | 102 |
| `platform/research/139_bitwarden_cli_april_2026_candidate_screen_notes.md` | 3,130 | 30 |
| `platform/research/140_bitwarden_cli_april_2026_candidate_assessment.json` | 7,030 | 220 |
| `platform/research/141_react_native_country_select_march_2026_candidate_screen_notes.md` | 2,278 | 24 |
| `platform/research/142_react_native_country_select_march_2026_candidate_assessment.json` | 4,849 | 120 |
| `platform/research/143_rand_user_agent_may_2025_candidate_screen_notes.md` | 2,075 | 20 |
| `platform/research/144_rand_user_agent_may_2025_candidate_assessment.json` | 8,150 | 295 |
| `platform/research/145_joyfill_components_july_2026_candidate_screen_notes.md` | 2,482 | 20 |
| `platform/research/146_joyfill_components_july_2026_candidate_assessment.json` | 3,324 | 70 |
| `platform/research/147_asyncapi_generator_july_2026_candidate_screen_notes.md` | 2,443 | 20 |
| `platform/research/148_asyncapi_generator_july_2026_candidate_assessment.json` | 8,710 | 329 |
| `platform/research/149_dydx_v4_client_february_2026_candidate_screen_notes.md` | 3,166 | 28 |
| `platform/research/150_dydx_v4_client_february_2026_candidate_assessment.json` | 7,581 | 269 |
| `platform/research/151_dydx_solo_september_2022_candidate_screen_notes.md` | 3,840 | 34 |
| `platform/research/152_dydx_solo_september_2022_candidate_assessment.json` | 7,930 | 275 |
| `platform/research/153_got_fetch_july_2025_candidate_screen_notes.md` | 1,339 | 18 |
| `platform/research/154_got_fetch_july_2025_candidate_assessment.json` | 3,569 | 68 |
| `platform/research/155_tanstack_history_may_2026_candidate_assessment.json` | 2,422 | 46 |
| `platform/research/156_ctrl_tinycolor_september_2025_candidate_screen_notes.md` | 1,722 | 15 |
| `platform/research/157_ctrl_tinycolor_september_2025_candidate_assessment.json` | 2,899 | 63 |
| `platform/research/158_ansi_styles_september_2025_candidate_assessment.json` | 1,254 | 33 |
| `platform/research/159_backslash_september_2025_candidate_assessment.json` | 1,216 | 32 |
| `platform/research/160_simple_swizzle_september_2025_candidate_assessment.json` | 1,207 | 31 |
| `platform/research/161_cloudplatform_search_may_2026_candidate_screen_notes.md` | 869 | 6 |
| `platform/research/162_opensearch_client_may_2026_candidate_assessment.json` | 1,045 | 33 |
| `platform/research/163_redhat_cloud_services_chrome_june_2026_candidate_assessment.json` | 2,556 | 47 |
| `platform/research/164_t_in_one_add_application_may_2026_candidate_assessment.json` | 3,182 | 64 |
| `platform/research/165_mastra_core_june_2026_candidate_assessment.json` | 2,384 | 45 |
| `platform/research/166_easy_day_js_june_2026_candidate_assessment.json` | 2,445 | 45 |
| `platform/research/167_echarts_for_react_may_2026_candidate_assessment.json` | 2,796 | 56 |
| `platform/research/168_node_ipc_may_2026_candidate_assessment.json` | 2,313 | 47 |
| `platform/research/169_redhat_compliance_client_june_2026_candidate_assessment.json` | 2,466 | 46 |
| `platform/research/170_redhat_config_manager_client_june_2026_candidate_assessment.json` | 2,482 | 46 |
| `platform/research/171_redhat_entitlements_client_june_2026_candidate_assessment.json` | 2,974 | 60 |
| `platform/research/172_atomic_arch_aur_cross_ecosystem_study.md` | 11,087 | 90 |
| `platform/research/173_atomic_arch_aur_candidate_assessment.json` | 2,681 | 50 |
| `platform/research/174_noblox_js_proxy_server_january_2024_candidate_screen_notes.md` | 3,992 | 38 |
| `platform/research/175_noblox_js_proxy_server_january_2024_candidate_assessment.json` | 2,796 | 59 |
| `platform/research/178_cloudplatform_search_may_2026_candidate_assessment.json` | 2,053 | 50 |
| `platform/research/20_novelty_and_gap_analysis.md` | 8,951 | 114 |
| `platform/research/21_research_questions_and_hypotheses.md` | 4,950 | 76 |
| `platform/research/30_proposed_methodology.md` | 10,708 | 176 |
| `platform/research/31_data_dictionary.md` | 7,232 | 100 |
| `platform/research/32_labeling_protocol.md` | 5,437 | 92 |
| `platform/research/33_temporal_split_and_leakage_controls.md` | 4,256 | 67 |
| `platform/research/34_threats_to_validity.md` | 4,712 | 81 |
| `platform/research/35_ethics_and_responsible_disclosure.md` | 3,880 | 39 |
| `platform/research/40_reproducibility_roadmap.md` | 4,790 | 112 |
| `platform/research/41_repository_change_plan.md` | 3,043 | 45 |
| `platform/research/43_data_provenance_and_checksums.md` | 2,553 | 59 |
| `platform/research/50_gap_resolution_study_protocol.md` | 100,293 | 589 |
| `platform/research/51_current_snapshot_findings.md` | 5,170 | 49 |
| `platform/research/51_current_snapshot_structural_analysis.json` | 2,756 | 93 |
| `platform/research/51_current_snapshot_top_legacy_structural_scores.csv` | 2,037 | 51 |
| `platform/research/52_seed_incident_registry.csv` | 1,841 | 5 |
| `platform/research/52_seed_incident_registry.md` | 2,267 | 22 |
| `platform/research/53_feature_availability_ledger.csv` | 3,191 | 12 |
| `platform/research/54_ecosystem_archive_schema_profile.json` | 6,383 | 277 |
| `platform/research/55_current_snapshot_ecosystem_findings.md` | 6,163 | 50 |
| `platform/research/55_current_snapshot_ecosystem_structure.json` | 2,648 | 73 |
| `platform/research/55_top_maintainer_portfolios.csv` | 916 | 51 |
| `platform/research/60_temporal_source_and_feasibility_audit.md` | 18,672 | 122 |
| `platform/research/61_temporal_pilot_protocol.md` | 6,029 | 63 |
| `platform/research/62_temporal_pilot_metadata_ledger.csv` | 23,842 | 131 |
| `platform/research/62_temporal_pilot_summary.json` | 2,305 | 65 |
| `platform/research/63_temporal_label_adjudication_ledger.csv` | 850 | 4 |
| `platform/research/64_package_level_temporal_companion_protocol.md` | 3,636 | 36 |
| `platform/research/64_temporal_package_event_ledger.csv` | 33,768 | 48 |
| `platform/research/65_package_temporal_companion_declared_edges.csv` | 49,413 | 259 |
| `platform/research/65_package_temporal_companion_diagnostics.json` | 10,999 | 281 |
| `platform/research/65_package_temporal_companion_snapshots.csv` | 16,095 | 48 |
| `platform/research/66_temporal_baseline_and_calibration_gate.json` | 13,579 | 348 |
| `platform/research/67_cutoff_direct_dependency_graph_edges.csv` | 84,589 | 259 |
| `platform/research/67_cutoff_direct_dependency_graph_manifest.json` | 28,332 | 599 |
| `platform/research/68_temporal_reconstruction_and_baseline_results.md` | 125,611 | 924 |
| `platform/research/69_temporal_incident_label_adjudication.md` | 61,611 | 399 |
| `platform/research/70_cutoff_direct_dependency_range_resolution.csv` | 174,526 | 259 |
| `platform/research/70_cutoff_direct_dependency_range_resolution_manifest.json` | 1,555 | 30 |
| `platform/research/71_direct_range_resolution_diagnostic.json` | 7,274 | 230 |
| `platform/research/72_chrono_resolution_archive_inventory.json` | 1,275 | 43 |
| `platform/research/73_chrono_resolution_streaming_attempt.json` | 1,405 | 18 |
| `platform/research/74_bounded_recursive_registry_semver_graph_edges.csv` | 1,257,054 | 1,849 |
| `platform/research/74_bounded_recursive_registry_semver_graph_manifest.json` | 14,719 | 454 |
| `platform/research/75_bounded_recursive_registry_graph_diagnostic.json` | 10,332 | 414 |
| `platform/research/76_amalfi_artifact_commit.json` | 133 | 5 |
| `platform/research/76_amalfi_basic_corpus.csv` | 110,210 | 1,791 |
| `platform/research/77_amalfi_release_sensitivity_diagnostics.json` | 1,245 | 27 |
| `platform/research/77_amalfi_release_sensitivity_ledger.csv` | 950,410 | 1,791 |
| `platform/research/78_amalfi_release_sensitivity_gate.json` | 1,961 | 40 |
| `platform/research/79_control_frame_resolution.md` | 4,898 | 50 |
| `platform/research/80_datadog_positive_membership_overlap.json` | 34,278 | 891 |
| `platform/research/81_provider_control_frame_assessment.md` | 4,896 | 47 |
| `platform/research/81_provider_control_frame_probe.json` | 1,554 | 26 |
| `platform/research/82_shai_hulud_second_coming_candidate_assessment.json` | 3,087 | 63 |
| `platform/research/83_control_frame_contract_and_access_assessment.md` | 6,909 | 65 |
| `platform/research/84_mini_shai_hulud_atool_candidate_assessment.json` | 3,391 | 76 |
| `platform/research/85_figshare_npm_benchmark_control_frame_assessment.json` | 3,439 | 70 |
| `platform/research/86_github_advisory_database_malware_path_assessment.json` | 1,984 | 31 |
| `platform/research/87_npm_follower_population_access_assessment.json` | 1,956 | 36 |
| `platform/research/88_supplytgn_methodology_transfer_assessment.json` | 1,681 | 30 |
| `platform/research/89_original_sin_npm_control_frame_assessment.json` | 1,994 | 30 |
| `platform/research/90_authorized_npm_control_frame_access_specification.json` | 7,214 | 123 |
| `platform/research/90_final_research_report.md` | 16,049 | 150 |
| `platform/research/90_gap_resolution_report.md` | 15,984 | 125 |
| `platform/research/91_executive_decision_memo.md` | 3,513 | 58 |
| `platform/research/91_is_package_compromise_candidate_assessment.json` | 3,800 | 76 |
| `platform/research/92_keyv_compromise_candidate_assessment.json` | 4,804 | 91 |
| `platform/research/92_priority_backlog.md` | 3,745 | 69 |
| `platform/research/93_gap_resolution_evidence_log.md` | 135,725 | 788 |
| `platform/research/94_campaign_relatedness_and_grouped_inference_protocol.json` | 28,150 | 781 |
| `platform/research/95_release_authority_metadata_availability_audit.json` | 67,204 | 1,314 |
| `platform/research/96_release_authority_delta_semantics_protocol.json` | 11,026 | 147 |
| `platform/research/97_official_npm_provenance_attestation_access_assessment.json` | 3,971 | 67 |
| `platform/research/98_full_ledger_source_object_retention_census.json` | 41,852 | 765 |
| `platform/research/99_release_authority_raw_evidence_capture_contract.json` | 15,628 | 235 |
| `platform/research/README.md` | 4,234 | 66 |
| `platform/research/benchmark_chart_data.json` | 2,544 | 131 |
| `platform/research/benchmark_snapshot_manifest.json` | 646 | 17 |
| `platform/scripts/analyze_ecosystem_structure.py` | 11,747 | 242 |
| `platform/scripts/profile_ecosystem_archive.py` | 3,552 | 89 |
| `platform/server/_core/context.ts` | 658 | 28 |
| `platform/server/_core/cookies.ts` | 1,299 | 48 |
| `platform/server/_core/dataApi.ts` | 1,899 | 64 |
| `platform/server/_core/env.ts` | 428 | 10 |
| `platform/server/_core/heartbeat.ts` | 6,784 | 213 |
| `platform/server/_core/imageGeneration.ts` | 4,458 | 160 |
| `platform/server/_core/index.ts` | 1,990 | 66 |
| `platform/server/_core/llm.ts` | 10,778 | 454 |
| `platform/server/_core/map.ts` | 9,151 | 319 |
| `platform/server/_core/nextProductionServer.ts` | 1,111 | 29 |
| `platform/server/_core/notification.ts` | 3,139 | 114 |
| `platform/server/_core/oauth.ts` | 2,429 | 65 |
| `platform/server/_core/sdk.ts` | 10,054 | 350 |
| `platform/server/_core/storageProxy.ts` | 1,392 | 48 |
| `platform/server/_core/systemRouter.ts` | 709 | 29 |
| `platform/server/_core/trpc.ts` | 1,033 | 45 |
| `platform/server/_core/types/cookie.d.ts` | 137 | 6 |
| `platform/server/_core/types/manusTypes.ts` | 1,406 | 71 |
| `platform/server/_core/vite.ts` | 1,901 | 67 |
| `platform/server/_core/voiceTranscription.ts` | 8,107 | 284 |
| `platform/server/auth.logout.test.ts` | 1,625 | 62 |
| `platform/server/clerk-connection.test.ts` | 580 | 16 |
| `platform/server/clerkAuth.test.ts` | 1,588 | 46 |
| `platform/server/clerkAuth.ts` | 1,543 | 38 |
| `platform/server/db.ts` | 2,511 | 92 |
| `platform/server/github-ingestion-connection.test.ts` | 665 | 18 |
| `platform/server/platformDb.ts` | 7,220 | 145 |
| `platform/server/postgres-connection.test.ts` | 857 | 23 |
| `platform/server/productionPackaging.test.ts` | 1,350 | 25 |
| `platform/server/researchIngestion.ts` | 5,777 | 66 |
| `platform/server/researchIngestionCron.test.ts` | 1,194 | 27 |
| `platform/server/researchRouter.test.ts` | 4,263 | 67 |
| `platform/server/researchRouter.ts` | 4,278 | 49 |
| `platform/server/researchSources.test.ts` | 112,859 | 1,077 |
| `platform/server/researchSources.ts` | 31,395 | 131 |
| `platform/server/researchTypes.ts` | 1,133 | 53 |
| `platform/server/routers.ts` | 980 | 28 |
| `platform/server/storage.ts` | 3,052 | 97 |
| `platform/server/trpc.ts` | 952 | 20 |
| `platform/shared/_core/errors.ts` | 601 | 19 |
| `platform/shared/const.ts` | 1,549 | 37 |
| `platform/shared/types.ts` | 158 | 7 |
| `platform/template.json` | 15,383 | 21 |
| `platform/todo.md` | 43,517 | 317 |
| `platform/tsconfig.json` | 861 | 46 |
| `platform/vercel.json` | 147 | 6 |
| `platform/vite.config.ts` | 5,765 | 187 |
| `platform/vitest.config.ts` | 499 | 19 |
| `research/00_research_brief.md` | 7,828 | 76 |
| `research/01_claim_and_implementation_audit.md` | 7,038 | 59 |
| `research/02_source_inventory.csv` | 7,282 | 29 |
| `research/03_definitions_and_notation.md` | 4,989 | 91 |
| `research/10_literature_review.md` | 11,466 | 105 |
| `research/11_literature_matrix.csv` | 5,837 | 16 |
| `research/12_research_taxonomy.md` | 4,851 | 47 |
| `research/20_novelty_and_gap_analysis.md` | 8,951 | 114 |
| `research/21_research_questions_and_hypotheses.md` | 4,950 | 76 |
| `research/30_proposed_methodology.md` | 10,708 | 176 |
| `research/31_data_dictionary.md` | 7,232 | 100 |
| `research/32_labeling_protocol.md` | 5,437 | 92 |
| `research/33_temporal_split_and_leakage_controls.md` | 4,256 | 67 |
| `research/34_threats_to_validity.md` | 4,712 | 81 |
| `research/35_ethics_and_responsible_disclosure.md` | 3,880 | 39 |
| `research/40_reproducibility_roadmap.md` | 4,790 | 112 |
| `research/41_repository_change_plan.md` | 3,043 | 45 |
| `research/43_data_provenance_and_checksums.md` | 2,553 | 59 |
| `research/90_final_research_report.md` | 16,049 | 150 |
| `research/91_executive_decision_memo.md` | 3,513 | 58 |
| `research/92_priority_backlog.md` | 3,745 | 69 |
| `research/README.md` | 4,234 | 66 |
| `scripts/calculate_metrics.py` | 10,689 | 264 |
| `scripts/check_progress.py` | 1,229 | 43 |
| `scripts/collect_data.py` | 30,230 | 709 |
| `scripts/collect_data_v2.py` | 3,585 | 63 |
| `scripts/freeze_prospective_cohort.py` | 13,581 | 229 |
| `scripts/generate_task01_report.py` | 24,261 | 345 |
| `scripts/research_observations.py` | 3,097 | 68 |
| `scripts/study_graph_validity.py` | 29,919 | 455 |
| `scripts/study_structural_interventions.py` | 44,989 | 755 |
| `scripts/validate_observation_semantics.py` | 2,120 | 32 |
| `scripts/validate_research_study.py` | 5,397 | 117 |

### 2.3 Verbatim Manuscript Extraction

#### A. Manuscript Titles
* **Anonymous Source Archive (`extracted_manuscript_source/config/metadata.tex`)**:
  > `"Auditing the Blast Radius: Artifact Consistency in npm Supply-Chain Prioritization"`
* **Active Working Manuscript (`manuscript/config/metadata.tex`)**:
  > `"Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation"`

#### B. Full Abstracts (Verbatim)

##### 1. Archive Abstract (`extracted_manuscript_source/sections/00_abstract.tex`):
> "Dependency reach, shared maintainers, and public continuous integration workflows offer useful but incomplete views of software supply-chain exposure. Their combination into a predictive score requires internally consistent artifacts and a defensible outcome population. We audit an npm research repository containing 25,228 packages and two compressed metric artifacts. Independent recomputation reproduces all seven database metric fields, yet the companion CSV disagrees on workflow reach for 17,809 packages: only 20 have nonzero values in the CSV, compared with 17,809 in the database. At a one-percent review budget of 253 packages, their equal-weight score queues share only 65 entries. Large score ties further affect queue membership. Separately, the incident companion contains 47 package-event records and 45 retained pre-event source objects, but supplies no cutoff-valid control population. These findings establish artifact inconsistency and evaluation ineligibility, rather than predictive accuracy. We provide an offline audit, aggregate results, and an evidence-aware protocol separating structural exposure, workflow configuration, release authority, and future documented compromise. The contribution is a reproducible measurement study and benchmark specification; no learned model or attacker-return estimate is claimed."

##### 2. Active Manuscript Abstract (`manuscript/sections/00_abstract.tex`):
> "Limited defensive budgets motivate prioritizing npm maintainers by downstream reach. However, reaching many repositories and reducing exposure to possible account compromises are different objectives. We study this distinction in our collected graph of 25,228 package nodes and 12,217 maintainer usernames. We compare five deterministic selection methods and 200 random orders across six budgets, using package and workflow-associated repository endpoints. At 100 identities, marginal coverage greedy reaches 5,538 of 7,171 observed workflow repositories (77.2%), versus 4,407 for exact maintainer-union ranking. Under a stipulated uniform single-account compromise model with perfect source hardening, their exposure reductions are 11.48% and 33.79%, respectively. Only 800 repositories covered by greedy satisfy exclusion of every observed source identity. Preserving version continuity reduces identity–repository exposure pairs by 42.44%, although aggregate greedy coverage remains similar. These results extend established maintainer-reach analyses with an explicit comparison of objectives and observation units. They support objective-specific prioritization and qualified structural measurements; they do not estimate incident probabilities or demonstrated control effectiveness."

#### C. All Research Questions (RQs) (Verbatim)

##### 1. Archive RQs (`extracted_manuscript_source/sections/01_introduction.tex`):
* **RQ1**: "whether stored metrics reproduce and agree across artifacts;"
* **RQ2**: "how artifact choice, weighting, and boundary ties change a fixed-budget review queue; and"
* **RQ3**: "which prediction claims the incident evidence supports."

##### 2. Active Manuscript RQs (`manuscript/sections/01_introduction.tex`):
* **RQ1**: "How do coverage-oriented and additive exposure-oriented selections differ at the same identity budget?"
* **RQ2**: "How much covered infrastructure remains reachable through unselected identities?"
* **RQ3**: "How sensitive are the results to graph representation, endpoint units, and observation gaps?"

#### D. Verbatim Bulleted/Numbered Contributions from Introduction

##### 1. Archive Contributions (`extracted_manuscript_source/sections/01_introduction.tex`):
> "The contributions are an independently executed offline metric audit, a quantitative analysis of review-queue drift, and an evidence-based assessment of benchmark readiness. For 25,228 packages, all seven database metric fields reproduce, but workflow reach differs across artifacts for 17,809 packages. Their equal-weight top-253 queues share only 65 entries. The incident companion supplies event records without eligible controls, so the paper reports measurement results and a proposed evaluation protocol rather than predictive accuracy."

##### 2. Active Manuscript Contributions (`manuscript/sections/01_introduction.tex`):
> "The contribution is an empirical replication and extension of maintainer-reach analysis. First, we compare five deterministic methods and a 200-order random baseline at six budgets, with exact graph closures and explicit objectives. Second, we quantify workflow-repository deduplication and version continuity effects on exposure mass and coverage. Third, we provide aggregate reproducibility records, independent correctness checks, and a frozen prospective acquisition pilot for subsequent outcome research. At 100 identities, coverage greedy reaches 77.2% of observed workflow repositories but removes 11.5% of exposure under our equal-account model; exact-union ranking removes 33.8%. This divergence motivates specifying the decision objective before interpreting a ranking as defensive benefit."

#### E. Structural Outline Table of Sections and Approximate Word Counts

| File Name | Section / Subsection Name | Approximate Word Count |
|---|---|---:|
| **Archive (`extracted_manuscript_source/`)** | | |
| `extracted_manuscript_source/sections/00_abstract.tex` | *(Frontmatter / Abstract / Notes)* | 167 |
| `extracted_manuscript_source/sections/01_introduction.tex` | `\section{Introduction}` | 256 |
| `extracted_manuscript_source/sections/02_related_work.tex` | `\section{Related Work and Novelty Boundary}` | 196 |
| `extracted_manuscript_source/sections/03_problem_and_evidence.tex` | `\section{Graph Metrics and Evidence}` | 174 |
| `extracted_manuscript_source/sections/04_audit_method.tex` | `\section{Audit Methodology}`, `\subsection{Inputs and Independent Reconstruction}`, `\subsection{Queues, Ties, and Sensitivity}` | 166 |
| `extracted_manuscript_source/sections/05_results.tex` | `\section{Empirical Results}`, `\subsection{RQ1: Metric and Artifact Consistency}`, `\subsection{RQ2: Queue Drift at a Fixed Review Budget}`, `\subsection{Concentration and Graph-Semantics Checks}`, `\subsection{RQ3: Temporal Evidence Supports an Inventory, Not a Fit}` | 702 |
| `extracted_manuscript_source/sections/06_benchmark_design.tex` | `\section{Discussion and Evaluation Requirements}` | 217 |
| `extracted_manuscript_source/sections/07_validity_and_ethics.tex` | `\section{Threats to Validity and Data Handling}` | 199 |
| `extracted_manuscript_source/sections/08_conclusion.tex` | `\section{Conclusion}` | 72 |
| `extracted_manuscript_source/sections/09_acknowledgment.tex` | `\section{Acknowledgment}` | 36 |
| **Active Manuscript (`manuscript/`)** | | |
| `manuscript/sections/00_abstract.tex` | *(Frontmatter / Abstract / Notes)* | 70 |
| `manuscript/sections/01_introduction.tex` | `\section{Introduction}` | 321 |
| `manuscript/sections/02_related_work.tex` | `\section{Related Work}` | 243 |
| `manuscript/sections/03_problem_and_evidence.tex` | `\section{Data and Graph Construction}`, `\subsection{Collection and Observation Scope}`, `\subsection{Endpoints and Missing Evidence}`, `\subsection{Two Graph Representations}` | 417 |
| `manuscript/sections/04_audit_method.tex` | `\section{Objectives and Experimental Method}`, `\subsection{Maintainer Exposure Sets}`, `\subsection{Three Quantities for the Same Selection}`, `\subsection{Selection Rules and Budget Grid}`, `\subsection{Reproducibility and Checks}` | 242 |
| `manuscript/sections/05_results.tex` | `\section{Results}`, `\subsection{RQ1: Coverage and Exposure Favor Different Selections}`, `\subsection{RQ2: Covered Endpoints Retain Other Sources}`, `\subsection{RQ3: Representation Changes Exposure Mass}` | 219 |
| `manuscript/sections/06_benchmark_design.tex` | `\section{Robustness and Research Implications}`, `\subsection{Observation and Selection Sensitivities}`, `\subsection{From Structural Reach to Outcome Research}` | 237 |
| `manuscript/sections/07_validity_and_ethics.tex` | `\section{Validity, Limitations, and Responsible Reporting}` | 211 |
| `manuscript/sections/08_conclusion.tex` | `\section{Conclusion}` | 51 |
| `manuscript/sections/09_acknowledgment.tex` | `\section{Acknowledgment}` | 41 |

---

### 2.4 Verbatim Experimental Tables (Converted to Markdown)

#### Table 1: Literature Positioning (`tables/literature_positioning.tex`)
| Work | Principal Evidence | Evaluated Target or Artifact | Boundary for this Study |
|---|---|---|---|
| Small World; Weak Links [Zimmermann et al. 2019, Zahan et al. 2022] | Dependencies, maintainers, metadata | Concentration and metadata weaknesses | Structural descriptors already established |
| Amalfi; detector benchmark [Sejfia & Schäfer 2022, Guo et al. 2026] | Released package content | Malicious-package detection | Detection labels do not define future non-events |
| CI characterization; ARGUS [Koishybayev et al. 2022, Muralee et al. 2023] | Workflow and action code | Configuration properties; injection paths | Directory presence is a weaker observation |
| On Good Authority [Santos-Grueiro 2026] | Predecessor release-path evidence | Authority discontinuities | Authority change and compromise differ |
| npm-follower; CHRONO-RESOLUTION [Pinckney et al. 2023, Rahman et al. 2026] | Archived releases; release-point resolution | Historical data resources | Graph reconstruction alone is not new |
| SupplyTGN; PatchRisk [Tran Truong et al. 2026, Shafin et al. 2026] | Temporal package/advisory evidence | Future vulnerability-risk ranking | Temporal forecasting is already studied |
| This study | Two local archives; incident-record inventory | Metric consistency, queue drift, feasibility | No fitted model or predictive benchmark result |

#### Table 2: Cross-Artifact Consistency Comparison (`extracted_manuscript_source/sections/05_results.tex`, Table I)
| Metric Field | CSV $>0$ Count | DB $>0$ Count | Package Disagreements |
|---|---:|---:|---:|
| Maintainer portfolio (max) | 22,147 | 22,147 | 0 |
| Maintainer portfolio (sum) | 22,147 | 22,147 | 0 |
| Workflow reach | 20 | 17,809 | 17,809 |
| Direct dependents | 20,331 | 20,331 | 0 |
| Workflow direct dependents | 15 | 15,017 | 15,014 |
| Transitive dependents | 20,328 | 20,328 | 0 |
| Legacy score | 22,147 | 24,502 | 17,809 |

#### Table 3: Priority Queue Overlap at Top-253 Budget (`extracted_manuscript_source/sections/05_results.tex`, Table II)
| Priority Review Queue (Top-253) | Shared Packages | Jaccard Similarity | Expected Shared (Random Tie-Break) |
|---|---:|---:|---:|
| Equal-weight score | 65 | 0.1474 | 55.14 |
| Dependency reach | 253 | 1.0000 | 253.00 |
| Workflow reach | 20 | 0.0412 | 22.15 |

#### Table 4: Maintainer Selection Methods Comparison at Budget 100 (`manuscript/sections/05_results.tex`, Table I)
| Selection Strategy (Budget = 100 Identities) | Distinct Repository Coverage ($C$) | Coverage Percent ($C$ %) | Exposure Reduction ($H$ %) | All-Source Full Exclusion ($P$) |
|---|---:|---:|---:|---:|
| Portfolio | 4,579 | 63.9% | 7.96% | 577 |
| Summed reach | 4,835 | 67.4% | 21.98% | 704 |
| Maximum reach | 4,268 | 59.5% | 33.59% | 533 |
| Exact maintainer-union ranking | 4,407 | 61.5% | 33.79% | 534 |
| Greedy marginal coverage | 5,538 | 77.2% | 11.48% | 800 |
| Random (mean of 200 trials) | 1,680.6 | 23.4% | 0.80% | 12.8 |

---

### 2.5 Methodology and Code Pipeline Summary

#### 1. Pipeline Architecture
* **Ingestion Layer (`scripts/collect_data.py`, `scripts/collect_data_v2.py`)**:
  * Ingests npm package registry metadata and Google deps.dev dependency trees.
  * Queries GitHub GraphQL API for the existence of `.github/workflows` directories.
  * Ingests OSV (Open Source Vulnerability) database entries.
* **Graph Modeling Layer (`scripts/study_structural_interventions.py`, `scripts/study_graph_validity.py`)**:
  * Bipartite Maintainer-Package graph ($M \times P$): 12,217 maintainer usernames, 25,228 packages, 79,405 account-package edges.
  * Package Dependency Graph: Directed graph with 88,113 name-level edges; exact version-continuous graph contains 121,885 edges across 40,806 version nodes.
  * Topological Condensation: Kosaraju Strongly Connected Component (SCC) condensation reduces graphs into Directed Acyclic Graphs (DAGs) to enable exact reverse topological traversals.
  * Bit-Parallel Closures: High-performance bit-vector reachability using arbitrary-precision integers propagates endpoint bitmasks across reverse dependency paths.
* **Structural Intervention Formulations**:
  * Maintainer Exposure Set: $E_m = \bigcup_{p \in P_m} \text{Reach}(p) \cap R_{workflow}$.
  * Distinct Endpoint Coverage: $C(S) = |\bigcup_{m \in S} E_m|$.
  * Additive Scenario Exposure Reduction: $H(S) = \frac{1}{|M|} \sum_{m \in S} |E_m|$ (fraction of total scenario exposure eliminated assuming mutually exclusive uniform single-account compromise).
  * All-Source Full Structural Exclusion: $P(S) = |\{r \in R_{workflow} : \text{Sources}(r) \subseteq S\}|$.
* **Absence of AST/Static/Dynamic/LLM Execution Components**:
  * The pipeline utilizes **zero JavaScript AST parsing** (e.g., Babel/Esprima), **zero shell AST parsing** (`bashlex`), **zero dynamic sandbox execution**, and **zero LLM inference** for package analysis. All computations are strictly graph-topological and registry-metadata-driven.

---

### 2.6 Bibliography Recency Audit

#### Breakdown for `extracted_manuscript_source/bibliography/references.bib` (15 references total):
* **Year Distribution**:
  * $\le 2020$: **2** (Zimmermann et al. USENIX Sec 2019, Ohm et al. DIMVA 2020)
  * 2021: **0**
  * 2022: **3** (Zahan et al. ICSE SEIP 2022, Sejfia et al. ICSE 2022, Koishybayev et al. USENIX Sec 2022)
  * 2023: **2** (Muralee et al. USENIX Sec 2023, Pinckney et al. arXiv 2023)
  * 2024: **0**
  * 2025: **0**
  * 2026: **5** (Guo et al. arXiv 2026, Santos-Grueiro arXiv 2026, Rahman et al. ICSME 2026, Tran Truong et al. SSRN 2026, Shafin et al. WI-IAT 2026)
  * Web Documentation / Undated: **3** (`githubsecure`, `depsdev`, `npmlock`)
* **Top Security & Software Engineering Venues**:
  * USENIX Security: **3** (Zimmermann 2019, Koishybayev 2022, Muralee 2023)
  * ICSE: **2** (Zahan 2022, Sejfia 2022)
  * IEEE S&P, ACM CCS, NDSS, FSE/ESEC, ASE, IEEE TSE, ACM TOSEM, EMSE, IEEE TDSC: **0**

#### Breakdown for `manuscript/bibliography/references.bib` (18 references total):
* **Year Distribution**:
  * $\le 2020$: **3** (Nemhauser et al. 1978, Zimmermann et al. USENIX Sec 2019, Ohm et al. DIMVA 2020)
  * 2021: **0**
  * 2022: **4** (Liu et al. ICSE 2022, Zahan et al. ICSE SEIP 2022, Sejfia et al. ICSE 2022, Koishybayev et al. USENIX Sec 2022)
  * 2023: **2** (Muralee et al. USENIX Sec 2023, Pinckney et al. arXiv 2023)
  * 2024: **0**
  * 2025: **0**
  * 2026: **6** (Wang arXiv 2026, Guo et al. arXiv 2026, Santos-Grueiro arXiv 2026, Rahman et al. ICSME 2026, Tran Truong et al. SSRN 2026, Shafin et al. WI-IAT 2026)
  * Web Documentation / Undated: **3** (`githubsecure`, `depsdev`, `npmlock`)
* **Top Security & Software Engineering Venues**:
  * USENIX Security: **3**
  * ICSE: **3** (Liu 2022, Zahan 2022, Sejfia 2022)
  * IEEE S&P, ACM CCS, NDSS, FSE/ESEC, ASE, IEEE TSE, ACM TOSEM, EMSE, IEEE TDSC: **0**

---

## 3. Code and Manuscript Diffs Performed
* **Diff Status**: `None (Read-Only Audit)`.
* **Repository Configuration**: Appended `research_sessions/` and `extracted_manuscript_source/` to `.gitignore` to prevent session logs, unpacked artifacts, and verification reports from polluting version control.

---

## 4. Anomaly and Vulnerability Flags

1. **Version Divergence Between Nested Archive and Working Workspace**:
   * `NPM_Supply_Chain_IEEE_Anonymous_Source.zip` represents an earlier paper draft focusing strictly on the *artifact consistency audit* between SQLite and CSV exports ("Auditing the Blast Radius: Artifact Consistency in npm Supply-Chain Prioritization").
   * The active `manuscript/` directory represents a newer revision expanding the contribution into *structural interventions, objective divergence (coverage vs. exposure reduction), and version continuity sensitivity* ("Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation").
2. **Severe 2024–2025 Citation Blindspot**:
   * Both bibliographies contain **zero** citations published in 2024 or 2025. Key recent supply-chain malware and defense literature (e.g., DONAPI USENIX 2024, Maltracker 2024, SocketAI 2024/2025, GuardDog 2024, Cerebro 2023/2025) is entirely absent.
   * Six 2026 citations rely predominantly on preprints (arXiv/SSRN) rather than peer-reviewed proceedings.
3. **No Code AST or Function-Level Call Reachability**:
   * The codebase operates exclusively at the package/maintainer/repository level. It does not inspect JavaScript source files, npm lifecycle scripts (`preinstall`), or function-level call paths.
4. **Unresolved Venue LLM Declaration Mismatch**:
   * The ICEEICT 2027 guideline limits LLM usage to non-intellectual assistance. The manuscript disclosure acknowledges extensive LLM involvement across study design, code development, literature review, and drafting.

---

## 5. Ledger Confirmation
* Initialized `research_sessions/SESSION_INDEX.md` with master table header.
* Appended Task 01 record:
  ```markdown
  | Task 01 | 2026-10-20 01:41:32 UTC+06:00 | `research_sessions/active_verification_track/01_workspace_extraction_and_manifest_audit.md` | Successfully unpacked archive (237,370 bytes), inventoried 372 files, extracted verbatim sections/tables, and completed bibliography recency audit (0 citations in 2024-2025). | COMPLETED |
  ```

---

## 6. Handoff Payload for Principal Research Advisor
```text
================================================================================
WORKSPACE EXTRACTION & MANIFEST AUDIT HANDOFF PAYLOAD (TASK 01)
================================================================================
1. REPOSITORY INVENTORY & ARTIFACT RECONCILIATION:
   - Archive NPM_Supply_Chain_IEEE_Anonymous_Source.zip (237,370 bytes, SHA-256: 4d6cc93f...) unpacked to extracted_manuscript_source/.
   - Total workspace inventory: 372 project files (.md: 105, .json: 111, .ts: 60, .tex: 38, .csv: 35, .py: 18, .bib: 2, .sh: 2, .js: 1).
   - Snapshot Discrepancy Flagged:
     * Archive Paper: "Auditing the Blast Radius: Artifact Consistency in npm Supply-Chain Prioritization" (Focus: SQLite vs. CSV drift).
     * Current Paper: "Maintainer Prioritization in npm Supply Chains: Coverage, Exposure, and Graph Representation" (Focus: Coverage vs. Exposure reduction, version continuity).

2. CORE QUANTITATIVE RESULTS EXTRACTED:
   - Dataset: 25,228 packages, 12,217 maintainer usernames, 7,171 workflow-associated GitHub repositories.
   - At Budget 100 Identities:
     * Greedy marginal coverage reaches 5,538 (77.2%) repositories, but removes only 11.48% scenario exposure (4,738 covered repositories remain exposed via unselected maintainers).
     * Exact maintainer-union ranking covers 4,407 (61.5%) repositories, but removes 33.79% scenario exposure (3x higher exposure reduction).
     * Only 800 repositories meet all-source exclusion under greedy coverage.
   - Version Continuity Effect: Collapsing versions introduces 1,273,291 spurious reach pairs across 8,587 packages; version continuity cuts identity-repository exposure pairs by 42.44% (from 462,170 to 266,016).

3. EMPIRICAL & BIBLIOGRAPHIC VULNERABILITIES FLAGGED:
   - Complete 2024-2025 Literature Gap: 0 citations from 2024 or 2025; 0 citations from IEEE S&P, ACM CCS, NDSS, IEEE TSE, ACM TOSEM, EMSE, or IEEE TDSC.
   - Analysis Boundaries: No code AST parsing, no lifecycle hook inspection (preinstall), no call-graph reachability, and no trained GNN/HGAT model in the active codebase.
   - Prospective Feasibility Cohort: 100 packages frozen on 2026-10-20; 90-day surveillance ends 2027-01-18 with all outcomes pending.
================================================================================
```

