"""Build a linked index of frozen evidence without exposing machine labels."""
from pathlib import Path
import hashlib
import html
import json
import re
from urllib.parse import quote

HERE = Path(__file__).resolve().parent


def main():
    sample = json.loads((HERE / 'task_manifest.json').read_text())['review_identity_rows']
    packet = (HERE / 'Evidence_Packet.md').read_text()
    chunks = re.split(r'(?m)^## (A\d{3}) — ', packet)[1:]
    bodies = {chunks[i]: chunks[i + 1] for i in range(0, len(chunks), 2)}
    toc, sections = [], []
    for row in sample:
        aid, repo, commit = [row[k] for k in ['audit_id', 'repository', 'commit_sha']]
        toc.append(f'<a href="#{aid}">{aid}: {html.escape(repo)}</a>')
        parts = [f'<section id="{aid}"><h2>{aid} — {html.escape(repo)}</h2>']
        if re.fullmatch('[0-9a-f]{40}', commit or ''):
            parts.append(f'<p>Pinned commit: <a href="https://github.com/{repo}/tree/{commit}">{commit}</a></p>')
        else:
            parts.append('<p>Commit acquisition unresolved. Inspect the retained request record; do not substitute current HEAD.</p>')
        state = HERE / 'evidence/github_responses' / (aid + '__commit.json')
        for candidate in sorted((HERE / 'evidence/github_responses').glob(aid + '*')):
            if '__file_' not in candidate.name:
                rel = candidate.relative_to(HERE).as_posix()
                parts.append(f'<p><a href="{quote(rel)}">Retained request: {html.escape(candidate.name)}</a></p>')
        parts.append('<h3>Original package/version mappings</h3><ul>')
        for m in row['original_mappings']:
            package, version = m['package'], m['version']
            key = hashlib.sha256((package + '@' + version).encode()).hexdigest()[:24]
            local = 'evidence/registry/' + key + '.json'
            api = 'https://registry.npmjs.org/' + quote(package, safe='') + '/' + quote(version, safe='')
            parts.append(f'<li><strong>{html.escape(package + "@" + version)}</strong>; '
                         f'<a href="{local}">retained registry evidence</a>; '
                         f'<a href="{api}">live version-specific API</a><br>'
                         f'Original repository field: <code>{html.escape(m["original_repository_url"])}</code></li>')
            assert (HERE / local).is_file(), local
        parts.append('</ul><h3>Commit-pinned file evidence</h3><ul>')
        for path, url, source in re.findall(r'- \[([^\]]+)\]\(([^)]+)\); retained response `([^`]+)`', bodies[aid]):
            local = 'evidence/github_responses/' + Path(source).name
            text = 'evidence/source_text/' + aid + '/' + path + '.txt'
            parts.append(f'<li><code>{html.escape(path)}</code>: '
                         f'<a href="{html.escape(url, quote=True)}">GitHub pinned source</a>; '
                         f'<a href="{quote(local)}">retained response JSON</a>')
            if (HERE / text).is_file():
                parts.append(f'; <a href="{quote(text)}">readable source text</a>')
            parts.append('</li>')
            assert (HERE / local).is_file(), local
        parts.append('</ul><p>Record judgments and notes in your own CSV, not in this index.</p>'
                     '<a href="#top">Back to index</a></section>')
        sections.append(''.join(parts))
    assert len(sections) == 120
    page = '''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Author evidence index: 120 endpoints</title><style>body{max-width:1000px;margin:40px auto;padding:0 22px;font:17px/1.6 system-ui;color:#182d3e}a{color:#075884}nav{columns:3;font-size:14px}nav a{display:block}section{margin:45px 0;padding-top:15px;border-top:1px solid #bbc9d0}code{overflow-wrap:anywhere;font-size:13px}h1,h2,h3{line-height:1.25}@media(max-width:700px){nav{columns:1}}</style></head><body id="top"><h1>Author evidence index: 120 endpoints</h1><p>Prepared 28 October 2026. Read Author_Validation_Guide.pdf first. Use browser Find for an audit ID. This index includes frozen request records and readable source files, without automated label suggestions. Retained files work offline after extracting the entire task ZIP. Live API responses may differ from the frozen observations.</p><p>Each author independently reviews the same 120 rows. Missing or failed acquisition is not automatically an unsupported label.</p><nav>'''
    (HERE / 'Evidence_Index.html').write_text(page + ''.join(toc) + '</nav>' + ''.join(sections) + '</body></html>')
    print('Built 120-endpoint index with checked local evidence links.')


if __name__ == '__main__':
    main()
