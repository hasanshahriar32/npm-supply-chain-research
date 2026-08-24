# Enhancement Verification

## Interactive benchmark charts

On 2026-08-20, an authenticated Clerk administrator loaded `/workspace/benchmark-findings`. The protected dashboard rendered the real repository snapshot values and interactive charts derived from all 25,228 records in `data/metrics_summary.csv.zip`: blast-radius frequency, packages with the highest observed transitive reach, and top attacker-ROI proxy values. The page includes the required evidence caveat that these deterministic structural metrics are not model-performance or exploitation predictions.

## Separate administration and ingestion

The authenticated administrator loaded `/admin` in a distinct dark-masthead console, separate from the research workspace frame. The console displayed its governance summary and one real pending snapshot created from the private repository metrics archive by the new authenticated ingestion route.

## Signed-in homepage behavior

An authenticated Clerk administrator visiting `/` was redirected server-side to `/workspace/literature-review`, preventing the public landing page from displaying a misleading sign-in action to an already signed-in user.

## Once-daily ingestion readiness

The Vercel configuration contains exactly one daily cron entry: `0 3 * * *` (03:00 UTC). An authenticated manual invocation retrieved the private-repository metrics archive and its paired benchmark manifest, staged snapshot `3` as pending, and recorded the composite source revision. A repeat invocation returned `skipped`, confirming idempotence for the same repository revision. The Git author was updated to `ashikulislamcf2000@gmail.com`; the pushed feature commit uses that address.

The live standalone administrator console subsequently displayed two pending source-backed snapshots, confirming that staged ingestion results remain visible for administrator review rather than appearing as automatically published benchmark data.

## Approval workflow validation

With explicit administrator confirmation, the live Reviews interface accepted the clearly labelled **Workflow Validation Record** and displayed it with a `pending` status. The validation record is used only to confirm the platform's governed state transitions.

The administrator then selected **Approve**; the live interface refreshed to show the record in the separate `approved` state, demonstrating that approval does not automatically publish content.

Finally, the administrator selected **Publish**. The record remained visibly labelled `published` in the Reviews queue, completing a verified `pending → approved → published` transition while leaving the validation record available for later inspection.

## Role, responsive, and deployment readiness

The administrator procedure tests confirm that promotion calls update both Clerk public metadata and PostgreSQL, while rejecting an administrator's attempt to remove their own role. The administrator console and chart suite both include a dedicated `max-width: 900px` layout: chart and console grids collapse to one column, console forms stack, approval actions wrap, and the workspace provides horizontally scrollable mobile navigation.

The committed `vercel.json` contains precisely one ingestion schedule, `0 3 * * *`, for `/api/cron/research-ingestion`. Vercel activates that schedule automatically when this GitHub revision is deployed to its production environment. The production Vercel project must have `CRON_SECRET`, `GITHUB_TOKEN`, `POSTGRES_DATABASE_URL`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, and `CLERK_SECRET_KEY` configured before its first scheduled run.

## Managed production packaging

The legacy full-stack publishing adapter initially expected `dist/public` while the Next.js build emitted only `.next`. The build now bundles a production Next request-handler server to `dist/index.js` and emits the required nonempty `dist/public` marker. The full suite passed with **22 tests across 9 files**, the production build completed, and the bundled server returned HTTP `200` with the landing-page marker when run against the deployment-style `PORT` environment variable.

## Research-gap program publication

On 2026-08-20, an authenticated administrator opened `/workspace/gap-analysis` after the research-source registry was updated. The live workspace rendered the new **“From ‘Attack-ROI Prediction’ to an Auditable npm Defense Benchmark”** report, including its executive assessment, related-work table, real-data audit, incident anchors, separate structural/CI/CD/authority queues, evaluation design, roadmap, references, and in-page navigation. This confirms the completed research artifacts are served through the governed platform rather than only stored in the repository.

The same authenticated session loaded `/workspace/methodology`, which rendered the **“A Multi-Queue, Time-Aware Benchmark for Defensive Prioritization in the npm Supply Chain”** protocol and its research decision, falsifiable questions, feature-availability ledger, distinct review queues, label hierarchy, split controls, and model ladder.

The `/workspace/incident-labels` view remained available in the same session and visibly presented the Shai-Hulud campaign and version-specific Axios anchor, together with the governing rule that all future records retain a package/version or range, incident family, event and detection times, evidence URLs, confidence, and an explicit inclusion or exclusion reason.

The `/workspace/benchmark-findings` section continued to render its authenticated interactive real-data cards and charts for 25,228 packages, 121,885 dependency edges, 12,217 maintainers, and workflow coverage. It displayed the non-predictive caveat that the structural metrics are not model-performance or exploitation claims, consistent with the new research program’s evidence boundary.

Finally, `/workspace/experiment-results` showed the **Current-snapshot interpretable audit** in the measured-comparison table and explicitly labelled it as a cross-sectional descriptive result rather than a temporal compromise prediction. The version-aware graph comparison remained planned and the heterogeneous graph attention model remained blocked until labels, temporal snapshots, and baselines are reproducible.

The managed production URL `https://supplyhub-mfhdnapy.manus.space/` was also opened successfully after checkpoint `6d007df8`. It served the finalized public landing page, including the research-position statements, 25,228-package index, documented Shai-Hulud and Axios anchors, and Clerk sign-in entry point. This verifies that the Next.js runtime packaging repair supports the managed production deployment; it does not substitute for the still-separate Vercel environment and cron activation steps.

After publishing the static marker asset in checkpoint `c6751c57`, the production URL `https://supplyhub-mfhdnapy.manus.space/__next_runtime_marker__.txt` returned the exact nonempty text `Next.js runtime handles dynamic application routes.` This explicitly verifies the hosted `dist/public`/Next public-static artifact contract in addition to the dynamic landing-page runtime.

## Vercel production verification

Using the connected Vercel project `cvehub`, the production deployment `dpl_HgzTGiLhwYRRYBpcCA29jhp63rzs` was confirmed `READY` with source type `git`, target `production`, framework `nextjs`, repository `ashik-hstu/npm-supply-chain-research`, root build path `/vercel/path0/platform`, and the corrected Git author email. Its build log completed the Next.js build successfully and listed the deployed `/api/cron/research-ingestion` route. The production static marker at `https://cvehub.vercel.app/__next_runtime_marker__.txt` returned HTTP 200 with the expected body; an unauthenticated request to `https://cvehub.vercel.app/api/cron/research-ingestion` returned HTTP 401 `{\"error\":\"unauthorized\"}`, confirming that the deployed daily endpoint is reachable but remains correctly protected outside Vercel’s scheduler.

After authenticated browser login, Vercel’s **Cron Jobs** settings showed the feature as `Enabled` and exactly one production job, `/api/cron/research-ingestion`, scheduled as `0 3 * * *` at 03:00 UTC. Its **Environment Variables** settings listed the required keys `CRON_SECRET`, `GITHUB_TOKEN`, `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY`, `CLERK_SECRET_KEY`, and `POSTGRES_DATABASE_URL`; secret values were not viewed or recorded.

The variable details further confirmed that all five required keys are assigned to **Production and Preview**. `CLERK_SECRET_KEY` and `POSTGRES_DATABASE_URL` are marked Sensitive; the remaining key values stayed masked throughout the verification.

## Live access-roster verification

Using the connected user browser, the authenticated administrator console loaded successfully and reported `Active researchers: 1`. The only synchronized user is the current administrator, so a real non-self promotion cannot be exercised without first having another researcher authenticate through Clerk. No user role was altered during this inspection.

The console’s **Access** tab was then opened directly. Its roster contained only `MD. ISLAM` (`ashikulislamcf2000@gmail.com`) with the existing `admin` role and an administrative role selector. This confirms that self-demotion protection must remain untested live until a distinct account joins; no role-change selector was used.

An isolated Clerk account named **Governance Validation** was then created for the authorized role-management test using a reserved verification identity and synchronized to PostgreSQL as a researcher. The live administrator overview subsequently changed from one to two active researchers, confirming that the non-self account is present in the governance roster before promotion.

The Access tab then displayed **Governance Validation** with the `researcher` role. Its selector was changed to `Administrator` by the current `MD. ISLAM` administrator. After the mutation completed, the same live roster displayed `admin` for both accounts. This confirms the non-self administrator workflow completed through the exact interface used by the platform; the current administrator’s role was unchanged.

The authenticated **Clerk Dashboard** then opened the isolated account’s own record. Its public metadata explicitly showed `role: "admin"` alongside `purpose: "isolated-role-promotion-verification"`. This is direct Clerk-side evidence that the live Access mutation synchronized the promotion to both the external identity record and the platform’s PostgreSQL roster; the verification account remains preserved for auditability.

The authenticated **GitHub** browser then verified the private repository’s `master` branch at commit `3163208ae656025d0c3428b1189d5df97d9090d3`, titled `feat: verify Clerk governance promotion`. The repository showed the synchronized `platform/` directory updated by that commit, confirming that the governance-validation scripts, verification notes, and tracker state were pushed under the corrected author identity.

## Temporal reconstruction publication — 2026-08-24

The temporal builders were run against official npm registry metadata and the independently adjudicated package-event ledger. They generated seven strict pre-event source-version snapshots from eight package-event records in four incident families, together with 20 declared runtime direct-dependency edges. The generated graph manifest records **zero** resolved target versions and **zero** computed transitive-reach values; it explicitly prohibits interpreting the artifact as a lockfile, package-manager resolution, transitive graph, historical centrality measure, or blast-radius estimate.

The temporal baseline gate was also executed on the exact snapshots. It records descriptive values only and blocks direct-dependency and package-age ranking, logistic regression, probability calibration, PR-AUC, and Recall@K because no cutoff-valid adjudicated control population exists, only seven exact snapshots are retained, only four independent incident families are represented, and current structural/workflow data cannot be backdated as historical features.

An authenticated Clerk administrator then opened `/workspace/incident-labels` in the protected development workspace. The rendered page showed the existing Shai-Hulud and Axios anchors plus the expanded 2021 Node.js, `event-stream`, and ESLint summaries. It also rendered the **Temporal Incident-Label Adjudication Register**, its eight package-event rows, event-family cautions, primary evidence links, and explicit non-negative-label boundary. This confirms that the expanded temporal incident evidence is served through the governed interface, not merely committed as repository files.

The same authenticated session opened `/workspace/experiment-results`. The measured-comparisons table displayed the **Pre-event metadata and declared-edge audit** as a completed feasibility result with eight records, seven exact pre-event snapshots, 20 declared edges, and no inferred target versions, transitive reach, controls, rankings, calibration, or model-performance metrics. The research queue displayed the resolver-dependent comparison as `blocked`, citing the validation/acquisition boundary and the August 2024 scope of the 10.2 GB CHRONO-RESOLUTION archive. The rendered report repeated the no-fit conclusion and the four-family grouping constraint.

After validating the isolated range-resolution extension, the same authenticated administrator loaded `/workspace/gap-analysis`. The published findings rendered **20 isolated cutoff-valid SemVer target approximations** alongside the seven exact source snapshots and 20 exact direct declarations. The visible report labels these target selections as approximations rather than lockfiles or package-manager traces, states that transitive reach remains zero, and retains the block on ranking, calibration, PR-AUC, Recall@K, logistic regression, blast-radius, and attack-return inference. The page also rendered the source-version correction for `eslint-scope@4.0.0`, matching the reproducible snapshot ledger.

The protected `/workspace/methodology` page also loaded successfully after the final source audit. It continues to render the principal time-aware benchmark protocol, including its strict historical-fidelity requirements and prohibition on treating dependency reach as exploitability. The completed temporal reconstruction, range-approximation, and archive-inspection implementation status is separately published through Gap Analysis and Experiment Results, with a concise implementation amendment added to the protocol source before final synchronization.

The Methodology page was reloaded after that amendment. Its in-page navigation now includes **“Temporal implementation amendment — 24 August 2026,”** confirming that the protected protocol itself exposes the eight-record/four-family pilot, seven exact source snapshots, 20 direct declarations, 20 explicitly approximate direct-range selections, the no-fit inference gate, and the 10.23 GB compressed / 138.73 GB uncompressed CHRONO-RESOLUTION relation-payload boundary.

After the bounded full-stream acquisition attempt, the same protected Methodology page was reloaded once more. The rendered amendment retained the archive schema boundary and now states that the memory-bounded one-pass stream timed out after 1,500 seconds with 7.6569% of the compressed member received and zero candidate rows retained. It continues to require bulk compute or an upstream filtered export before any transitive reconstruction is attempted.

The final authenticated Methodology reload rendered the additional control-population boundary: npm-follower is identified as a relevant but 20+ TB source without an available official query or frozen filtered export in this environment. The publication explicitly rejects treating registry rows with no known incident as benign controls and requires a frozen incident-coverage source plus documented at-risk population before temporal ranking or calibration work.

The protected `/workspace/gap-analysis` page was validated after the next-stage evidence work. Its rendered in-page navigation includes **“Bounded recursive registry-graph sensitivity”** and **“Explicit-label corpus control-frame review.”** The visible findings report 45 depth-bounded registry-only sensitivity edges, retain the prohibition on reach/blast-radius/model interpretation, and disclose the explicit-label corpus attrition result—9 retained malicious rows versus 1,093 retained benign rows—before reiterating the no-fit decision for ranking and calibration.

The protected `/workspace/incident-labels` page was then validated after the DataDog positive-manifest review. The rendered register exposes **“Human-vetted positive-catalogue overlap”**, reports one exact affected-version corroboration, one version-unspecified package membership, six absent packages with no conclusion, and zero new primary labels or controls. The primary CISA, Mandiant, npm, and ESLint evidence anchors and their family assignments remain unchanged.

The authenticated `/workspace/incident-labels` page was revalidated after the dated OpenSSF/SafeDep source review. It renders the independent `node-ipc 2026` summary, its three affected releases, the `node_ipc_2026` family, and the complete nine-record/five-family adjudication table. It also exposes both new evidence references and keeps the strict cutoff, non-negative-label, and no-control boundaries visible. The refreshed DataDog overlap reports two exact affected-version memberships, one version-unspecified membership, six absences with no conclusion, and zero new primary labels or controls.

The protected `/workspace/gap-analysis` page was then revalidated. Its rendered findings now state eight exact pre-event snapshots from nine package-event records in five incident families, 24 direct declarations and isolated range approximations, and 59 bounded registry-only sensitivity edges. The page visibly retains the distinctions from package locks, historical installed trees, transitive reach, blast radius, and predictive metrics; it also reports the one-record shortfall to the strict positive threshold and the absent cutoff-valid control population.

The authenticated `/workspace/methodology` page was also revalidated. Its temporal implementation amendment is present in the rendered protocol and states the nine-record/five-family expansion, `node-ipc@12.0.0` pre-event reconstruction, 24 exact direct declarations, and 59-edge bounded sensitivity artifact. It explicitly preserves the one-record positive shortfall, the missing cutoff-valid control population, and the prohibition on ranking, calibration, or blast-radius claims.

The authenticated `/workspace/incident-labels` page was revalidated after the independent SafeDep/OpenSSF `@emcd-vue/auth` review. It renders the tenth package-event record and sixth incident family, identifies the earliest malicious `6.4.8` publication as the strict cutoff, and states that this event remains label-only because no usable pre-cutoff registry version object is retained. The rendered register correctly keeps the benchmark at eight exact source snapshots, 24 exact direct declarations, zero added controls, and no predictive result.

After reconciling the baseline diagnostic schema, the authenticated `/workspace/incident-labels`, `/workspace/gap-analysis`, and `/workspace/methodology` pages were revalidated. They consistently distinguish ten adjudicated package-event records in six incident families from eight exact pre-event source snapshots across five feature-available families. The rendered research sources retain 24 exact direct declarations, 59 bounded registry-only sensitivity edges, zero cutoff-valid controls, and the explicit no-ranking/no-calibration/no-blast-radius decision.

The authenticated `/workspace/methodology` page was revalidated after the provider-backed control-frame assessment. Its implementation amendment explains that deps.dev offers snapshot and package-version provenance fields but its advisory coverage is vulnerability-oriented, records the no-credential HTTP 401 probe with zero retrieved rows, and preserves the rule that advisory or catalogue absence cannot create a benign temporal control.

The authenticated `/workspace/gap-analysis` page was then reloaded after publication. Its rendered in-page navigation now exposes **“Provider-backed control-frame assessment,”** and the visible content records the BigQuery access and target-coverage limits, zero controls created, the Figshare/Mendeley exclusion, and the preserved no-fit conclusion.

The authenticated `/workspace/incident-labels` page was revalidated after the bounded Shai-Hulud second-wave assessment. It visibly renders the Shai-Hulud summary with the single version-level `wenk` record, the complete eleven-record/seven-family register, `wenk@1.0.9` and `1.0.10`, the `wenk@1.0.8` pre-cutoff source state, and the rule that this bounded admission neither establishes campaign completeness nor creates a control observation.

The authenticated `/workspace/gap-analysis` page was revalidated after the same update. The rendered report shows eleven package-event records, seven adjudicated families, nine exact source snapshots, 24 direct declarations, and 59 bounded registry-only sensitivity edges. It continues to state that two records are label-only, no cutoff-valid controls exist, and no predictive, calibration, ranking, blast-radius, or attack-return result has been fitted.

The authenticated `/workspace/methodology` page was also revalidated. Its temporal implementation amendment renders the eleven-record/seven-family state, nine exact snapshots across six exact-snapshot families, the bounded `wenk` source reconstruction, and the unchanged block on calibration or ranking because no cutoff-valid control frame is available.

The authenticated `/workspace/gap-analysis` page was revalidated after publication of the control-frame contract. Its in-page navigation exposes **“Control-frame contract and public snapshot access assessment,”** and the rendered findings explicitly exclude the monolithic Zenodo GitHub-only snapshot, unauthenticated and target-mismatched deps.dev path, and current scraped Libraries.io metadata. The page retains zero valid controls and the no-model decision.
