# Bounded `@asyncapi/generator` July 2026 candidate screen

**Screen status:** candidate passes the finite exact-version, independent-corroboration, and preliminary separate-family gates; official npm registry metadata has **not** yet been accessed.

## Bounded source observations

Aikido lists `@asyncapi/generator@3.3.1` among the affected AsyncAPI releases and reports that the first compromised packages were published after a compromised workflow produced malicious commits in the `next` branch.[1] Microsoft independently lists `@asyncapi/generator@3.3.1` as affected and supplies a package-specific affected path and tarball SHA-256 as part of its incident analysis.[2] The strict affected-version target is the single-source intersection **`@asyncapi/generator@3.3.1`**. Other AsyncAPI packages named in either report are expressly outside this one-package screen.

## Candidate scope and relatedness boundary

The proposed family identifier is `asyncapi_github_actions_release_pipeline_compromise_2026`. Neither source documents a relationship to a governed family. Aikido notes a `prt-scan` pattern and Miasma-branding overlap with earlier Miasma tooling, but says definitive attribution is unclear; these observations do **not** establish operator identity, a complete campaign, or a relationship to any existing ledger family.[1] This candidate therefore remains a single bounded package-event lead pending the registry-only time-map and retained-predecessor evaluation.

## Pre-registry no-inference boundary

No npm registry request, package download, archive inspection, source extraction, installation, execution, version cutoff, pre-event source-object selection, dependency declaration, SemVer approximation, graph edge, control, benign label, historical installation, reach value, blast-radius value, authority value, score, rank, interval, calibration result, model, or predictive metric has been created. The source reports are used only to establish whether a finite independently corroborated candidate exists.

## References

[1]: https://www.aikido.dev/blog/asyncapi-npm-packages-backdoored-via-github-actions "Aikido, AsyncAPI npm packages backdoored via GitHub Actions"
[2]: https://www.microsoft.com/en-us/security/blog/2026/07/15/unpacking-asyncapi-npm-supply-chain-compromise-import-time-payload-delivery/ "Microsoft Security, Unpacking the AsyncAPI npm supply chain compromise and import-time payload delivery"
