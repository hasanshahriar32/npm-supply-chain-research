# Ethics and Responsible Disclosure

## Research boundary

This project is a defensive study of package and CI/CD structural risk. It should not develop, test, or publish credential theft, persistence, lateral movement, malware deployment, or evasion procedures. The project may analyze publicly documented incidents and benign synthetic examples, but it must not contact attacker infrastructure or execute untrusted package code outside a controlled, approved environment.

## Data minimization

Collect only fields necessary for the research question. Prefer package names, version identifiers, aggregate maintainer reach, repository identifiers, workflow configuration features, and public incident metadata. Do not publish maintainer email addresses, raw hashes that enable cross-dataset linkage without justification, access tokens, secrets, private repository content, personal contact details, or machine-specific indicators that are not needed for the evaluation.

If hashed identifiers are retained, document the hashing and salting policy and assess whether the values can be linked to external datasets. Aggregated maintainer features are preferable to publishing person-level mappings.

## Safe analysis

Do not install or execute real malicious packages. Static analysis should operate on archived artifacts without executing package lifecycle scripts. If dynamic behavior must be studied, use synthetic packages or institutionally approved malware-analysis infrastructure with no external network access and no secrets. Use inert placeholders for domains, credentials, and payloads in examples.

The supplied executive-summary draft proposes Docker isolation and disabled networking. These safeguards are useful but are not sufficient by themselves for untrusted-code execution; the final methodology should require explicit review, pinned images, resource limits, no host mounts containing secrets, and a disposable environment.

## Incident reporting

If the research discovers a previously unknown active compromise or a new vulnerable configuration, stop broad collection, preserve evidence safely, notify the affected maintainer or registry through an appropriate security channel, and follow coordinated-disclosure expectations. Do not publish actionable indicators before a mitigation path is available unless a competent authority or affected party has already released them.

## Reproducibility versus harm

Reproducibility does not require publishing malware, exploit chains, secret values, or instructions for compromise. Release schemas, synthetic fixtures, aggregate features, hashes, safe parsers, and evaluation code. Keep sensitive raw artifacts private and document their provenance and exclusion.

## Human-subject and organizational considerations

Maintainer usernames and repository associations are public but can still become personal-risk data when ranked as high-value targets. Avoid naming individual maintainers in research outputs unless essential and supported by a public source. Obtain institutional review or supervisor guidance if the project includes interviews, surveys, or analysis of non-public organizational information.

## Reporting language

Use neutral descriptions such as “associated with a documented compromise,” “publicly observable workflow exposure,” and “structural reach.” Avoid sensational labels such as “best target,” “easy victim,” or “optimal attacker entry point” in public-facing artifacts unless tightly qualified and necessary for the research question.

## References

[1]: https://docs.github.com/en/actions/reference/security/secure-use "GitHub workflow security guidance"
[2]: https://google.github.io/osv.dev/ "OSV documentation"
[3]: https://www.cisa.gov/news-events/alerts/2026/04/20/supply-chain-compromise-impacts-axios-node-package-manager "CISA Axios response guidance"
