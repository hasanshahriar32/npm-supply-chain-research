# YunoHost release-delivery evidence

The release follow-up checks whether pinned YunoHost recipes can be linked to exact release artifacts, public provenance, and npm dependency inventories. It covers all 39 recipes from the fresh sample with a release declaration and no matched JavaScript package command. Literal calls in the retained install and common scripts identify 38 GitHub assets across 37 recipes. The lookup uses the amd64 field when specified. It includes referenced helper assets and conditional choices. It measures what the static recipe and public records expose.

| Evidence stage | Count |
| --- | ---: |
| Recipes with an exact GitHub asset reference | 37 of 39 |
| Exact assets found in the release API | 37 of 38 |
| API SHA-256 agrees with recipe | 30 of 37 |
| API digest unavailable | 6 of 37 |
| API digest differs | 1 of 37 |
| Subject-matching public statements | 6 of 30 agreeing digests |
| SLSA statements declaring a commit in the release repository | 3 of 30 |

One release lookup redirected outside its frozen endpoint. Twenty-four of the 30 subject lookups returned HTTP 404, which leaves their attestation status unresolved. The six matching subjects yielded eight statements. Three were SLSA provenance statements naming one Git commit each. The declared commits refer to the release repositories, which also include helpers and independently distributed components. We checked the statements' exact subject digests. Signature verification remains outside this analysis. [GitHub release asset fields](https://docs.github.com/en/rest/releases/assets), [public attestation lookup](https://docs.github.com/en/rest/repos/attestations), and [in-toto statement specification](https://github.com/in-toto/attestation/blob/main/spec/v1/statement.md).

## Direct delivery and dependency information

Fifteen assets met the 12 MiB size limit and had a declared recipe checksum. Fourteen downloads matched the pin. Five of the matches fill gaps where the release API supplied no digest. The remaining download matched the API SHA-256 and differed from the recipe. The conflicting artifact cannot join to the pinned recipe in this audit.

Eleven verified ZIP or gzip TAR archives supported a metadata scan.

| Verified artifact | Dependency evidence | Implication for the npm comparison |
| --- | --- | --- |
| Mongo Express release archive | 198 bundled npm manifests, 190 with a name and version. No lockfile and no accepted public registry artifact identifiers. | Identifies bundled copies. Registry artifact linkage remains unresolved. |
| Pterodactyl panel release archive | Application manifest and a Yarn Classic lockfile with SHA-512 fields. The scan found no bundled npm manifests. | Supports checks of locked declarations. Packaged npm presence remains unresolved. |
| Selected Java runtime helper | A CycloneDX release sidecar binds one component to the selected filename and exact SHA-256. | The document contains zero npm package URLs. |

The archive audit used file names and bounded metadata reads. It did not extract payloads to the filesystem or run package code. These observations explain why source commit provenance, a lockfile, an inventory, and membership evidence can produce different coverage denominators. No new paired npm coverage result is included.

The [release results](../research/consumer_holdout/runs/yunohost-release-delivery/results.json), [archive receipts](../research/consumer_holdout/runs/yunohost-release-delivery/archive_results.json), and [evidence summary](../research/consumer_holdout/runs/yunohost-release-delivery/evidence_summary.json) retain the scope, per-asset results, and digest references. The earlier 215-project root comparison and recipe-importer diagnostic retain their original denominators.
