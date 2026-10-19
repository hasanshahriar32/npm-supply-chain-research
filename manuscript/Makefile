.PHONY: pdf audit figures reproduce verify package clean
pdf:
	bash compile.sh
audit:
	python3 scripts/audit_artifacts.py
figures:
	python3 scripts/render_figures.py
reproduce:
	python3 scripts/audit_artifacts.py
	python3 scripts/render_figures.py
	python3 scripts/verify_manuscript.py
	bash compile.sh
verify:
	python3 scripts/verify_manuscript.py
package:
	python3 scripts/package_overleaf.py
clean:
	rm -rf build
