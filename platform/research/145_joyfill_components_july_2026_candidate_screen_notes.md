# Bounded `@joyfill/components` July 2026 candidate screen

**Screen decision:** **Exclude from a new independent primary-ledger family before registry access.** No official npm registry request, cutoff selection, source-object selection, package download, archive inspection, installation, payload extraction, or execution occurred for this screen.

## Exact-version evidence and bounded target

StepSecurity reports that `@joyfill/components@4.0.0-rc24-2773-beta.4`, `4.0.0-rc24-2773-beta.5`, and `4.0.0-rc24-2773-beta.6` were malicious beta releases in a two-package Joyfill event.[1] Socket independently identifies `@joyfill/components@4.0.0-rc24-2773-beta.4` (alongside a separately named Joyfill package) as compromised.[2] The strict package-level source intersection is therefore one version only: `@joyfill/components@4.0.0-rc24-2773-beta.4`.

## Relatedness exclusion

Socket’s report explicitly labels the Joyfill release as linked to the ongoing **PolinRider** supply-chain attack.[2] The governed ledger already contains `common_stack_generate_plugin_polinrider_hijack_2026`; this new source relationship prevents the Joyfill version from being represented as a genuinely separate independent family or future validation unit. The screen does not decide whether the record would be a permissible *additional package row* in the existing PolinRider family, because this autonomous stage is constrained to identify a genuinely separate compact candidate and must not expand a related family by inference.

## No-inference boundary

This exclusion does not dispute the reported malicious version. It adds zero primary-ledger records, families, source snapshots, direct declarations, range approximations, graph edges, controls, benign labels, historical installations, reach or blast-radius values, authority values, scores, rankings, intervals, calibration results, models, or predictive metrics. The screenshots and source text do not establish campaign completeness, historical installation, current publisher state, downstream exposure, causal effects, or a statistical-independence claim.

## References

[1]: https://www.stepsecurity.io/blog/joyfill-npm-supply-chain-compromise "StepSecurity, Compromised npm Packages: @joyfill/components and @joyfill/layouts Ship an Obfuscated Remote Access Trojan"
[2]: https://socket.dev/blog/joyfill-npm-beta-releases-compromised "Socket, Two Joyfill npm Beta Releases Compromised to Deliver DEV#POPPER Remote Access Trojan"
