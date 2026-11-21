# Development results for npm workspaces, overrides and pnpm

The next consumer study needs better evidence yield. The preceding holdout resolved only 29 of 155 paired outcomes. This development stage checks importer and package-manager semantics on the original 40-project pilot. It preserves the completed holdout's frozen comparison and results.

| Development measurement | Observed result |
| --- | ---: |
| Original paired npm pilot projects with a path | 7 of 40 |
| New npm development projects with a public-registry path | 12 of 40 |
| Pinned workspace manifests recovered | 22 in one project |
| npm path witnesses containing an effective-range change | 418 |
| pnpm v9 root-importer paths within three mandatory edges | 659 in four projects |
| Distinct pnpm version identifiers checked at the registry | 598 |
| pnpm path identifiers matching public npm SHA-512 metadata | 659 of 659 |

The npm procedure uses the package manager for override semantics, with separate checks of each raw declaration, physical lockfile location and effective range. The pnpm procedure reads the project document independently and cross-checks the resulting paths with the native lockfile listing. Two pilot lockfiles have separate boot and project documents. Treating the boot document as the project graph would put package-manager dependencies in the wrong population. The project document supplies the consumer importers. [pnpm lockfile format](https://github.com/pnpm/pnpm/blob/main/pnpm/docs/lockfile.md) · [Native lockfile listing](https://pnpm.io/cli/list)

These are development measurements rather than accuracy estimates. Counts of path witnesses can repeat a package/version across importers and projects. The pnpm result covers root dependencies while retaining unknowns for deeper and unsupported edges. The hash comparison establishes matching content identifiers reported by the lockfile and registry. It does not establish what a production installation executed.

The local tests cover mismatch at the nearest npm location, separate workspace versions, stale workspace manifests, relevant and irrelevant overrides, exact pnpm peer snapshots, patched dependencies, two-document YAML and full SHA-512 values. A separate medchain VPS run passed all 13 JavaScript fixture tests with a temporary checksum-verified Node 24.22.0 runtime. Only code and synthetic fixtures were sent for that test. [Development replay](../research/consumer_parser_development/README.md)

## Second-frame screening on medchain

The captured YunoHost catalog had 705 application records. The upstream-field screen yielded 553 distinct root GitHub repository keys, of which 500 remained after earlier frame and endpoint exclusions. The VPS inspected a pinned root `package.json` for each candidate. It observed 219 manifests and 270 HTTP 404 responses. Eleven repository HEAD requests remained unresolved. A 404 in this stage establishes only that the pinned root path did not return a manifest.

Repository-key exclusions alone missed three commits already observed in the pilot or first holdout. A fourth duplicate appeared within the YunoHost frame. Exact-commit deduplication leaves **215 distinct pinned candidates with root manifests**. This checks exact commits. Forks with different commits can still share application code.

| Declared manager among the 215 candidates | Projects |
| --- | ---: |
| No explicit declaration | 162 |
| pnpm | 28 |
| Yarn | 20 |
| Bun | 3 |
| npm | 2 |

Seventeen of the 215 declare workspaces and 148 declare production dependencies in the root manifest. The lockfile evidence may reveal more project roots and managers. A manager declaration supplies an intake signal rather than proof of an eligible lockfile. This stage inspected zero dependency lockfiles and made zero portfolio comparisons. The exact-commit evidence and exclusions are recorded in the [second-frame ledger](../research/consumer_parser_development/yunohost_root_frame.json).

Both VPS jobs ended and their temporary directories were removed. A subsequent check found no study test or manifest-screen process still running.
