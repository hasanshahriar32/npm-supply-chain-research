.PHONY: pdf authors-pdf audit figures reproduce verify submission-check package clean
pdf:
	bash compile.sh
	python3 scripts/check_submission.py
authors-pdf:
	bash compile.sh main_authors.tex
audit:
	python3 scripts/audit_artifacts.py
figures:
	python3 scripts/render_figures.py
reproduce:
	python3 scripts/audit_artifacts.py
	python3 scripts/render_figures.py
	python3 scripts/verify_manuscript.py
	bash compile.sh
	python3 scripts/check_submission.py
verify:
	python3 scripts/verify_manuscript.py
submission-check:
	python3 scripts/check_submission.py
package:
	python3 scripts/package_overleaf.py
clean:
	rm -rf build
