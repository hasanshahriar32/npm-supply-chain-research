# Paired consumer coverage study

The first run evaluates the unused entries from the pinned Awesome-Selfhosted frame. It excludes the 40 feasibility-pilot projects and known repository keys in the training endpoints. The resulting frame contains 155 project keys. This is a finite-frame study of the listed applications, conditional on the supported evidence scope. Identity exclusions use repository keys, with redirects disallowed during acquisition.

## Design

The frozen primary contrast compares the existing name- and version-based additive rankings at five slots. The other two equally optimal version portfolios measure sensitivity to the cutoff tie. An identical 100-slot greedy portfolio is the scorer's control. The protocol records portfolio fingerprints and code, training, and frame hashes.

The collection window is 24 hours after the protocol freeze. Each project uses the public default HEAD observed during that window. This is a prospective collection of visible project state. Registry responses describe observed maintainer-list associations at collection time. Commit times, registry observations, and package releases have different meanings.

The extractor looks for mandatory production paths in the root npm importer with npm lockfile format 2 or 3. It checks these paths against Arborist's offline virtual tree. Unresolved root workspaces, overrides, other managers, missing inputs, and parser disagreements remain visible in the project ledger. The study does not install dependencies. Tool agreement measures reproducibility between two implementations that share SemVer.

The request queue contains every distinct public package/version witnessed by both the custom parser and Arborist. Registry acquisition runs before portfolio scoring and has no membership checks against training. Exact-version responses with missing or malformed maintainer lists remain unresolved.

## Commands

From the repository root:

```sh
python scripts/consumer_holdout.py freeze RUN-ID
python scripts/consumer_holdout.py paths RUN-ID
python scripts/consumer_holdout.py registry RUN-ID
python scripts/consumer_holdout.py score RUN-ID
python -m unittest discover -s scripts/tests
node --test scripts/tests/test_consumer_lock_evidence.cjs
```

The registry and path stages use network access during the collection window. They save completed observations and resume from those records after an interruption. The scoring stage is offline. `runs/selfhosted-v1/protocol.json` holds the local freeze record. Path and registry manifests seal the byte hashes for scoring. Retained third-party source and account observations are stored locally under `runs/RUN-ID/private/` and are ignored by Git. Archive that directory locally to replay the observations at their original dates. Live re-collection may observe different project or registry states.

## Reading the results

The documented cells use the entire frozen frame as the denominator. A documented zero means the procedure did not establish a witness. The full-reference bounds instead assign each project all evidence-compatible outcomes. For example, a confirmed shared witness forces coverage under both portfolios. A missing manifest and distinct portfolios allow all four paired outcomes. The lower and upper gross turnover and signed net gain are calculated jointly for each project before aggregation.

Report documented turnover beside the full-reference bounds. The finite frame is enumerated, so these are information bounds from missing evidence. Sampling uncertainty and claims about a wider application population require a separate design.

## Verification

Run the separate audit after scoring:

```sh
python scripts/verify_consumer_holdout.py research/consumer_holdout/runs/selfhosted-v1
python scripts/render_consumer_holdout.py
node --test scripts/tests/test_consumer_lock_evidence.cjs scripts/tests/test_consumer_override_reference.cjs
```

The audit checks the sealed queue and result hashes, the order of source and registry acquisition, every paired cell, and the aggregate bounds. The override fixture uses an inert local dependency tree to distinguish a valid ancestor-scoped override from the same locked version in the wrong scope. It does not alter support in the frozen study.

## Second frame

The [YunoHost protocol](runs/yunohost-v2/protocol.json) freezes the same portfolios and a different root-importer extraction procedure on 215 commit-pinned applications. Keep the [verified root evidence](../consumer_parser_development/README.md) and both acquisition receipts to replay this run. The registry receipt includes observed account associations and belongs in the ignored local evidence directory.

The protocol precedes both acquisition queues. The CLI uses a fixed output directory. For path reconstruction, run the `paths` stage in a separate copy containing the saved acquisition files and check that the reconstructed trace and queue hashes match the completed run. Live registry retrieval at another date changes the observations.

Replay the completed analysis from the repository root:

```sh
python scripts/study_yunohost_holdout.py score
python scripts/verify_yunohost_holdout.py
python scripts/compare_yunohost_npm_extractors.py
```

## Yarn Classic follow-up

The [follow-up protocol](runs/yunohost-yarn-classic/protocol.json) adds positive evidence in the same 215-project frame. It retains the original npm and pnpm pairs, selected portfolios, and observation dates. The [follow-up results](runs/yunohost-yarn-classic/results.json) retain both documented and feasible paired states.

Offline scoring uses the saved Classic-parser bundle and separate registry receipt in `runs/yunohost-yarn-classic/private/`. The [parser origin record](runs/yunohost-yarn-classic/parser_origin.json) specifies the versioned tarball and its SHA-512. The required parser is the archive member `package/index.js`; the protocol verifies the extracted file's SHA-256. The following commands replay scoring and check the displayed results from the retained inputs.

```sh
python scripts/study_yunohost_yarn_classic.py score
python scripts/verify_yunohost_yarn_classic.py
```

## YunoHost packaging and named importers

The [audit queue](runs/yunohost-packaging/queue.json) records two unresolved strata from the 215-project frame. The [recipe classifications](runs/yunohost-packaging/classification.json) cite file locations at the pinned catalog revisions. The [source intake](runs/yunohost-packaging/source_intake.json) records resolved source references. Archive checks bind the three eligible recipes to the declared checksums and the manifest and lockfile hashes.

The [importer protocol](runs/yunohost-packaging/importer_protocol.json) and [paired diagnostic](runs/yunohost-packaging/importer_results.json) evaluate the three recipes separately. Locally retained packaging, source and registry receipts are in the ignored `private/` directory.

```sh
python scripts/study_yunohost_recipe_importers.py score
python scripts/verify_yunohost_recipe_study.py
```

The expanded [99-recipe sample](runs/yunohost-importer-frame/sample.json) and [recipe ledger](runs/yunohost-importer-frame/recipes.json) are in `runs/yunohost-importer-frame`. The [prespecified completeness analysis](runs/yunohost-importer-frame/results.json) and [post hoc single-edge check](runs/yunohost-importer-frame/single_edge_sensitivity.json) share the same source commits, portfolios and registry observations for scoring. Raw source and registry receipts remain in the ignored local evidence directories.

```sh
python scripts/study_yunohost_same_commit_spans.py score
python scripts/check_yunohost_single_edge.py score
python scripts/verify_yunohost_importer_frame.py
```

## YunoHost release-delivery evidence

The [release queue](runs/yunohost-release-delivery/release_queue.json) enumerates exact GitHub release assets referenced by literal setup commands in the 39 recipes with release declarations and no matched JavaScript command. The [release results](runs/yunohost-release-delivery/results.json) link API digests and parsed subject statements. The separate [archive receipts](runs/yunohost-release-delivery/archive_results.json) and [evidence summary](runs/yunohost-release-delivery/evidence_summary.json) record the bounded byte checks, declared commits, embedded metadata, and Java runtime inventory.

The main comparison does not use these as coverage outcomes. For audit replay from the saved receipts:

```sh
python scripts/study_yunohost_release_delivery.py score
python scripts/verify_yunohost_release_delivery.py
```
