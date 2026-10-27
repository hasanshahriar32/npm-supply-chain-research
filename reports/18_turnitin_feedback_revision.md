# Conference paper revision against supplied reports

Review date: 27 October 2026 (Asia/Dhaka).

## Repository context established before editing

Reviewed the root and component guides, research protocols and claim audits, current research context and full report, historical handoff reports, both manuscript structures, build and verification tools, collection schema and semantics, structural-study implementation, graph-validity diagnostics, prospective cohort records, and platform source/data interfaces. No AGENTS.md was found in the repository or its enclosing research directory.

The repository has five distinct roles:

| Area | Role and authority for this revision |
|---|---|
| `data/`, `scripts/` | Retained SQLite/CSV archives, collection code, exact offline graph studies, independent validation, and journal extensions. Scientific inputs and analysis code are preserved. |
| `manuscript/` | Active six-page IEEE conference paper; anonymous and named entry points share sections, generated numbers, bibliography, and figures. This is the paper checked by the supplied reports. |
| `manuscript_q1/` | Separate journal expansion with additional weighted/hybrid/threshold experiments. Its prose is outside the supplied reports' scope. |
| `research/`, `platform/research/`, `docs/` | Earlier research plans, incident/source assessments, and background. Forecasting and HGAT proposals must not be confused with completed empirical work. |
| `platform/`, `reports/`, `research_sessions/` | Research browsing/administration application and historical audit records. Historical readiness assertions do not supersede the latest evidence and limitations. |

The completed contribution compares coverage C, conditional account-origin exposure H, and all-source exclusion P. It is a structural study, with 25,228 graph identifiers including 2,745 bundled-context strings, rather than a forecast of compromise or a test of deployed controls. The frozen 100-identifier cohort has 90 metadata captures and 100 pending outcomes, with follow-up ending 18 January 2027. The original illustrated architecture and four additional conference figures are retained.

## What the supplied reports establish

`turnitin_check/main - Similarity.pdf` is a ten-page report containing a six-page paper. It reports **12% overall similarity**, with 19 groups labeled “Not Cited or Quoted” (10%) and four labeled “Missing Citation” (1%). Those categories are the service's labels, not independently established plagiarism findings. The listed sources include arxiv.org (6%) and multiple smaller publication, website, and student-paper matches. Visual inspection shows numerous highlighted bibliography entries. Author names, publication titles, venues, identifiers, and source URLs must remain accurate even when they match another bibliography.

`turnitin_check/main - AI report.pdf` is an **academi.cx** report dated 26 October 2026, not an actual Turnitin AI report. It estimates 43%, reporting 102 high-likelihood and 21 medium-likelihood sentences. Its own explanation says medium-likelihood sentences are not counted in the score. It offers no substantive reviewer comments about methods or correctness. Its highlights are review locations, not proof of authorship or a specification for detector evasion.

The supplied similarity result is already below the repository's stated 30% threshold. Neither supplied score applies automatically to a revised PDF. No new report, lower percentage, author approval, or submission is asserted.

## Changes and reasons

| Location | Revision |
|---|---|
| Abstract | Replace generic motivation with the overlapping-account problem; identify graph identifiers and bundled contexts correctly; retain budget-100 results and explicit scenario assumptions. |
| Introduction | Explain why an already-covered repository can retain a distinct account origin; connect the research questions to this decision; keep incident attribution next to the corresponding reports. |
| Related work | Attribute reach sets and vetting to Zimmermann et al.; distinguish the prior metadata, package-hardening, version, workflow, and signing studies from our measured contribution. Preserve the source-specific limits on the 81.26% finding. |
| Data and method | Explain acquisition and missingness in concrete terms; distinguish identifier units, repository denominators, version continuity, and scenario multiplicity. Preserve equations, controls, tie rules, seeds, budgets, and guarantees. |
| Results | Separate the simulated random H mean (0.80%) from its exact expectation (0.819%). Name the relevant ranking order in the qix example; place its 444-endpoint non-overlap explicitly in the name graph, avoiding the former ambiguous parenthesis after the version-graph count. |
| Robustness and prospective work | Explain what exclusion of mismatched URLs actually changes, where context-node invariance holds, and why HTTP 405 context responses indicate a sampling-frame defect. |
| Limitations and conclusion | Replace compressed lists and repeated generic qualifications with consequences for interpreting the observed graph. Remove the unsupported need to discuss a specific cooldown interval; retain the cited operational boundaries and pending-outcome limits. |
| Compliance records | Record the supplied 12% result as a baseline and require a fresh report for the revised PDF. Preserve the accurate LLM disclosure and unresolved venue-policy status. |

All 24 active citations, five figures, generated result macros, primary C/H/P values, data archives, and analysis implementations are retained. Bibliography titles and metadata are not paraphrased to alter matching behavior. No invisible characters, text-as-image substitution, fabricated citations, or detector-score claim is introduced.

For attribution checks, consulted the primary [Zimmermann study page](https://www.usenix.org/conference/usenixsecurity19/presentation/zimmerman), [Zahan paper record](https://arxiv.org/abs/2112.10165v2), [deps.dev API documentation](https://docs.deps.dev/api/v3/), and [Kalu study page](https://www.usenix.org/conference/usenixsecurity25/presentation/kalu). This was a targeted check, not a fresh certification of every historical reference; existing source audits remain the provenance for the other retained contextual claims.

## Verification and deliverables

Current machine-readable checks are `manuscript/results/research_verification.json`, `submission_compliance.json`, `author_versions_validation.json`, and `package_validation.json`.

| Check | Executed result |
|---|---|
| Anonymous conference PDF | Six A4 pages, 207,216 bytes; 29 embedded fonts, no Type 3 fonts |
| Named conference PDF | Six A4 pages, 208,638 bytes; 30 embedded fonts, no Type 3 fonts |
| Scientific consistency | 106 hashes, 150 deterministic rows, 6,000 random rows, 24 citations, generated values, and frozen cohort timing pass |
| Layout and references | Both conference variants have no overfull boxes or unresolved citations/references; first-page, architecture-page, and final reference-page renders visually reviewed |
| Anonymous source archive | Independent compilation passes; extracted text matches the current PDF; author materials are excluded |
| Conference working archive | Current named and anonymous PDFs and generated inputs included; ZIP integrity passes |
| Journal integration | Current conference lock passes; both unchanged 17-page journal PDFs pass the journal verification suite |
| Source hygiene | `git diff --check` passes; no changes to scientific archives, analysis implementations, bibliography entries, or figure assets |

The journal's conference-artifact lock was replaced after conference validation, preserving the previous artifact hashes. The journal source archive is refreshed to include that lock and the current verification report. Journal sources were compiled to regenerate local verification logs; text was compared with the original PDFs, then the original delivered journal PDF bytes were restored. Thus the journal's prose and delivered PDFs remain unchanged.

Both conference archives are rebuilt. `reports/18_turnitin_feedback_artifact_manifest.json` records final artifact hashes and source-report hashes. Compilation still reports existing font-shape substitutions and underfull boxes; these produce no missing glyphs or overfull boxes in the conference checks.

Remaining external work: fresh similarity/AI-service reports if required by the authors, human review of sources and interpretations, resolution of the already-recorded venue LLM-use policy mismatch, and actual submission approval. These cannot be certified by a local build.
