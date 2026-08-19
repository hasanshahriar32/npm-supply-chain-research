# Data Provenance and Checksums

## Current committed snapshot

The repository contains compressed research artifacts under `data/`. The SQLite archive expands to approximately 206 MB and the metrics CSV archive expands to approximately 1.1 MB. The current inspected snapshot includes package, version, maintainer, package-maintainer, dependency, advisory, and package-metric tables.

A future manifest must record exact SHA-256 checksums for the compressed files, the uncompressed file sizes, row counts, extraction date, source code commit, and the script configuration that generated them.

## Source provenance requirements

For each external source, record:

| Field | Requirement |
|---|---|
| `source_name` | Human-readable name such as npm Registry or deps.dev |
| `source_url` | API, dataset, or documentation URL |
| `retrieved_at` | UTC retrieval timestamp |
| `effective_at` | Source’s observation or snapshot timestamp |
| `query_or_parameters` | Query, filters, pagination, and version |
| `response_checksum` | SHA-256 of raw response or archive |
| `parser_version` | Code commit or parser version |
| `rows_in` | Records before filtering |
| `rows_out` | Records after filtering |
| `missingness` | Counts by reason |
| `license_and_terms` | Applicable usage constraints |

## Reproducibility tiers

- **Tier 1:** raw public source or stable snapshot is archived with checksum.
- **Tier 2:** source is public but only a derived table and request manifest are retained.
- **Tier 3:** source is dynamic or historical reconstruction is approximate; results are descriptive or sensitivity-only.

The final paper should state the tier for every major feature family.

## Publication rules

Commit:

- schemas, data dictionaries, aggregate tables, synthetic fixtures, feature definitions, labels with public evidence URLs, checksums, manifests, and safe evaluation outputs.

Do not commit:

- credentials, API tokens, private repository content, raw maintainer emails, unredacted secret values, live malware, payloads, exploit code, or large raw downloads that are not necessary for reproducibility.

## Artifact naming

Use stable names such as:

```text
snapshot_YYYYMMDD_<source>_<version>.jsonl.gz
features_YYYYMMDD_cutoffYYYYMMDD_v01.parquet
labels_compromise_v01.csv
experiment_<id>_manifest.yaml
metrics_<id>.json
```

## Checksum command

The repository may use the standard `sha256sum` utility to produce checksum records. The checksum file should be committed with the artifact or manifest and should not be regenerated silently.
