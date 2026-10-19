# Structural intervention study: completed empirical work

Status: implemented and executed on 2026-10-20. The read-only study is reproduced by:

```bash
python scripts/study_structural_interventions.py
```

The implementation uses only Python's standard library. It extracts the source SQLite archive to a temporary directory, opens SQLite with `mode=ro&immutable=1`, and executes no package code. The generated manifest contains source checksums, script checksum, Python version, seeds, definitions, limitations, and output checksums. The saved local run plan describes an exploratory analysis; it is not external preregistration. No maintainer names, package names, email hashes, repository names, individual rankings, or payloads appear in these intervention outputs.

## Research questions and measured units

1. How do identity controls selected for distinct endpoint coverage differ from those selected to reduce the sum of hypothetical identity-loss scenario exposures?
2. How much prospective endpoint coverage remains reachable through identities outside the control budget?
3. How sensitive are conclusions to package/repository endpoint deduplication, version continuity, graph depth, tie order, missing workflow evidence, and the identity unit?

The observed graph contains 25,228 package names, 88,113 unique package adjacency pairs, 121,885 versioned adjacency rows, 12,217 maintainer usernames, and 79,405 package-maintainer relationships. There are 15,233 package names with at least one positive workflow flag, mapping to 7,171 distinct normalized GitHub repository keys. Of these, 15,188 packages and 7,158 repositories are reachable from at least one observed maintainer portfolio. There are 3,081 package names with no observed maintainer mapping and 3,772 package names without a completed workflow-check flag. These are evidence gaps, not safe packages.

All package-projected reach includes each maintained seed package itself and follows reverse dependency adjacency: dependency to dependent. Exact strongly connected component condensation and integer bitsets compute unions, with no approximate sketches, sampled propagation, fitted labels, or learned scores. Repository keys use case-insensitive owner/name matching and remove a transport `.git` suffix; redirects and actual remote identity are unverified.

## Three distinct estimands

Let `P_m` be maintainer `m`'s observed package portfolio. Let `E_m` be the union of the portfolio's reverse-reachable endpoints, including its seed packages when the endpoint filter includes them. We evaluate all package names, positive-workflow package names, and positive-workflow repository keys separately. The repository mapping is deduplicated within and across portfolios.

For a set `S` of hardened identities:

- **Scenario exposure reduction:** `H(S) = sum_{m in S}|E_m| / sum_m|E_m|`. This assumes a hypothetical, mutually exclusive identity-loss scenario selected uniformly among all 12,217 observed usernames. A hardened identity's own scenario contributes zero exposure; the remaining source scenarios are unchanged. Ranking by exact `|E_m|` maximizes this additive objective at each equal-cost budget. This is a stipulated scenario weighting, not an empirical compromise probability or an estimate of real incidents prevented.
- **Prospective endpoint coverage:** `C(S) = |union_{m in S} E_m|`. This measures the distinct structural reach represented by selected control or review scenarios. It does not mean each covered endpoint is protected against every source identity. Maximum-marginal greedy optimizes this coverage objective approximately; exact union and greedy coverage are established techniques, not a new algorithm.
- **All-source exclusion:** define `A_e = {m : e in E_m}`. Then `P(S) = |{e : A_e is nonempty and A_e subset S}|`. Every observed source scenario that can structurally reach such an endpoint has been selected. Residual possible endpoint exposure is `|union_m E_m| - P(S)`. This is an all-source structural exclusion statistic, not proof of security or execution prevention. No method in this study is asserted to globally optimize this objective.

The `C(S) - P(S)` endpoints are prospectively covered but remain reachable from at least one unselected identity. Treating `C(S)` as a protection count would conflate these estimands.

## Baselines and fixed budgets

All primary methods use nested selections at budgets 1, 5, 10, 25, 50, and 100 identities:

- Portfolio size: the number of packages linked to a username.
- Summed package reach: sum of each owned package's reach count; overlap within the portfolio is double-counted by this baseline.
- Maximum package reach: largest reach count among owned packages.
- Exact union: size of the union across all owned packages; optimal for the equal-weight additive scenario objective.
- Greedy endpoint coverage: repeatedly add the identity with the largest newly covered endpoint set.
- Uniform random: 200 fixed independent seeds, sampling usernames without replacement. The same sampled order is reused across endpoint representations.

Deterministic ties use ascending username order internally; reversing that order is reported as a sensitivity. Names and individual selections are not exported. Random results have empirical means, sample standard deviations, and central 95% simulation ranges. These ranges describe random selection variability on the fixed snapshot; they are not sampling confidence intervals for npm or uncertainty intervals for real attacks. Exact finite-population random expectations are also computed from endpoint source multiplicities using hypergeometric probabilities.

## Main result at 100 identities

The budget is 0.819% of observed usernames. The table concerns 7,171 observed positive-workflow repository keys; 7,158 are reachable from some observed identity.

| Method | Distinct covered repositories | Coverage of observed positive repositories | Equal-scenario exposure reduction | All-source excluded repositories |
| --- | ---: | ---: | ---: | ---: |
| Portfolio size | 4,579 | 63.85% | 7.96% | 577 |
| Summed package reach | 4,835 | 67.42% | 21.98% | 704 |
| Maximum package reach | 4,268 | 59.52% | 33.59% | 533 |
| Exact maintainer union | 4,407 | 61.46% | 33.79% | 534 |
| Greedy endpoint coverage | 5,538 | 77.23% | 11.48% | 800 |
| Uniform random, mean of 200 orders | 1,680.605 | 23.44% | 0.804% | 12.78 |

The random coverage count's central 95% empirical range is 659.8 to 2,610.65. Fractional endpoints here arise from summarizing simulations, not from the graph measurement.

Greedy covers 25.66% more repositories than exact-union ranking at this budget, while its additive equal-scenario exposure reduction is substantially lower. Thus the methods answer different resource-allocation questions. Of greedy's 5,538 covered repositories, 4,738 remain reachable from at least one unselected identity. Only 800 satisfy the stipulated all-source exclusion condition, and 6,358 remain structurally reachable from unselected identities. Neither 5,538 nor 800 is an observed incident-prevention count.

At budget 25, greedy covers 4,854 positive-workflow repositories, versus 4,284 for exact union and 4,067 for portfolio size. The corresponding equal-scenario exposure reductions are 6.08%, 9.86%, and 4.38%. Cross-identity overlap is substantial: at budget 100, `1 - C(S)/sum_selected|E_m|` is 89.57% for greedy and 97.18% for exact-union ranking.

## Representation and visibility sensitivity

- **Version continuity:** the exact `(package, version)` graph has 40,806 nodes. Seeding every observed version of each maintained package and requiring version-node continuity changes 8,587 package-root closures. Maintainer positive-workflow repository unions change for 2,582 usernames; total identity-repository pairs fall from 462,170 to 266,016, a 42.44% decrease. The version graph still combines multiple retained resolution contexts; it is not an installed tree or a common-time reconstruction.
- **Selecting and evaluating on the version graph:** at budget 100, greedy covers 5,516 repositories and yields 13.10% equal-scenario exposure reduction with 817 all-source excluded repositories. Exact-union ranking covers 4,479, yields 40.59% equal-scenario reduction, and excludes all sources for 527. Package-projected greedy selected identities evaluated on the version graph cover 5,491. Distinct coverage is relatively stable at this aggregate budget, while additive pair mass is sensitive to representation.
- **Limited graph depth:** selecting greedy controls using portfolio endpoints alone covers 5,255 repositories when evaluated against full reverse reach; using one-hop evidence covers 5,488, compared with 5,538 for full-reach selection. All evaluation denominators are held fixed for this comparison.
- **Endpoint transfer:** selecting greedy controls for all-package coverage and then evaluating workflow repositories covers 5,308 repositories; selecting for workflow-package coverage covers 5,315. Direct repository-level selection covers 5,538. This isolates the consequence of deduplicating shared repositories.
- **Repository-link validity:** 60 positive version rows have stored repository keys inconsistent with a lexical parse of their original repository URLs. We exclude these positive observations conservatively, without transferring workflow flags to another repository. This removes 24 unique positive keys (7,171 to 7,147); greedy then covers 5,524 with 799 all-source excluded repositories. The positive workflow flag's actual provenance cannot be repaired without reacquisition. The total link mismatch count is 657 under `.git` normalization, while a raw-key comparison in the separate validity study counts 658.
- **Candidate exclusion:** excluding the 1, 5, or 10 largest portfolios from selectable controls, while retaining all original source scenarios and denominators, gives greedy coverage of 5,522, 5,149, and 5,076 repositories respectively. This is an eligibility sensitivity, not a classification of accounts as bots, organizations, or untrustworthy maintainers.
- **Shared email hashes:** merging identical stored hashes as a hypothetical control unit gives 12,147 groups rather than 12,217 usernames; 67 hash groups contain multiple usernames. At budget 100 groups, greedy still covers 5,538 repositories and has 800 all-source excluded repositories. A hash match is not independently validated common credential control, and the scenario denominator changes, so this is not an identity-resolution claim.
- **Tie order:** reversing identity order changes greedy repository coverage at budget 100 from 5,538 to 5,537, all-source exclusion from 800 to 793, and additive reduction by 0.457 percentage points. Other repository method outcomes at budget 100 are unchanged in this tie sensitivity.
- **Workflow visibility:** all linked repositories and workflow-check-attempted package endpoints are separate descriptive alternatives. A zero workflow flag can mean an unavailable repository as well as a missing directory. No negative flag is interpreted as verified workflow absence or as a trustworthy malicious/benign label.

## Completed validation and limitations

Independent breadth-first traversals verify 288 roots, including the 32 largest closures; all 25,228 package reach counts match stored database transitive counts. A separate forward propagation of source identity bitsets verifies endpoint incidence against reverse closure. Repository incidence checks, sum/max/union bounds, lazy-versus-exhaustive greedy on a toy case, monotone nested-budget curves, all-source exclusion being a subset of coverage, and the version-continuous reach subset relation all pass. The parent workflow also adds separate semantic tests for the estimand distinction.

The study establishes a reproducible structural comparison and its observation-unit sensitivity. It does not establish compromise probabilities, exploitability, actual CI execution, secret availability, publishing authorization, credential sharing, or causal effects of an identity control. Maintainer metadata and observed dependency adjacency are the experimental inputs; the snapshot is a convenience sample and is not the entire npm ecosystem. Collection timestamps, extraction-root provenance, remote redirect identities, workflow commits, and package-specific publisher permissions are unavailable. The positive-only workflow analysis avoids treating these gaps as verified absence.

## Machine-readable outputs

All outputs are under `manuscript/results/structural_interventions/`:

- `manifest.json`, `run_config.json`, `results.json`
- `deterministic_curves.csv`, `random_trials.csv`, `random_summary.csv`, `random_analytic_expectations.csv`
- `concentration.csv`, `ablations.csv`, `version_representation_curves.csv`
- `repository_mapping_sensitivity.csv`, `identity_grouping_sensitivity.csv`

The manuscript should use the authored voice (for example, “we constructed” and “our observed snapshot”) while retaining the explicit observational and hypothetical scope. Avoid references to “the provided SQL,” “the platform,” or an external author performing this study. Exact maintainer unions and greedy coverage must be positioned against prior work as established methods; the empirical contribution is the controlled comparison of distinct estimands, workflow/repository units, and representation/visibility sensitivities on our collected data.
