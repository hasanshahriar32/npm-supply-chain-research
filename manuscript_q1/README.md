# Journal research draft

The named and anonymous PDFs are research drafts. Their compilation checks do not certify acceptance, submission, author approval, venue compliance, or complete bibliography verification. Author names, order and departments follow `manuscript/submission_files/authors.json`; no emails or IEEE memberships were supplied.

## Build

From the workspace root:

```sh
bash manuscript_q1/compile_q1.sh
bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex
python3 manuscript_q1/scripts/verify_manuscript_q1.py
python3 manuscript_q1/scripts/package_q1.py
```

The source ZIP supports typesetting from its `manuscript_q1` directory. Full numerical verification uses the surrounding repository and its retained datasets; the ZIP alone is not the complete research dataset.

## Threshold experiment

```sh
python3 scripts/study_q1_quorum_and_oct2026.py
```

Uses `data/npm_ecosystem.db.zip` and `scripts/study_structural_interventions.py`. The experiment writes workspace analysis outputs under `manuscript/results/q1_journal/` and copies the threshold results into `manuscript_q1/results/`. It does not modify the four frozen conference deliverables.

`results/quorum_reproducibility.json` records input and script hashes, all five ordered selections, zero-budget baselines, intervention increments, population conventions, and semantic checks. The table uses 7,158 endpoints with observed sources; coverage percentages use the 7,171-repository universe. All 13 source-free endpoints are excluded from strict counts. The strict metric is zero at zero budget, requires full exclusion when the total source count is below k, and is not necessarily monotone across k. Strict threshold counts alone do not establish an enforced release quorum or operational security. Uniform efficacy values are hypothetical multipliers, not measured bypass rates.

`results/source_verification_2026-10-25.json` records the focused source audit. The prospective cohort has 100 pending outcomes, with its horizon ending January 18, 2027; it supplies no forecast-performance result.

The strict-metric report is `../reports/14_q1_strict_quorum_exclusion_fix_and_lock.md`. The current conference artifact lock and cross-track handoff are documented in `../reports/15_conference_manuscript_oct2026_modernization_and_rebuild.md`. Task 15 explicitly lifted the earlier conference freeze; `config/conference_lock.json` records its reviewed replacement hashes. It supersedes Task 13's claims of incident verification, operational quorum protection, and submission readiness.

## Publication visuals (Task 16)

The current named and anonymous journal PDFs are 17 pages with eight figures. New observation, analysis-methodology, version-continuity and source-partition diagrams complement the existing analyses. The final named acknowledgment sentence was removed as requested. Current shared SVG/PDF/PNG assets match the conference provenance records. See `../reports/16_acknowledgment_and_publication_figure_expansion.md` for the latest artifact lock.

Task 17 restores the original icon-based architecture in the journal and conference. The added methodology, version-splicing, and quantitative figures are retained. See `../reports/17_original_architecture_restoration.md` for the current artifact lock.
