# Provenance of the 120-endpoint labels and author records

The two 120-row assessment sheets committed on the author-validation branch were produced by Python programs. Running those programs on the retained files reproduced both historical sheets byte for byte. The current programs write their results as rule A and rule B under the [generated evidence directory](../tasks/author_validation_2026-10-28/generated_evidence/). The old revision is available at commit `eb62a6c0ee35`.

Rule A marked 106 repository mappings, 115 workflows, 101 installation directives, 70 lockfiles and 70 version examples as supported. These counts describe the script's output on the sample. Their interpretation depends on the extraction rules and available artifacts. Report 28 records the comparison with rule B.

The old session log, contribution table and approval form attributed manual work and confirmation to named authors. The repository does not substantiate those attributions. The approval form also associated one hash with two different PDFs. The archived Editorial Manager copy has SHA-256 prefix `e6cf7faf3534` and the local export has prefix `5e64bfc1c649`. The generated labels do not appear as a human audit in either file.

The active task directory uses the original unfilled forms from the October packet. Author contributions and approval of any specific submission require each author's own account. The older filled records are preserved in Git history.
