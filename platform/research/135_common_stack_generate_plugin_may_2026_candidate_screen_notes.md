# Bounded candidate screen: `@common-stack/generate-plugin` — May 2026

## Scope and evidence status

This screen is limited to the single npm package `@common-stack/generate-plugin`; it does **not** expand to any broader PolinRider-associated activity. The selected screen is not asserted related to an existing governed incident family, because no prior primary-ledger row represents this package or campaign.

Sonatype’s 21 May 2026 report identifies the package as hijacked and explicitly names `9.0.2-alpha.21` and `9.0.2-alpha.22` as malicious releases. [1] GitHub’s reviewed malware advisory independently lists those same two versions in a finite package-specific affected-version set, alongside additional versions that were later curated into that advisory. [2] The strict candidate target is therefore the **two-version intersection only**—`9.0.2-alpha.21` and `9.0.2-alpha.22`—rather than any inferred or merged campaign-wide list.

The reports establish a bounded version-level incident screen, not a claim about a threat actor, campaign completeness, victim impact, installation, execution, or causal pathway. Official npm registry metadata must independently establish the affected-release time map, one-millisecond strict cutoff, and retained predecessor object before any admission decision. No package payload has been downloaded, extracted, installed, or executed.

## Interpretation boundaries

The screen currently creates **zero** primary-ledger records, families, source snapshots, declarations, dependency edges, validation units, controls, benign labels, historical installation traces, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, models, or predictive metrics. Absence from an existing ledger is not evidence of independence; it only confirms that this package has not previously been governed as a record.

## References

[1] [Sonatype, “Hijacked npm Package Attempts to Deliver PolinRider-Linked RAT,” 21 May 2026](https://www.sonatype.com/blog/hijacked-npm-package-attempts-to-deliver-polinrider-linked-rat).

[2] [GitHub Advisory Database, “Malware in @common-stack/generate-plugin,” GHSA-6p55-6hvr-3xmg](https://github.com/advisories/GHSA-6p55-6hvr-3xmg).
