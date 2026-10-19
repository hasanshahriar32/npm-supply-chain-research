# Research Verification & Empirical Audit Reports

This directory stores the official, sequential research audit reports and gap analyses for the `npm-supply-chain-research` repository. All reports are deterministically generated from workspace artifacts, verified against IEEE conference requirements and Q1 journal publication criteria (*IEEE TSE*, *ACM TOSEM*, *IEEE TDSC*, *EMSE*), and tracked in version control.

## Report Index

| Report File | Topic / Focus | Core Finding / Milestone | Status |
|---|---|---|---|
| [`00_research_verification_and_workflow_review.md`](00_research_verification_and_workflow_review.md) | Strategic Advisor Review & Workflow Framework | Synthesizes the 5 structural principles of npm security, dataset hygiene rules, and the Q1 transition roadmap from `NPM Research Verification and Workflow.docx`. | **COMPLETED** |
| [`01_workspace_extraction_and_manifest_audit.md`](01_workspace_extraction_and_manifest_audit.md) | Task 01: Workspace Extraction & Manifest Audit | Unpacked anonymous source archive (237 KB), inventoried 373 files, extracted verbatim manuscript sections/tables, and completed bibliography audit (0 citations in 2024–2025). | **COMPLETED** |
| [`02_novelty_and_dataset_hygiene_verification.md`](02_novelty_and_dataset_hygiene_verification.md) | Task 02: Structural Interventions, Graph Validity, & Incident Ledgers | Audited all 6 budgets for C/H/P, depth/exclusion ablations, version continuity (42.4% pair drop), 658 parser disagreements, and 49 incident assessments (16 packages in graph). | **COMPLETED** |
| [`03_q1_statistical_and_ablation_gap_analysis.md`](03_q1_statistical_and_ablation_gap_analysis.md) | Task 03: Statistical Rigor, Ablations, & Operational Evidence | Verified 6,000 random budget rows, 200 seeds, exact expectations, 378 ablation rows, 270 representation rows, hashes and descriptive effects; three identical-result reruns averaged 39.50 s with 1,038.43 MiB maximum RSS. Statistical independence and pending outcome limits are explicit. | **COMPLETED** |

## Master Tracking Ledger
The persistent session ledger is maintained at [`research_sessions/SESSION_INDEX.md`](../research_sessions/SESSION_INDEX.md).
