# Repository context and source selection

Assessment date: **20 October 2026**. Audited revision: `fc6b9de5758f00a6ca902dc7ba52bb38cef56553` (also recorded programmatically in the audit JSON).

## Implemented system

`scripts/collect_data.py` collects current npm metadata, dependency graphs from deps.dev, public GitHub workflow-directory observations, and keyword-classified advisory records into SQLite. It seeds packages from a high-impact list and expands by dependency discovery. The current schema does not timestamp every package-version observation or retain a complete historical workflow state.

`scripts/calculate_metrics.py` computes package-level reverse reach, maintainer portfolio size, counts of workflow-associated dependent packages, and a normalized weighted score. It writes a database table and optionally a CSV. It does not fit a model. The paper calls the `attacker_roi` field the **legacy score**, because attack success probability, cost, and utility are not observed.

`platform/` is a research browsing and administration application, with a much larger research corpus and additional data-reconstruction scripts. Its existence does not establish predictive validity.

## Conflicts identified during this work

1. **The compressed exports disagree.** The CSV has 20 nonzero `blast_radius` entries; SQLite has 17,809. Independent recomputation matches the SQLite values. All package names, maintainer statistics, and plain dependency metrics match across artifacts. This identifies an inconsistency, not its cause or which export came first.
2. **Snapshot timestamps have different meanings.** `benchmark_snapshot_manifest.json` supplies a June date; the SQLite metric table has a July calculation timestamp. Neither establishes all source observations at a single past time.
3. **Research prose contains stale totals.** `68_temporal_reconstruction_and_baseline_results.md` mixes multiple intermediate cohort sizes. The current CSV inventory has 47 records, 45 tagged retained source objects, and 258 declared edges. The manuscript uses the machine-readable input counts and labels them appropriately.
4. **A faithful CSV analysis can still misdescribe the database.** `51_current_snapshot_structural_analysis.json` describes the supplied CSV's sparse workflow metrics. It must not be generalized to mean the database has only 20 packages with nonzero workflow reach.
5. **Current temporal records are not a predictive cohort.** The supplied eligibility gate and ledger lack cutoff-valid controls. Family counts are identifiers and are not independent sample counts. Some label classes describe different outcomes.

## What was newly executed

The manuscript's Python audit independently traversed all package roots, recomputed all seven SQLite metric fields, compared every package with the compressed CSV, evaluated deterministic and tie-sensitive queue overlap, and swept eleven score weights. It inventoried the temporal CSVs without refetching incident reports or source registry responses. Figures use the resulting aggregate JSON.

No original data export, collector, metrics program, website, or previous research note was modified. New outputs live in `manuscript/`, with one README link at the repository root and an Overleaf ZIP at the root.

## Example-project adaptation

The reference `/home/m4x1d/Desktop/GOAD/manuscript/` supplied the structural pattern: a main file, section inputs, a separate style/configuration layer, and a compile script. The requested IEEE appearance is implemented with `IEEEtran[conference]`, replacing the example's ordinary one-column article layout. The paper's domain, empirical values, literature, and figures were developed for the npm repository.
