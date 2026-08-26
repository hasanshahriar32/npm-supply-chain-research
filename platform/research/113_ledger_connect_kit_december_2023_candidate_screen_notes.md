# Bounded `@ledgerhq/connect-kit` December 2023 Candidate Screen Notes

**Status:** Candidate-selection notes only; no ledger decision.  
**Date:** 26 August 2026.  
**Scope:** Bounded screen for `@ledgerhq/connect-kit@1.1.5`, `1.1.6`, and `1.1.7` only.

## Evidence preserved before registry screening

Ledger’s incident report states that an attacker phished a former employee and used the former employee’s npmjs access to upload a malicious Ledger Connect Kit version. [1] Socket independently identifies affected versions `1.1.5`, `1.1.6`, and `1.1.7`, describes the phishing source, and identifies `1.1.8` as safe. [2]

| Screening requirement | Current bounded evidence | Decision at this note stage |
|---|---|---|
| Finite affected version target | Socket identifies `1.1.5`, `1.1.6`, and `1.1.7`. [2] | Provisionally satisfied. |
| Primary compromise context | Ledger identifies phishing of a former employee and npmjs access misuse. [1] | Provisionally satisfied. |
| Independent technical corroboration | Socket independently documents the same version set and compromise context. [2] | Provisionally satisfied. |
| Relatedness | No relationship to an existing primary-ledger family is established by this bounded screen. | New-family or validation-unit treatment is prohibited unless the strict source-object gate is met. |
| Official registry cutoff and retained predecessor | Not yet assessed. | Requires bounded official registry metadata, an earliest-affected-version cutoff, and a retained source object strictly before the cutoff. |

No package payload was downloaded, extracted, installed, or executed. This note creates zero ledger records, families, validation units, snapshots, dependency declarations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, scores, models, rankings, intervals, calibration results, or predictive metrics.

## References

[1] [Ledger, “Security Incident Report,” 20 December 2023](https://www.ledger.com/blog/security-incident-report).

[2] [Socket, “Ledger Connect-Kit Supply Chain Attack Hits Decentralized Crypto Apps with Wallet-Draining Code,” 14 December 2023](https://socket.dev/blog/ledger-connect-kit-supply-chain-attack-wallet-drainer).
