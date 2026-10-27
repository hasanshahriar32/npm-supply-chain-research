# Implemented journal validation revision — 28 October 2026

This implements the computational and artifact work in Report 22. Independent human endpoint annotation and final author approval remain pending. The revised manuscript explicitly reports that limitation; it does not treat automated extraction as human validation.

## Executed evidence

- Froze a dated protocol and 120-endpoint probability sample before new audit requests: 30 endpoints from each of four source-cardinality strata. Population sizes and inclusion probabilities are retained; no acquisition failures were replaced.
- Captured 172 registry-request outcomes and 115 pinned commits. The machine evidence flags 106 mapping-support candidates, 115 workflow files, 88 aligned installation directives, 70 root lockfiles and 17 dependency/version examples. Five unresolved commit acquisitions are retained. These counts are provisional extraction findings, not precision or execution measurements.
- Created separate initially blank author review sheets, a source-linked evidence packet and label rubric. The local pipeline preserves independent initial labels, detects disagreements, requires adjudication and notes, and reports raw agreement, per-label confusion matrices and Cohen's kappa when defined. It produces no completed human result from blank cells.
- Evaluated 38 original/component/candidate-cap/tie selection runs across six budgets (228 metric rows). The parameterized original rule exactly matches the retained 100-account selection. The original rule gives P=1,022 at budget 100; removing reciprocal scoring gives P=1,024, C=5,043 and H=11.75%. Candidate-cap variants and thirty tie runs retain P=1,022 on this graph. The latter is selection variability, not an ecosystem sampling interval.
- Exhaustively evaluated 20 empirical candidate pools and 12 synthetic instances, each with twenty eligible accounts and budgets 1, 3 and 5. There are 96 settings and 288 method comparisons. Outside-candidate sources remain unselected. The original direct rule matches 51/60 empirical and 35/36 synthetic restricted optima; its worst empirical gap is 66 and minimum ratio is 16.46%. No full-graph optimality or approximation certificate is claimed.
- Executed a new bounded acquisition from 100 frozen roots in the original ordinary-name frame: 94 dependency graphs, 1,641 exact nodes, 1,476 identifiers, 4,357 version-edge rows and 1,051 observed usernames. No graph lost nodes to the frozen caps. One acquired root contains fifteen node-level API error records, preserved in the inputs. Root GitHub observation and dependency-acquisition requirements yield 70 records mapping to 66 repository endpoints, of which 65 have sources.
- On the new name graph at budget 100, greedy reaches 65 endpoints with H=11.19% and P=11; exact union reaches 42 with H=44.95% and P=4; the original direct rule reaches 62 with H=17.72% and P=34. The immediate-only variant has P=28. Thus its slight original-graph advantage does not repeat here.
- Name/version pair mass is 2,494/2,411: a 3.33% decrease, versus the original 42.44%. Different roots, observations and graph extent prevent attribution solely to time. Budget 100 is 9.51% of the new observed accounts versus 0.82% originally.
- Reoptimized on 65 common repository keys and 1,036 common selectable accounts while preserving each full source universe. At budget 100 the account-set Jaccard overlaps are 0.667 (union), 0.835 (greedy) and 0.587 (direct P). H denominators remain dataset-specific (12,833 versus 2,487 pairs).

## Manuscript and figures

The journal now has four focused research questions, a discussion section, heuristic ablations/exact benchmarks and the fresh-cohort comparison. The introduction credits established reach/vetting methods and separates mathematical expectations from empirical effect sizes. The closest-work matrix uses verified primary descriptions of Zimmermann, Zahan and Weeraddana rather than a broad detector comparison.

Extended scalarization/weight/threshold sensitivities and the historical/prospective companions are appendices. The prospective outcome record is untouched; no forecasting model or outcome labels were invented. The original illustrated architecture is retained. Two new data-generated figures show provisional audit evidence/exact gaps and new-cohort budget curves; one redundant weighting plot is no longer active. There are thirteen active figures. Clipped titles/legends found during visual review were corrected before release.

Named and anonymous working PDFs, the Springer EMSE PDF, title page, reference PDF and flat source ZIP are rebuilt. The named documents cite the public research release. The anonymous working PDF omits its author-identifying URL. The draft before this validation revision is preserved under submission/emse/archive/.

## Public research release

https://github.com/hasanshahriar32/npm-supply-chain-research/releases/tag/research-validation-2026-10-28

The attached companion ZIP contains code, new observations, derived audit data, protocols, generated results and checksums. It links the original database at repository commit 43c039bebe7c36b07a5aeb50b1c8a412ad058e0f and supplies a checksum-verifying download helper. Raw third-party workflow/manifest/lockfile bodies are referenced by pinned URLs and hashes rather than redistributed in the companion.

The public companion download and original input were checked without authentication. Companion SHA-256: ff306ac5392cf8fda4420b8a13855a21adccbff534e85fb1559009d62f75e756. The original input SHA-256 remains ab45439cf94cf43f3133b0aaff644557d55e86e99430a0a7937bfd0ce5266315. The release is explicitly a prerelease because human labels are pending; no manuscript was published with it.

The 30 MB self-contained local asset passed clean reproduction but its upload timed out. The published companion is approximately 2.9 MB and references the same versioned original input. A clean companion extraction downloaded and checked that input, validated all recorded file checksums, independently rebuilt 12,217 baseline account masks, checked 228 ablation rows, recomputed restricted optima underlying 288 comparisons, checked 120 cohort metric rows, and reproduced the cohort in an isolated workspace with network acquisition disabled. Source-body validation is explicitly distinguished from derived-data reproduction.

The original collector's execution hash is preserved in protocols/executed_scripts/ and in the base commit. The packaged current collector adds an offline guard without changing online collection logic. Subsequent local human-review tooling adds richer agreement diagnostics; any human-reviewed data belong in a subsequent artifact version.

## Checks and remaining work

Machine-readable evidence: manuscript_q1/results/revision_validation/verification.json, submission/emse/validation.json, submission/research_artifact/clean_reproduction.json and package_manifest.json. Final PDF page counts, hashes and technical-check status are recorded in 23_validation_artifact_manifest.json.

The scientific consistency suite covers the original active numeric tables, independently reconstructed endpoints, temporal/authority semantics, graph incidence, new results and figure provenance. Four frozen conference deliverable hashes remain unchanged. Fourteen local unit tests cover strict thresholds, evidence reconciliation, source-set boundaries, exact optima, deterministic ties, blank review sheets and disagreement handling. PDF checks cover fonts, undefined references/citations, glyphs, overflow and standalone compilation of the extracted flat EMSE source.

Both authors must now independently complete their own CSVs under manuscript_q1/review_packets/. Run scripts/study_validated_endpoints.py --label-source human, resolve generated adjudication rows, then update claims/tables from those actual labels and publish the next artifact version. Actual author-contribution roles and final manuscript approval also remain for the authors. The local PDFs and the public data release do not update the Editorial Manager submission; use its existing draft or editorial revision route as appropriate.
