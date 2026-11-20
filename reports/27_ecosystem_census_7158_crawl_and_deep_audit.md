# Automated census of the 7,158 repositories in the retained frame

The collection covers 7,158 baseline repositories with an observed source account. The baseline selection used workflow-associated repositories. Consequently this frame cannot estimate how often projects across npm have workflows.

| Retained evidence | Count |
| --- | ---: |
| Rows and unique repository keys | 7,158 |
| Commit request records | 7,158 |
| Successful commit requests (two HTTP 404s) | 7,156 |
| Workflow-directory response records | 7,156 |
| Directories under source_text | 7,141 |
| Tracked files under source_text | 36,504 |
| Registry request records | 15,280 |

The prior report listed 60,772 downloaded files and 7,156 source directories. The counts above describe what is available to inspect in this checkout. Request records include unsuccessful requests. See the [collection directory](../data/full_census/).

| Automated criterion | Supported | Unsupported | Unknown |
| --- | ---: | ---: | ---: |
| Repository mapping | 5,640 | 1,484 | 34 |
| Workflow file | 7,129 | 25 | 4 |
| Installation directive | 6,046 | 1,108 | 4 |
| Lockfile | 4,420 | 2,734 | 4 |
| Dependency version example | 4,375 | 2,771 | 12 |

The table reproduces the legacy labels. The parser searches a bounded set of files and can classify a missing search result as unsupported. It combines declarations from multiple manifests, selects a retained lockfile and accepts a package match without tracing the selected consumer importer. The pnpm and Yarn branches use text patterns. The first positive version example pairs declared range `^1.3.2` with version `1.2.0`. A range check on the stored examples found 227 outside their declared range, 4,039 compatible and 109 unassessable. Range compatibility alone does not identify the applicable importer. Treat these labels as automated candidates for source inspection. [Frozen data](../data/full_census/census_audit_labels.csv) · [Legacy rule](../scripts/census_audit_manager.py)

The November offline rerun examines the root importer and its mandatory npm dependency declarations, a narrower question than the legacy example search. The default audit now writes a separate [root-example CSV](../data/full_census/census_root_examples.csv). Of 7,158 rows, 905 have a semver-compatible direct dependency at a public npm tarball location in a supported retained npm lockfile, and 6,253 are unresolved by that procedure. The count describes evidence in the locally captured files. It cannot identify the workflow's active importer, demonstrate execution, or validate the original account-to-consumer path. The legacy file stays available to reproduce the [range consistency check](../research/consumer_evaluation/census_note_check.json).
