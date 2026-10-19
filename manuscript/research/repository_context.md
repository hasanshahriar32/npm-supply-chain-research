# Research context, study data and executed work

Assessment date: **20 October 2026, Asia/Dhaka**. This is author-side context. The paper describes our collection and experiments directly; it does not present our data as somebody else's platform or a supplied SQL exercise. Exact revisions and hashes belong to each experiment's manifest.

## Completed empirical study

Our study examines how maintainer portfolio overlap, dependency representation and workflow observation units change budgeted defensive review and idealized hardening decisions. The data contain **25,228 graph identifiers**, **12,217 maintainer usernames**, **79,405 maintainer/package relations**, **121,885 version-level dependency edges**, and **88,113 distinct name-level adjacencies**. They form an observed edge union, not a historical installed tree or a random sample of all npm. Of the identifiers, **2,745 are bundled-context strings containing `>`** and **22,483 have ordinary-name shape**. Context strings have no matching metadata or maintainer membership in this archive; they are not independently registered package observations. [identifier_scope.json](../results/graph_validity/identifier_scope.json) records the census and removal sensitivity. Removing context nodes preserves all maintainer/workflow-repository incidence sets and all 462,170 primary pairs; package-level endpoints are not universally invariant.

`scripts/study_structural_interventions.py` compares portfolio size, summed package reach, maximum package reach, exact portfolio-union reach, greedy marginal coverage and 200 seeded random baselines at budgets 1, 5, 10, 25, 50 and 100. It evaluates package and repository endpoints, uniform source-loss scenario exposure, distinct endpoint coverage and a separate all-source exclusion statistic. It executes version-continuity, repository-link consistency, depth, account-grouping and dominant-portfolio sensitivities. Completed results, manifests and checks are in `manuscript/results/structural_interventions/`.

These objectives differ. Summing selected identity-loss scenario sizes measures their share under an explicitly uniform scenario model. Taking their union measures endpoint coverage for review. A covered endpoint can remain reachable from an unselected identity; all-source exclusion requires all its observed source identities to be selected under the idealized model. None is an observed attack probability, achieved security benefit or causal effect of deployed hardening.

## Completed graph and observation-unit experiments

`scripts/study_graph_validity.py` independently checks every package root. Its projected reach and workflow-positive reach reproduce the stored database, and every version-continuous reached-name set is contained in its name projection.

- Projection adds reachable names for **8,587 roots**, producing **1,273,291 additional ordered root/dependent-name pairs**. The top-253 raw reach queues share only **155 names**.
- **15,233 workflow-positive package names** map to **7,171 repository keys**; **1,087 linked repositories** serve multiple packages.
- The old URL parser truncates dotted repository names, producing **658 target disagreements**, including **60 workflow-positive rows**. A flag queried for a wrong target must be excluded or recollected, not transferred to a corrected target.
- **3,772 graph identifiers** have only missing/NULL workflow observations. Another **6,223** have only zero flags, which conflate directory absence and repository unavailability.
- Only **14,248 of 32,240 distinct dependency target-version nodes** have matching metadata-version rows. Another version's metadata cannot be substituted while claiming exact alignment.

Results and checked path examples are in `manuscript/results/graph_validity/`. The detailed assessment is [2026-10-20_groundwork_assessment.md](2026-10-20_groundwork_assessment.md), with machine-readable status in [2026-10-20_research_status.json](2026-10-20_research_status.json).

## Acquisition semantics and limitations

The original `scripts/collect_data.py` seeds high-impact packages, expands through dependency discovery, requests current npm `/latest` metadata and merges deps.dev resolved adjacencies. Its DIRECT/INDIRECT label is the target node's relation to the query root. Filtering it to DIRECT would discard genuine adjacency edges. The merged table loses extraction-root context, graph errors and retrieval times.

The maintainer array supplies account/package metadata, not a historical version-publisher log, token scope or trusted-publisher configuration. The workflow flag records a directory lookup at repository HEAD. It does not retain YAML, a commit SHA, permissions, execution, secrets or historical release linkage. Queue creation in June 2026 and metric calculation in July do not establish one source-observation cutoff.

The original collector and compressed archives remain unchanged. New `scripts/research_observations.py`, `scripts/collect_data_v2.py` and semantic validation code provide corrected lexical GitHub parsing and distinct unavailable/error/directory-observed states for future collection. They do not repair old observations retroactively. No new live GitHub workflow data has been acquired.

`scripts/calculate_metrics.py` stores a weighted structural baseline in an `attacker_roi` column. No attacker utility, cost, success probability or predictor is estimated. The earlier consistency analysis in `manuscript/results/artifact_audit.json` found 17,809 differing workflow-reach and weighted-score records between compressed exports. This remains a provenance check; the current contribution is the structural decision study.

## Existing incident companion

The companion contains 47 package-event records, 31 family identifiers, 45 source-version reconstruction records and 258 runtime declaration edges. Its builder retains derived features and response hashes, not 45 complete immutable raw objects. Family identifiers do not establish independent incidents. Its depth-three range-resolution diagnostic follows dependencies outward and does not reconstruct complete reverse-dependent populations.

The advisory import uses keywords and publication-month filtering, omits affected-version arrays and withdrawal state, and retains one row per advisory ID. It is candidate discovery rather than reviewed publisher-compromise ground truth. Present-day or post-event features cannot be assigned to earlier incidents.

A documented-event-versus-unlabeled study is meaningful with an explicit population, follow-up and ascertainment process; it need not certify every unreported package benign. Such a predictor has not been evaluated here: historical feature timing and outcome coverage remain incomplete, and the new prospective outcome horizon has not elapsed.

## Newly acquired prospective cohort

`scripts/freeze_prospective_cohort.py` selected **100 graph identifiers uniformly without replacement**, seed **20261020**, from our fixed population. The selection manifest was saved before the first official npm `/latest` request. The 92 ordinary-shaped names yielded **90 successful responses** and **two HTTP 404** responses. The eight bundled-context strings all returned **HTTP 405**, identifying invalid registry sampling units. No selected identifier was replaced. A future registry-level wave needs a separately frozen sampling frame with validated units.

Allowlisted features separate maintainer usernames from a version's publisher username where present. No email addresses, raw metadata bodies, install-script bodies or tarballs are retained. Manifest timing, all selected names, pending labels and file/collector hashes have been checked.

The exact feature cutoff is **20 October 2026, 00:48:38.569362 Asia/Dhaka**. The 90-day follow-up ends **18 January 2027, 00:48:38.569362 Asia/Dhaka**. All **100 outcomes are pending**. No labels, fitted models or forecast metrics exist. This is an acquisition-feasibility wave; the surveillance, censoring and analysis plan still needs finalization before outcome review.

Frozen outputs are in `manuscript/results/prospective_cohort/`. Separate bounded source probes actually accessed npm retained publication maps, a deps.dev graph, an OSV version-specific report, Zenodo release metadata and the OpenSSF source contract. The large historical relation archive has not been ingested.

## Writing and reproduction context

The reference GOAD project supplied the modular writing structure; the paper uses IEEE conference formatting and our scientific content. Anonymous and authored entry points share the paper body and differ in author presentation.

Reproduce completed experiments with their scripts and manifests. The prospective collector deliberately refuses to overwrite its selection; subsequent waves require a separate directory. The distinction between completed experiments and future benchmark work is described in [extended_benchmark_design.md](extended_benchmark_design.md).
