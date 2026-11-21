# YunoHost packaging and importer audit

The packaging audit identifies three applications whose recipes name an importer or subdirectory with a recoverable lockfile. All three have documented hits under both five-account portfolios, across all three cutoff choices. One recipe builds a frontend at the exact commit where the original root walk found no mandatory dependencies. The other two recipes select different commits from those studied at the upstream roots.

## Audit population

The audit covers two unresolved groups from the 215-project YunoHost frame after the Yarn Classic follow-up.

| Checked group | Projects | Findings |
| --- | ---: | --- |
| Empty pnpm workspace root | 15 | 12 use release or distribution payloads. Three run a JavaScript build, including two with identifiable workspace paths. |
| No conventional root lockfile | 16 | Three recipes contain npm dependency commands. One uses a nested server lockfile. The other two lack a committed npm lockfile at the selected root. |

The frozen capture contains 248 file receipts across 31 catalog packaging revisions. There are 151 retained files and 97 HTTP 404 observations. Evidence consists of pinned manifests, recipes and service templates. Each positive classification records its supporting file, line and hash. The absence of an explicit command in the retained files leaves other build and delivery paths unresolved. [YunoHost app scripts](https://doc.yunohost.org/en/dev/packaging/scripts/).

## Source identity and dependency paths

Four of the six recipes with explicit JavaScript package commands select a source commit different from the original study's pin. We resolved all four named source tags and recorded the two directly declared commits. Two recipes use npm install without a committed root lockfile. The Discourse recipe delegates to an asset compilation task. This audit's inspected chain reaches an upstream build script without establishing one named importer for the app.

For the three named cases, each downloaded archive matches its recipe's declared SHA-256. The exact manifest and lockfile bytes in the archive also match the commit-pinned files. The packaging trees contain no patches for these sources in the checked locations. [YunoHost source acquisition and patching](https://doc.yunohost.org/dev/packaging/scripts/helpers_v2.1/).

| Recipe | Selected importer | Source matches the root study | Verified paths |
| --- | --- | --- | ---: |
| Jellyfin Vue | packages/frontend | Yes | 63 |
| LAN Games | server | No | 146 |
| Papra | apps/papra-client and apps/papra-server | No | 216 |

The npm reader cross-checks the selected importer offline. For pnpm, the original named importer is projected into a sterile root for native comparison against the retained snapshots. That check traces up to three mandatory edges and leaves unresolved, linked and other unsupported paths unconfirmed. A path joins only when each prefix has a registry identity and observed maintainer list. All 401 requested version records yielded usable lists. There are 425 verified paths, counted within importers. No recipe or project scripts ran.

The three applications have a documented hit under both portfolios for each cutoff choice. They make up a conditional diagnostic with a different importer or source definition. The 215-project comparison retains its original scope and bounds of 2.3–42.3% turnover after the Yarn Classic follow-up. This check verifies dependency declarations in the recipe-selected source. Build contents, runtime use and installed versions remain unobserved.

The [recipe evidence](../research/consumer_holdout/runs/yunohost-packaging/classification.json), [source checks](../research/consumer_holdout/runs/yunohost-packaging/archive_checks.json), and [paired results](../research/consumer_holdout/runs/yunohost-packaging/importer_results.json) support the counts. Offline replay uses the original pinned packaging files, selected source files, and registry receipts in the ignored local evidence directory.
