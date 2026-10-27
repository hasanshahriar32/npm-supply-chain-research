Versioned data and code for the npm structural-prioritization validation revision.

Download **npm-research-validation-2026-10-28-companion.zip**, the attached reproduction companion. The automatically generated source-code archives follow the base repository tag and do not replace this asset.

The asset links the preserved original database at its immutable base commit and includes a frozen 120-endpoint audit sample and derived automated evidence, fresh observations for a 100-root bounded cohort, 38 heuristic/component/tie runs, and 32 exact benchmark instances evaluated at three budgets. Independent human audit annotations remain pending. No journal manuscript is included or asserted to have author/editorial approval.

Reproduction:

```sh
python3 download_original_input.py
python3 scripts/reproduce_journal_validation.py --recompute-cohort
```

A clean extraction passed checksum checks, rebuilt the original account incidence, checked 228 ablation rows, recomputed the restricted optima underlying 288 comparisons, checked 120 cohort metric rows, and reproduced the cohort comparisons in an isolated workspace with network acquisition disabled.

The artifact README documents population limits, unknown observations, source attribution and raw-source exclusions. Third-party workflow/manifest bodies are referenced by pinned URLs and hashes; derived audit evidence is included. This prerelease does not certify human labels, workflow execution, compromise probabilities or deployed security effects.

Asset SHA-256: `ff306ac5392cf8fda4420b8a13855a21adccbff534e85fb1559009d62f75e756`.

Original database: https://raw.githubusercontent.com/hasanshahriar32/npm-supply-chain-research/43c039bebe7c36b07a5aeb50b1c8a412ad058e0f/data/npm_ecosystem.db.zip

The database download is verified against SHA-256 ab45439cf94cf43f3133b0aaff644557d55e86e99430a0a7937bfd0ce5266315 before offline reproduction.
