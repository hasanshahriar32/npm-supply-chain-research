# November consumer pilot

The 40 application repositories were drawn from 199 entries in a pinned index, independently of the earlier endpoint sampling frame. The [sampling protocol](../consumer_pilot/protocol.json) and [evaluation protocol](protocol.md) specify the draw, inputs and comparison. The JSON [project assessments](reviews.json) and [paired summary](summary.json) are automated. The pilot includes no human annotation.

Eight projects passed the root npm input and parser checks. Seven yielded a corroborated mandatory dependency path. The two software implementations agreed on 1,147 installation locations. The exact historical metadata join covered 278 of 1,110 distinct versions counted within each project. Of the eight compared projects, both frozen portfolios had evidence in five. Three lacked a documented hit. Neither the 32 unevaluable projects nor missing exact-version observations are negatives. At budget 100 the two account sets were identical before evaluation. This budget cannot distinguish their consumer coverage, even with perfect data. The pilot cannot establish ranking equivalence or reduction in security incidents.

## Replay

Run from the repository root with Python 3 and Node with npm installed. The run used npm's bundled SemVer 7.8.5 and Arborist 9.9.1. On a fresh checkout restore the retained public root files with `python scripts/collect_consumer_pilot.py replay`. This obtains the pinned files and verifies their recorded hashes. For the existing local cache, the following steps require no network.

```sh
python scripts/collect_consumer_pilot.py verify
node scripts/tests/test_consumer_lock_evidence.cjs
python scripts/evaluate_consumer_pilot.py
python scripts/check_census_version_notes.py
python scripts/census_audit_manager.py --audit
```

The [request ledger](../consumer_pilot/observations.json) retains URLs, HTTP outcomes, timestamps and hashes for the consumer data. Software agreement uses the same underlying lockfile and SemVer library. A corroborated example is a static dependency path, and a matched username is a dated registry association. The earlier human-labeled filenames have been corrected in the validation materials. Neither author is credited with manually adjudicating these pilot results.

## Implications for a follow-up

Six of the eight unsupported inputs had npm overrides. Tests for override semantics, other managers and nested application roots should be developed outside the confirmatory sample. Before acquiring another cohort, check whether training portfolios differ at the intended budgets. Retain an identical-selection case as a control and specify a separate contrast with distinct portfolios using training data only. Freeze it before scoring fresh consumers. The pilot data have already been inspected and cannot serve as that fresh test.

Training-only diagnostic after the pilot. Entries give common slots in name-based and version-based selections at each budget. These are descriptive and have no fresh consumer outcomes.

| Rule | 1 | 5 | 10 | 25 | 50 | 100 |
|---|---:|---:|---:|---:|---:|---:|
| direct_p | 1 | 5 | 10 | 24 | 46 | 96 |
| exact_union | 1 | 3 | 10 | 25 | 49 | 97 |
| greedy_coverage | 1 | 5 | 10 | 25 | 50 | 100 |
| immediate_only | 1 | 5 | 10 | 25 | 48 | 96 |
| portfolio | 1 | 5 | 10 | 25 | 50 | 100 |
