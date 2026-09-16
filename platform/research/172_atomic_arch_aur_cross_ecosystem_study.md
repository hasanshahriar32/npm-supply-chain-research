# Atomic Arch and the AUR: Cross-Ecosystem Supply-Chain Study

**Status:** Governed contextual study; not a primary npm package-event admission.

## Executive conclusion

The June 2026 Atomic Arch campaign aligns strongly with this project’s research problem. It demonstrates a supply-chain path that begins with **ownership transfer in a community package repository**, crosses into the npm ecosystem through an install-time dependency, and targets developer credentials and build environments. Arch Linux’s official notice confirms a high volume of malicious package adoptions and updates in the Arch User Repository (AUR) and explicitly advises users to review all `PKGBUILD` and install-script changes.[1]

The event should **not** be inserted into the primary npm temporal ledger as an ordinary npm package-version observation. The delivery surface was AUR package metadata and build instructions. The npm package `atomic-lockfile` was a downstream execution component, not sufficient evidence that the npm registry event itself satisfies the project’s independent npm incident-label gates. The study therefore records Atomic Arch as a **cross-ecosystem contextual event** and a design input for a future multi-registry benchmark.

The reported count also requires careful wording. Early technical reporting described more than 400 hijacked AUR packages, while later reporting and Sonatype updates described approximately 1,500 affected packages across multiple waves.[2] [3] These figures are campaign-scope estimates, not a retained, version-level census. The project must not convert either number into a reach, blast-radius, prevalence, or model target.

## Is AUR or `yay` safe?

Neither AUR nor `yay` should be treated as equivalent to Arch’s official repositories. The AUR is a community repository of build recipes. An AUR helper such as `yay` automates retrieval, review, building, and installation; it does not independently establish that a recipe or its upstream downloads are trustworthy. In the Atomic Arch incident, attackers abused the AUR’s orphan-adoption process and altered trusted package build instructions so that installation fetched a malicious npm dependency.[2]

The practical conclusion is not that `yay` itself was the root cause or that every AUR package is malicious. The conclusion is that **the helper inherits the trust boundary of the AUR recipe and every command executed by that recipe**. A safe operating posture is therefore:

1. Prefer official Arch repository packages when they satisfy the requirement.
2. Treat every AUR package as an untrusted build script, including packages with an old name, download history, or apparently familiar maintainer.
3. Review the complete `PKGBUILD`, install scripts, source URLs, ownership changes, and meaningful diffs before an update. This is consistent with Arch’s incident guidance.[1]
4. Build and install AUR software in a disposable or separately confined environment when the package is not essential on the host.
5. Avoid granting unnecessary credentials, SSH agents, browser sessions, cloud tokens, or CI secrets to the build environment.
6. If a suspected package has executed, treat credentials available to that host as exposed and rebuild or re-provision according to incident-response policy. Sonatype specifically warns that removing the package may be insufficient after second-stage execution.[2]

These controls reduce risk; they do not turn AUR into a signed, centrally reviewed distribution channel. AUR and `yay` are therefore suitable for a risk-managed user who understands the execution boundary, but they are not “safe by default.”

## What Atomic Arch adds to the research

Atomic Arch is a useful stress test for the project’s selected multi-queue contribution because it exercises three queues at once.

| Research queue | Atomic Arch observation | What can be measured | What cannot be inferred |
|---|---|---|---|
| Release authority | Attackers appear to have adopted orphaned AUR packages and inherited names, history, and user trust.[2] | Ownership-transfer events, maintainer inactivity, predecessor-to-successor changes, and time from adoption to malicious update | A transfer is not itself evidence of compromise or user exposure |
| Install-time execution | Modified `PKGBUILD` logic invoked npm or Bun during package installation.[2] [3] | Presence and type of external package-manager calls, lifecycle hooks, network access, and build-script churn | A script’s presence does not establish execution, successful payload delivery, or victim count |
| Cross-registry propagation | AUR recipes pulled `atomic-lockfile`; technical analysis links its `preinstall` hook to a native payload.[2] [4] | Registry-to-registry dependency edges, first-observed timestamps, payload identity, and corroborated artifact relationships | A downstream npm component does not automatically become an independent npm incident label |

The campaign also exposes a gap in an npm-only benchmark: the package-manager graph is not the whole supply chain. A package may be benign in its own registry metadata while a downstream build recipe injects an external dependency at install time. Conversely, the presence of a malicious npm package in a cross-registry attack does not establish the historical population of AUR installations.

## Comparison with related events already in the cohort

Atomic Arch should be compared structurally with, not merged indiscriminately into, existing npm families.

**Axios** demonstrates a compromised npm publishing path in which a malicious dependency was added to affected releases. Sonatype explicitly compares the Atomic Arch technique with the Axios compromise because both use a trusted package or release to introduce a second malicious dependency.[2] The difference is the control plane: Axios is an npm publisher/release event, whereas Atomic Arch begins with AUR ownership and build-script control.

**Shai-Hulud** demonstrates a multi-package npm campaign whose package-level rows must be grouped by campaign family rather than treated as independent observations. Atomic Arch reinforces the same family-correlation problem, but its AUR-to-npm path means it should remain outside the npm primary ledger unless a future source set independently establishes exact npm release scope and npm event timing.

**`event-stream` and `node-ipc`** show why install-time behavior and maintainer intent must remain separate target dimensions. A destructive or credential-stealing payload may be technically clear while the release authority, affected-version scope, and family independence remain different questions. Atomic Arch adds a repository-stewardship dimension to this distinction.

The resulting methodological principle is: **join ecosystems for propagation analysis, but retain registry-specific label gates for primary outcome construction**.

## Evidence-gated adjudication

| Gate | Result | Rationale |
|---|---|---|
| Independent incident corroboration | Pass for contextual study | Arch’s official notice confirms the incident; Sonatype, SecurityWeek, StepSecurity, and an independent malware-analysis report provide complementary technical or timeline evidence.[1] [2] [3] [4] |
| Finite exact AUR package set | Fail for primary cohort | Public counts changed from hundreds to approximately 1,500 across waves; the available evidence is not a stable, version-level retained census.[2] [3] |
| Exact npm affected-version intersection | Not adjudicated here | This study intentionally avoids package-payload inspection and npm-ledger expansion. The presence of `atomic-lockfile` is recorded as a cross-registry relationship, not as a new primary npm row. |
| Strict pre-event npm source object | Not adjudicated here | No npm registry timestamp/cutoff reconstruction was performed for the contextual study. |
| Control population or historical installation evidence | Fail | The sources document attack mechanics and remediation, not a cutoff-valid control frame or observed installation population. |
| Primary temporal-ledger admission | Excluded | Admission would violate the current npm-only unit-of-analysis and all-stream source-object rules. |
| Future multi-registry benchmark value | Pass | The case motivates registry-aware release-authority and install-time propagation features. |

## Proposed extension

The most valuable follow-up is a **registry-agnostic propagation layer** attached to, but not merged with, the npm temporal benchmark. Its unit should be a package-manager execution edge: source repository, recipe or workflow, external package-manager command, exact referenced artifact, observed time, and evidence confidence. The layer should distinguish declaration from execution and should retain the originating registry separately from the fetched registry.

A future benchmark could test whether release-authority discontinuities and install-time external-fetch behavior improve review prioritization beyond package popularity and dependency topology. The primary outcomes should remain separate: confirmed compromise, malicious publication, and review surface. AUR adoption or a `PKGBUILD` change should be a review-surface feature, never a compromise label by itself.

The first implementation should be descriptive. It should measure queue overlap, missingness, temporal availability, cross-registry edge counts, and reviewer agreement. Predictive claims should wait until the project has independently adjudicated, cutoff-valid labels and a suitable negative or control frame across the participating ecosystems.

## Decision

**Atomic Arch is highly relevant to the research and should be retained as a governed cross-ecosystem case study. It is not admitted to the 47-record npm primary cohort.** The incident strengthens the project’s novelty argument: a defensible contribution can connect release authority, install-time execution, and registry-crossing propagation without collapsing them into an unsupported “attacker ROI” score.

## References

[1]: https://archlinux.org/news/active-aur-malicious-packages-incident/ "Arch Linux: Active AUR malicious packages incident"
[2]: https://www.sonatype.com/blog/atomic-arch-npm-campaign-adds-malicious-dependency "Sonatype: Atomic Arch attackers hijack trusted AUR packages"
[3]: https://www.securityweek.com/atomic-arch-supply-chain-attack-hits-1500-aur-packages/ "SecurityWeek: Atomic Arch supply-chain attack hits 1,500 AUR packages"
[4]: https://ioctl.fail/preliminary-analysis-of-aur-malware/ "Preliminary analysis of AUR malware"
[5]: https://www.stepsecurity.io/blog/400-aur-packages-hijacked-atomic-arch-campaign "StepSecurity: 400+ AUR packages hijacked"
[6]: https://lists.archlinux.org/archives/list/aur-requests@lists.archlinux.org/thread/CPGWM4B7DMEMETK7KVHFFPBBSZN6JP7K/?sort=date "Arch mailing list: Status of compromised packages after AUR attack"
[7]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7338168/ "A review of open source software supply-chain attacks"

## Author

**Manus AI**

**Retrieval date:** 2026-09-16
