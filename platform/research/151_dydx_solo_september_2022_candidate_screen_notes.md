# Bounded dYdX Solo September 2022 candidate screen

**Screen date:** 27 August 2026  
**Candidate package:** `@dydxprotocol/solo`  
**Candidate event family:** `dydx_solo_september_2022_npm_account_compromise`  
**Screen status:** Eligible to request bounded official npm registry metadata only; no ledger entry or reconstruction has been made by this note.

## Evidence observations before registry access

BleepingComputer reports a September 2022 compromise of packages published by dYdX and lists `@dydxprotocol/solo@0.41.1` and `@0.41.2` as the affected releases.[1] It separately lists another package and pair of versions; those are explicitly outside this single-package screen.[1]

Mend independently reports that packages owned by dYdX, including `@dydxprotocol/solo`, received new npm releases on 23 September 2022 and characterizes the incident as an npm-account compromise.[2] The rendered Mend text reviewed in this screen does not itself enumerate the Solo version pair. Accordingly, it establishes package-level incident context only and is not used as independent exact-version corroboration.

GitHub’s reviewed malware advisory independently identifies the npm package and affected range `>= 0.41.1, <= 0.41.2`, which resolves to exactly the same two releases in the cited BleepingComputer report.[3] The strict candidate target is therefore `0.41.1` and `0.41.2` only. No unlisted version or companion dYdX package may enter this screen.

| Source | Package observation | Exact-version support in this screen | Permitted use |
|---|---|---|---|
| BleepingComputer | Names `@dydxprotocol/solo` in the September 2022 dYdX package event. | `0.41.1`, `0.41.2` | Candidate exact set, pending independent confirmation. |
| Mend | Names `@dydxprotocol/solo` among the newly published dYdX packages and describes an account compromise. | Not enumerated in reviewed rendered text | Package-level context only; not version confirmation. |
| GitHub Advisory Database | Reviewed npm malware advisory for `@dydxprotocol/solo`. | `>= 0.41.1, <= 0.41.2`, intersecting as `0.41.1`, `0.41.2` | Independent exact-version confirmation. |

The 2022 candidate is temporally distinct from the separately governed January–February 2026 `@dydxprotocol/v4-client-js` row. Temporal separation alone does not establish actor, campaign, or statistical independence. No relationship to any governed family is asserted unless an independently reviewed source documents one.

## Strict no-inference boundary

No official registry metadata has been accessed in this screen. The independent exact-version condition is now met by the BleepingComputer and GitHub Advisory Database intersection. The next permitted step is a metadata-only registry assessment for this single package to determine the earliest reported-version publication timestamp, its one-millisecond cutoff, and whether a retained pre-event object is selectable across all SemVer streams.

No archive, tarball, or package payload has been downloaded, extracted, installed, or executed. This provisional screen creates zero package-event records, families, exact snapshots, dependency declarations, range approximations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, models, or predictive metrics.

## References

[1]: https://www.bleepingcomputer.com/news/security/npm-packages-used-by-crypto-exchanges-compromised/ "BleepingComputer, npm packages used by crypto exchanges compromised"
[2]: https://www.mend.io/blog/popular-cryptocurrency-exchange-dydx-has-had-its-npm-account-hacked/ "Mend, Popular Cryptocurrency Exchange Dydx Has Its NPM Acct Hacked"
[3]: https://github.com/advisories/GHSA-xjr5-5w2w-3233 "GitHub Advisory Database, Malware in @dydxprotocol/solo"
