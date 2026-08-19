# Reproducibility Roadmap

## Current state

The repository already contains a useful collection and deterministic metric prototype, compressed data artifacts, research documents, and a README. The main reproducibility gaps are missing dependency pinning, inconsistent database paths, absent tests, missing snapshot manifests, no temporal data builder, no label-review workflow, and no model or evaluation package.

## Priority changes

| Priority | Change | Acceptance criterion |
|---|---|---|
| P0 | Add data and experiment provenance manifest | Every dataset and result records source, date, query, version, checksum, and code commit |
| P0 | Standardize database paths and CLI options | All scripts accept `--db` and work from any current directory |
| P0 | Add strict temporal cutoff controls | A run fails if a feature or label violates the cutoff |
| P0 | Add label-review schema and evidence URLs | Every positive and excluded candidate has a documented reason |
| P1 | Add pinned dependency manifest | Clean environment can install exact versions |
| P1 | Add tests for graph and metric logic | Unit and smoke tests pass on fixtures and edge cases |
| P1 | Add baseline experiment runner | Popularity, graph, maintainer, workflow, and tabular baselines run from one config |
| P1 | Add workflow feature extractor | Parser coverage, feature schema, and missingness are reported |
| P2 | Add version-aware graph builder | Resolved graph can be regenerated from documented source snapshots |
| P2 | Add homogeneous and heterogeneous graph models | Models share split, label, and metric interfaces |
| P2 | Add calibration and uncertainty analysis | Results include confidence intervals and reliability diagnostics |
| P3 | Add prospective monitoring or dashboard | Only after offline benchmark validity is established |

## Suggested repository layout

```text
research/
  README.md
  references.bib
  *.md
  *.csv
  configs/
  manifests/
  labels/
  reports/
src/
  acquisition/
  resolution/
  features/
  labels/
  models/
  evaluation/
tests/
  fixtures/
configs/
  sampling.yaml
  temporal_splits.yaml
  model_baselines.yaml
scripts/
  collect_data.py
  build_snapshot.py
  build_features.py
  train.py
  evaluate.py
```

The project does not need to adopt this layout immediately. It should first preserve the current working scripts and add tests around them.

## Environment and dependency control

Add either `pyproject.toml` with pinned or bounded dependencies and a lock file, or a versioned `requirements.txt` plus a documented Python version. For graph learning, record compatible PyTorch and PyTorch Geometric versions. Record external command versions such as GitHub CLI, Node/npm, and Docker when they affect data collection or analysis.

## Data provenance

For each source, store:

- source URL or API endpoint;
- query or request parameters;
- retrieval timestamp;
- source version or commit if available;
- snapshot or effective date;
- response checksum;
- parser version;
- row counts before and after filtering;
- error and missingness counts;
- license and usage constraints.

Do not commit credentials or raw private responses. Compressed public artifacts should be accompanied by checksums and an explanation of how to unpack them.

## Testing strategy

### Unit tests

Test URL normalization, scoped package parsing, retry classification, semver handling, workflow parsing, advisory classification, maintainer aggregation, reverse graph traversal, normalization, and empty-data behavior.

### Fixture tests

Use tiny hand-verified graphs with cycles, multiple versions, optional edges, duplicate edges, no workflows, missing repositories, and shared maintainers. Expected metric values should be committed as fixtures.

### Integration tests

Mock external API responses and verify that collection can resume after a failure without duplicate rows or incorrect completion flags. Never use live credentials or run tests against attacker infrastructure.

### Reproducibility tests

Run a clean end-to-end fixture pipeline twice with the same seed and verify identical outputs. Record intentional nondeterminism when GPU or graph sampling is used.

## Experiment manifests

Every experiment should have a machine-readable manifest with fields from `42_experiment_manifest_template.yaml`. The manifest should be copied into the result directory and referenced in the report.

## Documentation quality gates

Before each release or checkpoint:

1. run syntax and unit checks;
2. validate Markdown links and CSV headers;
3. verify no secrets or raw personal data are staged;
4. calculate checksums for committed compressed artifacts;
5. record unresolved data-quality warnings;
6. compare row counts with the previous snapshot;
7. write a short changelog entry.
