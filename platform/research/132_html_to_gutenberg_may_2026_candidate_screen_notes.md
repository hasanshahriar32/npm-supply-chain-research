# Bounded candidate screen: html-to-gutenberg May 2026 npm hijack

## Status

**Preliminary corroboration only; not admitted.** This note records independently reviewed report text before any registry reconstruction. It neither asserts a primary-ledger label nor creates a source snapshot, control, historical installation, dependency reach or blast-radius value, authority value, score, model, rank, interval, calibration result, or predictive metric.

## Public-report observations

| Source | Published | Bounded observation |
|---|---:|---|
| JFrog Security Research | 24 June 2026 | Identifies the hijacked npm release `html-to-gutenberg@4.2.11`; separately names `fetch-page-assets@1.2.9`; says the versions were uploaded during 25 May 2026 and subsequently removed. |
| The Hacker News | 29 June 2026 | Independently reports the same two npm package names, says they were uploaded on 25 May 2026, and states that they were no longer available from the registry. |
| Corgea advisory index | 24 June 2026 | Independently indexes `html-to-gutenberg` as npm malware and links to GitHub advisory `GHSA-2gqj-wrf5-35w8`, but its visible index text does not state an affected version. |
| GitHub Advisory Database | Reviewed 24 June 2026 | Reviewed malware advisory `GHSA-2gqj-wrf5-35w8` identifies `html-to-gutenberg` affected versions `4.2.11` and `4.2.14`; it carries no source-code link. |

The JFrog report describes the package releases as hijacked and identifies `4.2.11`; the independent news report corroborates the package-level incident and upload date. The reviewed GitHub advisory independently states the finite affected-version set `4.2.11|4.2.14`. The sources provide a candidate basis to proceed to a metadata-only cutoff and retention screen. They do not establish an association with any governed family; no relationship is asserted absent explicit source evidence.

## Boundaries

No archive, tarball, payload, source-code extraction, installation, execution, package reach calculation, or dependency-resolution claim was performed. Registry metadata, if accessed in the next stage, may support only time-map and retention selection under the frozen protocol; it cannot establish payload facts, historical installs, outcome labels, controls, reach, authority deltas, or model inputs.

## References

[1] [JFrog Security Research, “Hijacked npm Packages Use Novel VSCode Autorun and Blockchain Dead Drops to Deploy a Credential/Crypto Stealer”](https://research.jfrog.com/post/hijacked-npm-vscode-tasks-blockchain/)

[2] [The Hacker News, “Hijacked npm and Go Packages Use VS Code Tasks to Deploy Python Infostealer”](https://thehackernews.com/2026/06/hijacked-npm-and-go-packages-use-vs.html)

[3] [Corgea, “html-to-gutenberg vulnerabilities”](https://corgea.com/advisories/packages/npm/html-to-gutenberg)

[4] [GitHub Advisory Database, “Malware in html-to-gutenberg” (GHSA-2gqj-wrf5-35w8)](https://github.com/advisories/GHSA-2gqj-wrf5-35w8)
