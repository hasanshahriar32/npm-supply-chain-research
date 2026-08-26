# node-ipc March 2022 candidate screen

## Bounded screen status

This screen concerns the March 2022 maintainer-published protestware event only. It is **not** the separately governed May 2026 `node-ipc` compromise already in the primary ledger. It is not a primary-ledger admission until the strict official-registry selection below succeeds.

| Candidate package-event | Finite affected versions | Proposed family | Relationship to current ledger | Status |
| --- | --- | --- | --- | --- |
| `node-ipc` March 2022 | `10.1.1`, `10.1.2` | `node_ipc_march_2022_maintainer_protestware` | Separate 2022 event and family; do not merge with `node_ipc_2026` | Pending registry time-map and retained-object screen |

## Bounded corroboration

GitHub’s reviewed advisory identifies `node-ipc` versions `10.1.1` and `10.1.2` as containing malicious code introduced by the maintainer, with `10.1.3` as the patch. Snyk’s contemporaneous incident report independently identifies `10.1.1` and `10.1.2` as the short-lived destructive releases and distinguishes them from later `peacenotwar`-linked releases. NVD records the same affected range (`>=10.1.1`, `<10.1.3`) and describes its publication as malicious code.[1] [2] [3]

The registry time-map must select the latest version published strictly before the earliest corroborated affected publication. The selected exact version object must still be present in the bounded official registry metadata response; otherwise the candidate will be excluded. No branch substitution is permitted.

> The cited sources establish an adverse 2022 publication event. They do not establish historical installation, dependency resolution, reach, a benign label, a control, or a predictive outcome.

## References

[1]: https://github.com/advisories/GHSA-97m3-w2cp-4xx6 "GitHub Advisory Database: Embedded Malicious Code in node-ipc"
[2]: https://snyk.io/blog/peacenotwar-malicious-npm-node-ipc-package-vulnerability/ "Snyk: peacenotwar module sabotages npm developers"
[3]: https://nvd.nist.gov/vuln/detail/CVE-2022-23812 "NVD: CVE-2022-23812"
[4]: https://registry.npmjs.org/node-ipc "npm registry metadata for node-ipc"
