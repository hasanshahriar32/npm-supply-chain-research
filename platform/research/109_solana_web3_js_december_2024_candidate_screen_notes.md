# Bounded `@solana/web3.js` December 2024 Candidate Screen Notes

**Status:** Candidate-selection notes only; no ledger decision.  
**Date:** 26 August 2026.  
**Scope:** Bounded screen for `@solana/web3.js@1.95.6` and `1.95.7` only.

## Evidence preserved before registry screening

The project’s GitHub security advisory identifies `@solana/web3.js` versions `1.95.6` and `1.95.7` as affected. It states that a publish-access account was compromised, allowing unauthorized malicious packages to be published, and says the two versions were subsequently unpublished. [1] Socket independently identifies the same exact version pair and reports a social-engineering or phishing attack against maintainers as the compromise context. [2]

| Screening requirement | Current bounded evidence | Decision at this note stage |
|---|---|---|
| Finite affected version target | The project advisory and Socket identify `1.95.6` and `1.95.7`. [1] [2] | Provisionally satisfied. |
| Independent compromise-context corroboration | The project advisory reports publish-access compromise; Socket independently reports phishing/social engineering. [1] [2] | Provisionally satisfied. |
| Relatedness | No row is yet assigned to an existing family. | A new family and validation unit are prohibited unless the strict source-object gate is met. |
| Official registry cutoff and retained predecessor | Not yet assessed. | Requires bounded official registry metadata, a documented event-time rule, and a retained source object strictly before the cutoff. |

No package payload was downloaded, extracted, installed, or executed. This note creates zero ledger records, families, validation units, snapshots, dependency declarations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, scores, models, rankings, intervals, calibration results, or predictive metrics.

## References

[1] [Solana web3.js Security Advisory, “Modified package published to npm, containing malware that exfiltrates private key material,” `GHSA-jcxm-7wvp-g6p5`, 4 December 2024](https://github.com/solana-foundation/solana-web3.js/security/advisories/GHSA-jcxm-7wvp-g6p5).

[2] [Socket, “Supply Chain Attack Detected in Solana's web3.js Library,” 3 December 2024](https://socket.dev/blog/supply-chain-attack-solana-web3-js-library).
