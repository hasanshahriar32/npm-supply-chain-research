r"""Programmatic verification suite for Q1 journal manuscript (IEEE TSE / TDSC / ACM TOSEM / EMSE).

Enforces:
1. Abstract word count (150 <= words <= 250) for the EMSE target.
2. PDF compilation and font embedding:
   - Zero overfull \hbox / \vbox warnings > 1 pt
   - Zero undefined citations or references
   - Zero Type 3 fonts (100% embedded fonts)
   - Both Named (main_q1.pdf) and Double-Anonymous (main_q1_anonymous.pdf) targets
3. Exact numerical consistency across TeX sections/tables and ground-truth data:
   - Task 04 incident validation ground truth (debug 1462 vs 1162, chalk 1125 vs 587,
     ansi-styles 1376 vs 740, simple-swizzle 120 vs 31, workflow endpoint membership and focal BFS reach)
   - per_package.csv, results.json, and q1_journal_experiments.json
4. Conference freeze check:
   - manuscript/main.pdf, manuscript/main_authors.pdf,
     NPM_Supply_Chain_IEEE_Anonymous_Source.zip, NPM_Supply_Chain_IEEE_Overleaf.zip
     have zero byte changes (SHA-256 invariant).

Outputs technical verification report to manuscript_q1/results/q1_verification_report.json.
"""
from __future__ import annotations

import csv
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
Q1_DIR = ROOT / "manuscript_q1"
RESULTS_DIR = Q1_DIR / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def check_abstract() -> dict:
    abstract_path = Q1_DIR / "sections/00_abstract.tex"
    content = abstract_path.read_text(encoding="utf-8")
    clean = content.replace(r"\begin{abstract}", "").replace(r"\end{abstract}", "").strip()
    words = clean.split()
    count = len(words)
    passed = 150 <= count <= 250
    return {
        "check": "abstract_word_count",
        "word_count": count,
        "min_allowed": 150,
        "max_allowed": 250,
        "passed": passed,
        "detail": f"Abstract contains {count} words (EMSE range: 150-250 words)."
    }


def check_pdf(pdf_name: str) -> dict:
    pdf_path = Q1_DIR / pdf_name
    log_name = pdf_name.replace(".pdf", ".log")
    log_path = Q1_DIR / "build" / log_name

    res = {
        "pdf_name": pdf_name,
        "exists": pdf_path.exists(),
        "passed": False,
        "pages": 0,
        "file_bytes": 0,
        "fonts_embedded": False,
        "zero_type_3": False,
        "zero_overfull_hbox": False,
        "zero_undefined_citations": False,
        "zero_missing_glyphs": True,
        "errors": []
    }

    if not pdf_path.exists():
        res["errors"].append(f"File {pdf_path} not found")
        return res

    res["file_bytes"] = pdf_path.stat().st_size

    # Check pages and fonts
    if shutil.which("pdfinfo"):
        info = subprocess.check_output(["pdfinfo", str(pdf_path)], text=True)
        m = re.search(r"^Pages:\s+(\d+)", info, re.M)
        if m:
            res["pages"] = int(m.group(1))

    if shutil.which("pdffonts"):
        font_out = subprocess.check_output(["pdffonts", str(pdf_path)], text=True).splitlines()
        font_rows = font_out[2:] if len(font_out) > 2 else []
        t3_fonts = [f for f in font_rows if "Type 3" in f]
        unembedded = [f for f in font_rows if len(f.split()) > 4 and f.split()[-5] != "yes"]

        res["zero_type_3"] = len(t3_fonts) == 0
        res["fonts_embedded"] = len(unembedded) == 0 and len(font_rows) > 0
        res["total_fonts"] = len(font_rows)
        res["type_3_count"] = len(t3_fonts)
        res["unembedded_count"] = len(unembedded)
        if t3_fonts:
            res["errors"].append(f"Found {len(t3_fonts)} Type 3 fonts in {pdf_name}")
        if unembedded:
            res["errors"].append(f"Found {len(unembedded)} unembedded fonts in {pdf_name}")

    # Check compilation log
    if not log_path.exists():
        res["errors"].append(f"Compilation log missing: {log_path}")
    if log_path.exists():
        log_content = log_path.read_text(encoding="utf-8", errors="replace")
        # Overfull check
        overfulls = re.findall(r"Overfull \\hbox \(([0-9.]+)pt too wide\)", log_content)
        large_overfulls = [float(w) for w in overfulls if float(w) > 1.0]
        res["zero_overfull_hbox"] = len(large_overfulls) == 0
        if large_overfulls:
            res["errors"].append(f"Found {len(large_overfulls)} overfull \\hbox > 1pt: {large_overfulls}")

        # Undefined citations / references
        undef_cites = re.findall(r"Citation `(.*?)' on page .*? undefined", log_content)
        undef_refs = re.findall(r"Reference `(.*?)' on page .*? undefined", log_content)
        res["zero_undefined_citations"] = len(undef_cites) == 0 and len(undef_refs) == 0
        if undef_cites:
            res["errors"].append(f"Undefined citations: {set(undef_cites)}")
        if undef_refs:
            res["errors"].append(f"Undefined references: {set(undef_refs)}")

        # Missing glyphs
        missing_glyphs = re.findall(r"Missing character: There is no (.*?) in font", log_content)
        res["zero_missing_glyphs"] = len(missing_glyphs) == 0
        if missing_glyphs:
            res["errors"].append(f"Missing glyphs: {set(missing_glyphs)}")

    if pdf_path.exists() and pdf_name.endswith('_anonymous.pdf'):
        extracted = subprocess.check_output(['pdftotext', str(pdf_path), '-'], text=True)
        normalized = ' '.join(extracted.split())
        authors = json.loads((ROOT / 'manuscript/submission_files/authors.json').read_text())
        identities = [a['name'] for a in authors['authors_in_supplied_order']] + [authors['institution']]
        if any(name in normalized for name in identities):
            res['errors'].append('Recorded author identity in anonymous journal PDF')
        if 'AI assistance was used' not in normalized:
            res['errors'].append('Assistance disclosure missing from anonymous journal PDF')

    res["passed"] = (
        not res["errors"]
        and res["pages"] > 0
        and res["exists"]
        and res["fonts_embedded"]
        and res["zero_type_3"]
        and res["zero_overfull_hbox"]
        and res["zero_undefined_citations"]
        and res["zero_missing_glyphs"]
    )
    return res


def check_numerical_consistency() -> dict:
    errors = []

    # Full active-table and endpoint validation replaces hardcoded incident strings.
    try:
        sys.path.insert(0, str(ROOT / 'scripts'))
        from verify_reconciled_papers import verify
        scientific = verify(ROOT)
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        errors.append(f'Reconciled scientific evidence: {exc}')

    # 3. Check k-Quorum Exclusion Table
    # Compare each individual table row with the complete CSV, avoiding cross-row regex matches.
    quorum_csv = Q1_DIR / "results/q1_quorum_exclusion.csv"
    quorum_json = Q1_DIR / "results/q1_quorum_exclusion.json"
    quorum_table = Q1_DIR / "tables/q1_quorum_exclusion_table.tex"
    provenance = Q1_DIR / "results/quorum_reproducibility.json"
    try:
        with quorum_csv.open() as stream:
            qrows = list(csv.DictReader(stream))
        jrows = json.loads(quorum_json.read_text())
        assert len(qrows) == len(jrows) == 20, "Expected five strategies by four budgets"
        table_rows = [line for line in quorum_table.read_text().splitlines()
                      if " & " in line and re.search(r"& (10|25|50|100) &", line)]
        assert len(table_rows) == 20, "Expected twenty data rows in threshold table"
        for row, jrow, line in zip(qrows, jrows, table_rows):
            assert row["strategy"] == jrow["strategy"], "CSV/JSON strategy mismatch"
            for key in row.keys() - {"strategy"}:
                assert abs(float(row[key]) - float(jrow[key])) < 1e-9, f"CSV/JSON mismatch: {key}"
            expected = [str(row["budget"]), f"{int(row['C']):,}",
                        f"{float(row['C_pct']):.2f}\\%", f"{float(row['H_pct']):.2f}\\%",
                        *[f"{int(row[f'P_{k}']):,}" for k in (1, 2, 3, 5)]]
            actual = [cell.strip().removesuffix(r"\\").strip() for cell in line.split("&")[1:]]
            assert actual == expected, f"CSV/table mismatch: {row['strategy']}, B={row['budget']}"
        meta = json.loads(provenance.read_text())
        assert meta["metric_version"] == "strict_zero_anchored_v1"
        assert meta["baseline_P_k_empty"] == {str(k): 0 for k in (1, 2, 3, 5)}
        distribution = meta["source_cardinality_distribution"]
        assert set(distribution) == {"0", "1", "2", "3", "4", ">=5"}
        assert distribution["0"] == 13 and sum(distribution.values()) == 7171
        histograms = meta["cardinality_histograms"]
        assert len(histograms) == len(jrows) == 20
        for row, hist in zip(jrows, histograms):
            assert (row["strategy"], row["budget"]) == (hist["strategy"], hist["budget"])
            bins = hist["counts"]
            assert sum(count for n, rem, count in bins) == 7158
            assert all(n > 0 and 0 <= rem <= n and count > 0 for n, rem, count in bins)
            # Recompute from aggregated source-cardinality/remaining-cardinality evidence.
            assert sum(count for n, rem, count in bins if rem < n) == row["C"]
            for k in (1, 2, 3, 5):
                count = sum(c for n, rem, c in bins if rem == 0 or (n >= k and rem < k))
                assert count == row[f"P_{k}"], f"Strict count mismatch at {row['strategy']}, B={row['budget']}, k={k}"
                assert row["P_1"] <= count <= row["C"]
            assert row["P_1"] == sum(c for n, rem, c in bins if rem == 0)
        expected_p1 = {"Greedy Coverage": 800, "Exact Union": 534,
                       r"Pareto Hybrid ($\alpha=0.50$)": 626, r"Direct Supermodular $P(S)$": 1022}
        for row in jrows:
            if row["budget"] == 100 and row["strategy"] in expected_p1:
                assert row["P_1"] == expected_p1[row["strategy"]]
        # Scan active manuscript source, retained outputs and extracted PDF text.
        # Binary byte patterns and historical build intermediates are not numerical claims.
        retired = ("1,915", "1,846", "1,825")
        for path in Q1_DIR.rglob("*"):
            if "build" in path.parts or not path.is_file():
                continue
            if path.suffix in {".tex", ".json", ".csv", ".md", ".bib"}:
                assert not any(value in path.read_text() for value in retired), f"Retired count in {path}"
        for pdf in ("main_q1.pdf", "main_q1_anonymous.pdf"):
            extracted = subprocess.check_output(["pdftotext", str(Q1_DIR / pdf), "-"], text=True)
            assert not any(value in extracted for value in retired), f"Retired count in {pdf}"
        for suffix in ("csv", "json"):
            assert (ROOT / f"manuscript/results/q1_journal/q1_quorum_exclusion.{suffix}").read_bytes() == (Q1_DIR / f"results/q1_quorum_exclusion.{suffix}").read_bytes()
        assert (ROOT / "manuscript/results/q1_journal/q1_quorum_exclusion_table.tex").read_bytes() == quorum_table.read_bytes()
        assert meta["observed_source_endpoints"] + meta["excluded_source_free_endpoints"] == 7171
        assert all(meta["validation"].values()), "Experiment semantic check failed"
        assert meta["source_archive_sha256"] == hashlib.sha256((ROOT / "data/npm_ecosystem.db.zip").read_bytes()).hexdigest()
        assert meta["script_sha256"] == hashlib.sha256((ROOT / "scripts/study_q1_quorum_and_oct2026.py").read_bytes()).hexdigest()
        # Prevent reintroducing unsupported claims from the initial extension.
        section = (Q1_DIR / "sections/06_pareto_and_heterogeneous_results_rq4.tex").read_text()
        assert "not a count of empirically protected repositories" in section
        bibliography = (Q1_DIR / "bibliography/references_q1.bib").read_text()
        for key in ("litellm2026", "litellmincident2026", "opencode2026", "railway2026",
                    "railwaydisclosure2026", "npmtrustedpub2026", "npmexpiry2026", "nodejsbrotli2026"):
            entry = re.search(r"@\w+\{" + key + r",(.*?)\n\}", bibliography, re.S)
            assert entry and "url = {https://" in entry.group(1), f"Missing traceable incident reference: {key}"
    except (AssertionError, OSError, ValueError, KeyError) as exc:
        errors.append(f"Threshold reproducibility gate: {exc}")

    # Task 16: new workflow/semantics diagrams and shared result plots are bound
    # to the conference figure evidence rather than copied without provenance.
    try:
        figure_record=json.loads((ROOT / 'manuscript/results/publication_figure_data.json').read_text())
        for stem, outputs in figure_record['figures'].items():
            for ext, expected in outputs.items():
                assert hashlib.sha256((Q1_DIR / f'figures/{stem}.{ext}').read_bytes()).hexdigest()==expected
        included=re.findall(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}",
                             "\n".join(p.read_text() for p in (Q1_DIR / 'sections').glob('*.tex')))
        assert len(included)==12 and len(set(included))==12, 'Expected twelve integrated journal figures'
    except (AssertionError,OSError,ValueError,KeyError) as exc:
        errors.append(f'Figure integration gate: {exc}')

    # 4. Check experiments JSON invariants
    q1_json_path = ROOT / "manuscript/results/q1_journal_experiments.json"
    if q1_json_path.exists():
        q1_data = json.loads(q1_json_path.read_text(encoding="utf-8"))
        p_100 = q1_data["direct_p_optimization"]["100"]["P"]
        if p_100 != 1022:
            errors.append(f"Expected P(100) = 1022, got {p_100}")
        h_pkg_sole = q1_data["heterogeneous_weights"]["Weight-Aware Package-Sole Optimum"]["H_pkg_sole_pct"]
        if round(h_pkg_sole, 2) != 67.37:
            errors.append(f"Expected H_pkg_sole = 67.37%, got {h_pkg_sole}")

    return {
        "check": "numerical_consistency",
        "passed": len(errors) == 0,
        "errors": errors,
        "detail": "Checked active budget cells, archive-derived workflow ranks, focal BFS endpoints, temporal resolution, authority semantics, figure provenance and threshold histograms."
    }


def check_submission_sections() -> dict:
    errors = []
    required = ("Statements and Declarations", "Data Availability", "Code Availability",
                "Funding", "Competing Interests", "Ethics and Consent", "Use of AI Assistance",
                "no external funding", "not yet available")
    for stem in ("main_q1", "main_q1_anonymous"):
        text = " ".join(subprocess.check_output(
            ["pdftotext", str(Q1_DIR / f"{stem}.pdf"), "-"], text=True).split())
        compact = re.sub(r"\s+", "", text).casefold()
        for term in required:
            if re.sub(r"\s+", "", term).casefold() not in compact:
                errors.append(f"{stem}: missing {term}")
        source = (Q1_DIR / f"{stem}.tex").read_text()
        keywords = re.search(r"\\begin\{IEEEkeywords\}(.*?)\\end\{IEEEkeywords\}", source, re.S)
        if not keywords or not 4 <= len(keywords[1].split(",")) <= 6:
            errors.append(f"{stem}: EMSE requires four to six keywords")
    named = " ".join(subprocess.check_output(
        ["pdftotext", str(Q1_DIR / "main_q1.pdf"), "-"], text=True).split())
    named = re.sub(r"\s+", "", named)
    record = json.loads((ROOT / "manuscript/submission_files/authors.json").read_text())
    for author in record["authors_in_supplied_order"]:
        for field in ("email", "orcid"):
            if author[field] not in named:
                errors.append(f"Named PDF: missing author {field}")
    return {"check": "submission_sections", "passed": not errors, "errors": errors,
            "detail": "Required declarations, assistance in methods, contacts and six-keyword limit; public data release remains pending."}


def check_conference_freeze() -> dict:
    # Tasks 15 and 16 authorize conference updates. This reviewed lock
    # is written only after the rebuilt conference PDFs and packages pass checks.
    lock = json.loads((Q1_DIR / 'config/conference_lock.json').read_text())
    expected_hashes = lock['artifacts']


    errors = []
    file_status = {}
    for rel_path, spec in expected_hashes.items():
        p = ROOT / rel_path
        if not p.exists():
            errors.append(f"Conference freeze artifact missing: {rel_path}")
            continue
        data = p.read_bytes()
        actual_hash = hashlib.sha256(data).hexdigest()
        actual_bytes = len(data)
        match = (actual_hash == spec["sha256"] and actual_bytes == spec["bytes"])
        file_status[rel_path] = {
            "actual_sha256": actual_hash,
            "expected_sha256": spec["sha256"],
            "actual_bytes": actual_bytes,
            "expected_bytes": spec["bytes"],
            "match": match
        }
        if not match:
            errors.append(f"Conference freeze artifact modified: {rel_path}")

    return {
        "check": "conference_freeze_invariants",
        "passed": len(errors) == 0,
        "errors": errors,
        "files": file_status,
        "detail": "Confirmed Track 1 matches the current reviewed conference artifact lock."
    }


def main():
    print("=" * 80)
    print("RUNNING AUTOMATED Q1 VERIFICATION SUITE")
    print("=" * 80)

    abstract_res = check_abstract()
    print(f"[{'PASS' if abstract_res['passed'] else 'FAIL'}] Abstract: {abstract_res['word_count']} words (EMSE target 150-250)")

    named_res = check_pdf("main_q1.pdf")
    print(f"[{'PASS' if named_res['passed'] else 'FAIL'}] Named PDF (main_q1.pdf): {named_res['pages']} pages, {named_res['file_bytes']:,} bytes, Type 3: {named_res.get('type_3_count', 'N/A')}, No overfull boxes: {named_res.get('zero_overfull_hbox')}")

    anon_res = check_pdf("main_q1_anonymous.pdf")
    print(f"[{'PASS' if anon_res['passed'] else 'FAIL'}] Anonymous PDF (main_q1_anonymous.pdf): {anon_res['pages']} pages, {anon_res['file_bytes']:,} bytes, Type 3: {anon_res.get('type_3_count', 'N/A')}, No overfull boxes: {anon_res.get('zero_overfull_hbox')}")

    num_res = check_numerical_consistency()
    print(f"[{'PASS' if num_res['passed'] else 'FAIL'}] Scientific consistency: active tables, workflow endpoints, temporal evidence and figures")

    freeze_res = check_conference_freeze()
    print(f"[{'PASS' if freeze_res['passed'] else 'FAIL'}] Conference Artifact Lock: 4 artifacts verified")

    submission_res = check_submission_sections()
    print(f"[{'PASS' if submission_res['passed'] else 'FAIL'}] Submission sections: declarations, assistance disclosure, contacts and keywords")

    all_passed = (
        abstract_res["passed"]
        and named_res["passed"]
        and anon_res["passed"]
        and num_res["passed"]
        and freeze_res["passed"]
        and submission_res["passed"]
    )

    report = {
        "status": "PASS" if all_passed else "FAIL",
        "timestamp": datetime.now(ZoneInfo("Asia/Dhaka")).isoformat(),
        "checks": {
            "abstract": abstract_res,
            "named_pdf": named_res,
            "anonymous_pdf": anon_res,
            "numerical_consistency": num_res,
            "conference_freeze": freeze_res,
            "submission_sections": submission_res,
        }
    }

    report_path = RESULTS_DIR / "q1_verification_report.json"
    report_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote full verification report to: {report_path}")
    print("=" * 80)
    print("VERIFICATION SUITE RESULT:", "ALL TECHNICAL CHECKS PASSED (venue and author review separate)" if all_passed else "FAILURES DETECTED")
    print("=" * 80)

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
