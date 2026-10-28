# Journal research draft

For the current EMSE submission, use [`../submission/emse/EMSE_Manuscript.pdf`](../submission/emse/EMSE_Manuscript.pdf), the updated title page and flat source archive described in [`../submission/emse/README.md`](../submission/emse/README.md). The journal manuscript has 13 active figures, four focused research questions and appended exploratory material. Its data/code [prerelease](https://github.com/hasanshahriar32/npm-supply-chain-research/releases/tag/research-validation-2026-10-28) is publicly accessible and was reproduced offline after downloading the checksum-verified original input. The endpoint indicators were not manually validated. Individual contribution roles and author approval have not been inferred. See [Report 23](../reports/23_journal_validation_implementation.md) for the executed evidence and [Report 25](../reports/25_emse_guideline_correction.md) for the current manuscript and guideline correction.

The named and anonymous PDFs are research drafts. Their compilation checks do not certify acceptance, submission, author approval, venue compliance, or complete bibliography verification. Author names, order and departments follow `manuscript/submission_files/authors.json`; contact details now follow the user-supplied record, with Shahriar Hasan as first and corresponding author. The separate title-page attachment is `../submission/emse/EMSE_Title_Page.pdf`. No IEEE memberships were supplied.

## Build

From the workspace root:

```sh
bash manuscript_q1/compile_q1.sh
bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex
python3 manuscript_q1/scripts/verify_manuscript_q1.py
python3 manuscript_q1/scripts/package_q1.py
python3 submission/emse/build_emse.py
```

The source ZIP supports typesetting from its `manuscript_q1` directory. Full numerical verification uses the surrounding repository and its retained datasets; the ZIP alone is not the complete research dataset.

## Threshold experiment

The new validation workflow is documented in [`protocols/REVISION_WORKFLOW.md`](protocols/REVISION_WORKFLOW.md). Independent review sheets and pinned evidence are under [`review_packets/`](review_packets/ENDPOINT_REVIEW_INSTRUCTIONS.md). After both authors complete their own sheets, run `python3 scripts/study_validated_endpoints.py --label-source human` from the repository root; unresolved disagreements require the generated adjudication file. The command reports pending status rather than inventing labels when sheets are incomplete.

```sh
python3 scripts/study_q1_quorum_and_oct2026.py
```

Uses `data/npm_ecosystem.db.zip` and `scripts/study_structural_interventions.py`. The experiment writes workspace analysis outputs under `manuscript/results/q1_journal/` and copies the threshold results into `manuscript_q1/results/`. It does not modify the four frozen conference deliverables.

`results/quorum_reproducibility.json` records input and script hashes, all five ordered selections, zero-budget baselines, intervention increments, population conventions, and semantic checks. The table uses 7,158 endpoints with observed sources; coverage percentages use the 7,171-repository universe. All 13 source-free endpoints are excluded from strict counts. The strict metric is zero at zero budget, requires full exclusion when the total source count is below k, and is not necessarily monotone across k. Strict threshold counts alone do not establish an enforced release quorum or operational security. Uniform efficacy values are hypothetical multipliers, not measured bypass rates.

`results/source_verification_2026-10-25.json` records the focused source audit. The prospective cohort has 100 pending outcomes, with its horizon ending January 18, 2027; it supplies no forecast-performance result.

The strict-metric report is `../reports/14_q1_strict_quorum_exclusion_fix_and_lock.md`. The current conference artifact lock and cross-track handoff are documented in `../reports/15_conference_manuscript_oct2026_modernization_and_rebuild.md`. Task 15 explicitly lifted the earlier conference freeze; `config/conference_lock.json` records its reviewed replacement hashes. It supersedes Task 13's claims of incident verification, operational quorum protection, and submission readiness.

## Publication visuals (Task 16)

The Task 16 named and anonymous journal PDFs were 17 pages with eight figures. New observation, analysis-methodology, version-continuity and source-partition diagrams complement the existing analyses. The final named acknowledgment sentence was removed as requested. Current shared SVG/PDF/PNG assets match the conference provenance records. See `../reports/16_acknowledgment_and_publication_figure_expansion.md` for the latest artifact lock.

Task 17 restores the original icon-based architecture in the journal and conference. The added methodology, version-splicing, and quantitative figures are retained. See `../reports/17_original_architecture_restoration.md` for the historical Task 17 artifact lock.

## Evidence reconciliation (27 October 2026)

The current named and anonymous journal PDFs have **15 pages and 12 figures**. Corrected tables, workflow-only account ranks, temporal attempt resolution and unassessed provenance status are documented in [Report 20](../reports/20_evidence_reconciliation_and_figures.md). New source distributions, representation matrices and observation-unit diagrams complement the restored architecture. Exclusion and weighting plots are separate readable figures. Earlier page counts and audit assertions are historical.

Regenerate tables with `python3 scripts/reconcile_full_manuscript.py`, shared figures with `python3 manuscript/scripts/render_research_figures.py`, and journal plots with `python3 manuscript_q1/scripts/render_q1_figures.py` from the repository root. `python3 scripts/verify_reconciled_papers.py` checks active numerical sources and units. The current conference lock binds the rebuilt Task 20 artifacts; numerical verification requires the surrounding repository data.
