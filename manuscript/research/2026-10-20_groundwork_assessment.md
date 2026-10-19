# Groundwork, new empirical findings, and research status — 20 October 2026

This record documents work executed for our npm supply-chain study. It separates completed measurements, observed source limitations, newly collected prospective data, and experiments that still need outcome follow-up. Existing research protocols are background documents; their self-imposed gates are not treated as binding instructions or substitutes for a current feasibility assessment.

## Research question supported by completed measurements

**How do dependency representation and the unit of workflow observation change defensive review and idealized hardening decisions?** The original account/package graph supports an empirical comparison of maintainer review strategies, while the new work here establishes which graph and endpoint assumptions those results depend on. This is a structural decision study. It does not require inventing compromise probabilities, treating advisory absence as benignness, or presenting a trained predictor that has not been evaluated.

The most consequential new representation result is that deleting version identities creates additional paths for **8,587 of 25,228 graph-identifier roots (34.04%)**. Their top-253 reach queues share only **155 identifiers**. The dependency graph and account-package memberships are our study data; scientific prose should introduce their acquisition, construction and semantics directly, rather than speak of somebody else's platform or a supplied SQL file.

## Completed graph experiments

Reproduction command, requiring only Python's standard library:

```bash
python3 scripts/study_graph_validity.py
```

The analysis extracts the database to a temporary directory, opens it read-only, and leaves the source archive unchanged. `manuscript/results/graph_validity/summary.json` binds results to archive and script SHA-256 values. For every one of the 25,228 roots, both the package reach count and workflow-positive package count exactly reproduce the archived database. The version-continuous name set is checked to be a subset of the projected name set for every root.

### Identifier scope and sampling-frame validity

The archive's `package_name` field contains **25,228 graph identifiers**, not 25,228 independently registered npm package names. A lexical census finds **2,745 bundled-context strings containing `>`** and **22,483 ordinary-shaped names**. No context string has a matching metadata row or maintainer membership in this archive. Their presence affects graph and missingness denominators, so all-root results retain the original graph identifier unit. The census is recorded in [identifier_scope.json](../results/graph_validity/identifier_scope.json) and reproduced by `scripts/check_identifier_scope.py`. Removing every context node leaves all maintainer/workflow-repository incidence sets identical, retaining all 462,170 pairs, so repository-level `C/H/P` results are unchanged for a fixed identity selection. Summed or maximum individual-package ranking invariance has not been established. Workflow-package incidence loses 28 pairs; context removal does not preserve every endpoint definition and is not asserted to repair resolution semantics.

This finding also limits the frozen feasibility wave: eight of its 100 selected identifiers are context strings. A new registry-level wave should validate its sampling units before selection and use a separate manifest. The original selection is retained as evidence of the defect. Nothing in this lexical classification independently verifies every ordinary-shaped name as a currently registered package.

### Version identities and reach

Let a retained dependency edge point from a dependent version to its dependency version. The package graph collapses all versions with the same name. The comparison graph keeps exact `(package, version)` identities. For a root package, the version-continuous experiment starts from **all observed versions** of that root, traverses reverse edges, and then deduplicates the reached package names. The root package name is excluded from both counts. This gives the projection a conservative comparison: no observed root version is arbitrarily discarded.

| Measurement | Result |
|---|---:|
| Queued graph identifiers | 25,228 |
| Ordinary-shaped names without a bundled-context separator | 22,483 |
| Bundled-context strings containing `>` | 2,745 |
| Distinct name-level dependency edges | 88,113 |
| Distinct version-level dependency edges | 121,885 |
| Version nodes, including isolated metadata versions | 40,806 |
| Roots whose name projection adds reachable names | 8,587 |
| Excess ordered root/dependent-name pairs caused by projection | 1,273,291 |
| Median excess among changed roots | 28 |
| Largest excess for one root | 4,127 |
| Top-253 reach queue overlap | 155/253 |
| Queue Jaccard similarity | 0.4416 |

A short observed example is `pseudomap → lru-cache → @apollo/server` in the reverse dependency direction. The first adjacency involves `lru-cache` versions 3.2.0, 4.0.0 or 4.1.5, while the retained `@apollo/server@5.5.1` edge uses `lru-cache@11.5.1`. Collapsing the names joins these incompatible intermediate identities. The complete version traversal confirms that `@apollo/server` is absent from *all* version-continuous reverse paths from the observed `pseudomap` versions. `version_projection_witnesses.json` retains this and four other checked examples. This is a graph-construction illustration; none of these package names is assigned a maliciousness label.

The largest example is `pseudomap`, with 4,273 projected dependent names versus 146 version-continuous names. These counts compare representations of the retained edge union. **Neither graph is an installed dependency tree or a historically complete ecosystem graph.** Even the version graph merges edges from different dependency-resolution contexts. It lacks the original root, lockfile, acquisition time and resolver error records needed to reconstruct a particular installation.

The package graph has 82 nontrivial strongly connected components containing 403 names; its largest has 61 names and it contains 13 self loops. The exact-version union has 68 nontrivial components containing 304 version nodes, a largest component of 61 nodes and 9 self loops. Traversals therefore explicitly support cycles and exclude the root; acyclic-graph assumptions would be unjustified.

### Workflow packages and repository observation units

The stored positive workflow flags cover **15,233 package names**, but their normalized GitHub owner/repository keys cover **7,171 repositories**. Across all linked records, 21,460 packages map to 12,743 repository keys, with 1,087 repositories serving more than one package. A workflow directory observed once in a monorepository is consequently represented by many package flags. This is a difference in observation units, not proof of multiple independent CI systems or multiple credentials.

| Sensitivity comparison, budget 253 | Overlap | Jaccard |
|---|---:|---:|
| Projected package reach vs version-continuous name reach | 155 | 0.4416 |
| Workflow-positive package reach vs distinct workflow repository reach | 245 | 0.9387 |
| Workflow-positive package reach vs version-continuous distinct repository reach | 135 | 0.3639 |
| Equal-weight maintainer/reach score, package vs repository endpoint | 221 | 0.7754 |
| Equal-weight maintainer/reach score, projected package vs version-continuous repository endpoint | 173 | 0.5195 |

Ties use descending numeric score followed by ascending Unicode package name. The equal-weight score keeps the same max-maintainer portfolio term and separately max-normalizes each reach definition. Thus the score comparison describes sensitivity to endpoint and graph definitions, including the associated normalization change. It is not measured forecast accuracy. Changing to repository units changes reach counts for 11,320 roots. All per-root numbers are in `per_package.csv`; repository multiplicities are in `repository_units.csv`.

### A concrete collection defect and its limits

The original URL parser stops a repository name at its first period. For example, `https://github.com/tj/commander.js.git` becomes `tj/commander`, and `https://github.com/isaacs/fs.realpath.git` becomes `isaacs/fs`. Comparing the retained raw repository URL with a parser that preserves periods identifies **658 package records with different repository targets**, including **60 workflow-positive rows**. Exact counterexamples are in `repository_parser_disagreements.csv`.

Correcting a lexical URL does **not** repair the old workflow observation. A flag obtained for a truncated repository must not be reassigned to the corrected repository without a new query. The main historical inputs are left unchanged. The structural study conservatively excludes the 60 positive version observations, removing 24 distinct repository keys. At budget 100, greedy then covers 5,524 of 7,147 retained keys and satisfies all-source exclusion for 799; no positive flag is transferred to a corrected target. Repository-key normalization here is lexical and case insensitive; redirects, repository transfers and immutable GitHub repository identities have not been validated.

### Missingness and semantics

There are 813 metadata packages with only NULL workflow flags and 2,959 queued packages without a metadata row, leaving **3,772 graph identifiers without a positive or zero flag**. Another **6,223 packages have only zero flags**. The collector maps missing GraphQL repository objects and HTTP 404 to zero, as well as genuinely missing workflow directories. Zero therefore conflates absence with unavailability. It does not establish no CI, low risk, an inaccessible secret, or an uncompromised package.

In 8,473 rooted neighborhoods, at least one reached package has only NULL/missing flags. The output's `workflow_reach_upper_with_unknown` adds only these NULL/missing cases to the observed positive count. It is a conditional bound if zero flags are trusted. Allowing uncertainty in the zero flags requires the full projected name reach as an even looser within-graph upper bound. Neither bound covers packages outside our observed graph.

Only **14,248 of 32,240 distinct target-version nodes (44.19%)** have matching metadata-version rows. Both endpoint versions have metadata in **51,427 of 121,885 dependency rows (42.19%)**. Version-level dependency structure therefore has substantially weaker metadata coverage than package-name coverage. A missing version metadata row must not be filled using a different version while claiming exact version alignment.

## Collector semantics and data-generation findings

The collector requests npm `/latest`, not a sequence of dated maintainer snapshots. It obtains a deps.dev resolution graph and writes every `edges[]` adjacency, including edges between non-root nodes. The stored `relation` is copied from the **target node's relation to that query root**, rather than from a property saying whether the edge itself is direct. Official [deps.dev API definitions](https://docs.deps.dev/api/v3/) distinguish these node relations from declaring-to-resolving edges.

There are 48,705 stored rows marked DIRECT and 73,180 marked INDIRECT. The current metrics appropriately use every explicit adjacency. Filtering to DIRECT would retain only 46,986 name-level pairs instead of 88,113 and alter reverse reach for 12,993 roots. It would discard genuine adjacencies rather than recover a correct global direct-dependency graph. The same name-level pair has both labels across versions in 8,054 cases. This is compatible with the query-relative meaning, not evidence of inconsistent dependency declarations.

The primary key omits the extraction root. `INSERT OR REPLACE` merges observations of the same version adjacency and can overwrite the relation and requirement strings from earlier contexts. The archive also omits deps.dev error records and query times. The graph is consequently described as an **observed union of resolved adjacencies**, with context limitations stated explicitly.

The account-package mapping is collected from the `maintainers` array. It is not a historical log of the actor who published each version, a token-scope record, or a trusted-publisher configuration. Official [npm trusted-publishing documentation](https://docs.npmjs.com/trusted-publishers/) describes workflow-bound OIDC publication as a separate authorization mechanism. Account portfolio size measures observed metadata membership; idealized interventions based on that membership must declare their authorization assumptions.

The original advisory importer selects records using keywords and publication months September 2025–April 2026. It drops affected-version arrays, aliases, withdrawal state and event timing; its single advisory-ID primary key can replace one affected package with another from the same report. Its `compromise` classification is thus candidate discovery, not adjudicated publisher-compromise ground truth. The current work does not train on those imported labels.

## Temporal artifacts reassessed

The companion has 47 package-event rows, 31 family identifiers, 45 records whose selected pre-event version object was accessible to its builder, and 258 direct runtime declaration edges. The builder stores **derived CSV features and response hashes**, not complete raw registry response bodies or version objects. Its `registry_reconstructed_exact` label should therefore be reported as a source-version reconstruction record, not as a claim that 45 immutable raw objects are retained locally or that historical maintainer authority is known.

The depth-three registry SemVer diagnostic contains 1,848 bounded rows over 30 roots, with seven unresolved rows. It follows dependencies outward from selected incident packages. It cannot supply the complete reverse-dependent population needed for downstream reach. Current metadata time maps can help choose previously published versions but do not recover historical workflow contents, ownership state, installed trees or deleted versions.

There is no statistical need to certify every non-event row benign before studying **documented-event outcomes**. A clearly defined at-risk population, observable follow-up interval, reviewed events and explicit censoring/reporting assumptions could support event-versus-unlabeled or positive/unlabeled evaluation. The present limitation is more specific: the archive does not record sufficiently aligned feature observation times and the historical companion has no independently frozen comparison population or outcome-coverage process. Retrospective publisher-compromise prediction has not been evaluated, and present-day metadata is not substituted for pre-incident observations.

## Actual bounded public-source acquisition

The optional access command is:

```bash
python3 scripts/study_graph_validity.py --probe-public-sources
```

Each request has a 15-second timeout and 1 MiB response bound. The first sandbox execution failed DNS for all six endpoints; its exact failures are preserved in `source_access/sandbox_access_attempts.json`. The same authorized read-only requests were retried through the available network execution path. `source_access/access_attempts.json` records status, request body, response size, raw response SHA-256 and retained-file SHA-256.

| Primary source and exact access path | Actual result | What this resolves |
|---|---|---|
| `GET https://registry.npmjs.org/is-number` | HTTP 200; 15 retained versions; 17 time-map keys | Current retained version manifests and publication-time maps are accessible. Retained copy is sanitized; emails and full raw bodies are omitted. |
| `GET https://api.deps.dev/v3/systems/npm/packages/is-number/versions/7.0.0:dependencies` | HTTP 200; one node, zero edges | Version-specific resolved graph acquisition works; this minimal package is a source-access check rather than a new ecosystem graph. |
| `POST https://api.osv.dev/v1/query`, package `keyv`, ecosystem `npm` | HTTP 200; one non-withdrawn report, MAL-2026-11524, affected version 6.0.0 | A version-specific documented malicious-package outcome can be acquired, including source references. Its publication time is 4 August 2026; it is not retroactively treated as a forecast result. |
| `GET https://zenodo.org/api/records/17576373` | HTTP 200; main ZIP 10,228,800,396 bytes; scripts ZIP 9,581,599 bytes | Historical relation data remains publicly discoverable, but it is not a small filtered export. No main relation-data archive is downloaded in this step. |
| `GET https://dependencies.science/` | DNS failure even after network retry | The historical population portal was actually attempted; its present failure does not prove the dataset is unavailable through every other path. |
| OpenSSF `malicious-packages` primary README | HTTP 200 | The source explicitly contains reports from several attack classes and allows borderline records; absence is not complete outcome coverage. |

The [OpenSSF corpus scope](https://github.com/ossf/malicious-packages) and [OSV API documentation](https://google.github.io/osv.dev/quickstart/) establish the source and query semantics. A malware report alone does not identify whether the package was an established publisher-compromise target, a newly created malicious package, a dependency-confusion package or protestware. Version membership, incident role, reporting delay and withdrawal state still need adjudication.

## Completed prospective data collection, with outcomes pending

Rather than stop at a generic request for future data, this work **collected a new small prospective feasibility cohort**. It selected 100 graph identifiers uniformly without replacement from our fixed 25,228-identifier study population, with seed **20261020**, and wrote the selection manifest before the first metadata request. Names were not selected using future outcomes, and unavailable packages were not replaced.

The selection contains **92 ordinary-shaped names and eight bundled-context strings**. Ordinary names obtained **90 successful official npm `/latest` responses** and **two HTTP 404** responses. Every sampled bundled-context string obtained **HTTP 405**. The eight context strings are invalid registry sampling units rather than eight confirmed unavailable npm packages; they remain in the frozen selection and are not replaced. Sanitized records include feature-capture timestamps, response hashes, version identifiers, public maintainer usernames, a distinct version-publisher username when present, lexical repository keys, dependency counts and metadata availability indicators. It does not retain email addresses, raw registry bodies, script bodies or tarballs and does not execute package code.

The feature cutoff is the latest finished response: **20 October 2026, 00:48:38.569362 Asia/Dhaka** (`2026-10-19T18:48:38.569362+00:00`). The 90-day follow-up interval is `(cutoff, cutoff + 90 days]`, ending **18 January 2027, 00:48:38.569362 Asia/Dhaka**. All **100 outcomes remain pending**. No probabilities, fitted models, positive labels, negative labels or forecast-performance metrics were produced.

The fixed files are in `manuscript/results/prospective_cohort/`: `selection_manifest.json`, `capture_records.jsonl`, `cohort_status.json`, and `README.md`. `scripts/freeze_prospective_cohort.py` refuses to overwrite an existing selection manifest. Validation confirms selection preceded requests, selected names match all 100 records, outcomes are NULL/pending, hashes agree, and no email-pattern matches occur in the feature records.

This is a completed acquisition feasibility step, not a powered or fully preregistered predictive benchmark. Before examining future outcomes, the authors must finalize the outcome-source freeze, documented-publisher-compromise definition, reporting-delay allowance, censoring rules and analysis plan. The small cohort may yield no eligible events; that would be a real result, not a reason to relabel unrelated vulnerabilities or create artificial positives. Additional current collection can enlarge the at-risk cohort, while historical release-point data would require separate interval validation and acquisition.

## What is completed and what remains

- **Completed:** all-root graph representation experiment; cycle/SCC checks; repository observation-unit analysis; concrete collector linkage-defect evidence; metadata/version coverage census; primary-source access tests; 100-name prospective selection and 90 successful metadata captures; explicit pending-outcome records.
- **Also completed:** the maintainer-review and idealized-hardening comparison at six budgets, with 200 seeded random trials, version-continuity and repository-link sensitivity results, exact union objectives and separate all-source exclusion statistics. The executable is `scripts/study_structural_interventions.py`; its final numeric tables and checks are in `manuscript/results/structural_interventions/`. This document leaves those numbers bound to that experiment's manifest rather than duplicating a partial run.
- **Still pending:** outcome follow-up through January 2027; final prospective surveillance and analysis registration; historical workflow or publication-authority reconstruction; independently evaluated compromise prediction; real hardening outcomes or causal intervention validation.

The paper should report completed structural experiments as our research results, and describe the prospective collection as groundwork whose outcomes are not yet observed. Every risk, compromise-probability, credential-exposure, actual propagation or deployed-hardening claim still requires observations beyond the structural graphs.
