# Bounded `sbx-mask` March 2026 candidate screen

**Status:** Continuing evidence screen; **not** a ledger admission.
**Date:** 27 August 2026.
**Scope:** One package-event candidate, `sbx-mask`; the related `touch-adv` package is not added, grouped, or otherwise inferred into this screen.

## Bounded source observations

Sonatype’s dated 19 March 2026 research report identifies `sbx-mask` and `touch-adv` as malicious npm packages, describes secret exfiltration behavior, and reports a suspected compromise of a trusted npm maintainer account. It states that the incident was reported to npm on 19 March and remained active and under investigation. [1]

GitHub’s publicly reviewed malware advisory `GHSA-r934-qgg3-v7fg`, published and reviewed on 24 March 2026, separately identifies the npm package `sbx-mask` and gives the finite affected-version set `1.0.0`, `1.0.1`, and `1.0.2`. [2] The linked public OSV representation `MAL-2026-2132` carries the same three version identifiers and separately records Amazon Inspector and GitHub malware-source provenance; it is supporting positive-version metadata, not a source of negative evidence. [3]

| Candidate question | Current bounded finding | Permitted interpretation |
|---|---|---|
| Package event | Sonatype reports malicious `sbx-mask` in a suspected maintainer-account compromise; GitHub separately classifies it as malware. | Supports continued package-event screening only. |
| Exact version set | GitHub advisory and linked OSV representation list `1.0.0`, `1.0.1`, and `1.0.2`. | A finite candidate set exists; no additional versions may be inferred. |
| Independence | No retrieved evidence establishes a relationship to a current governed family. | No relationship is asserted; later registry selection cannot establish one. |
| Pre-event source object | Not yet inspected. | No cutoff, predecessor, ledger row, snapshot, declaration, or graph edge exists. |

## Interpretation boundary

This source screen creates **zero** controls, benign labels, historical installation records, dependency reach or blast-radius claims, ranks, authority values, scores, calibration results, intervals, models, or predictive metrics. It does not download, extract, install, or execute package material. The next step, if any, is a metadata-only official npm registry time-map and retained-predecessor assessment; registry metadata can establish strict cutoff selection and current object retention only, not historical installation, downstream reach, current publisher state, causality, or a non-event label.

## References

[1] [Sonatype, “Sonatype Discovers Two Malicious npm Packages,” 19 March 2026](https://www.sonatype.com/blog/sonatype-discovers-two-malicious-npm-packages).

[2] [GitHub Advisory Database, “Malware in sbx-mask,” GHSA-r934-qgg3-v7fg](https://github.com/advisories/GHSA-r934-qgg3-v7fg).

[3] [OpenSSF Malicious Packages, “MAL-2026-2132: Malicious code in sbx-mask (npm)”](https://osv-vulnerabilities.storage.googleapis.com/npm/MAL-2026-2132.json).
