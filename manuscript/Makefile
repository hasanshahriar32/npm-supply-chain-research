.PHONY: pdf authors-pdf both audit study profile figures reproduce verify submission-check package clean
pdf:
	bash compile.sh
	python3 scripts/check_submission.py
authors-pdf:
	bash compile.sh main_authors.tex
both:
	bash compile.sh --both
	python3 scripts/check_submission.py
	python3 scripts/check_author_versions.py
audit:
	python3 scripts/audit_artifacts.py
study:
	python3 ../scripts/validate_research_study.py
	python3 ../scripts/validate_observation_semantics.py
	python3 ../scripts/study_structural_interventions.py
	python3 ../scripts/study_graph_validity.py
	python3 ../scripts/check_identifier_scope.py
figures:
	python3 scripts/render_research_figures.py
profile:
	python3 ../scripts/profile_structural_study.py
reproduce:
	python3 scripts/audit_artifacts.py
	$(MAKE) study
	python3 scripts/render_research_figures.py
	python3 scripts/verify_manuscript.py
	bash compile.sh --both
	python3 scripts/check_submission.py
	python3 scripts/check_author_versions.py
verify:
	python3 scripts/verify_manuscript.py
submission-check:
	python3 scripts/check_submission.py
package:
	python3 scripts/package_overleaf.py
	python3 scripts/validate_packages.py
clean:
	rm -rf build
