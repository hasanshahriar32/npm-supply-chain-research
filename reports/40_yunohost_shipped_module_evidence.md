# Dependency evidence in two checksum-pinned releases

Two releases from the earlier YunoHost audit allow separate checks on declared dependencies, compiled assets, and packaged files. Both downloaded archives match the SHA-256 values in the recipes. These two archives were selected for the evidence they preserved, so the results describe the selected artifacts. [Archive queue](../research/consumer_holdout/runs/yunohost-release-modules/archive_queue.json).

| Release | Evidence checked | Result |
| --- | --- | --- |
| Pterodactyl Panel v1.15.1 | All 17 JavaScript files under `public/assets` | Zero `.map` files in that directory and zero source-map directive comments in the JavaScript |
| Mongo Express v1.1.0-rc-4 | All 39 regular direct dependencies bundled under `package/node_modules` | All 39 match the corresponding npm tarball across 1,571 own regular-file paths |

## Pterodactyl Panel

The earlier comparison found identical manifest and lockfile bytes in the archive and the tag-resolved source. To check for a link from those declarations to the shipped code, we matched each asset to its recorded SHA-256 and parsed it with Acorn 8.18.0 using Node.js v24.22.0. The one literal `sourceMappingURL` occurrence is a string token. Source-map discovery relies on a directive comment, a separately supplied map link, or other map evidence. The archive check covered map files in `public/assets` and directives in its JavaScript assets. [Asset inventory](../research/consumer_holdout/runs/yunohost-release-modules/module_inputs.json), [static parser results](../research/consumer_holdout/runs/yunohost-release-modules/static_bundle_parser.json), [ECMA-426](https://tc39.es/ecma426/2024/).

The Webpack configuration at the tag-resolved commit disables source maps by default in production and allows an environment override. The actual build environment and live HTTP headers are outside the archive inspection. [Pinned configuration](https://github.com/pterodactyl/panel/blob/e98678c5a1d07a74036660a459d87a4eb7c105c1/webpack.config.js), [Webpack documentation](https://webpack.js.org/configuration/devtool/).

## Mongo Express

The archived application manifest defines 39 regular direct dependencies after excluding optional dependencies. All 39 bundled manifests have the expected name and a version satisfying the declared range. For each exact version, the collector required a canonical npm registry tarball and verified the returned bytes against the registry's SHA-512 integrity value. We compared the relative file paths and SHA-256 hashes within each package directory, skipping nested `node_modules` in both archives. Every compared path and hash agrees. [Frozen registry queue](../research/consumer_holdout/runs/yunohost-release-modules/registry_queue.json), [per-dependency counts and results](../research/consumer_holdout/runs/yunohost-release-modules/results.json).

All 39 exact-version records supplied usable maintainer lists at collection time. The preselected name portfolio, all three version cutoff choices, and the control each contain a recorded maintainer of at least one matched package. This links a common positive coverage finding to bytes present in a delivered artifact. The check covers this release's regular direct packages and current registry associations. It leaves runtime loading, complete transitive contents, and historical release authority unresolved.

The replay uses the pinned application archives and recorded registry file hash receipts. Tarball SHA-512 verification is performed at acquisition. [Replay commands](../research/consumer_holdout/README.md).
