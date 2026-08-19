# Proposed Data Dictionary

## Design principles

Each row should have a stable identifier, source provenance, observation timestamp, and missingness reason. The dataset must distinguish raw observations from derived features and labels.

| Entity | Key | Core fields | Derived fields | Time rule |
|---|---|---|---|---|
| Package | `package_id` | canonical npm name, scope, registry URL | popularity, age, activity, label status | Use only values available by snapshot date |
| Package version | `package_version_id` | package name, exact version, publication time, tarball integrity | install-script indicators, dependency counts | Version must be published by cutoff |
| Maintainer | `maintainer_id` | npm username, hashed email if needed, source | package count, concentration, tenure | Ownership association must predate cutoff |
| Repository | `repository_id` | provider, owner, repo, visibility, URL | activity, mapping confidence, workflow state | Use repository state as of cutoff where historical data permits |
| Dependency edge | `edge_id` | source package/version, target package/version or range, relation, source | resolved reach, depth, path counts | Resolve using data available by cutoff |
| Workflow | `workflow_id` | repository, path, file hash, last change if available | triggers, permissions, action pinning, deployment indicators | Do not use workflow changes after cutoff |
| Advisory | `advisory_id` | source, package, affected range, publication time | vulnerability class, confidence | Advisory content is not a feature if published after cutoff |
| Incident label | `incident_label_id` | incident family, package/version, event times, evidence URLs | binary or confidence-weighted target | Label window occurs after observation date |
| Model run | `run_id` | code commit, dataset version, config, seed | metrics, rank outputs, checksum | Immutable record of experiment |

## Package and version fields

| Field | Type | Description | Risk or caveat |
|---|---|---|---|
| `package_name` | string | Canonical npm name, including scope | Case and alias normalization must be specified |
| `version` | semver string | Exact published version | Pre-releases and invalid semver need explicit handling |
| `published_at` | timestamp | Registry publication time | Registry clocks and backfills may differ |
| `dist_integrity` | string | Package integrity metadata | Store hash, not unnecessary tarball content |
| `scripts_install_present` | boolean | Presence of relevant lifecycle script | A script is not malicious by itself |
| `downloads` | numeric | Popularity observation if available | Strong confounder and time-varying |
| `repository_mapping_confidence` | categorical | Exact, normalized, inferred, missing | Inferred mappings should be sensitivity-tested |

npm documentation states that lifecycle events such as `preinstall`, `install`, `postinstall`, `prepare`, and related hooks can execute during package operations. This supports collecting lifecycle metadata, but the presence of a lifecycle script is not proof of maliciousness.[1]

## Maintainer fields

| Field | Type | Description | Privacy handling |
|---|---|---|---|
| `maintainer_username` | string | Registry identifier | Public identifier, but do not infer real identity |
| `email_hash` | string or null | Salted or unsalted hash as documented | Prefer not to publish reversible or linkable values |
| `maintainer_package_count` | integer | Number of associated packages at cutoff | Association is not proof of shared credential control |
| `maintainer_tenure_days` | integer | Time since first observed association | Historical availability required |
| `ownership_change_recent` | boolean | Recent ownership change if verifiable | High risk of false positives without reliable history |

## Dependency fields

| Field | Type | Description |
|---|---|---|
| `relation_type` | categorical | direct, indirect, peer, optional, bundled, or source-specific relation |
| `version_range` | string | Declared semver or package-manager range |
| `resolved_target_version` | string | Version selected under documented resolution rules |
| `dependency_depth` | integer | Shortest path depth in resolved graph |
| `direct_dependent_count` | integer | Number of direct downstream dependents |
| `transitive_dependent_count` | integer | Number of reachable downstream dependents |
| `depth_weighted_reach` | numeric | Documented depth-weighted reach score |
| `resolution_confidence` | categorical | exact, source-resolved, approximated, unavailable |

## Workflow fields

| Field | Type | Description |
|---|---|---|
| `workflow_exists` | boolean | Public workflow file or directory observed |
| `workflow_count` | integer | Number of workflow files |
| `workflow_last_changed_at` | timestamp | Last observable workflow change |
| `trigger_pull_request` | boolean | Pull-request trigger present |
| `trigger_workflow_run` | boolean | Workflow-run trigger present |
| `trigger_schedule` | boolean | Scheduled trigger present |
| `explicit_permissions` | boolean | Workflow declares permissions |
| `write_permissions_present` | boolean | Broad or write-scoped token permissions detected |
| `id_token_write` | boolean | OIDC token permission detected |
| `third_party_action_count` | integer | External actions referenced |
| `unpinned_action_count` | integer | Actions not pinned to immutable commit identifiers |
| `deployment_job_present` | boolean | Deployment or release behavior detected |
| `self_hosted_runner_present` | boolean | Self-hosted runner label detected |
| `workflow_observability_status` | categorical | observed, private, archived, deleted, API-failure, parse-failure |

These fields are deliberately phrased as observable configuration signals. They should not be transformed into claims that a repository contains secrets or has exploitable privilege.

## Label fields

| Field | Type | Description |
|---|---|---|
| `incident_family` | categorical | campaign, maintainer compromise, malicious publication, dependency confusion, other |
| `affected_package` | string | Canonical package name |
| `affected_version_range` | string | Version or range documented by source |
| `first_malicious_publish_at` | timestamp | Earliest supported malicious publication time |
| `first_public_detection_at` | timestamp | Earliest reliable public report |
| `removed_at` | timestamp | Registry removal time if known |
| `label_confidence` | categorical | high, medium, low, unknown |
| `evidence_urls` | list | Primary source references |
| `label_exclusion_reason` | string | Why a candidate was not used as a positive |

## Missingness policy

Missingness must be represented explicitly. A private repository, a deleted repository, an API timeout, an unavailable historical snapshot, and a parser failure are different situations. Imputing all missing workflow observations as `false` would systematically bias public and popular packages.

## References

[1]: https://docs.npmjs.com/cli/v11/using-npm/scripts "npm lifecycle scripts documentation"
[2]: https://docs.deps.dev/ "deps.dev documentation"
[3]: https://google.github.io/osv.dev/ "OSV documentation"
[4]: https://docs.github.com/en/graphql "GitHub GraphQL documentation"
