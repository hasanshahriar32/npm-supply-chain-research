"""Check the corrected EMSE files against applicable, machine-checkable rules.

Author consent, actual contribution roles and editorial decisions cannot be
established by this script. They are deliberately not synthesized.
"""
from pathlib import Path
from datetime import datetime
from zoneinfo import ZoneInfo
import hashlib
import json
import re
import subprocess
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def main():
    tex = (HERE / 'source/EMSE_Manuscript.tex').read_text()
    pdf = HERE / 'EMSE_Manuscript.pdf'
    text = ' '.join(subprocess.check_output(['pdftotext', str(pdf), '-'], text=True).split())
    title_text = ' '.join(subprocess.check_output(['pdftotext', str(HERE / 'EMSE_Title_Page.pdf'), '-'], text=True).split())
    build = json.loads((HERE / 'validation.json').read_text())
    checks = {'clean_build_and_pdf_checks': build['passed'],
              'abstract_150_to_250_words': 150 <= build['abstract_words'] <= 250,
              'four_to_six_keywords': 4 <= build['keywords'] <= 6,
              'springer_template_author_year_style': r'\documentclass[pdflatex,sn-basic]{sn-jnl}' in tex,
              'no_fourth_level_headings': r'\paragraph{' not in tex and r'\subsubsubsection' not in tex,
              'ai_use_disclosed_in_methods': 'OpenAI Codex was used' in text,
              'absence_of_manual_validation_explicit': 'indicators were not manually validated' in text,
              'funding_competing_interests_data_code_in_article': all(x in text for x in
                  ['Funding', 'Competing Interests', 'Data Availability', 'Code Availability']),
              'declarations_and_acknowledgments_on_title_page': all(x in title_text for x in
                  ['Statements and Declarations', 'Funding', 'Competing Interests', 'Data Availability', 'Acknowledgments']),
              'title_page_no_stale_review_status': 'is under review elsewhere' not in title_text,
              'figure_caption_style': r'\captionsetup[figure]{name=Fig.,labelfont=bf,labelsep=space}' in tex,
              'doi_links_are_full_urls': r'\url{https://doi.org/#1}' in (HERE / 'build/EMSE_Manuscript.bbl').read_text(),
              'internal_workflow_notes_removed': all(x.casefold() not in text.casefold() for x in
                  ['initially blank', 'review sheets', 'remain pending', 'await independent',
                   'No reviewer role', 'authors must review', 'human audit pending'])}
    for kind in ('fig', 'tab'):
        labels = re.findall(r'\\label\{(' + kind + r':[^}]+)\}', tex)
        refs = re.findall(r'\\ref\{(' + kind + r':[^}]+)\}', tex)
        checks[kind + '_all_cited'] = set(labels) <= set(refs)
        checks[kind + '_first_citations_in_number_order'] = list(dict.fromkeys(refs)) == labels
    authors = json.loads((ROOT / 'manuscript/submission_files/authors.json').read_text())
    checks['author_names_contacts_orcids_match'] = all(
        a['name'] in text and all(a[k] in title_text for k in ('name', 'email', 'orcid'))
        for a in authors['authors_in_supplied_order'])
    with zipfile.ZipFile(HERE / 'EMSE_LaTeX_Source.zip') as archive:
        members = archive.namelist()
        checks['flat_complete_archive'] = (archive.testzip() is None and
            all('/' not in x for x in members) and
            {'EMSE_Manuscript.tex', 'EMSE_Manuscript.bbl', 'references_q1.bib', 'sn-jnl.cls', 'sn-basic.bst'} <= set(members))
        checks['figures_named_by_number'] = {x for x in members if x.endswith('.pdf')} == {
            f'Fig{i}.pdf' for i in range(1, build['figures'] + 1)}
        checks['archive_matches_current_sources'] = all(archive.read(x) == (
            HERE / 'build' / x if x.endswith('.bbl') else HERE / 'source' / x).read_bytes() for x in members)
    form = (HERE / 'form_metadata.txt').read_text().split('ABSTRACT\n', 1)[1].split('\n\nKEYWORDS', 1)[0]
    checks['portal_abstract_matches_current_source'] = form.replace('%', r'\%').replace('–', '--') in (
        ROOT / 'manuscript_q1/sections/00_abstract.tex').read_text()
    report = {'checked_at': datetime.now(ZoneInfo('Asia/Dhaka')).isoformat(),
              'guidelines_url': 'https://link.springer.com/journal/10664/submission-guidelines',
              'status': 'PASS' if all(checks.values()) else 'FAIL', 'checks': checks,
              'author_controlled_items': {
                  'actual_contribution_roles_confirmed': False,
                  'both_authors_approval_confirmed': False,
                  'note': 'The optional contribution statement is omitted. No author approval or manual review was invented.'},
              'scientific_validation': 'Automated endpoint indicators were not manually validated; this limitation is retained.',
              'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in
                  [pdf, HERE / 'EMSE_Title_Page.pdf', HERE / 'EMSE_LaTeX_Source.zip', HERE / 'form_metadata.txt']}}
    (HERE / 'guideline_review/checks.json').write_text(json.dumps(report, indent=2) + '\n')
    for name, passed in checks.items():
        print(('PASS ' if passed else 'FAIL ') + name)
    if not all(checks.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
