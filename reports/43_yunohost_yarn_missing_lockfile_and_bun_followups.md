# Coverage evidence from newer Yarn, missing lockfiles, and Bun

The 215-project YunoHost comparison had 70 unresolved primary pairs after the empty pnpm root sensitivity. We checked three groups using pinned files and already retained registry observations. These analyses extend the sensitivity comparison in the same frame.

| Evidence checked | Candidates | Additional resolved primary pairs |
| --- | ---: | ---: |
| Yarn 3 and 4 manifest and root lock entries | 14 | 6 common negatives |
| Pinned manifest and failed root lockfile probes | 18 | 9 common negatives |
| Bun direct paths joined to existing registry observations | 6 | 1 common positive |

For Yarn, the check requires a unique root workspace locator and agreement between its locked dependency ranges and the development declarations in the pinned manifest. The six accepted roots contain no regular, optional, peer, or bundled production declarations. Yarn's workspace resolver combines regular and development declarations when it builds this entry. We record the supported lockfile generation, including version 10 after checking it against the Yarn 4.18 source. [Workspace resolver](https://github.com/yarnpkg/berry/blob/%40yarnpkg/cli/4.18.0/packages/yarnpkg-core/sources/WorkspaceResolver.ts) · [Lockfile implementation](https://github.com/yarnpkg/berry/blob/%40yarnpkg/cli/4.18.0/packages/yarnpkg-core/sources/Project.ts)

For missing lockfiles, nine pinned manifests had no production declarations or child workspaces. All six supported lockfile probes and the pnpm workspace-file probe returned HTTP 404. A mandatory path from the root requires a root declaration. This identifies an empty root scope even when lockfiles are absent from the capture. [Protocol and source observations](../research/consumer_holdout/runs/yunohost-empty-declared-roots/results.json)

Of six Bun candidates, two were eligible for checking direct regular dependencies. One supplied only a binary lockfile and three declared overrides or patches. The two eligible text lockfiles yielded 42 same-name versions within their declared ranges. Four versions in Y098 and ten in Y473 matched SHA-512 values in retained npm receipts. For Y473, the regular dependency `p-queue@10.0.0` supplied a hit for the name portfolio, all three version portfolios, and the control. The check uses earlier registry observations and measures positive evidence from direct paths. [Bun lockfile documentation](https://bun.com/docs/pm/lockfile) · [Y473 pinned lockfile](https://github.com/vert-sh/vert/blob/35ebeb1679eb0b1af3f099c03060cb89f72e70f8/bun.lock) · [Bun evidence](../research/consumer_holdout/runs/yunohost-bun-direct/results.json)

| Sensitivity stage | Resolved of 215 | Turnover bounds | Net change in percentage points |
| --- | ---: | ---: | ---: |
| After the pnpm check | 145 | 2.3–34.9% | −32.6 to +31.2 |
| After the Yarn and missing-lockfile checks | 160 | 2.3–27.9% | −25.6 to +24.2 |
| After the Bun direct check | 161 | 2.3–27.4% | −25.1 to +23.7 |

The five confirmed changes persist. The final sensitivity leaves 54 projects unresolved, and both directions of net change remain possible. The companion reproduces the bounds from the recorded source observations and redoes the Bun SHA-512 joins. [Replication companion](../submission/emse/EMSE_Consumer_Replication.zip)
