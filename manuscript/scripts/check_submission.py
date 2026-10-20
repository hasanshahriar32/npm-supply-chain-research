#!/usr/bin/env python3
"""Check observable PDF requirements; keep author/venue attestations separate.

Requires Poppler's pdfinfo, pdffonts, and pdftotext. A technical pass does not
certify the unresolved LLM policy, similarity, authorship, or submission status.
"""
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

PAPER = Path(__file__).resolve().parents[1]
pdf = PAPER / "main.pdf"
requirements = json.loads((PAPER / "submission_files/requirements.json").read_text())
for name in ("pdfinfo", "pdffonts", "pdftotext"):
    if not shutil.which(name):
        raise SystemExit(f"Required PDF inspection tool is missing: {name}")
if not pdf.exists():
    raise SystemExit("Compile main.tex before running PDF checks.")


def run(*args):
    return subprocess.check_output(args, text=True)


info = run("pdfinfo", str(pdf))
page_count = int(re.search(r"^Pages:\s+(\d+)", info, re.M).group(1))
pages_info = run("pdfinfo", "-f", "1", "-l", str(page_count), str(pdf))
sizes = [(float(w), float(h)) for w, h in re.findall(
    r"^Page\s+\d+ size:\s+([\d.]+) x ([\d.]+) pts", pages_info, re.M)]
font_info = run("pdffonts", str(pdf))
font_rows = [line for line in font_info.splitlines()[2:] if line.strip()]
fonts = [{"name": line.split()[0], "embedded": line.split()[-5] == "yes",
          "type_3": bool(re.search(r"\bType\s+3\b", line))} for line in font_rows]
text = run("pdftotext", str(pdf), "-")
normalized = " ".join(text.split())
author = re.search(r"^Author:\s*(.*)$", info, re.M)
author_value = author.group(1).strip() if author else ""
main = (PAPER / "main.tex").read_text()
metadata = (PAPER / "config/metadata.tex").read_text()
checks = {
    "page_limit": page_count <= requirements["max_pages_including_references"],
    "file_size": pdf.stat().st_size <= requirements["max_file_bytes"],
    "all_pages_a4": len(sizes) == page_count and all(
        abs(w-requirements["paper_width_pt"]) <= requirements["paper_tolerance_pt"] and
        abs(h-requirements["paper_height_pt"]) <= requirements["paper_tolerance_pt"] for w, h in sizes),
    "all_fonts_embedded": bool(fonts) and all(f["embedded"] for f in fonts),
    "no_type_3_fonts": bool(fonts) and not any(f["type_3"] for f in fonts),
    "ieee_conference_a4_10pt_source": bool(re.search(
        r"\\documentclass\[conference,a4paper,10pt\]\{IEEEtran\}", main)),
    "anonymous_author_block": "\\IEEEauthorblockN{Anonymous Authors}" in metadata and "Anonymous Authors" in normalized,
    "empty_pdf_author_metadata": not author_value,
    "no_local_home_paths_or_emails_in_pdf": not re.search(
        r"/home/|/Users/|[A-Za-z]:\\Users\\|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", text),
}
venue_policy_checks = {
    "llm_acknowledgment_present": bool(re.search(r"ACKNOWLEDG(?:E)?MENT", normalized, re.I))
        and bool(re.search(r"large language model|\bLLM\b|ChatGPT", normalized, re.I)),
}
author_record_path = PAPER / "submission_files/authors.json"
if author_record_path.exists():
    author_record = json.loads(author_record_path.read_text())
    checks["recorded_author_names_absent_from_review_pdf"] = all(
        author["name"] not in normalized for author in author_record["authors_in_supplied_order"])
    checks["recorded_institution_absent_from_review_pdf"] = author_record["institution"] not in normalized
log = PAPER / "build/main.log"
if log.exists():
    content = log.read_text(errors="replace")
    checks["no_unresolved_citations_or_references"] = not re.search(
        r"(?:Citation|Reference)\s+.*?undefined|There were undefined references", content)
    checks["no_overfull_boxes"] = "Overfull" not in content

report = {
    "venue": requirements["venue"], "stage": requirements["stage"],
    "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    "file_bytes": pdf.stat().st_size, "pages": page_count, "page_sizes_pt": sizes,
    "font_count": len(fonts), "fonts": fonts, "checks": checks,
    "technical_checks_pass": all(checks.values()), "submission_ready": False,
    "venue_policy_checks": venue_policy_checks,
    "venue_policy_checks_pass": all(venue_policy_checks.values()),
    "anonymity_scope": "Author block, PDF author metadata, local paths, and email patterns checked; indirect identification requires human review.",
    "llm_policy_status": requirements["llm_policy_status"],
    "similarity_check": "not performed; no similarity-service report is available",
    "author_actions_pending": requirements["author_actions_pending"],
    "guideline_hashes": {name: hashlib.sha256((PAPER/name).read_bytes()).hexdigest() for name in [
        requirements["local_guideline"], requirements["local_template_link"]]},
}
(PAPER / "results/submission_compliance.json").write_text(json.dumps(report, indent=2)+"\n")
print(f"PDF: {page_count} pages, {pdf.stat().st_size:,} bytes, {len(fonts)} fonts.")
for name, passed in checks.items():
    print(f"{'PASS' if passed else 'FAIL'} {name}")
for name, passed in venue_policy_checks.items():
    print(f"{'PASS' if passed else 'UNMET'} venue_policy.{name}")
print("Author/venue requirements remain pending; see results/submission_compliance.json.")
sys.exit(0 if report["technical_checks_pass"] else 1)
