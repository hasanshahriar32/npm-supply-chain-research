# Release lockfile comparison and bibliography refresh

## Declared dependencies in the Pterodactyl release

The Pterodactyl panel archive is the one inspected release with a Node manifest and a Yarn Classic lockfile. Its SHA-256 matches the pinned YunoHost recipe. Both dependency files match the Git files at the commit resolved from the named source release tag. The diagnostic compares these exact dependency inputs using the same parser and registry collection.

| Evidence | Archive | Tag-resolved source |
| --- | ---: | ---: |
| Corroborated descriptor candidates | 294 | 294 |
| Registry-linked package versions | 224 | 224 |
| Documented hit for the name portfolio | Yes | Yes |
| Documented hit for each of the three version cutoff choices | Yes | Yes |

All 252 requested exact versions supplied usable maintainer lists. The agreement follows from the identical manifest and lockfile. The archive contains 17 JavaScript files in its public assets directory. The evidence establishes preservation of declared dependencies through the release archive. It leaves their inclusion in the built JavaScript unresolved. This is a one-release diagnostic. [Frozen protocol](../research/consumer_holdout/runs/yunohost-release-lock/protocol.json), [results](../research/consumer_holdout/runs/yunohost-release-lock/results.json).

## Active manuscript references

The two journal PDFs use 11 journal articles and two conference publications from 2024–2026. The verification counts the FSE issue of Proceedings of the ACM on Software Engineering as a conference publication. Publication details were checked against publisher records and Crossref metadata. The next revision should retain recent archival journal work where it directly supports the claim, with conference papers reserved for the closest evidence. [Bibliography audit](../manuscript_q1/results/bibliography_audit.json).

- **Dependency measurement.** Gamage et al. compare lockfile designs, Bifolco et al. examine errors in GitHub dependency and dependent records, and Wang et al. evaluate ecosystem-scale dependency resolution. These studies inform the choice to bind a path to its consumer importer and observation date. [Empirical Software Engineering](https://doi.org/10.1007/s10664-025-10789-w), [Information and Software Technology](https://doi.org/10.1016/j.infsof.2025.107854), [IEEE Transactions on Software Engineering](https://www.computer.org/csdl/journal/ts/2026/11/11627712/2iwk9uDqra8).
- **Artifact inventories.** Bi et al. analyze practical SBOM design issues, and Xiao et al. measure omissions in published Java SBOMs. These inform the audit's separate checks for an exact artifact digest and relevant dependency metadata. [ACM Transactions on Software Engineering and Methodology](https://doi.org/10.1145/3654442), [NDSS proceedings](https://www.ndss-symposium.org/ndss-paper/jbomaudit-assessing-the-landscape-compliance-and-security-implications-of-java-sboms/).
- **Closest intervention.** He et al. simulate how coordinated pinning at selected upstream npm packages changes exposure. The present study compares account portfolios at equal budgets and measures documented reach to pinned consumers. [FSE proceedings](https://doi.org/10.1145/3715728).

The objective section attributes the classical greedy bound to Nemhauser, Wolsey, and Fisher and gives the gap-decrease proof directly.
