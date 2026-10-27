# Evidence reconciliation and empirical figure expansion

Date: 27 October 2026 (Asia/Dhaka). Applies Report 19 following the user's authorization. This handoff supersedes earlier numerical and readiness statements where the corrections below apply. Earlier reports remain historical records.

## Corrected evidence

Both papers now use generated workflow-repository account measurements. The retained qix portfolio contains **eight package associations**, rather than the three examples previously treated as its entire portfolio. Its workflow reach is **1,942**, exact-union rank **7**, version-continuous workflow reach **1,476**, version-union rank **5**, and hybrid rank **35**. There are **366** name-graph workflow endpoints outside sindresorhus's reach. These are cross-sectional associations, without historical publisher attribution or forecasting validation. The primary budget-100 C/H/P comparison remains unchanged.

The journal includes the generated multi-budget table in place of its conflicting handwritten copy. All 90 deterministic values and 36 random mean/MCSE values are checked against retained results. The sixteen-row incident-associated table uses workflow endpoints for both package reach and account ranking. Version labels and dependency counts remain in the companion CSV; the paper table is condensed for readability.

Historical edge resolution is **1,841/1,848 = 99.62% among recorded attempts**. Its 1,272-node count is summed across roots. Forty-five records contain 44 distinct event/root/cutoff tuples. Depth/node bounds, excluded dependency kinds, and registry retention limit reconstruction; no historical installation completeness or downstream prediction result is claimed.

The release audit reports field availability rather than validated authority continuity. Embedded maintainers are metadata, not signatures. Attestation states remain **unassessed**, with zero requests or classifications. Claims of 0/45 historical attestations and 100% PGP signatures were removed.

Corrected graph statistics distinguish 82 nontrivial name SCCs containing 403 nodes from 68 version SCCs containing 304 nodes; the largest component has 61 nodes in each. Mean source count is 64.57 over 7,158 source-reachable repositories, maximum 1,502. SCC condensation preserves reach. Unsupported cycle-change, depth-2/3/4, doubled-cap and historical downstream-change percentages were removed.

The journal consistently distinguishes graph identifiers, directory presence, maintainer membership, hypothetical hardening, and measured deployment effects. Seven scalarization settings yield exploratory tradeoff points, not a certified global Pareto frontier or universal alpha. Direct P selection remains a heuristic. The H difference uses full precision (22.30 percentage points). The prospective protocol is internal, not external preregistration; all 100 outcomes remain pending through January 18, 2027. The revised journal title reflects npm objectives, representation sensitivity and metadata limits.

## Figures

The conference retains **five figures in six A4 pages** and the original architecture. A compact residual-source distribution replaces the generic methodology diagram. Its denominator, source-free exclusions and logarithmic-above-one horizontal scale are stated.

The journal has **twelve figures in fifteen pages**. Added:

1. Observed and residual-source distributions over the same source-reachable population.
2. A C/H/P matrix separating selection representation from evaluation representation, with H denominators stated.
3. An observation-unit and prospective-frame diagram separating overlapping populations.

The crowded combined P/weighting figure is split into exclusion curves and a labeled weight-sensitivity heatmap. The scalarization figure no longer declares a universal sweet spot. Captions match the actual panels and weight definitions. New figures have PDF/SVG/PNG exports with input, renderer and output hashes. The original architecture remains byte-identical to its preserved source. No AI-generated raster artwork is used.

## Generators and verification

`scripts/reconcile_full_manuscript.py` is the canonical table and focal-account generator. The former temporal/authority extractor delegates to it. Case labels are retained in `manuscript_q1/config/incident_case_records.json` instead of reading a generated output CSV as its own input. Shared generated macros bind the account example in both papers.

`scripts/verify_reconciled_papers.py` checks active table inclusion, 126 budget values, archive-derived workflow ranks, independent focal BFS endpoints, all sixteen case rows, temporal attempts, field-availability rows, macros and figure provenance. Every representation-matrix cell is checked. Both manuscript verifiers invoke this scientific gate. Four regression tests reject old table values, an analytic expectation substituted for a simulation mean, and missing rows. The Makefile regenerates reconciliation inputs before plotting.

The platform ingestion source and documentation now use `hasanshahriar32/npm-supply-chain-research`. Its integration check tests repository access rather than a token owner's login and skips without a token. No live ingestion or publication was performed. Platform runtime tests were not run because the checkout lacks installed platform dependencies; this small source change received static inspection.

## Reproduction

Run from the repository root:

```sh
python3 scripts/reconcile_full_manuscript.py
python3 manuscript/scripts/render_research_figures.py
python3 manuscript_q1/scripts/render_q1_figures.py
python3 -m unittest discover -s scripts/tests -p 'test_paper_evidence.py'
python3 scripts/verify_reconciled_papers.py
TECTONIC="$HOME/.local/bin/tectonic" bash manuscript/compile.sh --both
bash manuscript_q1/compile_q1.sh
bash manuscript_q1/compile_q1.sh main_q1_anonymous.tex
python3 manuscript/scripts/verify_manuscript.py
python3 manuscript/scripts/check_submission.py
python3 manuscript/scripts/check_author_versions.py
python3 manuscript/scripts/package_overleaf.py
TECTONIC="$HOME/.local/bin/tectonic" python3 manuscript/scripts/validate_packages.py --compile-anonymous
```

Refresh the authorized conference lock only after validating rebuilt conference PDFs and archives. Then run journal verification and packaging. Standalone ZIPs support typesetting; numerical reproduction requires the surrounding repository and data.

## Delivery and limits

Final artifact hashes, counts, archive parity and check outcomes are recorded in `reports/20_reconciliation_artifact_manifest.json`. Both conference versions pass A4, six-page, embedding, Type 3, references, overflow and author/anonymity checks. Both journal versions pass PDF and scientific checks. All three archives are rebuilt; anonymous conference sources compile independently with matching PDF text. Existing font substitutions and underfull-box warnings are separate from overflow or missing-glyph failures.

Local checks do not certify a fresh similarity/AI-service score, deployed-control effects, venue eligibility, author approval or submission. The truthful assistance disclosure and previously recorded venue-policy limitation remain in place.
