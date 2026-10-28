# Endpoint audit evidence packet

Both authors agreed to review independently. Initial label sheets contain no automated suggestions. Use supported / unsupported / unknown for each label and cite evidence paths in notes. Do not discuss initial labels until both sheets are saved. Automated evidence remains provisional.

Current-time static evidence does not establish old HEAD validity, workflow execution, or historical publisher authority.

## Label rubric

- `repository_mapping_supported`: every listed package/version mapping has registry repository evidence and a matching named package manifest at the inspected commit. Ambiguous monorepo paths and redirects remain unknown.
- `workflow_file_present`: an actual workflow YAML file is present at the pinned commit.
- `install_directive_observed`: a relevant workflow run step contains an installation command in the package path, or a reusable workflow/action has been resolved to equivalent evidence. Echoed examples, comments and unrelated paths do not count. Record conditions. This never claims a run succeeded.
- `lockfile_present`: an inspected lockfile applies to the named package path or enclosing workspace. Record the relationship.
- `dependency_version_supported`: a manifest dependency has a specific corresponding version entry in the relevant lockfile. Record at least one dependency/version pair; this does not validate every graph path.
- `unsupported`: inspected evidence contradicts the criterion, with a cited reason. `unknown`: evidence is missing, ambiguous or unresolved. Blank means not reviewed.

Save initial labels independently. Human results require both complete sheets and resolution of disagreements. Do not copy automated labels into the independent sheets.

## A001 — ai/nanoevents

Commit: `081aa8995d82321b8d5d4bb64f97d63cb04380d7`.
Original package/version mappings: nanoevents@9.1.0

Evidence:
- [.github/workflows/test.yml](https://github.com/ai/nanoevents/blob/081aa8995d82321b8d5d4bb64f97d63cb04380d7/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A001__file_faff1af3d8ff4089.json`
- [.github/workflows/release.yml](https://github.com/ai/nanoevents/blob/081aa8995d82321b8d5d4bb64f97d63cb04380d7/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A001__file_87db21a973eed4fe.json`
- [pnpm-lock.yaml](https://github.com/ai/nanoevents/blob/081aa8995d82321b8d5d4bb64f97d63cb04380d7/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A001__file_32824c984905bb02.json`
- [package.json](https://github.com/ai/nanoevents/blob/081aa8995d82321b8d5d4bb64f97d63cb04380d7/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A001__file_7ae45ad102eab3b6.json`

## A002 — arthurfiorette/tinylibs

Commit: `c6dc5ed55654dfa6e006a9817b48db1f80d20a6e`.
Original package/version mappings: cache-parser@1.2.6, fast-defer@1.1.9, http-vary@1.0.3, object-code@2.0.0

Evidence:
- [.github/workflows/publish.yml](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_551d1fcf87f78cc3.json`
- [packages/cache-parser/package.json](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/packages/cache-parser/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_67401df07a61f593.json`
- [.github/workflows/ci.yml](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_b803fcb7f17ed923.json`
- [.github/workflows/codeql.yml](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/.github/workflows/codeql.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_12783128521e452a.json`
- [package.json](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_7ae45ad102eab3b6.json`
- [pnpm-lock.yaml](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_32824c984905bb02.json`
- [packages/http-vary/package.json](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/packages/http-vary/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_84d66f468448c853.json`
- [packages/object-code/package.json](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/packages/object-code/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_b93016910f98694e.json`
- [.github/workflows/automerge.yml](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/.github/workflows/automerge.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_cc8c65daed8907e6.json`
- [packages/fast-defer/package.json](https://github.com/arthurfiorette/tinylibs/blob/c6dc5ed55654dfa6e006a9817b48db1f80d20a6e/packages/fast-defer/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A002__file_c280f074bac3f0a0.json`

## A003 — beaugunderson/ip-address

Commit: `db0dbda0505a70ddbbfeea7f04023798c0f156bf`.
Original package/version mappings: ip-address@10.2.0

Evidence:
- [.github/workflows/release.yml](https://github.com/beaugunderson/ip-address/blob/db0dbda0505a70ddbbfeea7f04023798c0f156bf/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A003__file_87db21a973eed4fe.json`
- [package-lock.json](https://github.com/beaugunderson/ip-address/blob/db0dbda0505a70ddbbfeea7f04023798c0f156bf/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A003__file_053150b640a7ce75.json`
- [.github/workflows/ci.yml](https://github.com/beaugunderson/ip-address/blob/db0dbda0505a70ddbbfeea7f04023798c0f156bf/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A003__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/beaugunderson/ip-address/blob/db0dbda0505a70ddbbfeea7f04023798c0f156bf/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A003__file_7ae45ad102eab3b6.json`

## A004 — bendrucker/builtin-status-codes

Commit: `1b2ef4de7f813025b8f1f1a4cbd3938102e7da26`.
Original package/version mappings: builtin-status-codes@3.0.0

Evidence:
- [.github/workflows/test.yml](https://github.com/bendrucker/builtin-status-codes/blob/1b2ef4de7f813025b8f1f1a4cbd3938102e7da26/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A004__file_faff1af3d8ff4089.json`
- [package.json](https://github.com/bendrucker/builtin-status-codes/blob/1b2ef4de7f813025b8f1f1a4cbd3938102e7da26/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A004__file_7ae45ad102eab3b6.json`

## A005 — catdad-experiments/heic-decode

Commit: `47773f7b17acc22bfb8bb7869b6ef087d24c0ca9`.
Original package/version mappings: heic-decode@2.1.0

Evidence:
- [package.json](https://github.com/catdad-experiments/heic-decode/blob/47773f7b17acc22bfb8bb7869b6ef087d24c0ca9/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A005__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci.yml](https://github.com/catdad-experiments/heic-decode/blob/47773f7b17acc22bfb8bb7869b6ef087d24c0ca9/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A005__file_b803fcb7f17ed923.json`

## A006 — dcastil/tailwind-merge

Commit: `7b5d20c543c3de07cd9fad570a9af0b5a0f976f6`.
Original package/version mappings: tailwind-merge@3.6.0

Evidence:
- [.github/workflows/npm-publish.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/npm-publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_8a5ce8b612395836.json`
- [.github/workflows/label.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/label.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_10c0cd6a4f95e78d.json`
- [pnpm-lock.yaml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_32824c984905bb02.json`
- [package.json](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_7ae45ad102eab3b6.json`
- [.github/workflows/benchmark.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/benchmark.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_aacbd0338bcf5989.json`
- [.github/workflows/test.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_faff1af3d8ff4089.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_63bd641104d10e25.json`
- [.github/workflows/metrics-report.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/metrics-report.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_bb3731845fc22656.json`
- [.github/workflows/comment-released-prs-and-issues.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/comment-released-prs-and-issues.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_3f88555d25211643.json`
- [.github/workflows/draft-release.yml](https://github.com/dcastil/tailwind-merge/blob/7b5d20c543c3de07cd9fad570a9af0b5a0f976f6/.github/workflows/draft-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A006__file_3d80a0bd2aa86725.json`

## A007 — dmonad/lib0

Commit: `8cee1b4564ab77caf4e316901040b8289043a4b4`.
Original package/version mappings: lib0@0.2.117

Evidence:
- [package-lock.json](https://github.com/dmonad/lib0/blob/8cee1b4564ab77caf4e316901040b8289043a4b4/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A007__file_053150b640a7ce75.json`
- [.github/workflows/publish.yml](https://github.com/dmonad/lib0/blob/8cee1b4564ab77caf4e316901040b8289043a4b4/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A007__file_551d1fcf87f78cc3.json`
- [package.json](https://github.com/dmonad/lib0/blob/8cee1b4564ab77caf4e316901040b8289043a4b4/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A007__file_7ae45ad102eab3b6.json`
- [.github/workflows/node.js.yml](https://github.com/dmonad/lib0/blob/8cee1b4564ab77caf4e316901040b8289043a4b4/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A007__file_014228303dff9a1a.json`

## A008 — dougwilson/nodejs-depd

Commit: `7ad9a48dff1e7fe52d4298da7c1235944073bfc9`.
Original package/version mappings: depd@2.0.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/dougwilson/nodejs-depd/blob/7ad9a48dff1e7fe52d4298da7c1235944073bfc9/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A008__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/dougwilson/nodejs-depd/blob/7ad9a48dff1e7fe52d4298da7c1235944073bfc9/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A008__file_7ae45ad102eab3b6.json`

## A009 — dumbmatter/fakeindexeddb

Commit: `8881007614a7c04e1766f0b802992a5dfacfafd7`.
Original package/version mappings: fake-indexeddb@6.2.5

Evidence:
- [package.json](https://github.com/dumbmatter/fakeindexeddb/blob/8881007614a7c04e1766f0b802992a5dfacfafd7/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A009__file_7ae45ad102eab3b6.json`
- [.github/workflows/test.yml](https://github.com/dumbmatter/fakeindexeddb/blob/8881007614a7c04e1766f0b802992a5dfacfafd7/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A009__file_faff1af3d8ff4089.json`
- [pnpm-lock.yaml](https://github.com/dumbmatter/fakeindexeddb/blob/8881007614a7c04e1766f0b802992a5dfacfafd7/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A009__file_32824c984905bb02.json`

## A010 — emilkowalski/sonner

Commit: `8e4662b39255120b62138312058f5d77c0139a5e`.
Original package/version mappings: sonner@2.0.7

Evidence:
- [.github/workflows/playwright.yml](https://github.com/emilkowalski/sonner/blob/8e4662b39255120b62138312058f5d77c0139a5e/.github/workflows/playwright.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A010__file_7afcd2d8f7b49bda.json`
- [pnpm-lock.yaml](https://github.com/emilkowalski/sonner/blob/8e4662b39255120b62138312058f5d77c0139a5e/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A010__file_32824c984905bb02.json`
- [package.json](https://github.com/emilkowalski/sonner/blob/8e4662b39255120b62138312058f5d77c0139a5e/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A010__file_7ae45ad102eab3b6.json`

## A011 — harlan-zw/packrup

Commit: `0185f9a29923c5e4e2a098c7547dfa9c5617e249`.
Original package/version mappings: packrup@0.1.2

Evidence:
- [.github/workflows/test.yml](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_faff1af3d8ff4089.json`
- [.github/workflows/export-sizes-comment.yml](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/.github/workflows/export-sizes-comment.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_32e1e6bbc68b6835.json`
- [pnpm-lock.yaml](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_32824c984905bb02.json`
- [.github/workflows/release.yml](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_87db21a973eed4fe.json`
- [.github/workflows/export-sizes.yml](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/.github/workflows/export-sizes.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_dd4e5d657995db57.json`
- [package.json](https://github.com/harlan-zw/packrup/blob/0185f9a29923c5e4e2a098c7547dfa9c5617e249/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A011__file_7ae45ad102eab3b6.json`

## A012 — hustcc/size-sensor

Commit: `95142567be1731cdb70591d36e82691083cb630f`.
Original package/version mappings: size-sensor@1.0.3

Evidence:
- [.github/workflows/build.yml](https://github.com/hustcc/size-sensor/blob/95142567be1731cdb70591d36e82691083cb630f/.github/workflows/build.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A012__file_5c3fa597431eda03.json`
- [package.json](https://github.com/hustcc/size-sensor/blob/95142567be1731cdb70591d36e82691083cb630f/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A012__file_7ae45ad102eab3b6.json`

## A013 — iamolegga/nestjs-pino

Commit: `6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0`.
Original package/version mappings: nestjs-pino@4.6.1

Evidence:
- [.github/workflows/publish-alpha.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/publish-alpha.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_fd2b3e20d4e18a3e.json`
- [.github/workflows/on-pr-master.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/on-pr-master.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_5bd2cec95b117954.json`
- [package.json](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_053150b640a7ce75.json`
- [.github/workflows/publish-with-git-tag-version.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/publish-with-git-tag-version.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_b90325ec3fb16e95.json`
- [.github/workflows/publish-coverage.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/publish-coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_be2c9642e19f3f4f.json`
- [.github/workflows/on-push-or-release.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/on-push-or-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_548b36f3597c4260.json`
- [.github/workflows/build-lint-test.yml](https://github.com/iamolegga/nestjs-pino/blob/6a1b7a4e8f86ebc9c41a76937ab9673466ca4dd0/.github/workflows/build-lint-test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A013__file_b168d1081eb1f2b4.json`

## A014 — jwalton/js-promise-breaker

Commit: `889b20b6f6bf5fb62ca4c95d154c38b435b4616b`.
Original package/version mappings: promise-breaker@7.0.0

Evidence:
- [package.json](https://github.com/jwalton/js-promise-breaker/blob/889b20b6f6bf5fb62ca4c95d154c38b435b4616b/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A014__file_7ae45ad102eab3b6.json`
- [.github/workflows/github-ci.yaml](https://github.com/jwalton/js-promise-breaker/blob/889b20b6f6bf5fb62ca4c95d154c38b435b4616b/.github/workflows/github-ci.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A014__file_1102636ac9e880a7.json`

## A015 — kuceb/cypress-plugin-tab

Commit: `a3c81aa384e97716ecfc751f46eab394b2d50a08`.
Original package/version mappings: cypress-plugin-tab@2.0.0

Evidence:
- [.github/workflows/release.yml](https://github.com/kuceb/cypress-plugin-tab/blob/a3c81aa384e97716ecfc751f46eab394b2d50a08/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A015__file_87db21a973eed4fe.json`
- [yarn.lock](https://github.com/kuceb/cypress-plugin-tab/blob/a3c81aa384e97716ecfc751f46eab394b2d50a08/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A015__file_51e4f558fae53465.json`
- [package.json](https://github.com/kuceb/cypress-plugin-tab/blob/a3c81aa384e97716ecfc751f46eab394b2d50a08/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A015__file_7ae45ad102eab3b6.json`
- [.github/workflows/nodejs.yml](https://github.com/kuceb/cypress-plugin-tab/blob/a3c81aa384e97716ecfc751f46eab394b2d50a08/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A015__file_e98936aa52a6dd74.json`

## A016 — lovell/detect-libc

Commit: `98928b7d26bd5c50dee12af0e433b47825d84df0`.
Original package/version mappings: detect-libc@2.1.2

Evidence:
- [package.json](https://github.com/lovell/detect-libc/blob/98928b7d26bd5c50dee12af0e433b47825d84df0/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A016__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci.yml](https://github.com/lovell/detect-libc/blob/98928b7d26bd5c50dee12af0e433b47825d84df0/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A016__file_b803fcb7f17ed923.json`
- [.github/workflows/integration.yml](https://github.com/lovell/detect-libc/blob/98928b7d26bd5c50dee12af0e433b47825d84df0/.github/workflows/integration.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A016__file_82454b2fc887e998.json`

## A017 — lukeed/totalist

Commit: `4b071d3e54d466a4059de89006c752da782c8b02`.
Original package/version mappings: totalist@3.0.1

Evidence:
- [.github/workflows/ci.yml](https://github.com/lukeed/totalist/blob/4b071d3e54d466a4059de89006c752da782c8b02/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A017__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/lukeed/totalist/blob/4b071d3e54d466a4059de89006c752da782c8b02/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A017__file_7ae45ad102eab3b6.json`

## A018 — matthewp/robot

Commit: `bde04654c082c3ba4a54ed57c29d91fbc59e54a9`.
Original package/version mappings: robot3@1.2.0

Evidence:
- [.github/workflows/site.yml](https://github.com/matthewp/robot/blob/bde04654c082c3ba4a54ed57c29d91fbc59e54a9/.github/workflows/site.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A018__file_8efa99d007eda512.json`
- [.github/workflows/nodejs.yml](https://github.com/matthewp/robot/blob/bde04654c082c3ba4a54ed57c29d91fbc59e54a9/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A018__file_e98936aa52a6dd74.json`
- [.github/workflows/release.yml](https://github.com/matthewp/robot/blob/bde04654c082c3ba4a54ed57c29d91fbc59e54a9/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A018__file_87db21a973eed4fe.json`
- [package.json](https://github.com/matthewp/robot/blob/bde04654c082c3ba4a54ed57c29d91fbc59e54a9/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A018__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/matthewp/robot/blob/bde04654c082c3ba4a54ed57c29d91fbc59e54a9/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A018__file_053150b640a7ce75.json`

## A019 — paulmillr/noble-ciphers

Commit: `fe4336756e8b352ea520d8bd6e8547552e352189`.
Original package/version mappings: @noble/ciphers@2.2.0

Evidence:
- [package.json](https://github.com/paulmillr/noble-ciphers/blob/fe4336756e8b352ea520d8bd6e8547552e352189/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A019__file_7ae45ad102eab3b6.json`
- [.github/workflows/fuzz.yml](https://github.com/paulmillr/noble-ciphers/blob/fe4336756e8b352ea520d8bd6e8547552e352189/.github/workflows/fuzz.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A019__file_05173c6260b3a634.json`
- [.github/workflows/release.yml](https://github.com/paulmillr/noble-ciphers/blob/fe4336756e8b352ea520d8bd6e8547552e352189/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A019__file_87db21a973eed4fe.json`
- [package-lock.json](https://github.com/paulmillr/noble-ciphers/blob/fe4336756e8b352ea520d8bd6e8547552e352189/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A019__file_053150b640a7ce75.json`
- [.github/workflows/test.yml](https://github.com/paulmillr/noble-ciphers/blob/fe4336756e8b352ea520d8bd6e8547552e352189/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A019__file_faff1af3d8ff4089.json`

## A020 — rcbyr/keen-slider

Commit: `520c757a80aa10ff224e9c89b0917edfa811adcf`.
Original package/version mappings: keen-slider@6.8.6

Evidence:
- [package-lock.json](https://github.com/rcbyr/keen-slider/blob/520c757a80aa10ff224e9c89b0917edfa811adcf/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A020__file_053150b640a7ce75.json`
- [package.json](https://github.com/rcbyr/keen-slider/blob/520c757a80aa10ff224e9c89b0917edfa811adcf/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A020__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/rcbyr/keen-slider/blob/520c757a80aa10ff224e9c89b0917edfa811adcf/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A020__file_7829468e86c1cc5d.json`

## A021 — richienb/char-regex

Commit: `b2a1dc9967b556f9a576ce0f7ded2a457ba4aefa`.
Original package/version mappings: char-regex@2.0.2

Evidence:
- [package.json](https://github.com/richienb/char-regex/blob/b2a1dc9967b556f9a576ce0f7ded2a457ba4aefa/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A021__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/richienb/char-regex/blob/b2a1dc9967b556f9a576ce0f7ded2a457ba4aefa/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A021__file_7829468e86c1cc5d.json`

## A022 — ruimarinho/google-libphonenumber

Commit: `e13ae0fa7e71feec88958ef5c5f6fa2e9239a291`.
Original package/version mappings: google-libphonenumber@3.2.44

Evidence:
- [package-lock.json](https://github.com/ruimarinho/google-libphonenumber/blob/e13ae0fa7e71feec88958ef5c5f6fa2e9239a291/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A022__file_053150b640a7ce75.json`
- [package.json](https://github.com/ruimarinho/google-libphonenumber/blob/e13ae0fa7e71feec88958ef5c5f6fa2e9239a291/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A022__file_7ae45ad102eab3b6.json`
- [.github/workflows/publish.yaml](https://github.com/ruimarinho/google-libphonenumber/blob/e13ae0fa7e71feec88958ef5c5f6fa2e9239a291/.github/workflows/publish.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A022__file_e81e13daadd1745d.json`
- [.github/workflows/release.yaml](https://github.com/ruimarinho/google-libphonenumber/blob/e13ae0fa7e71feec88958ef5c5f6fa2e9239a291/.github/workflows/release.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A022__file_e426ed4584283702.json`
- [.github/workflows/ci.yaml](https://github.com/ruimarinho/google-libphonenumber/blob/e13ae0fa7e71feec88958ef5c5f6fa2e9239a291/.github/workflows/ci.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A022__file_944291df2c9c0635.json`

## A023 — sindresorhus/dot-prop

Commit: `d5d11c71a70bfb643a45d22821ed6d284240fce5`.
Original package/version mappings: dot-prop@10.1.0

Evidence:
- [package.json](https://github.com/sindresorhus/dot-prop/blob/d5d11c71a70bfb643a45d22821ed6d284240fce5/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A023__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/sindresorhus/dot-prop/blob/d5d11c71a70bfb643a45d22821ed6d284240fce5/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A023__file_7829468e86c1cc5d.json`

## A024 — sindresorhus/is-fn

Commit: `b836d524750a1688e1ac26ad02d0534005e87eb4`.
Original package/version mappings: is-fn@3.0.0

Evidence:
- [.github/workflows/main.yml](https://github.com/sindresorhus/is-fn/blob/b836d524750a1688e1ac26ad02d0534005e87eb4/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A024__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/sindresorhus/is-fn/blob/b836d524750a1688e1ac26ad02d0534005e87eb4/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A024__file_7ae45ad102eab3b6.json`

## A025 — tada5hi/smob

Commit: `a3fac78f200ec7f8d5b20eaf09add25f1c2c4208`.
Original package/version mappings: smob@1.6.2

Evidence:
- [.github/workflows/release.yml](https://github.com/tada5hi/smob/blob/a3fac78f200ec7f8d5b20eaf09add25f1c2c4208/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A025__file_87db21a973eed4fe.json`
- [package.json](https://github.com/tada5hi/smob/blob/a3fac78f200ec7f8d5b20eaf09add25f1c2c4208/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A025__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/tada5hi/smob/blob/a3fac78f200ec7f8d5b20eaf09add25f1c2c4208/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A025__file_053150b640a7ce75.json`
- [.github/workflows/main.yml](https://github.com/tada5hi/smob/blob/a3fac78f200ec7f8d5b20eaf09add25f1c2c4208/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A025__file_7829468e86c1cc5d.json`

## A026 — thefrontside/ctrlc-windows

Commit: `aa2145df1bedd0bc8b578dfba684ff745a6f75ad`.
Original package/version mappings: ctrlc-windows@2.2.0

Evidence:
- [yarn.lock](https://github.com/thefrontside/ctrlc-windows/blob/aa2145df1bedd0bc8b578dfba684ff745a6f75ad/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A026__file_51e4f558fae53465.json`
- [package.json](https://github.com/thefrontside/ctrlc-windows/blob/aa2145df1bedd0bc8b578dfba684ff745a6f75ad/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A026__file_7ae45ad102eab3b6.json`
- [.github/workflows/test.yml](https://github.com/thefrontside/ctrlc-windows/blob/aa2145df1bedd0bc8b578dfba684ff745a6f75ad/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A026__file_faff1af3d8ff4089.json`
- [.github/workflows/changeset.yml](https://github.com/thefrontside/ctrlc-windows/blob/aa2145df1bedd0bc8b578dfba684ff745a6f75ad/.github/workflows/changeset.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A026__file_9977bcef16cc0176.json`
- [.github/workflows/release.yml](https://github.com/thefrontside/ctrlc-windows/blob/aa2145df1bedd0bc8b578dfba684ff745a6f75ad/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A026__file_87db21a973eed4fe.json`

## A027 — tricinel/highlight-words

Commit: `44cfc4311664c70832a2750a4b5b2925592ec464`.
Original package/version mappings: highlight-words@2.0.0

Evidence:
- [package.json](https://github.com/tricinel/highlight-words/blob/44cfc4311664c70832a2750a4b5b2925592ec464/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A027__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci.yml](https://github.com/tricinel/highlight-words/blob/44cfc4311664c70832a2750a4b5b2925592ec464/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A027__file_b803fcb7f17ed923.json`
- [pnpm-lock.yaml](https://github.com/tricinel/highlight-words/blob/44cfc4311664c70832a2750a4b5b2925592ec464/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A027__file_32824c984905bb02.json`

## A028 — unjs/rc9

Commit: `b95fe6a022713e008d075c6ced7dbce8aa917d53`.
Original package/version mappings: rc9@3.0.1

Evidence:
- [.github/workflows/autofix.yml](https://github.com/unjs/rc9/blob/b95fe6a022713e008d075c6ced7dbce8aa917d53/.github/workflows/autofix.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A028__file_89b476612e9731e1.json`
- [.github/workflows/checks.yml](https://github.com/unjs/rc9/blob/b95fe6a022713e008d075c6ced7dbce8aa917d53/.github/workflows/checks.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A028__file_3ea54af4839eb754.json`
- [package.json](https://github.com/unjs/rc9/blob/b95fe6a022713e008d075c6ced7dbce8aa917d53/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A028__file_7ae45ad102eab3b6.json`
- [pnpm-lock.yaml](https://github.com/unjs/rc9/blob/b95fe6a022713e008d075c6ced7dbce8aa917d53/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A028__file_32824c984905bb02.json`

## A029 — webdriverio-community/node-safaridriver

Commit: `d5df5239da69c26c9a3c7eb2a5a0e475f98efecf`.
Original package/version mappings: safaridriver@1.0.1

Evidence:
- [.github/workflows/expense.yml](https://github.com/webdriverio-community/node-safaridriver/blob/d5df5239da69c26c9a3c7eb2a5a0e475f98efecf/.github/workflows/expense.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A029__file_d04dbd23c0ea73cf.json`
- [package-lock.json](https://github.com/webdriverio-community/node-safaridriver/blob/d5df5239da69c26c9a3c7eb2a5a0e475f98efecf/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A029__file_053150b640a7ce75.json`
- [.github/workflows/ci.yml](https://github.com/webdriverio-community/node-safaridriver/blob/d5df5239da69c26c9a3c7eb2a5a0e475f98efecf/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A029__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/webdriverio-community/node-safaridriver/blob/d5df5239da69c26c9a3c7eb2a5a0e475f98efecf/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A029__file_7ae45ad102eab3b6.json`

## A030 — yomguithereal/mnemonist

Commit: `6b86cfbd9f0af47153737058fd82610623b1ace3`.
Original package/version mappings: mnemonist@0.40.4

Evidence:
- [.github/workflows/tests.yml](https://github.com/yomguithereal/mnemonist/blob/6b86cfbd9f0af47153737058fd82610623b1ace3/.github/workflows/tests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A030__file_1db27d93186e46d3.json`
- [package-lock.json](https://github.com/yomguithereal/mnemonist/blob/6b86cfbd9f0af47153737058fd82610623b1ace3/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A030__file_053150b640a7ce75.json`
- [package.json](https://github.com/yomguithereal/mnemonist/blob/6b86cfbd9f0af47153737058fd82610623b1ace3/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A030__file_7ae45ad102eab3b6.json`

## A031 — awslabs/aws-jwt-verify

Commit: `8f8352630a3ba5d07a4e364b1425b032597f66d8`.
Original package/version mappings: aws-jwt-verify@5.2.1

Evidence:
- [.github/workflows/main.yml](https://github.com/awslabs/aws-jwt-verify/blob/8f8352630a3ba5d07a4e364b1425b032597f66d8/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A031__file_7829468e86c1cc5d.json`
- [.github/workflows/browser.yml](https://github.com/awslabs/aws-jwt-verify/blob/8f8352630a3ba5d07a4e364b1425b032597f66d8/.github/workflows/browser.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A031__file_c76511afeed26896.json`
- [package.json](https://github.com/awslabs/aws-jwt-verify/blob/8f8352630a3ba5d07a4e364b1425b032597f66d8/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A031__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/awslabs/aws-jwt-verify/blob/8f8352630a3ba5d07a4e364b1425b032597f66d8/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A031__file_053150b640a7ce75.json`

## A032 — bigstickcarpet/readdir-enhanced

Commit: `None`.
Original package/version mappings: @mrmlnc/readdir-enhanced@2.2.1

Evidence:
- Acquisition unresolved; record unknown unless independently documented.

## A033 — bjornharrtell/jsts

Commit: `34166d7e96f2b1f3a099a20c9408741a9a7cacec`.
Original package/version mappings: jsts@2.12.1

Evidence:
- [.github/workflows/node.js.yml](https://github.com/bjornharrtell/jsts/blob/34166d7e96f2b1f3a099a20c9408741a9a7cacec/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A033__file_014228303dff9a1a.json`
- [package.json](https://github.com/bjornharrtell/jsts/blob/34166d7e96f2b1f3a099a20c9408741a9a7cacec/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A033__file_7ae45ad102eab3b6.json`
- [yarn.lock](https://github.com/bjornharrtell/jsts/blob/34166d7e96f2b1f3a099a20c9408741a9a7cacec/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A033__file_51e4f558fae53465.json`

## A034 — brooooooklyn/canvas

Commit: `bf0052671d7dfd998456eec0e1ac305fa9879dd1`.
Original package/version mappings: @napi-rs/canvas@1.0.0, @napi-rs/canvas-android-arm64@1.0.0, @napi-rs/canvas-darwin-arm64@1.0.0, @napi-rs/canvas-darwin-x64@1.0.0, @napi-rs/canvas-linux-arm-gnueabihf@1.0.0, @napi-rs/canvas-linux-arm64-gnu@1.0.0, @napi-rs/canvas-linux-arm64-musl@1.0.0, @napi-rs/canvas-linux-riscv64-gnu@1.0.0, @napi-rs/canvas-linux-x64-gnu@1.0.0, @napi-rs/canvas-linux-x64-musl@1.0.0, @napi-rs/canvas-win32-arm64-msvc@1.0.0, @napi-rs/canvas-win32-x64-msvc@1.0.0

Evidence:
- [package.json](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_7ae45ad102eab3b6.json`
- [.github/workflows/libcxxabi.yml](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/.github/workflows/libcxxabi.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_fa8e3a254c8819da.json`
- [.github/workflows/CI.yaml](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/.github/workflows/CI.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_b268bb7dc66e8638.json`
- [yarn.lock](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_51e4f558fae53465.json`
- [.github/workflows/skia.yaml](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/.github/workflows/skia.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_a0ee1d62aff37df2.json`
- [.github/workflows/docker.yml](https://github.com/brooooooklyn/canvas/blob/bf0052671d7dfd998456eec0e1ac305fa9879dd1/.github/workflows/docker.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A034__file_3f5366f6d6df3ec1.json`

## A035 — d3/d3-zoom

Commit: `c8df708b78b46553bc4a0fbf1baf4ffc10cef8bd`.
Original package/version mappings: d3-zoom@3.0.0

Evidence:
- [.github/workflows/node.js.yml](https://github.com/d3/d3-zoom/blob/c8df708b78b46553bc4a0fbf1baf4ffc10cef8bd/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A035__file_014228303dff9a1a.json`
- [package.json](https://github.com/d3/d3-zoom/blob/c8df708b78b46553bc4a0fbf1baf4ffc10cef8bd/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A035__file_7ae45ad102eab3b6.json`
- [yarn.lock](https://github.com/d3/d3-zoom/blob/c8df708b78b46553bc4a0fbf1baf4ffc10cef8bd/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A035__file_51e4f558fae53465.json`

## A036 — developit/web-worker

Commit: `9d20474a7d7cefa98add3d59dba8293f01ab70bc`.
Original package/version mappings: web-worker@1.5.0

Evidence:
- [.github/workflows/main.yml](https://github.com/developit/web-worker/blob/9d20474a7d7cefa98add3d59dba8293f01ab70bc/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A036__file_7829468e86c1cc5d.json`
- [package-lock.json](https://github.com/developit/web-worker/blob/9d20474a7d7cefa98add3d59dba8293f01ab70bc/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A036__file_053150b640a7ce75.json`
- [package.json](https://github.com/developit/web-worker/blob/9d20474a7d7cefa98add3d59dba8293f01ab70bc/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A036__file_7ae45ad102eab3b6.json`

## A037 — dperini/nwsapi

Commit: `ee46926a7bcd7751dbd12abf35128d6c6e42bf56`.
Original package/version mappings: @asamuzakjp/nwsapi@2.3.9, nwsapi@2.2.24

Evidence:
- [.github/workflows/publish-npm.yml](https://github.com/dperini/nwsapi/blob/ee46926a7bcd7751dbd12abf35128d6c6e42bf56/.github/workflows/publish-npm.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A037__file_f089b0e55b389f53.json`
- [.github/workflows/ci.yml](https://github.com/dperini/nwsapi/blob/ee46926a7bcd7751dbd12abf35128d6c6e42bf56/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A037__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/dperini/nwsapi/blob/ee46926a7bcd7751dbd12abf35128d6c6e42bf56/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A037__file_7ae45ad102eab3b6.json`
- [.github/workflows/onboarding.yml](https://github.com/dperini/nwsapi/blob/ee46926a7bcd7751dbd12abf35128d6c6e42bf56/.github/workflows/onboarding.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A037__file_845c678cc76daad8.json`
- [package-lock.json](https://github.com/dperini/nwsapi/blob/ee46926a7bcd7751dbd12abf35128d6c6e42bf56/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A037__file_053150b640a7ce75.json`

## A038 — enisdenjo/graphql-ws

Commit: `7281f1b8f09637ab383c1aab4d14247d683bc15d`.
Original package/version mappings: graphql-ws@6.0.8

Evidence:
- [.github/workflows/test.yml](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_faff1af3d8ff4089.json`
- [package.json](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_7ae45ad102eab3b6.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_63bd641104d10e25.json`
- [.github/workflows/check.yml](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/.github/workflows/check.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_55f05888fd854d99.json`
- [yarn.lock](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_51e4f558fae53465.json`
- [.github/workflows/release.yml](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_87db21a973eed4fe.json`
- [.github/workflows/website.yml](https://github.com/enisdenjo/graphql-ws/blob/7281f1b8f09637ab383c1aab4d14247d683bc15d/.github/workflows/website.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A038__file_c7731b29de71fca2.json`

## A039 — gulpjs/parse-node-version

Commit: `17ee569c3809adab91a5228d6411d118864bce57`.
Original package/version mappings: parse-node-version@2.0.0

Evidence:
- [package-lock.json](https://github.com/gulpjs/parse-node-version/blob/17ee569c3809adab91a5228d6411d118864bce57/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A039__file_053150b640a7ce75.json`
- [.github/workflows/release.yml](https://github.com/gulpjs/parse-node-version/blob/17ee569c3809adab91a5228d6411d118864bce57/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A039__file_87db21a973eed4fe.json`
- [.github/workflows/dev.yml](https://github.com/gulpjs/parse-node-version/blob/17ee569c3809adab91a5228d6411d118864bce57/.github/workflows/dev.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A039__file_914da273e1d93625.json`
- [package.json](https://github.com/gulpjs/parse-node-version/blob/17ee569c3809adab91a5228d6411d118864bce57/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A039__file_7ae45ad102eab3b6.json`

## A040 — hilongjw/vue-lazyload

Commit: `0d9a95ee9a09d2f082f1226037ac3a895f97fade`.
Original package/version mappings: vue-lazyload@3.0.0

Evidence:
- [package.json](https://github.com/hilongjw/vue-lazyload/blob/0d9a95ee9a09d2f082f1226037ac3a895f97fade/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A040__file_7ae45ad102eab3b6.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/hilongjw/vue-lazyload/blob/0d9a95ee9a09d2f082f1226037ac3a895f97fade/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A040__file_63bd641104d10e25.json`

## A041 — httptoolkit/httpolyglot

Commit: `89064d5801caf500032461048ceb72884d40d0c4`.
Original package/version mappings: @httptoolkit/httpolyglot@3.1.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/httptoolkit/httpolyglot/blob/89064d5801caf500032461048ceb72884d40d0c4/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A041__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/httptoolkit/httpolyglot/blob/89064d5801caf500032461048ceb72884d40d0c4/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A041__file_7ae45ad102eab3b6.json`

## A042 — httptoolkit/read-tls-client-hello

Commit: `e67df7c043233534a56ac810168494c9c93b27ab`.
Original package/version mappings: read-tls-client-hello@2.0.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/httptoolkit/read-tls-client-hello/blob/e67df7c043233534a56ac810168494c9c93b27ab/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A042__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/httptoolkit/read-tls-client-hello/blob/e67df7c043233534a56ac810168494c9c93b27ab/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A042__file_7ae45ad102eab3b6.json`

## A043 — jaredhanson/passport

Commit: `217018dbc46dcd4118dd6f2c60c8d97010c587f8`.
Original package/version mappings: passport@0.7.0

Evidence:
- [.github/workflows/node.yml](https://github.com/jaredhanson/passport/blob/217018dbc46dcd4118dd6f2c60c8d97010c587f8/.github/workflows/node.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A043__file_4e88a8cc63d2540b.json`
- [package.json](https://github.com/jaredhanson/passport/blob/217018dbc46dcd4118dd6f2c60c8d97010c587f8/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A043__file_7ae45ad102eab3b6.json`

## A044 — joshstevens19/ethereum-bloom-filters

Commit: `d7235450fbe47e4a6213619b3be93ccb0b64ddbc`.
Original package/version mappings: ethereum-bloom-filters@1.2.0

Evidence:
- [.github/workflows/branch-check.yml](https://github.com/joshstevens19/ethereum-bloom-filters/blob/d7235450fbe47e4a6213619b3be93ccb0b64ddbc/.github/workflows/branch-check.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A044__file_a83d9f9ec8b1b07f.json`
- [package.json](https://github.com/joshstevens19/ethereum-bloom-filters/blob/d7235450fbe47e4a6213619b3be93ccb0b64ddbc/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A044__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/joshstevens19/ethereum-bloom-filters/blob/d7235450fbe47e4a6213619b3be93ccb0b64ddbc/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A044__file_053150b640a7ce75.json`
- [.github/workflows/pr-checks.yml](https://github.com/joshstevens19/ethereum-bloom-filters/blob/d7235450fbe47e4a6213619b3be93ccb0b64ddbc/.github/workflows/pr-checks.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A044__file_1da7a27709d11ac1.json`

## A045 — kcnarf/d3-weighted-voronoi

Commit: `1d3684d6292ea314b7a07a65506b363d45d83009`.
Original package/version mappings: d3-weighted-voronoi@1.1.3

Evidence:
- [yarn.lock](https://github.com/kcnarf/d3-weighted-voronoi/blob/1d3684d6292ea314b7a07a65506b363d45d83009/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A045__file_51e4f558fae53465.json`
- [.github/workflows/main.yml](https://github.com/kcnarf/d3-weighted-voronoi/blob/1d3684d6292ea314b7a07a65506b363d45d83009/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A045__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/kcnarf/d3-weighted-voronoi/blob/1d3684d6292ea314b7a07a65506b363d45d83009/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A045__file_7ae45ad102eab3b6.json`

## A046 — linusu/fs-temp

Commit: `cbda7828f686c3c6380bf494a49b974237bf0cd3`.
Original package/version mappings: fs-temp@2.0.1

Evidence:
- [package.json](https://github.com/linusu/fs-temp/blob/cbda7828f686c3c6380bf494a49b974237bf0cd3/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A046__file_7ae45ad102eab3b6.json`
- [.github/workflows/test.yml](https://github.com/linusu/fs-temp/blob/cbda7828f686c3c6380bf494a49b974237bf0cd3/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A046__file_faff1af3d8ff4089.json`

## A047 — matter-js/matter

Commit: `None`.
Original package/version mappings: @matter/general@0.17.2, @matter/main@0.17.2, @matter/model@0.17.2, @matter/node@0.17.2, @matter/nodejs@0.17.2, @matter/protocol@0.17.2, @matter/types@0.17.2

Evidence:
- Acquisition unresolved; record unknown unless independently documented.

## A048 — mattiasbuelens/web-streams-polyfill

Commit: `e1199b926be1b2891a3db31527e7d4c7f83ca990`.
Original package/version mappings: web-streams-polyfill@4.3.0

Evidence:
- [package-lock.json](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_053150b640a7ce75.json`
- [package.json](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_7ae45ad102eab3b6.json`
- [.github/workflows/publish.yml](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_551d1fcf87f78cc3.json`
- [.github/workflows/changelog.yml](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/.github/workflows/changelog.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_a0aba5a2bd30b2f8.json`
- [.github/workflows/prepare-release.yml](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/.github/workflows/prepare-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_ddf2bab74923dcd4.json`
- [.github/workflows/test.yml](https://github.com/mattiasbuelens/web-streams-polyfill/blob/e1199b926be1b2891a3db31527e7d4c7f83ca990/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A048__file_faff1af3d8ff4089.json`

## A049 — multiformats/js-multiformats

Commit: `0dcd129adb06743d5005245c0e39631f13b86251`.
Original package/version mappings: multiformats@14.0.0

Evidence:
- [.github/workflows/semantic-pull-request.yml](https://github.com/multiformats/js-multiformats/blob/0dcd129adb06743d5005245c0e39631f13b86251/.github/workflows/semantic-pull-request.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A049__file_4b00edf4b36f281b.json`
- [.github/workflows/generated-pr.yml](https://github.com/multiformats/js-multiformats/blob/0dcd129adb06743d5005245c0e39631f13b86251/.github/workflows/generated-pr.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A049__file_c60814178801a234.json`
- [.github/workflows/stale.yml](https://github.com/multiformats/js-multiformats/blob/0dcd129adb06743d5005245c0e39631f13b86251/.github/workflows/stale.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A049__file_b5e0854ed0838024.json`
- [package.json](https://github.com/multiformats/js-multiformats/blob/0dcd129adb06743d5005245c0e39631f13b86251/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A049__file_7ae45ad102eab3b6.json`
- [.github/workflows/js-test-and-release.yml](https://github.com/multiformats/js-multiformats/blob/0dcd129adb06743d5005245c0e39631f13b86251/.github/workflows/js-test-and-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A049__file_e3eb95b1bd081edf.json`

## A050 — orchidjs/unicode-variants

Commit: `a395f53aa4763170636bee90d50b38f700f7c84a`.
Original package/version mappings: @orchidjs/unicode-variants@1.1.2

Evidence:
- [.github/workflows/publish.yml](https://github.com/orchidjs/unicode-variants/blob/a395f53aa4763170636bee90d50b38f700f7c84a/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A050__file_551d1fcf87f78cc3.json`
- [.github/workflows/ci.yaml](https://github.com/orchidjs/unicode-variants/blob/a395f53aa4763170636bee90d50b38f700f7c84a/.github/workflows/ci.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A050__file_944291df2c9c0635.json`
- [package-lock.json](https://github.com/orchidjs/unicode-variants/blob/a395f53aa4763170636bee90d50b38f700f7c84a/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A050__file_053150b640a7ce75.json`
- [package.json](https://github.com/orchidjs/unicode-variants/blob/a395f53aa4763170636bee90d50b38f700f7c84a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A050__file_7ae45ad102eab3b6.json`

## A051 — sindresorhus/md5-hex

Commit: `e16f78aa9aede5c99507241dafbc3cf5d9c4c89b`.
Original package/version mappings: md5-hex@5.0.0

Evidence:
- [.github/workflows/main.yml](https://github.com/sindresorhus/md5-hex/blob/e16f78aa9aede5c99507241dafbc3cf5d9c4c89b/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A051__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/sindresorhus/md5-hex/blob/e16f78aa9aede5c99507241dafbc3cf5d9c4c89b/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A051__file_7ae45ad102eab3b6.json`

## A052 — southpolesteve/node-abort-controller

Commit: `a0e10df97c446fdacc4d2911c42a8c403afff1fc`.
Original package/version mappings: node-abort-controller@3.1.1

Evidence:
- [package.json](https://github.com/southpolesteve/node-abort-controller/blob/a0e10df97c446fdacc4d2911c42a8c403afff1fc/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A052__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/southpolesteve/node-abort-controller/blob/a0e10df97c446fdacc4d2911c42a8c403afff1fc/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A052__file_053150b640a7ce75.json`
- [.github/workflows/test.yml](https://github.com/southpolesteve/node-abort-controller/blob/a0e10df97c446fdacc4d2911c42a8c403afff1fc/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A052__file_faff1af3d8ff4089.json`

## A053 — sveltejs/acorn-typescript

Commit: `5e2e70417f655a70c592b55590ac24f9c995fb11`.
Original package/version mappings: @sveltejs/acorn-typescript@1.0.10

Evidence:
- [.github/workflows/ci.yml](https://github.com/sveltejs/acorn-typescript/blob/5e2e70417f655a70c592b55590ac24f9c995fb11/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A053__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/sveltejs/acorn-typescript/blob/5e2e70417f655a70c592b55590ac24f9c995fb11/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A053__file_7ae45ad102eab3b6.json`
- [pnpm-lock.yaml](https://github.com/sveltejs/acorn-typescript/blob/5e2e70417f655a70c592b55590ac24f9c995fb11/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A053__file_32824c984905bb02.json`
- [.github/workflows/release.yml](https://github.com/sveltejs/acorn-typescript/blob/5e2e70417f655a70c592b55590ac24f9c995fb11/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A053__file_87db21a973eed4fe.json`

## A054 — syntax-tree/hast-util-embedded

Commit: `79c68d31fc7dd133c086a1a483583fbc02b48636`.
Original package/version mappings: hast-util-embedded@3.0.0

Evidence:
- [.github/workflows/main.yml](https://github.com/syntax-tree/hast-util-embedded/blob/79c68d31fc7dd133c086a1a483583fbc02b48636/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A054__file_7829468e86c1cc5d.json`
- [.github/workflows/bb.yml](https://github.com/syntax-tree/hast-util-embedded/blob/79c68d31fc7dd133c086a1a483583fbc02b48636/.github/workflows/bb.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A054__file_e2d60cb7c8f4e264.json`
- [package.json](https://github.com/syntax-tree/hast-util-embedded/blob/79c68d31fc7dd133c086a1a483583fbc02b48636/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A054__file_7ae45ad102eab3b6.json`

## A055 — syntax-tree/hast-util-to-text

Commit: `6aeca3a28f690c1bbcb656f20192ecd1ba04ad2a`.
Original package/version mappings: hast-util-to-text@4.0.2

Evidence:
- [.github/workflows/main.yml](https://github.com/syntax-tree/hast-util-to-text/blob/6aeca3a28f690c1bbcb656f20192ecd1ba04ad2a/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A055__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/syntax-tree/hast-util-to-text/blob/6aeca3a28f690c1bbcb656f20192ecd1ba04ad2a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A055__file_7ae45ad102eab3b6.json`
- [.github/workflows/bb.yml](https://github.com/syntax-tree/hast-util-to-text/blob/6aeca3a28f690c1bbcb656f20192ecd1ba04ad2a/.github/workflows/bb.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A055__file_e2d60cb7c8f4e264.json`

## A056 — tanstack/table

Commit: `c14e0221b1e656c7bb35e7b3d4cdf188719a3599`.
Original package/version mappings: @tanstack/match-sorter-utils@8.19.4, @tanstack/react-table@8.21.3, @tanstack/table-core@8.21.3, @tanstack/vue-table@8.21.3

Evidence:
- [package.json](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_7ae45ad102eab3b6.json`
- [.github/workflows/autofix.yml](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/.github/workflows/autofix.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_89b476612e9731e1.json`
- [.github/workflows/zizmor.yml](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/.github/workflows/zizmor.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_8e6408444d2bf2be.json`
- [.github/workflows/release.yml](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_87db21a973eed4fe.json`
- [packages/table-core/package.json](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/packages/table-core/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_f20e86b1209fa1ba.json`
- [.github/workflows/pr.yml](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/.github/workflows/pr.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_15c806aa50953819.json`
- [.github/workflows/check-skills.yml](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/.github/workflows/check-skills.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_d9408a8747edfb2e.json`
- [packages/react-table/package.json](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/packages/react-table/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_0d204b354affc6f5.json`
- [packages/vue-table/package.json](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/packages/vue-table/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_fdd506d1b3ad7dab.json`
- [packages/match-sorter-utils/package.json](https://github.com/tanstack/table/blob/c14e0221b1e656c7bb35e7b3d4cdf188719a3599/packages/match-sorter-utils/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A056__file_d46daf5747b72a8c.json`

## A057 — thlorenz/convert-source-map

Commit: `c65bc392d87ef6d18419593cfbe75fda81e2847b`.
Original package/version mappings: convert-source-map@2.0.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/thlorenz/convert-source-map/blob/c65bc392d87ef6d18419593cfbe75fda81e2847b/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A057__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/thlorenz/convert-source-map/blob/c65bc392d87ef6d18419593cfbe75fda81e2847b/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A057__file_7ae45ad102eab3b6.json`

## A058 — vercel/geist-font

Commit: `b5d164a0c066c2c9bfcd5ab65dd8244551f0ac06`.
Original package/version mappings: geist@1.7.2

Evidence:
- [.github/workflows/guard-prerelease.yaml](https://github.com/vercel/geist-font/blob/b5d164a0c066c2c9bfcd5ab65dd8244551f0ac06/.github/workflows/guard-prerelease.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A058__file_4d4d8363151a82be.json`
- [packages/next/package.json](https://github.com/vercel/geist-font/blob/b5d164a0c066c2c9bfcd5ab65dd8244551f0ac06/packages/next/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A058__file_9c1a3867443c5452.json`
- [.github/workflows/ci.yaml](https://github.com/vercel/geist-font/blob/b5d164a0c066c2c9bfcd5ab65dd8244551f0ac06/.github/workflows/ci.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A058__file_944291df2c9c0635.json`

## A059 — wooorm/stringify-entities

Commit: `69b10d61dfc27e59be57eb8a51ba7c1830451e90`.
Original package/version mappings: stringify-entities@4.0.4

Evidence:
- [package.json](https://github.com/wooorm/stringify-entities/blob/69b10d61dfc27e59be57eb8a51ba7c1830451e90/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A059__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/wooorm/stringify-entities/blob/69b10d61dfc27e59be57eb8a51ba7c1830451e90/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A059__file_7829468e86c1cc5d.json`

## A060 — zachleat/esm-import-transformer

Commit: `5a25755538b243641ee5cee38b64a4794c2ba933`.
Original package/version mappings: esm-import-transformer@3.0.5

Evidence:
- [.github/workflows/ci.yml](https://github.com/zachleat/esm-import-transformer/blob/5a25755538b243641ee5cee38b64a4794c2ba933/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A060__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/zachleat/esm-import-transformer/blob/5a25755538b243641ee5cee38b64a4794c2ba933/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A060__file_7ae45ad102eab3b6.json`

## A061 — airbnb/react-with-styles

Commit: `68100eecd92ab5bbe3dff25cc454cbe137ef4f05`.
Original package/version mappings: react-with-styles@5.0.0

Evidence:
- [package.json](https://github.com/airbnb/react-with-styles/blob/68100eecd92ab5bbe3dff25cc454cbe137ef4f05/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A061__file_7ae45ad102eab3b6.json`
- [.github/workflows/node-pretest.yml](https://github.com/airbnb/react-with-styles/blob/68100eecd92ab5bbe3dff25cc454cbe137ef4f05/.github/workflows/node-pretest.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A061__file_f618bae3eaba832e.json`
- [.github/workflows/rebase.yml](https://github.com/airbnb/react-with-styles/blob/68100eecd92ab5bbe3dff25cc454cbe137ef4f05/.github/workflows/rebase.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A061__file_63e050857aa8769f.json`
- [.github/workflows/node.yml](https://github.com/airbnb/react-with-styles/blob/68100eecd92ab5bbe3dff25cc454cbe137ef4f05/.github/workflows/node.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A061__file_4e88a8cc63d2540b.json`
- [.github/workflows/require-allow-edits.yml](https://github.com/airbnb/react-with-styles/blob/68100eecd92ab5bbe3dff25cc454cbe137ef4f05/.github/workflows/require-allow-edits.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A061__file_26951abb3a963d5a.json`

## A062 — archiverjs/node-compress-commons

Commit: `28f1a732a832dd40f4e6549975679366276eabdf`.
Original package/version mappings: compress-commons@7.0.1

Evidence:
- [.github/workflows/release-drafter.yml](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/.github/workflows/release-drafter.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_6942706d71f70018.json`
- [package.json](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_7ae45ad102eab3b6.json`
- [.github/workflows/npmpublish.yml](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/.github/workflows/npmpublish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_982aa7638644ab23.json`
- [.github/workflows/labels.yml](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/.github/workflows/labels.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_09793c303182c720.json`
- [.github/workflows/nodejs.yml](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_e98936aa52a6dd74.json`
- [package-lock.json](https://github.com/archiverjs/node-compress-commons/blob/28f1a732a832dd40f4e6549975679366276eabdf/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A062__file_053150b640a7ce75.json`

## A063 — berkmann18/json-fixer

Commit: `f6bfe63c90a26589edc9c136df7d4212049668af`.
Original package/version mappings: json-fixer@1.6.15

Evidence:
- [package-lock.json](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_053150b640a7ce75.json`
- [package.json](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_7ae45ad102eab3b6.json`
- [.github/workflows/nodejs.yml](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_e98936aa52a6dd74.json`
- [.github/workflows/snyk.yml](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/.github/workflows/snyk.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_279a5a5997dd6e7a.json`
- [.github/workflows/semantic-pr.yml](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/.github/workflows/semantic-pr.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_b461a4aae3e02f4e.json`
- [.github/workflows/semantic-release.yml](https://github.com/berkmann18/json-fixer/blob/f6bfe63c90a26589edc9c136df7d4212049668af/.github/workflows/semantic-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A063__file_ea3710a52b3ef06a.json`

## A064 — bevry/istextorbinary

Commit: `3ba79905cef46d374567bb7280ef1adc7e44b78d`.
Original package/version mappings: istextorbinary@9.5.0

Evidence:
- [.github/workflows/bevry.yml](https://github.com/bevry/istextorbinary/blob/3ba79905cef46d374567bb7280ef1adc7e44b78d/.github/workflows/bevry.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A064__file_815ee3ab2255855e.json`
- [package.json](https://github.com/bevry/istextorbinary/blob/3ba79905cef46d374567bb7280ef1adc7e44b78d/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A064__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/bevry/istextorbinary/blob/3ba79905cef46d374567bb7280ef1adc7e44b78d/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A064__file_053150b640a7ce75.json`

## A065 — bevry/safefs

Commit: `5f5b4140607a90b8ff722fa8fd251f49091bbafc`.
Original package/version mappings: safefs@8.10.0

Evidence:
- [.github/workflows/bevry.yml](https://github.com/bevry/safefs/blob/5f5b4140607a90b8ff722fa8fd251f49091bbafc/.github/workflows/bevry.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A065__file_815ee3ab2255855e.json`
- [package.json](https://github.com/bevry/safefs/blob/5f5b4140607a90b8ff722fa8fd251f49091bbafc/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A065__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/bevry/safefs/blob/5f5b4140607a90b8ff722fa8fd251f49091bbafc/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A065__file_053150b640a7ce75.json`

## A066 — deepgram/deepgram-js-sdk

Commit: `d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c`.
Original package/version mappings: @deepgram/sdk@5.4.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_b803fcb7f17ed923.json`
- [.github/workflows/release-please.yml](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/.github/workflows/release-please.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_2c84033033d49186.json`
- [pnpm-lock.yaml](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_32824c984905bb02.json`
- [.github/workflows/context7.yml](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/.github/workflows/context7.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_24701bff4383cb99.json`
- [.github/workflows/pr-title-check.yml](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/.github/workflows/pr-title-check.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_74c9ec5ec6d2baa9.json`
- [package.json](https://github.com/deepgram/deepgram-js-sdk/blob/d521639a80b9e7af6ebf4f74ac9dd5ac18c9a79c/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A066__file_7ae45ad102eab3b6.json`

## A067 — emmatown/sembear

Commit: `5a413f1cab2650357b43ba580fe319f8fea113c5`.
Original package/version mappings: sembear@0.7.0

Evidence:
- [.github/workflows/main.yml](https://github.com/emmatown/sembear/blob/5a413f1cab2650357b43ba580fe319f8fea113c5/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A067__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/emmatown/sembear/blob/5a413f1cab2650357b43ba580fe319f8fea113c5/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A067__file_7ae45ad102eab3b6.json`
- [yarn.lock](https://github.com/emmatown/sembear/blob/5a413f1cab2650357b43ba580fe319f8fea113c5/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A067__file_51e4f558fae53465.json`

## A068 — fastify/fast-json-stringify

Commit: `968bf202868005077f535129262d7ce094d231aa`.
Original package/version mappings: fast-json-stringify@7.0.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/fastify/fast-json-stringify/blob/968bf202868005077f535129262d7ce094d231aa/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A068__file_b803fcb7f17ed923.json`
- [.github/workflows/lock-threads.yml](https://github.com/fastify/fast-json-stringify/blob/968bf202868005077f535129262d7ce094d231aa/.github/workflows/lock-threads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A068__file_46c2f09fa03ea1b7.json`
- [package.json](https://github.com/fastify/fast-json-stringify/blob/968bf202868005077f535129262d7ce094d231aa/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A068__file_7ae45ad102eab3b6.json`
- [.github/workflows/release.yml](https://github.com/fastify/fast-json-stringify/blob/968bf202868005077f535129262d7ce094d231aa/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A068__file_87db21a973eed4fe.json`

## A069 — fastify/fast-uri

Commit: `00f41407ef64b4944060ca3e7fd2d637916a71ea`.
Original package/version mappings: fast-uri@4.0.0

Evidence:
- [.github/workflows/ossf-scorecard.yml](https://github.com/fastify/fast-uri/blob/00f41407ef64b4944060ca3e7fd2d637916a71ea/.github/workflows/ossf-scorecard.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A069__file_0f32dffa00fbb4b5.json`
- [.github/workflows/release.yml](https://github.com/fastify/fast-uri/blob/00f41407ef64b4944060ca3e7fd2d637916a71ea/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A069__file_87db21a973eed4fe.json`
- [.github/workflows/lock-threads.yml](https://github.com/fastify/fast-uri/blob/00f41407ef64b4944060ca3e7fd2d637916a71ea/.github/workflows/lock-threads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A069__file_46c2f09fa03ea1b7.json`
- [.github/workflows/ci.yml](https://github.com/fastify/fast-uri/blob/00f41407ef64b4944060ca3e7fd2d637916a71ea/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A069__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/fastify/fast-uri/blob/00f41407ef64b4944060ca3e7fd2d637916a71ea/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A069__file_7ae45ad102eab3b6.json`

## A070 — goatandsheep/react-native-dotenv

Commit: `None`.
Original package/version mappings: react-native-dotenv@3.4.11

Evidence:
- Acquisition unresolved; record unknown unless independently documented.

## A071 — isaacs/prismjs-terminal

Commit: `182e9c3ea81136c73d7c700d471bec6d52f1f398`.
Original package/version mappings: prismjs-terminal@1.2.4

Evidence:
- [package-lock.json](https://github.com/isaacs/prismjs-terminal/blob/182e9c3ea81136c73d7c700d471bec6d52f1f398/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A071__file_053150b640a7ce75.json`
- [.github/workflows/typedoc.yml](https://github.com/isaacs/prismjs-terminal/blob/182e9c3ea81136c73d7c700d471bec6d52f1f398/.github/workflows/typedoc.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A071__file_cb5da8b92071f0cd.json`
- [.github/workflows/ci.yml](https://github.com/isaacs/prismjs-terminal/blob/182e9c3ea81136c73d7c700d471bec6d52f1f398/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A071__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/isaacs/prismjs-terminal/blob/182e9c3ea81136c73d7c700d471bec6d52f1f398/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A071__file_7ae45ad102eab3b6.json`

## A072 — jsdom/html-encoding-sniffer

Commit: `b3e1a74ac48df34369a93ad87507147e9531d1d0`.
Original package/version mappings: html-encoding-sniffer@6.0.0

Evidence:
- [.github/workflows/build.yml](https://github.com/jsdom/html-encoding-sniffer/blob/b3e1a74ac48df34369a93ad87507147e9531d1d0/.github/workflows/build.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A072__file_5c3fa597431eda03.json`
- [package-lock.json](https://github.com/jsdom/html-encoding-sniffer/blob/b3e1a74ac48df34369a93ad87507147e9531d1d0/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A072__file_053150b640a7ce75.json`
- [package.json](https://github.com/jsdom/html-encoding-sniffer/blob/b3e1a74ac48df34369a93ad87507147e9531d1d0/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A072__file_7ae45ad102eab3b6.json`
- [.github/workflows/publish.yml](https://github.com/jsdom/html-encoding-sniffer/blob/b3e1a74ac48df34369a93ad87507147e9531d1d0/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A072__file_551d1fcf87f78cc3.json`

## A073 — jwtk/njwt

Commit: `ec9483b6eec1150d56f772ddd308c2bbdf2f98f4`.
Original package/version mappings: njwt@2.0.1

Evidence:
- [package-lock.json](https://github.com/jwtk/njwt/blob/ec9483b6eec1150d56f772ddd308c2bbdf2f98f4/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A073__file_053150b640a7ce75.json`
- [.github/workflows/main.yml](https://github.com/jwtk/njwt/blob/ec9483b6eec1150d56f772ddd308c2bbdf2f98f4/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A073__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/jwtk/njwt/blob/ec9483b6eec1150d56f772ddd308c2bbdf2f98f4/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A073__file_7ae45ad102eab3b6.json`

## A074 — ljharb/json-stable-stringify

Commit: `547244f61dc04b77a90d4c627a079ae5a9ace138`.
Original package/version mappings: json-stable-stringify@1.3.0

Evidence:
- [.github/workflows/rebase.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/rebase.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_63e050857aa8769f.json`
- [.github/workflows/require-allow-edits.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/require-allow-edits.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_26951abb3a963d5a.json`
- [.github/workflows/node-tens.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/node-tens.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_ad181dc539e4f666.json`
- [.github/workflows/node-pretest.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/node-pretest.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_f618bae3eaba832e.json`
- [package.json](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_7ae45ad102eab3b6.json`
- [.github/workflows/node-twenties.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/node-twenties.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_d7df1eed5a3668f7.json`
- [.github/workflows/node-aught.yml](https://github.com/ljharb/json-stable-stringify/blob/547244f61dc04b77a90d4c627a079ae5a9ace138/.github/workflows/node-aught.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A074__file_90566430f80b1c64.json`

## A075 — ljharb/side-channel

Commit: `3d260956bc92a85f140352bd814dc5c9d31fc65a`.
Original package/version mappings: side-channel@1.1.1

Evidence:
- [.github/workflows/node-twenties.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/node-twenties.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_d7df1eed5a3668f7.json`
- [.github/workflows/node-pretest.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/node-pretest.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_f618bae3eaba832e.json`
- [.github/workflows/node-aught.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/node-aught.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_90566430f80b1c64.json`
- [package.json](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_7ae45ad102eab3b6.json`
- [.github/workflows/require-allow-edits.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/require-allow-edits.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_26951abb3a963d5a.json`
- [.github/workflows/rebase.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/rebase.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_63e050857aa8769f.json`
- [.github/workflows/node-tens.yml](https://github.com/ljharb/side-channel/blob/3d260956bc92a85f140352bd814dc5c9d31fc65a/.github/workflows/node-tens.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A075__file_ad181dc539e4f666.json`

## A076 — mathjax/mathjax-src

Commit: `fb987178c2d279a99b0db5ea02e751691703955e`.
Original package/version mappings: mathjax-full@3.2.2

Evidence:
- [.github/workflows/test.yml](https://github.com/mathjax/mathjax-src/blob/fb987178c2d279a99b0db5ea02e751691703955e/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A076__file_faff1af3d8ff4089.json`
- [.github/workflows/publish.yml](https://github.com/mathjax/mathjax-src/blob/fb987178c2d279a99b0db5ea02e751691703955e/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A076__file_551d1fcf87f78cc3.json`
- [pnpm-lock.yaml](https://github.com/mathjax/mathjax-src/blob/fb987178c2d279a99b0db5ea02e751691703955e/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A076__file_32824c984905bb02.json`
- [.github/workflows/docs.yml](https://github.com/mathjax/mathjax-src/blob/fb987178c2d279a99b0db5ea02e751691703955e/.github/workflows/docs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A076__file_9cf2000c53760d83.json`
- [package.json](https://github.com/mathjax/mathjax-src/blob/fb987178c2d279a99b0db5ea02e751691703955e/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A076__file_7ae45ad102eab3b6.json`

## A077 — mozilla/hawk

Commit: `ed7c3d8a624ec97cda91c3b52433714fc2433eaf`.
Original package/version mappings: hawk@9.0.2

Evidence:
- [.github/workflows/codeql-analysis.yml](https://github.com/mozilla/hawk/blob/ed7c3d8a624ec97cda91c3b52433714fc2433eaf/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A077__file_63bd641104d10e25.json`
- [package.json](https://github.com/mozilla/hawk/blob/ed7c3d8a624ec97cda91c3b52433714fc2433eaf/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A077__file_7ae45ad102eab3b6.json`

## A078 — node-modules/get-ready

Commit: `528b1bbce44c5c97ab5596d333a8165795de8f0c`.
Original package/version mappings: get-ready@3.4.0

Evidence:
- [.github/workflows/pkg.pr.new.yml](https://github.com/node-modules/get-ready/blob/528b1bbce44c5c97ab5596d333a8165795de8f0c/.github/workflows/pkg.pr.new.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A078__file_9d547244c7ba3708.json`
- [package.json](https://github.com/node-modules/get-ready/blob/528b1bbce44c5c97ab5596d333a8165795de8f0c/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A078__file_7ae45ad102eab3b6.json`
- [.github/workflows/nodejs.yml](https://github.com/node-modules/get-ready/blob/528b1bbce44c5c97ab5596d333a8165795de8f0c/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A078__file_e98936aa52a6dd74.json`
- [.github/workflows/release.yml](https://github.com/node-modules/get-ready/blob/528b1bbce44c5c97ab5596d333a8165795de8f0c/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A078__file_87db21a973eed4fe.json`

## A079 — polkadot-js/wasm

Commit: `65286fb3ecacf8b3a1fa4a60b265f861f5a32eef`.
Original package/version mappings: @polkadot/wasm-bridge@7.5.4, @polkadot/wasm-crypto@7.5.4, @polkadot/wasm-crypto-asmjs@7.5.4, @polkadot/wasm-crypto-init@7.5.4, @polkadot/wasm-crypto-wasm@7.5.4, @polkadot/wasm-util@7.5.4

Evidence:
- [packages/wasm-bridge/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-bridge/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_bc8204584a84a42d.json`
- [yarn.lock](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_51e4f558fae53465.json`
- [.github/workflows/lock.yml](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/.github/workflows/lock.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_d53fada4c18b028e.json`
- [package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_7ae45ad102eab3b6.json`
- [packages/wasm-crypto/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-crypto/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_39dd1edcc1b52fcd.json`
- [.github/workflows/push-master.yml](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/.github/workflows/push-master.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_8b1dff209b15d207.json`
- [packages/wasm-crypto-init/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-crypto-init/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_a48fe11fa1d4bf78.json`
- [.github/workflows/pr-any.yml](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/.github/workflows/pr-any.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_ffaa2de7b784327b.json`
- [.github/workflows/auto-merge.yml](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/.github/workflows/auto-merge.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_9e68ee04621d1e0e.json`
- [packages/wasm-crypto-asmjs/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-crypto-asmjs/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_0f0d1082daef24aa.json`
- [packages/wasm-util/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-util/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_0aea73d5d1e41abb.json`
- [packages/wasm-crypto-wasm/package.json](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/packages/wasm-crypto-wasm/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_89f126bf792f49b6.json`
- [.github/workflows/auto-approve.yml](https://github.com/polkadot-js/wasm/blob/65286fb3ecacf8b3a1fa4a60b265f861f5a32eef/.github/workflows/auto-approve.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A079__file_283c890e639e6172.json`

## A080 — portabletext/to-html

Commit: `1dec622022b85b10865774f3e7d98babb66ba550`.
Original package/version mappings: @portabletext/to-html@5.0.2

Evidence:
- [pnpm-lock.yaml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_32824c984905bb02.json`
- [.github/workflows/format-if-needed.yml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/.github/workflows/format-if-needed.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_9081e470dec7c9fa.json`
- [.github/workflows/deploy.yml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/.github/workflows/deploy.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_28802fbf11c83a2e.json`
- [.github/workflows/main.yml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_7829468e86c1cc5d.json`
- [package.json](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_7ae45ad102eab3b6.json`
- [.github/workflows/release.yml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_87db21a973eed4fe.json`
- [.github/workflows/renovate.yml](https://github.com/portabletext/to-html/blob/1dec622022b85b10865774f3e7d98babb66ba550/.github/workflows/renovate.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A080__file_2f2dcee4f3f279ea.json`

## A081 — preactjs/preact-render-to-string

Commit: `dc7d06b07a2e65322a311fafb9642c8802575b7a`.
Original package/version mappings: preact-render-to-string@6.7.0

Evidence:
- [package-lock.json](https://github.com/preactjs/preact-render-to-string/blob/dc7d06b07a2e65322a311fafb9642c8802575b7a/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A081__file_053150b640a7ce75.json`
- [package.json](https://github.com/preactjs/preact-render-to-string/blob/dc7d06b07a2e65322a311fafb9642c8802575b7a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A081__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci.yml](https://github.com/preactjs/preact-render-to-string/blob/dc7d06b07a2e65322a311fafb9642c8802575b7a/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A081__file_b803fcb7f17ed923.json`
- [.github/workflows/release.yml](https://github.com/preactjs/preact-render-to-string/blob/dc7d06b07a2e65322a311fafb9642c8802575b7a/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A081__file_87db21a973eed4fe.json`

## A082 — remarkablemark/html-react-parser

Commit: `90970fd0a7859a169fa7889dbc5d9efe2c9c7de1`.
Original package/version mappings: html-react-parser@6.1.3

Evidence:
- [.github/workflows/scorecard.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/scorecard.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_2e3112f4e81a9c47.json`
- [.github/workflows/release-please.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/release-please.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_2c84033033d49186.json`
- [.github/workflows/test.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_faff1af3d8ff4089.json`
- [.github/workflows/build.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/build.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_5c3fa597431eda03.json`
- [.github/workflows/lint.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/lint.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_107e910e9f2ebfb9.json`
- [.github/workflows/size-limit.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/size-limit.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_0e6e5ca89e96a26e.json`
- [package-lock.json](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_053150b640a7ce75.json`
- [package.json](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_7ae45ad102eab3b6.json`
- [.github/workflows/commitlint.yml](https://github.com/remarkablemark/html-react-parser/blob/90970fd0a7859a169fa7889dbc5d9efe2c9c7de1/.github/workflows/commitlint.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A082__file_6afdd3d5a5b90ed7.json`

## A083 — remarkjs/remark-retext

Commit: `fc2d264ccee621e24074da0de655ceff6be7f1bc`.
Original package/version mappings: remark-retext@6.0.1

Evidence:
- [.github/workflows/main.yml](https://github.com/remarkjs/remark-retext/blob/fc2d264ccee621e24074da0de655ceff6be7f1bc/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A083__file_7829468e86c1cc5d.json`
- [.github/workflows/bb.yml](https://github.com/remarkjs/remark-retext/blob/fc2d264ccee621e24074da0de655ceff6be7f1bc/.github/workflows/bb.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A083__file_e2d60cb7c8f4e264.json`
- [package.json](https://github.com/remarkjs/remark-retext/blob/fc2d264ccee621e24074da0de655ceff6be7f1bc/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A083__file_7ae45ad102eab3b6.json`

## A084 — retextjs/retext-diacritics

Commit: `ae0eeff28653fdd4b890291f5748f75fe06b6f7a`.
Original package/version mappings: retext-diacritics@5.0.0

Evidence:
- [package.json](https://github.com/retextjs/retext-diacritics/blob/ae0eeff28653fdd4b890291f5748f75fe06b6f7a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A084__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/retextjs/retext-diacritics/blob/ae0eeff28653fdd4b890291f5748f75fe06b6f7a/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A084__file_7829468e86c1cc5d.json`
- [.github/workflows/bb.yml](https://github.com/retextjs/retext-diacritics/blob/ae0eeff28653fdd4b890291f5748f75fe06b6f7a/.github/workflows/bb.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A084__file_e2d60cb7c8f4e264.json`

## A085 — rich-harris/sorcery

Commit: `f3d28054ca7744ea34b01785713860288489d1b5`.
Original package/version mappings: sorcery@1.0.0

Evidence:
- [package.json](https://github.com/rich-harris/sorcery/blob/f3d28054ca7744ea34b01785713860288489d1b5/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A085__file_7ae45ad102eab3b6.json`
- [pnpm-lock.yaml](https://github.com/rich-harris/sorcery/blob/f3d28054ca7744ea34b01785713860288489d1b5/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A085__file_32824c984905bb02.json`
- [.github/workflows/ci.yml](https://github.com/rich-harris/sorcery/blob/f3d28054ca7744ea34b01785713860288489d1b5/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A085__file_b803fcb7f17ed923.json`

## A086 — sindresorhus/cli-truncate

Commit: `0dac9fe1ac7ad9d93a3186c8552f806c7926f24f`.
Original package/version mappings: cli-truncate@6.0.0

Evidence:
- [package.json](https://github.com/sindresorhus/cli-truncate/blob/0dac9fe1ac7ad9d93a3186c8552f806c7926f24f/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A086__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/sindresorhus/cli-truncate/blob/0dac9fe1ac7ad9d93a3186c8552f806c7926f24f/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A086__file_7829468e86c1cc5d.json`

## A087 — stdlib-js/array-int16

Commit: `6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba`.
Original package/version mappings: @stdlib/array-int16@0.2.3

Evidence:
- [.github/workflows/cancel.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/cancel.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_2d26dd5833955d0d.json`
- [.github/workflows/examples.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/examples.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_8906835152921ef9.json`
- [.github/workflows/close_pull_requests.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/close_pull_requests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_c2534226e5caf507.json`
- [.github/workflows/npm_downloads.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/npm_downloads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_1fe260de46339e7e.json`
- [.github/workflows/test_published_package.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/test_published_package.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_079490fa1829e381.json`
- [package.json](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_7ae45ad102eab3b6.json`
- [.github/workflows/productionize.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/productionize.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_930e2da5f5534327.json`
- [.github/workflows/test_install.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/test_install.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_1b9d64a0720ac550.json`
- [.github/workflows/test.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_faff1af3d8ff4089.json`
- [.github/workflows/benchmark.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/benchmark.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_aacbd0338bcf5989.json`
- [.github/workflows/test_coverage.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/test_coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_f0a9c26e26715ff4.json`
- [.github/workflows/test_bundles.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/test_bundles.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_5e991fbea792b8a6.json`
- [.github/workflows/publish.yml](https://github.com/stdlib-js/array-int16/blob/6e7bb1df3ee2efe3d2a396e6f1e2f7c6fd3da7ba/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A087__file_551d1fcf87f78cc3.json`

## A088 — syntax-tree/unist-util-find

Commit: `4dbadee35fa572fbc10eda1aed85e81768135fe0`.
Original package/version mappings: unist-util-find@3.0.0

Evidence:
- [package.json](https://github.com/syntax-tree/unist-util-find/blob/4dbadee35fa572fbc10eda1aed85e81768135fe0/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A088__file_7ae45ad102eab3b6.json`
- [.github/workflows/main.yml](https://github.com/syntax-tree/unist-util-find/blob/4dbadee35fa572fbc10eda1aed85e81768135fe0/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A088__file_7829468e86c1cc5d.json`
- [.github/workflows/bb.yml](https://github.com/syntax-tree/unist-util-find/blob/4dbadee35fa572fbc10eda1aed85e81768135fe0/.github/workflows/bb.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A088__file_e2d60cb7c8f4e264.json`

## A089 — thlorenz/anchor-markdown-header

Commit: `8da01b01d2fffa48574efc17a99067539f16b998`.
Original package/version mappings: anchor-markdown-header@0.8.4

Evidence:
- [.github/workflows/node.js.yml](https://github.com/thlorenz/anchor-markdown-header/blob/8da01b01d2fffa48574efc17a99067539f16b998/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A089__file_014228303dff9a1a.json`
- [package.json](https://github.com/thlorenz/anchor-markdown-header/blob/8da01b01d2fffa48574efc17a99067539f16b998/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A089__file_7ae45ad102eab3b6.json`
- [.github/workflows/release.yaml](https://github.com/thlorenz/anchor-markdown-header/blob/8da01b01d2fffa48574efc17a99067539f16b998/.github/workflows/release.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A089__file_e426ed4584283702.json`
- [package-lock.json](https://github.com/thlorenz/anchor-markdown-header/blob/8da01b01d2fffa48574efc17a99067539f16b998/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A089__file_053150b640a7ce75.json`

## A090 — vercel/serve-handler

Commit: `ead85eb0819cde32eed2bc5726ff6c8ac895f975`.
Original package/version mappings: serve-handler@6.1.7

Evidence:
- [.github/workflows/publish.yaml](https://github.com/vercel/serve-handler/blob/ead85eb0819cde32eed2bc5726ff6c8ac895f975/.github/workflows/publish.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A090__file_e81e13daadd1745d.json`
- [.github/workflows/tests.yaml](https://github.com/vercel/serve-handler/blob/ead85eb0819cde32eed2bc5726ff6c8ac895f975/.github/workflows/tests.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A090__file_95557d53bf91069e.json`
- [yarn.lock](https://github.com/vercel/serve-handler/blob/ead85eb0819cde32eed2bc5726ff6c8ac895f975/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A090__file_51e4f558fae53465.json`
- [package.json](https://github.com/vercel/serve-handler/blob/ead85eb0819cde32eed2bc5726ff6c8ac895f975/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A090__file_7ae45ad102eab3b6.json`

## A091 — alfredosalzillo/rollup-plugin-multi-input

Commit: `f12ec1c1f401d1a33bd167b9f36a2bad74e7c2c3`.
Original package/version mappings: rollup-plugin-multi-input@1.9.0

Evidence:
- [.github/workflows/CI.yml](https://github.com/alfredosalzillo/rollup-plugin-multi-input/blob/f12ec1c1f401d1a33bd167b9f36a2bad74e7c2c3/.github/workflows/CI.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A091__file_3ab46ee209a12747.json`
- [package.json](https://github.com/alfredosalzillo/rollup-plugin-multi-input/blob/f12ec1c1f401d1a33bd167b9f36a2bad74e7c2c3/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A091__file_7ae45ad102eab3b6.json`
- [.github/workflows/CD.yml](https://github.com/alfredosalzillo/rollup-plugin-multi-input/blob/f12ec1c1f401d1a33bd167b9f36a2bad74e7c2c3/.github/workflows/CD.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A091__file_a64cbb6e953e697c.json`
- [package-lock.json](https://github.com/alfredosalzillo/rollup-plugin-multi-input/blob/f12ec1c1f401d1a33bd167b9f36a2bad74e7c2c3/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A091__file_053150b640a7ce75.json`

## A092 — alibaba/ice

Commit: `2742ac4678781ee982bc4cdb428457b36163b6b5`.
Original package/version mappings: @builder/app-helpers@2.5.4, @builder/babel-preset-ice@1.0.2, @ice/screenshot@0.1.9, build-plugin-fusion@0.1.23, build-plugin-moment-locales@0.1.3, build-scripts-config@3.0.3, webpack-plugin-import@0.3.0

Evidence:
- [.github/workflows/canary.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/canary.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_4b56c7c159ef6d18.json`
- [package.json](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_b803fcb7f17ed923.json`
- [.github/workflows/version.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/version.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_fd17c77905dbf19e.json`
- [.github/workflows/website.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/website.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_c7731b29de71fca2.json`
- [.github/workflows/coverage.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_a2115d277b5ca5a2.json`
- [pnpm-lock.yaml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_32824c984905bb02.json`
- [.github/workflows/release.yml](https://github.com/alibaba/ice/blob/2742ac4678781ee982bc4cdb428457b36163b6b5/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A092__file_87db21a973eed4fe.json`

## A093 — anncwb/vite-plugin-svg-icons

Commit: `None`.
Original package/version mappings: vite-plugin-svg-icons@2.0.1

Evidence:
- Acquisition unresolved; record unknown unless independently documented.

## A094 — bahmutov/start-server-and-test

Commit: `7f129c354ee4a44e42c8404063bb75b675a1a220`.
Original package/version mappings: start-server-and-test@3.0.11

Evidence:
- [package-lock.json](https://github.com/bahmutov/start-server-and-test/blob/7f129c354ee4a44e42c8404063bb75b675a1a220/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A094__file_053150b640a7ce75.json`
- [.github/workflows/ci.yml](https://github.com/bahmutov/start-server-and-test/blob/7f129c354ee4a44e42c8404063bb75b675a1a220/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A094__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/bahmutov/start-server-and-test/blob/7f129c354ee4a44e42c8404063bb75b675a1a220/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A094__file_7ae45ad102eab3b6.json`

## A095 — cfware/babel-plugin-template-html-minifier

Commit: `47ed74197b969ae26b079549a1ef57e7694c00e6`.
Original package/version mappings: babel-plugin-template-html-minifier@4.1.0

Evidence:
- [.github/workflows/test.yml](https://github.com/cfware/babel-plugin-template-html-minifier/blob/47ed74197b969ae26b079549a1ef57e7694c00e6/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A095__file_faff1af3d8ff4089.json`
- [package.json](https://github.com/cfware/babel-plugin-template-html-minifier/blob/47ed74197b969ae26b079549a1ef57e7694c00e6/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A095__file_7ae45ad102eab3b6.json`

## A096 — chadkillingsworth/closure-compiler-npm

Commit: `2d1e648c1a1c7e02180ef85cd260fc35ce434d1d`.
Original package/version mappings: google-closure-compiler@20260610.0.0, google-closure-compiler-java@20260614.0.0, google-closure-compiler-linux@20260614.0.0, google-closure-compiler-linux-arm64@20260614.0.0, google-closure-compiler-macos@20260614.0.0, google-closure-compiler-windows@20260614.0.0

Evidence:
- [yarn.lock](https://github.com/chadkillingsworth/closure-compiler-npm/blob/2d1e648c1a1c7e02180ef85cd260fc35ce434d1d/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A096__file_51e4f558fae53465.json`
- [.github/workflows/release.yml](https://github.com/chadkillingsworth/closure-compiler-npm/blob/2d1e648c1a1c7e02180ef85cd260fc35ce434d1d/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A096__file_87db21a973eed4fe.json`
- [package.json](https://github.com/chadkillingsworth/closure-compiler-npm/blob/2d1e648c1a1c7e02180ef85cd260fc35ce434d1d/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A096__file_7ae45ad102eab3b6.json`
- [.github/workflows/build.yml](https://github.com/chadkillingsworth/closure-compiler-npm/blob/2d1e648c1a1c7e02180ef85cd260fc35ce434d1d/.github/workflows/build.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A096__file_5c3fa597431eda03.json`

## A097 — felixmosh/bull-board

Commit: `e3fca332d5faa0f84dac70f0e4efd2953f4a369a`.
Original package/version mappings: @bull-board/api@8.0.0, @bull-board/express@8.0.0, @bull-board/ui@8.0.0

Evidence:
- [package.json](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_7ae45ad102eab3b6.json`
- [.github/workflows/lint-pr.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/lint-pr.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_70c3a017bfdb629f.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_63bd641104d10e25.json`
- [.github/workflows/docker.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/docker.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_3f5366f6d6df3ec1.json`
- [.github/workflows/nextjs.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/nextjs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_2deb6c1e57ba666c.json`
- [.github/workflows/release.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_87db21a973eed4fe.json`
- [packages/express/package.json](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/packages/express/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_8dbc0c74c558223c.json`
- [yarn.lock](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_51e4f558fae53465.json`
- [packages/api/package.json](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/packages/api/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_069a572372e4f257.json`
- [.github/workflows/docs.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/docs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_9cf2000c53760d83.json`
- [packages/ui/package.json](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/packages/ui/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_1ae5a5e8c23bd3bc.json`
- [.github/workflows/nodejs.yml](https://github.com/felixmosh/bull-board/blob/e3fca332d5faa0f84dac70f0e4efd2953f4a369a/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A097__file_e98936aa52a6dd74.json`

## A098 — gkushang/cucumber-html-reporter

Commit: `e37df003d3c1d0b697e2124b21c1d6aee4fce62a`.
Original package/version mappings: cucumber-html-reporter@7.2.0

Evidence:
- [package.json](https://github.com/gkushang/cucumber-html-reporter/blob/e37df003d3c1d0b697e2124b21c1d6aee4fce62a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A098__file_7ae45ad102eab3b6.json`
- [.github/workflows/npm-publish.yml](https://github.com/gkushang/cucumber-html-reporter/blob/e37df003d3c1d0b697e2124b21c1d6aee4fce62a/.github/workflows/npm-publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A098__file_8a5ce8b612395836.json`
- [yarn.lock](https://github.com/gkushang/cucumber-html-reporter/blob/e37df003d3c1d0b697e2124b21c1d6aee4fce62a/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A098__file_51e4f558fae53465.json`

## A099 — goto-bus-stop/browser-pack-flat

Commit: `d041fc47abf1a1d14c0907638fe684b924fac333`.
Original package/version mappings: browser-pack-flat@3.5.0

Evidence:
- [.github/workflows/ci.yml](https://github.com/goto-bus-stop/browser-pack-flat/blob/d041fc47abf1a1d14c0907638fe684b924fac333/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A099__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/goto-bus-stop/browser-pack-flat/blob/d041fc47abf1a1d14c0907638fe684b924fac333/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A099__file_7ae45ad102eab3b6.json`

## A100 — gruntjs/grunt-contrib-cssmin

Commit: `e06534e25b780c9d3f4e37d7acc3743fae78d434`.
Original package/version mappings: grunt-contrib-cssmin@5.0.0

Evidence:
- [package-lock.json](https://github.com/gruntjs/grunt-contrib-cssmin/blob/e06534e25b780c9d3f4e37d7acc3743fae78d434/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A100__file_053150b640a7ce75.json`
- [.github/workflows/test.yml](https://github.com/gruntjs/grunt-contrib-cssmin/blob/e06534e25b780c9d3f4e37d7acc3743fae78d434/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A100__file_faff1af3d8ff4089.json`
- [package.json](https://github.com/gruntjs/grunt-contrib-cssmin/blob/e06534e25b780c9d3f4e37d7acc3743fae78d434/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A100__file_7ae45ad102eab3b6.json`

## A101 — i18next/i18next-parser

Commit: `6c10a2b66ebadb8250039d078ad2a53e52753a6e`.
Original package/version mappings: i18next-parser@9.4.0

Evidence:
- [.github/workflows/node.js.yml](https://github.com/i18next/i18next-parser/blob/6c10a2b66ebadb8250039d078ad2a53e52753a6e/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A101__file_014228303dff9a1a.json`
- [package.json](https://github.com/i18next/i18next-parser/blob/6c10a2b66ebadb8250039d078ad2a53e52753a6e/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A101__file_7ae45ad102eab3b6.json`
- [yarn.lock](https://github.com/i18next/i18next-parser/blob/6c10a2b66ebadb8250039d078ad2a53e52753a6e/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A101__file_51e4f558fae53465.json`

## A102 — luin/ioredis

Commit: `None`.
Original package/version mappings: ioredis@5.11.1

Evidence:
- Acquisition unresolved; record unknown unless independently documented.

## A103 — metamask/auto-changelog

Commit: `7a75c4af4eedf8c7f514c94906e20a1d2974ea4c`.
Original package/version mappings: @metamask/auto-changelog@6.1.1

Evidence:
- [.github/workflows/publish-release.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/publish-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_232ead425069ad86.json`
- [yarn.lock](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_51e4f558fae53465.json`
- [.github/workflows/main.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_7829468e86c1cc5d.json`
- [.github/workflows/publish-preview.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/publish-preview.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_83a4e378910355f2.json`
- [.github/workflows/create-release-pr.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/create-release-pr.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_06bbf35eee323b69.json`
- [package.json](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_7ae45ad102eab3b6.json`
- [.github/workflows/build-lint-test.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/build-lint-test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_b168d1081eb1f2b4.json`
- [.github/workflows/security-code-scanner.yml](https://github.com/metamask/auto-changelog/blob/7a75c4af4eedf8c7f514c94906e20a1d2974ea4c/.github/workflows/security-code-scanner.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A103__file_40f4e64a64b5e3f5.json`

## A104 — mweibel/lcov-result-merger

Commit: `9ccc71df10c3349100bfdd79c57ac239b48c835b`.
Original package/version mappings: lcov-result-merger@6.0.0

Evidence:
- [package-lock.json](https://github.com/mweibel/lcov-result-merger/blob/9ccc71df10c3349100bfdd79c57ac239b48c835b/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A104__file_053150b640a7ce75.json`
- [.github/workflows/ci.yml](https://github.com/mweibel/lcov-result-merger/blob/9ccc71df10c3349100bfdd79c57ac239b48c835b/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A104__file_b803fcb7f17ed923.json`
- [package.json](https://github.com/mweibel/lcov-result-merger/blob/9ccc71df10c3349100bfdd79c57ac239b48c835b/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A104__file_7ae45ad102eab3b6.json`

## A105 — node-red/node-red-admin

Commit: `c5329a5185895434839e05f4232f6267d52f2ead`.
Original package/version mappings: node-red-admin@4.1.6

Evidence:
- [package.json](https://github.com/node-red/node-red-admin/blob/c5329a5185895434839e05f4232f6267d52f2ead/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A105__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/node-red/node-red-admin/blob/c5329a5185895434839e05f4232f6267d52f2ead/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A105__file_053150b640a7ce75.json`
- [.github/workflows/tests.yml](https://github.com/node-red/node-red-admin/blob/c5329a5185895434839e05f4232f6267d52f2ead/.github/workflows/tests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A105__file_1db27d93186e46d3.json`

## A106 — npm/metavuln-calculator

Commit: `119ab9d3a22dff6f1492f2556ec5e8077a3c6db1`.
Original package/version mappings: @npmcli/metavuln-calculator@9.0.3

Evidence:
- [.github/workflows/pull-request.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/pull-request.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_b71166ed0f585913.json`
- [.github/workflows/post-dependabot.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/post-dependabot.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_1cb6b2b8125f1b16.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_63bd641104d10e25.json`
- [.github/workflows/release-integration.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/release-integration.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_2c3b5a007a3ca539.json`
- [.github/workflows/release.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_87db21a973eed4fe.json`
- [package.json](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_7ae45ad102eab3b6.json`
- [.github/workflows/ci-release.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/ci-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_42a22ead44f8caf1.json`
- [.github/workflows/ci.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_b803fcb7f17ed923.json`
- [.github/workflows/audit.yml](https://github.com/npm/metavuln-calculator/blob/119ab9d3a22dff6f1492f2556ec5e8077a3c6db1/.github/workflows/audit.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A106__file_93a89f16f6717d1e.json`

## A107 — npm/npm-profile

Commit: `67b32d049d41dac10b8ccba96208af522d1c8f40`.
Original package/version mappings: npm-profile@13.0.0

Evidence:
- [.github/workflows/post-dependabot.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/post-dependabot.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_1cb6b2b8125f1b16.json`
- [.github/workflows/ci.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_b803fcb7f17ed923.json`
- [.github/workflows/codeql-analysis.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/codeql-analysis.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_63bd641104d10e25.json`
- [.github/workflows/release.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_87db21a973eed4fe.json`
- [.github/workflows/pull-request.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/pull-request.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_b71166ed0f585913.json`
- [.github/workflows/audit.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/audit.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_93a89f16f6717d1e.json`
- [.github/workflows/ci-release.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/ci-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_42a22ead44f8caf1.json`
- [.github/workflows/release-integration.yml](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/.github/workflows/release-integration.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_2c3b5a007a3ca539.json`
- [package.json](https://github.com/npm/npm-profile/blob/67b32d049d41dac10b8ccba96208af522d1c8f40/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A107__file_7ae45ad102eab3b6.json`

## A108 — oclif/eslint-config-oclif-typescript

Commit: `4ea48166d9cc9e49861b193232cc82ee0ad84966`.
Original package/version mappings: eslint-config-oclif-typescript@3.1.14

Evidence:
- [.github/workflows/test.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_faff1af3d8ff4089.json`
- [.github/workflows/notify-slack-on-pr-open.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/notify-slack-on-pr-open.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_fe2c94f75439fa59.json`
- [.github/workflows/stale.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/stale.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_b5e0854ed0838024.json`
- [.github/workflows/onRelease.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/onRelease.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_07ad11b4716ea9cf.json`
- [package.json](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_7ae45ad102eab3b6.json`
- [.github/workflows/automerge.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/automerge.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_cc8c65daed8907e6.json`
- [.github/workflows/failureNotifications.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/failureNotifications.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_1df421f02f91b743.json`
- [.github/workflows/create-github-release.yml](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/.github/workflows/create-github-release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_2832baa5db895caf.json`
- [yarn.lock](https://github.com/oclif/eslint-config-oclif-typescript/blob/4ea48166d9cc9e49861b193232cc82ee0ad84966/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A108__file_51e4f558fae53465.json`

## A109 — openai/openai-node

Commit: `60224b376e25912bb1143007c81d2ecdc7a7434c`.
Original package/version mappings: openai@6.42.0

Evidence:
- [.github/workflows/castiron-custom-code-comment.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/castiron-custom-code-comment.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_8bbdbfb0c6c94eab.json`
- [.github/workflows/benchmarks.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/benchmarks.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_22eef62c9d7b36d0.json`
- [.github/workflows/node-version-review.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/node-version-review.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_86ef79ef5f0efac9.json`
- [.github/workflows/codeql.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/codeql.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_12783128521e452a.json`
- [.github/workflows/detect-breaking-changes.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/detect-breaking-changes.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_f00d10fad6b42151.json`
- [.github/workflows/create-releases.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/create-releases.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_4d451953a7b4e5f8.json`
- [package.json](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_7ae45ad102eab3b6.json`
- [pnpm-lock.yaml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_32824c984905bb02.json`
- [.github/workflows/node-version-policy.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/node-version-policy.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_45d687fb1e857854.json`
- [.github/workflows/ci.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_b803fcb7f17ed923.json`
- [.github/workflows/castiron-custom-code.yml](https://github.com/openai/openai-node/blob/60224b376e25912bb1143007c81d2ecdc7a7434c/.github/workflows/castiron-custom-code.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A109__file_bbe534f5ae2cdeac.json`

## A110 — sanity-io/ui

Commit: `ad916e75555cb08427f12d59efecb18cfb1e3906`.
Original package/version mappings: @sanity/ui@3.2.0

Evidence:
- [pnpm-lock.yaml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_32824c984905bb02.json`
- [package.json](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_7ae45ad102eab3b6.json`
- [.github/workflows/changesets-from-conventional-commits.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/changesets-from-conventional-commits.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_9ef7926450f19f95.json`
- [.github/workflows/pkg-pr-new.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/pkg-pr-new.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_ec60a2a16cce0f74.json`
- [.github/workflows/ci.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_b803fcb7f17ed923.json`
- [.github/workflows/format-if-needed.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/format-if-needed.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_9081e470dec7c9fa.json`
- [.github/workflows/release.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/release.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_87db21a973eed4fe.json`
- [.github/workflows/renovate.yml](https://github.com/sanity-io/ui/blob/ad916e75555cb08427f12d59efecb18cfb1e3906/.github/workflows/renovate.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A110__file_2f2dcee4f3f279ea.json`

## A111 — sap/ui5-project

Commit: `e0e0f9a6d7e92bcee25bd70b53cfde900e82da57`.
Original package/version mappings: @ui5/project@4.0.17

Evidence:
- [.github/workflows/reuse-compliance.yml](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/.github/workflows/reuse-compliance.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_40fa806d5e00789e.json`
- [.github/workflows/dependabot-auto-merge.yml](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/.github/workflows/dependabot-auto-merge.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_2fe48d1021006468.json`
- [.github/workflows/test.yml](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_faff1af3d8ff4089.json`
- [package-lock.json](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_053150b640a7ce75.json`
- [package.json](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_7ae45ad102eab3b6.json`
- [.github/workflows/github-ci.yml](https://github.com/sap/ui5-project/blob/e0e0f9a6d7e92bcee25bd70b53cfde900e82da57/.github/workflows/github-ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A111__file_86c810903f863122.json`

## A112 — sindresorhus/eslint-plugin-unicorn

Commit: `a6c2fdf97bd9a37687f31fb3807d23323d877bd8`.
Original package/version mappings: eslint-plugin-unicorn@65.0.1

Evidence:
- [.github/workflows/update-snapshots.yml](https://github.com/sindresorhus/eslint-plugin-unicorn/blob/a6c2fdf97bd9a37687f31fb3807d23323d877bd8/.github/workflows/update-snapshots.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A112__file_4b6fce1c311539ad.json`
- [.github/workflows/smoke-test.yml](https://github.com/sindresorhus/eslint-plugin-unicorn/blob/a6c2fdf97bd9a37687f31fb3807d23323d877bd8/.github/workflows/smoke-test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A112__file_f18045ce29bc2840.json`
- [package.json](https://github.com/sindresorhus/eslint-plugin-unicorn/blob/a6c2fdf97bd9a37687f31fb3807d23323d877bd8/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A112__file_7ae45ad102eab3b6.json`
- [.github/workflows/title-formatter.yml](https://github.com/sindresorhus/eslint-plugin-unicorn/blob/a6c2fdf97bd9a37687f31fb3807d23323d877bd8/.github/workflows/title-formatter.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A112__file_ddec3bf4d505c96e.json`
- [.github/workflows/main.yml](https://github.com/sindresorhus/eslint-plugin-unicorn/blob/a6c2fdf97bd9a37687f31fb3807d23323d877bd8/.github/workflows/main.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A112__file_7829468e86c1cc5d.json`

## A113 — stdlib-js/math-base-assert-is-finite

Commit: `f6cabb1f0c33f27fc9e189e1008828f00188f5e9`.
Original package/version mappings: @stdlib/math-base-assert-is-finite@0.2.3

Evidence:
- [.github/workflows/close_pull_requests.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/close_pull_requests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_c2534226e5caf507.json`
- [.github/workflows/test_install.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/test_install.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_1b9d64a0720ac550.json`
- [.github/workflows/test_bundles.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/test_bundles.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_5e991fbea792b8a6.json`
- [.github/workflows/test_coverage.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/test_coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_f0a9c26e26715ff4.json`
- [.github/workflows/test_published_package.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/test_published_package.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_079490fa1829e381.json`
- [.github/workflows/productionize.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/productionize.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_930e2da5f5534327.json`
- [.github/workflows/benchmark.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/benchmark.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_aacbd0338bcf5989.json`
- [.github/workflows/test.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_faff1af3d8ff4089.json`
- [.github/workflows/publish.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_551d1fcf87f78cc3.json`
- [.github/workflows/cancel.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/cancel.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_2d26dd5833955d0d.json`
- [.github/workflows/examples.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/examples.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_8906835152921ef9.json`
- [.github/workflows/npm_downloads.yml](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/.github/workflows/npm_downloads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_1fe260de46339e7e.json`
- [package.json](https://github.com/stdlib-js/math-base-assert-is-finite/blob/f6cabb1f0c33f27fc9e189e1008828f00188f5e9/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A113__file_7ae45ad102eab3b6.json`

## A114 — stdlib-js/number-float64-base-assert-is-same-value

Commit: `485843aa372e4e9f887219ef889b67aa1ac6b7f6`.
Original package/version mappings: @stdlib/number-float64-base-assert-is-same-value@0.2.2

Evidence:
- [package.json](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_7ae45ad102eab3b6.json`
- [.github/workflows/cancel.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/cancel.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_2d26dd5833955d0d.json`
- [.github/workflows/publish.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_551d1fcf87f78cc3.json`
- [.github/workflows/examples.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/examples.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_8906835152921ef9.json`
- [.github/workflows/test_bundles.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/test_bundles.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_5e991fbea792b8a6.json`
- [.github/workflows/test.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_faff1af3d8ff4089.json`
- [.github/workflows/productionize.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/productionize.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_930e2da5f5534327.json`
- [.github/workflows/benchmark.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/benchmark.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_aacbd0338bcf5989.json`
- [.github/workflows/test_coverage.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/test_coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_f0a9c26e26715ff4.json`
- [.github/workflows/npm_downloads.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/npm_downloads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_1fe260de46339e7e.json`
- [.github/workflows/close_pull_requests.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/close_pull_requests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_c2534226e5caf507.json`
- [.github/workflows/test_published_package.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/test_published_package.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_079490fa1829e381.json`
- [.github/workflows/test_install.yml](https://github.com/stdlib-js/number-float64-base-assert-is-same-value/blob/485843aa372e4e9f887219ef889b67aa1ac6b7f6/.github/workflows/test_install.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A114__file_1b9d64a0720ac550.json`

## A115 — stdlib-js/number-float64-base-exponent

Commit: `d7cb3ec00d24943f58694365e2a180c88dac6b91`.
Original package/version mappings: @stdlib/number-float64-base-exponent@0.2.3

Evidence:
- [.github/workflows/test.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_faff1af3d8ff4089.json`
- [.github/workflows/benchmark.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/benchmark.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_aacbd0338bcf5989.json`
- [.github/workflows/npm_downloads.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/npm_downloads.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_1fe260de46339e7e.json`
- [.github/workflows/test_coverage.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/test_coverage.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_f0a9c26e26715ff4.json`
- [.github/workflows/productionize.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/productionize.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_930e2da5f5534327.json`
- [.github/workflows/publish.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_551d1fcf87f78cc3.json`
- [.github/workflows/close_pull_requests.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/close_pull_requests.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_c2534226e5caf507.json`
- [package.json](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_7ae45ad102eab3b6.json`
- [.github/workflows/cancel.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/cancel.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_2d26dd5833955d0d.json`
- [.github/workflows/test_published_package.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/test_published_package.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_079490fa1829e381.json`
- [.github/workflows/test_bundles.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/test_bundles.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_5e991fbea792b8a6.json`
- [.github/workflows/examples.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/examples.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_8906835152921ef9.json`
- [.github/workflows/test_install.yml](https://github.com/stdlib-js/number-float64-base-exponent/blob/d7cb3ec00d24943f58694365e2a180c88dac6b91/.github/workflows/test_install.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A115__file_1b9d64a0720ac550.json`

## A116 — unassert-js/unassertify

Commit: `8c73fe2f9269db6576525a1a901bdac0ceed534c`.
Original package/version mappings: unassertify@3.0.1

Evidence:
- [package-lock.json](https://github.com/unassert-js/unassertify/blob/8c73fe2f9269db6576525a1a901bdac0ceed534c/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A116__file_053150b640a7ce75.json`
- [package.json](https://github.com/unassert-js/unassertify/blob/8c73fe2f9269db6576525a1a901bdac0ceed534c/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A116__file_7ae45ad102eab3b6.json`
- [.github/workflows/node.js.yml](https://github.com/unassert-js/unassertify/blob/8c73fe2f9269db6576525a1a901bdac0ceed534c/.github/workflows/node.js.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A116__file_014228303dff9a1a.json`

## A117 — vueuse/vueuse

Commit: `bd187a7ff0a793df754e9dc56c206298493ce81a`.
Original package/version mappings: @vueuse/components@14.3.0, @vueuse/core@14.3.0, @vueuse/integrations@14.3.0, @vueuse/metadata@14.3.0, @vueuse/nuxt@14.3.0, @vueuse/shared@14.3.0

Evidence:
- [packages/shared/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/shared/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_3752b1e4e3e20325.json`
- [.github/workflows/autofix.yml](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/.github/workflows/autofix.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_89b476612e9731e1.json`
- [.github/workflows/ci.yml](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/.github/workflows/ci.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_b803fcb7f17ed923.json`
- [packages/core/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/core/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_0b810c38f3c138a3.json`
- [packages/integrations/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/integrations/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_c58bc85600ab5682.json`
- [packages/metadata/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/metadata/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_cdd176d14a02115f.json`
- [pnpm-lock.yaml](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/pnpm-lock.yaml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_32824c984905bb02.json`
- [.github/workflows/publish.yml](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/.github/workflows/publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_551d1fcf87f78cc3.json`
- [package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_7ae45ad102eab3b6.json`
- [packages/components/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/components/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_2c76dc06185f93be.json`
- [packages/nuxt/package.json](https://github.com/vueuse/vueuse/blob/bd187a7ff0a793df754e9dc56c206298493ce81a/packages/nuxt/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A117__file_36b207d79434b922.json`

## A118 — webpack/css-loader

Commit: `be04ec290ee57bafbc75f5936c1f6a2532681b49`.
Original package/version mappings: css-loader@7.1.4

Evidence:
- [.github/workflows/nodejs.yml](https://github.com/webpack/css-loader/blob/be04ec290ee57bafbc75f5936c1f6a2532681b49/.github/workflows/nodejs.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A118__file_e98936aa52a6dd74.json`
- [.github/workflows/dependency-review.yml](https://github.com/webpack/css-loader/blob/be04ec290ee57bafbc75f5936c1f6a2532681b49/.github/workflows/dependency-review.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A118__file_7cdd3ccec44c8ba1.json`
- [package.json](https://github.com/webpack/css-loader/blob/be04ec290ee57bafbc75f5936c1f6a2532681b49/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A118__file_7ae45ad102eab3b6.json`
- [package-lock.json](https://github.com/webpack/css-loader/blob/be04ec290ee57bafbc75f5936c1f6a2532681b49/package-lock.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A118__file_053150b640a7ce75.json`

## A119 — yakovmeister/pdf2image

Commit: `879746fbbe6b8df9b5840e26c08fcf06a04f94ce`.
Original package/version mappings: pdf2pic@3.2.0

Evidence:
- [package.json](https://github.com/yakovmeister/pdf2image/blob/879746fbbe6b8df9b5840e26c08fcf06a04f94ce/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A119__file_7ae45ad102eab3b6.json`
- [.github/workflows/test.yml](https://github.com/yakovmeister/pdf2image/blob/879746fbbe6b8df9b5840e26c08fcf06a04f94ce/.github/workflows/test.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A119__file_faff1af3d8ff4089.json`
- [.github/workflows/npm-publish.yml](https://github.com/yakovmeister/pdf2image/blob/879746fbbe6b8df9b5840e26c08fcf06a04f94ce/.github/workflows/npm-publish.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A119__file_8a5ce8b612395836.json`
- [.github/workflows/lint.yml](https://github.com/yakovmeister/pdf2image/blob/879746fbbe6b8df9b5840e26c08fcf06a04f94ce/.github/workflows/lint.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A119__file_107e910e9f2ebfb9.json`

## A120 — yarnpkg/berry

Commit: `8f638c0806ec8f3758adb13d93567fc782f9c903`.
Original package/version mappings: @yarnpkg/core@4.9.0, @yarnpkg/esbuild-plugin-pnp@3.0.0-rc.15, @yarnpkg/fslib@3.1.5, @yarnpkg/libzip@3.2.2, @yarnpkg/parsers@3.0.3, @yarnpkg/shell@4.1.3

Evidence:
- [.github/workflows/e2e-esbuild-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-esbuild-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_2769c460eb6b32ee.json`
- [.github/workflows/e2e-gatsby-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-gatsby-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_23277fcc6e7c6582.json`
- [yarn.lock](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/yarn.lock); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_51e4f558fae53465.json`
- [.github/workflows/e2e-create-vue-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-create-vue-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_112149db0429e7ba.json`
- [.github/workflows/e2e-nm-babel-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-nm-babel-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_81c8a2affab25726.json`
- [.github/workflows/e2e-nm-berry-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-nm-berry-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_ad2888285c4eba1b.json`
- [.github/workflows/e2e-nyc-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-nyc-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_2697e61518c037ef.json`
- [.github/workflows/e2e-fsevents-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-fsevents-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_a1bda641dbcfec2d.json`
- [.github/workflows/e2e-nm-angular-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-nm-angular-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_8e6b72baaac63c3f.json`
- [packages/yarnpkg-fslib/package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/packages/yarnpkg-fslib/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_e970e91c0730f4b2.json`
- [.github/workflows/e2e-mocha-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-mocha-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_33076cf254a5fca5.json`
- [packages/yarnpkg-shell/package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/packages/yarnpkg-shell/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_ea2bf9317e68f6b4.json`
- [packages/yarnpkg-parsers/package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/packages/yarnpkg-parsers/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_ab1a767a9b135f6c.json`
- [.github/workflows/e2e-eslint-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-eslint-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_dff6df939f3a9c1a.json`
- [package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_7ae45ad102eab3b6.json`
- [.github/workflows/e2e-next-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-next-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_2744a9261e79335e.json`
- [.github/workflows/e2e-pnp-angular-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-pnp-angular-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_decd473bad929d30.json`
- [.github/workflows/e2e-jest-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-jest-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_eec89f33b0cfef37.json`
- [.github/workflows/e2e-husky-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-husky-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_60e7955b22191537.json`
- [packages/yarnpkg-libzip/package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/packages/yarnpkg-libzip/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_fe970db0da97cc88.json`
- [.github/workflows/e2e-prettier-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-prettier-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_52c727fa1c23c3f7.json`
- [.github/workflows/benchmark-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/benchmark-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_b6a9ad6deba86159.json`
- [.github/workflows/e2e-gulp-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-gulp-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_dc33bb6a54ccb536.json`
- [.github/workflows/debug.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/debug.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_22ec448956849a92.json`
- [packages/yarnpkg-core/package.json](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/packages/yarnpkg-core/package.json); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_9dbba033e665015f.json`
- [.github/workflows/e2e-docusaurus-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-docusaurus-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_da8524c5add809c0.json`
- [.github/workflows/e2e-parcel-workflow.yml](https://github.com/yarnpkg/berry/blob/8f638c0806ec8f3758adb13d93567fc782f9c903/.github/workflows/e2e-parcel-workflow.yml); retained response `manuscript_q1/results/revision_validation/endpoint_audit/github_responses/A120__file_1c6692320724439e.json`
