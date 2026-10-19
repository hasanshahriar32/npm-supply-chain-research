# Literature extension and a defensible completed study

Reviewed on **20 October 2026**. This targeted review extends the earlier notes; it is not a systematic review and cannot establish an absence of all related work. Metadata and URLs appear in `2026-10-20_verified_sources.csv`. The mathematical consequences below are derived here from explicitly stated assumptions. They are not empirical findings, and numerical results must come from the new experiment outputs.

## The most important novelty correction

The full text of **Small World with High Risks** already defines maintainer reach as a union of package reach sets (Definition 3.6), then selects maintainers by greatest marginal union growth (Definition 3.8), explicitly identifying maximum coverage. Section 5.4 simulates influential-maintainer vetting. Thus a package–maintainer graph, account portfolio reach, overlap-aware greedy coverage, and a maintainer-hardening simulation are established methods, not new contributions. Our analysis should be described as an empirical replication and extension with different decision objectives. [Zimmermann et al., USENIX Security 2019](https://www.usenix.org/system/files/sec19-zimmermann.pdf), printed pp. 999 and 1006; PDF pp. 5 and 12.

**Defending the Core** studies package-node hardening in npm, combining degree/PageRank prioritization with dependency pruning. Its experiments include node-removal robustness and SI cascade simulations. The intervention model lets hardened nodes resist removal or inhibit propagation. Our source-account intervention has different semantics: it removes an account as a possible malicious publisher while leaving dependencies and other publishers intact. This is a useful distinction, not evidence of a new optimization algorithm. [Wang, arXiv:2606.14036v1, 2026](https://arxiv.org/html/2606.14036v1), Sections III-C and IV-C.

The strongest remaining question is therefore narrower: **How much does the preferred npm maintainer review queue change when the defender switches from broad downstream review coverage to reducing conditional account-compromise exposure, and how robust is that tradeoff to dependency depth, overlap, and repository-level workflow deduplication?** A completed, reproducible measurement of that question is more defensible than claiming a first graph method or a trained risk predictor. Novelty remains contingent on the measured findings and a broader related-work review.

## Closest research streams and boundaries

| Stream | Verified primary source | Implication for our study |
|---|---|---|
| npm metadata weak links | [Zahan et al., ICSE SEIP 2022](https://arxiv.org/abs/2112.10165v2) | Metadata hygiene is established background. Structural reach is neither proof of weak account security nor a compromise probability. |
| Workflow security | [Koishybayev et al., USENIX Security 2022](https://www.usenix.org/conference/usenixsecurity22/presentation/koishybayev) | Configuration analysis considers access and execution properties. A public workflow-directory observation has a much weaker meaning. |
| Workflow injection | [Muralee et al., ARGUS, USENIX Security 2023](https://www.usenix.org/conference/usenixsecurity23/presentation/muralee) | Static taint analysis evaluates actual input-to-execution paths. Our metadata does not establish an injection flaw or exposed secret. |
| Precise npm resolution | [Liu et al., ICSE 2022](https://arxiv.org/abs/2201.03981v2) | Package-level reachability differs from npm-resolved dependency trees. Describe the present graph as an observed structural projection. |
| Large-scale vulnerability propagation | [Robinson et al., AsiaCCS 2026 preprint](https://arxiv.org/abs/2604.17668v1) | Concentration of dependency vulnerability exposure already has recent ecosystem-scale evidence. We study a conditional account-origin scenario instead of advisory propagation. |
| Repository availability | [Tsakpinis and Pretschner, EASE 2024; revised preprint 2025](https://arxiv.org/abs/2404.17403v2) | Repository mapping availability varies with library importance. Missing workflow evidence can reflect selection or inaccessible repositories. |
| Release authority | [Santos-Grueiro, arXiv:2606.22593v2, 2026](https://arxiv.org/abs/2606.22593v2) | Public release-path changes are a distinct review surface. A maintainer list does not reconstruct that surface or prove release authority security. |
| Archival data | [Pinckney et al., npm-follower, 2023](https://arxiv.org/abs/2308.12545) | Retaining metadata and code as published addresses deleted artifacts; present-day snapshots cannot replace historical observations. |
| Historical resolution | [Rahman et al., CHRONO-RESOLUTION, 2026](https://arxiv.org/abs/2607.15315) | Release-point dependency resolution is already an explicit research artifact. Reuse matching resources for future temporal work rather than claiming that reconstruction itself is new. |
| Temporal prediction | [Shafin and Ahmed, PatchRisk, WI-IAT 2026 preprint](https://arxiv.org/abs/2609.13719) | Future advisory exposure forecasting already uses temporal and package-disjoint evaluation. A cross-sectional conditional simulation does not compete on predictive accuracy. |

Only directly verified pages are used here. The earlier SSRN-only SupplyTGN record is unnecessary to establish the boundary above; this extension does not rely on it or claim its results were reproduced.

## Separate the decision objectives before computing a score

Let `M` be the observed maintainer identities, `Q` the target packages, and `P(m)` the set of packages associated with account `m`. Let `R_m` contain the distinct targets reachable by following dependency edges in reverse from `P(m)`. Include the portfolio packages themselves if the scenario includes direct victims, and state that convention. For a depth limit `h`, restrict reverse paths to at most `h` edges. Let `A_q = {m : q in R_m}`, `w_q >= 0`, and `S` be a budget-limited selected set of accounts.

### 1. Breadth of downstream review coverage

`C(S) = sum_q w_q * 1[A_q intersects S]`.

This counts each target once even if many selected portfolios reach it. Adding an account contributes only targets not already covered. Consequently the objective is normalized, nondecreasing, and submodular. Repeatedly select the greatest marginal gain, with a documented deterministic tie rule. For equal-cost selections of at most `k` accounts, the standard greedy bound is `1 - (1 - 1/k)^k`, at least `1 - 1/e`, relative to optimal coverage. This is existing theory, not a new theorem or an observed optimality result. [Nemhauser, Wolsey, and Fisher, Mathematical Programming 14, 265–294, 1978](https://link.springer.com/article/10.1007/BF01588971).

The guarantee applies to this stated coverage objective and equal-cost budget. It does not show prevention, forecasting accuracy, or the optimality of an arbitrary weighted score. Greedy gain divided by unequal cost does not inherit the same guarantee without the relevant cost-constrained algorithm and assumptions.

### 2. Conditional expected exposure removed by ideal account hardening

Assume exactly one account is selected as the attack origin according to a fixed prior `pi_m`, with `sum_m pi_m = 1`. Conditional on an account compromise, every target in its footprint is structurally exposed. Perfectly hardening selected account `m` removes that origin; it does not block other origins or remove dependency edges. The expected weighted exposure removed is

`H(S) = sum_{m in S} pi_m * sum_{q in R_m} w_q`.

The objective is **modular**. For a uniform origin prior and unit account costs, descending weighted account reach is exactly optimal for this scenario. Overlap is appropriately counted across *mutually exclusive account-origin scenarios*, unlike union coverage within one review portfolio. With fixed account-specific efficacy `e_m`, replace each coefficient by `pi_m * e_m * reach_w(m)`; modularity still holds. No empirical compromise probabilities or intervention efficacies are supplied by the snapshot.

The residual expectation is `H_total - H(S)` under the same fixed prior, counting blocked attacks as zero rather than renormalizing the distribution onto unhardened accounts. An adaptive adversary selecting only remaining accounts is another scenario. Its worst-case footprint is `max_{m not in S} reach_w(m)`, and descending reach also minimizes that worst case under equal costs. These are scenario consequences, not guarantees of real security controls.

### 3. Targets with every observed origin removed

For targets with at least one observed account origin, define

`P(S) = sum_{q: A_q nonempty} w_q * 1[A_q subset S]`.

This is complete protection **within the idealized observed account-origin model**. The condition requires all upstream reachable accounts to be selected; selecting one account whose footprint contains a target is insufficient. This objective is generally supermodular: gains can increase after other necessary accounts have been selected. The maximum-coverage greedy guarantee does not apply. Targets with no observed origin must be excluded or handled as an explicit baseline, not counted as newly protected. Accounts absent from the data, alternate release paths, malicious contributors, and already compromised CI remain outside the model.

### A small counterexample

Account `a` reaches `{1,2,3,4}`, `b` reaches `{1,2,3}`, and `c` reaches `{5,6}`. At budget two, coverage greedy selects `a,c`: coverage is six, and summed account-origin exposure removed is six. Descending reach selects `a,b`: coverage is four, and summed account-origin exposure removed is seven. Under a uniform fixed single-account origin prior, the latter removes more expected exposure. This example is derived for explanation; it is not an npm observation.

## Workflow-associated targets need a second observation unit

For the package unit, set `w_q = 1` only for targets with a successfully observed public workflow directory. For a second unit, map those targets to normalized GitHub `(owner, repository)` keys and compute unions of **distinct repositories**. Report how many package targets collapse to each repository. A package count cannot be called a count of distinct workflows, builds, organizations, or machines. npm explicitly supports a `repository.directory` inside a shared repository, so the mapping need not be one-to-one. [npm, package.json repository documentation](https://docs.npmjs.com/cli/v11/configuring-npm/package-json/#repository).

Repository normalization should strip transport syntax, `.git`, trailing slashes, and subdirectory URL suffixes only through a documented parser. Preserve unresolved/conflicting mappings and missing observations as unknown. Do not silently count missing workflow observations as successful negatives. The package- and repository-based objectives should be compared at the same account budget, with each reported denominator.

Public CI hardening can include permissions, dependency controls, and authentication changes, but directory presence proves none of those properties. [GitHub, Secure use reference](https://docs.github.com/en/actions/reference/security/secure-use). npm documents OIDC trusted publishing as a workflow-specific alternative to long-lived tokens; merely observing workflows does not establish its adoption or exclude other authentication paths. [npm, Trusted publishing](https://docs.npmjs.com/trusted-publishers/).

## Feasible experiments and honest interpretation

1. Recompute account footprints from the original dependency and maintainer relations. Validate small hand-checked cases, cycles, and set-union behavior; independently cross-check graph traversal on sampled accounts.
2. Compare seeded-random accounts, portfolio count, direct-dependent reach, aggregated package PageRank, total account reach, and marginal coverage greedy. Define aggregation before running and preserve ties.
3. Report both `C(S)` and normalized `H(S)` at fixed, prespecified budgets. Include the maximum residual account footprint and complete-protection count when feasible. Avoid declaring a winner from whichever objective each queue was optimized to maximize.
4. Repeat for bounded depths and unrestricted reach, and for package versus unique workflow-associated repository targets. Distinguish graph semantics sensitivity from a probability model of malware transmission.
5. Use multiple seeded random draws and report their simulation variation. This is uncertainty in a randomized baseline, not a confidence interval for the sampled npm ecosystem. Deterministic graph quantities need no bootstrap merely to appear statistical.
6. Report overlap redundancy as `sum_m in S |R_m| - |union_m in S R_m|`, plus the ratio or percentage with a clear denominator. High redundancy is undesirable for breadth review but can be valuable for removing multiple independent origins to the same high-value target.
7. Preserve source hashes, inclusion rules, code versions, all queue outputs or stable private identifiers, and aggregate comparison tables. Keep account-security implications conditional and avoid naming accounts as likely attackers or likely victims.

The completed study can contribute **measured objective mismatch and sensitivity** on the collected npm sample. It cannot establish ecosystem representativeness, newly discovered compromise events, causal intervention effectiveness, machine privilege, or calibrated future attack risk. A negative result—little ranking difference, weak workflow specificity, or no broad advantage over reach—must be reported.

## Recommended author-voiced positioning

> We investigate how defensive objectives change maintainer prioritization in npm. We construct package–maintainer exposure sets from our collected graph and compare fixed-budget review queues for downstream coverage and conditional account-origin exposure reduction. We extend established maintainer-reach analysis with explicit objective comparisons, dependency-depth sensitivity, and a distinction between workflow-associated packages and distinct repositories. Our findings quantify decision tradeoffs in the observed sample; the analysis does not estimate compromise probabilities or the effectiveness of deployed security controls.

Use this wording only after the described experiments run. Replace references to “the supplied SQL,” “the platform,” or “the given repository” in the paper with the actual scientific object: **our dataset**, **our collection procedure**, **our observed dependency graph**, or **our experiment**. Preserve provenance in the artifact documentation without centering the paper on an editor's inspection of files.

## Search record and limitations

Queries covered npm maintainer reach, trusted-maintainer vetting, maximum coverage, centrality-based protection, workflow exposure, package/repository mapping, and temporal prediction. Full text was inspected for the two closest graph-hardening studies and the classic approximation result; primary abstract or publisher/conference metadata was checked for the other studies. arXiv records retain their preprint/version status; acceptance statements are attributed to those records. No cited experiments were independently reproduced. The only completed outputs of this literature task are this review and verified source metadata; numerical graph findings are produced by the separate experiment task.
