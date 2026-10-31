#!/usr/bin/env python3
"""Comprehensive Author Validation Audit Engine.

Evaluates all 120 endpoints against the 5 criteria from Author_Validation_Guide.md.
"""
import csv
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANIFEST_PATH = HERE / 'task_manifest.json'
EVIDENCE_DIR = HERE / 'evidence'
REG_DIR = EVIDENCE_DIR / 'registry'
GH_DIR = EVIDENCE_DIR / 'github_responses'
SRC_DIR = EVIDENCE_DIR / 'source_text'
OUTPUT_CSV = HERE / 'reviews' / 'Md_Ashikul_Islam_independent_labels.csv'

# 1. Build Registry Lookup
reg_lookup = {}
for p in REG_DIR.glob('*.json'):
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        pkg = data.get('package')
        ver = data.get('version')
        if pkg and ver:
            reg_lookup[(pkg, ver)] = (p.name, data)
    except Exception as e:
        pass

# 2. Read Manifest
manifest = json.loads(MANIFEST_PATH.read_text(encoding='utf-8'))
audit_rows = manifest['review_identity_rows']

results = []

for r in audit_rows:
    aid = r['audit_id']
    repo = r['repository']
    commit = r['commit_sha']
    mappings = r['original_mappings']
    
    sdir = SRC_DIR / aid
    
    notes_parts = []
    
    # Check if sdir exists (redirect check)
    if not sdir.exists():
        gh_commit_file = GH_DIR / f'{aid}__commit.json'
        redirect_msg = 'Unknown'
        if gh_commit_file.exists():
            gh_cdata = json.loads(gh_commit_file.read_text(encoding='utf-8'))
            cnt = gh_cdata.get('content', '')
            if 'Moved Permanently' in cnt:
                redirect_msg = 'GitHub API returned 301 Moved Permanently'
        
        note = (
            f"Mapping: {mappings[0]['package']}@{mappings[0]['version']} unresolved; tree uninspected due to {redirect_msg}. "
            f"Workflow: unknown (uninspected tree). "
            f"Install: unknown (uninspected tree). "
            f"Lock: unknown (uninspected tree). "
            f"Version: unknown (uninspected tree). "
            f"Unknown reasons: repository endpoint could not be inspected due to redirect."
        )
        results.append({
            'audit_id': aid,
            'repository': repo,
            'commit_sha': commit,
            'repository_mapping_supported': 'unknown',
            'workflow_file_present': 'unknown',
            'install_directive_observed': 'unknown',
            'lockfile_present': 'unknown',
            'dependency_version_supported': 'unknown',
            'evidence_notes': note
        })
        continue

    # --- Criterion 1: repository_mapping_supported ---
    all_pj = sorted(list(sdir.glob('package.json.txt')) + 
                    list(sdir.glob('packages/*/package.json.txt')) + 
                    list(sdir.glob('packages/*/*/package.json.txt')))
    pj_map = {}
    for pj in all_pj:
        try:
            pj_data = json.loads(pj.read_text(encoding='utf-8'))
            name = pj_data.get('name')
            if name:
                pj_map[name] = (pj.relative_to(sdir), pj_data)
        except Exception:
            pass

    map_supported = True
    map_unknown = False
    map_notes = []
    
    for m in mappings:
        pkg = m['package']
        ver = m['version']
        reg_file, reg_data = reg_lookup.get((pkg, ver), (None, {}))
        reg_repo = reg_data.get('repository', {})
        reg_repo_url = reg_repo.get('url', '') if isinstance(reg_repo, dict) else str(reg_repo)
        
        if pkg in pj_map:
            pj_rel, pj_data = pj_map[pkg]
            pj_ver = pj_data.get('version', '')
            map_notes.append(f"{pkg}@{ver} -> {pj_rel} (name='{pkg}', ver='{pj_ver}'); reg={reg_file}")
        else:
            # Check if root is monorepo workspace container
            root_pj = sdir / 'package.json.txt'
            is_monorepo = False
            root_name = ''
            if root_pj.exists():
                try:
                    rpj_data = json.loads(root_pj.read_text(encoding='utf-8'))
                    root_name = rpj_data.get('name', '')
                    if 'workspaces' in rpj_data or (sdir / 'pnpm-workspace.yaml.txt').exists() or 'monorepo' in root_name:
                        is_monorepo = True
                except Exception:
                    pass
            
            if is_monorepo:
                map_unknown = True
                map_supported = False
                map_notes.append(f"{pkg}@{ver} in monorepo '{root_name}' where subpackage manifest omitted from sample")
            else:
                # Contradiction
                map_supported = False
                map_notes.append(f"{pkg}@{ver} contradicts manifest name '{root_name}' (reg={reg_file})")

    if map_supported:
        c1_label = 'supported'
    elif map_unknown:
        c1_label = 'unknown'
    else:
        c1_label = 'unsupported'

    # --- Criterion 2: workflow_file_present ---
    wf_dir = sdir / '.github' / 'workflows'
    wf_files = sorted(list(wf_dir.glob('*.yml.txt')) + list(wf_dir.glob('*.yaml.txt'))) if wf_dir.exists() else []
    
    if wf_files:
        c2_label = 'supported'
        c2_note = f"{len(wf_files)} workflow files present at pinned commit: {wf_files[0].name.replace('.txt', '')}"
        if len(wf_files) > 1:
            c2_note += f" (+{len(wf_files)-1} more)"
    else:
        c2_label = 'unsupported'
        c2_note = "demonstrated absence: no workflow files found in .github/workflows/ at pinned commit"

    # --- Criterion 3: install_directive_observed ---
    install_regexes = [
        (re.compile(r'run:\s*.*(npm\s+ci)\b', re.IGNORECASE), 'npm ci'),
        (re.compile(r'run:\s*.*(pnpm\s+ci)\b', re.IGNORECASE), 'pnpm ci'),
        (re.compile(r'run:\s*.*(npm\s+install)\b', re.IGNORECASE), 'npm install'),
        (re.compile(r'run:\s*.*(pnpm\s+install)\b', re.IGNORECASE), 'pnpm install'),
        (re.compile(r'run:\s*.*(pnpm\s+i)\b', re.IGNORECASE), 'pnpm i'),
        (re.compile(r'run:\s*.*(yarn\s+install)\b', re.IGNORECASE), 'yarn install'),
        (re.compile(r'run:\s*.*(yarn\s+--frozen-lockfile)\b', re.IGNORECASE), 'yarn --frozen-lockfile'),
        (re.compile(r'run:\s*yarn\s*$', re.IGNORECASE), 'yarn'),
        (re.compile(r'run:\s*.*(npm\s+i)\b', re.IGNORECASE), 'npm i'),
        (re.compile(r'npm\s+ci\b', re.IGNORECASE), 'npm ci'),
        (re.compile(r'pnpm\s+ci\b', re.IGNORECASE), 'pnpm ci'),
        (re.compile(r'npm\s+install\b', re.IGNORECASE), 'npm install'),
        (re.compile(r'pnpm\s+install\b', re.IGNORECASE), 'pnpm install'),
        (re.compile(r'yarn\s+install\b', re.IGNORECASE), 'yarn install'),
        (re.compile(r'yarn\s+--frozen-lockfile\b', re.IGNORECASE), 'yarn --frozen-lockfile'),
        (re.compile(r'run:\s*.*(bun\s+install)\b', re.IGNORECASE), 'bun install'),
    ]

    c3_label = None
    c3_note = None

    for wf in wf_files:
        lines = wf.read_text(encoding='utf-8').splitlines()
        for idx, line in enumerate(lines):
            l_str = line.strip()
            for rgx, cmd_name in install_regexes:
                if rgx.search(l_str):
                    c3_label = 'supported'
                    c3_note = f"{wf.name.replace('.txt', '')} L{idx+1} command '{l_str}'"
                    break
            if c3_label:
                break
        if c3_label:
            break

    if not c3_label:
        # Check if external reusable workflow or composite action is used
        has_reusable = False
        reusable_name = ''
        for wf in wf_files:
            lines = wf.read_text(encoding='utf-8').splitlines()
            for line in lines:
                if 'uses:' in line and not any(k in line for k in ['actions/checkout', 'actions/setup', 'codecov', 'github/codeql-action']):
                    has_reusable = True
                    reusable_name = line.strip()
                    break
            if has_reusable:
                break
        
        if has_reusable:
            c3_label = 'unknown'
            c3_note = f"uses external/composite action ({reusable_name}); definition uninspected"
        else:
            c3_label = 'unsupported'
            c3_note = "no install command observed across inspected workflow files"

    # --- Criterion 4: lockfile_present ---
    lock_files = []
    if (sdir / 'package-lock.json.txt').exists():
        lock_files.append(('package-lock.json', sdir / 'package-lock.json.txt'))
    if (sdir / 'npm-shrinkwrap.json.txt').exists():
        lock_files.append(('npm-shrinkwrap.json', sdir / 'npm-shrinkwrap.json.txt'))
    if (sdir / 'pnpm-lock.yaml.txt').exists():
        lock_files.append(('pnpm-lock.yaml', sdir / 'pnpm-lock.yaml.txt'))
    if (sdir / 'yarn.lock.txt').exists():
        lock_files.append(('yarn.lock', sdir / 'yarn.lock.txt'))

    if lock_files:
        c4_label = 'supported'
        c4_note = f"{lock_files[0][0]} present at repository root"
    else:
        c4_label = 'unsupported'
        c4_note = "demonstrated absence: no lockfile present in pinned tree"

    # --- Criterion 5: dependency_version_supported ---
    if not lock_files:
        c5_label = 'unsupported'
        c5_note = "no lockfile available to verify resolved dependency version"
    else:
        # Collect manifest declared dependencies
        manifest_deps = {}
        for pj in all_pj:
            try:
                pj_d = json.loads(pj.read_text(encoding='utf-8'))
                for sec in ['dependencies', 'devDependencies', 'peerDependencies']:
                    if sec in pj_d and isinstance(pj_d[sec], dict):
                        for dn, ds in pj_d[sec].items():
                            manifest_deps[dn] = (sec, ds, pj.name.replace('.txt', ''))
            except Exception:
                pass

        c5_match = None
        lock_name, lock_path = lock_files[0]
        lock_txt = lock_path.read_text(encoding='utf-8')

        # Check npm lockfile
        if lock_name in ['package-lock.json', 'npm-shrinkwrap.json']:
            try:
                pld = json.loads(lock_txt)
                if 'packages' in pld and isinstance(pld['packages'], dict):
                    for dn, (sec, ds, pjn) in manifest_deps.items():
                        k = f"node_modules/{dn}"
                        if k in pld['packages'] and 'version' in pld['packages'][k]:
                            c5_match = (dn, sec, ds, pld['packages'][k]['version'], k, lock_name)
                            break
                if not c5_match and 'dependencies' in pld and isinstance(pld['dependencies'], dict):
                    for dn, (sec, ds, pjn) in manifest_deps.items():
                        if dn in pld['dependencies'] and 'version' in pld['dependencies'][dn]:
                            c5_match = (dn, sec, ds, pld['dependencies'][dn]['version'], dn, lock_name)
                            break
            except Exception:
                pass

        # Check pnpm lockfile
        elif lock_name == 'pnpm-lock.yaml':
            for dn, (sec, ds, pjn) in manifest_deps.items():
                pat = re.compile(r'[/\"\']?' + re.escape(dn) + r'@([0-9][0-9a-zA-Z\.\-\+]+)')
                m = pat.search(lock_txt)
                if m:
                    c5_match = (dn, sec, ds, m.group(1), m.group(0), 'pnpm-lock.yaml')
                    break

        # Check yarn lockfile
        elif lock_name == 'yarn.lock':
            # Check v1 format
            for dn, (sec, ds, pjn) in manifest_deps.items():
                pat_v1 = re.compile(re.escape(dn) + r'@[^:\n]+:\s*\n\s+version:?\s+[\"\']?([0-9][0-9a-zA-Z\.\-\+]+)')
                m = pat_v1.search(lock_txt)
                if m:
                    c5_match = (dn, sec, ds, m.group(1), f"{dn}@...", 'yarn.lock')
                    break
            # Check Berry format
            if not c5_match:
                for dn, (sec, ds, pjn) in manifest_deps.items():
                    pat_berry = re.compile(r'[\"\' ]?' + re.escape(dn) + r'@npm:[^:\n]+:\s*\n\s+version:\s*[\"\']?([0-9][0-9a-zA-Z\.\-\+]+)')
                    m = pat_berry.search(lock_txt)
                    if m:
                        c5_match = (dn, sec, ds, m.group(1), f"{dn}@npm:...", 'yarn.lock')
                        break

        if c5_match:
            c5_label = 'supported'
            c5_note = f"'{c5_match[0]}' ({c5_match[1]} '{c5_match[2]}') resolved to '{c5_match[3]}' in {c5_match[5]} ({c5_match[4]})"
        else:
            if not manifest_deps:
                c5_label = 'unsupported'
                c5_note = "no dependencies declared in manifest to match against lockfile"
            else:
                c5_label = 'unknown'
                c5_note = f"lockfile present ({lock_name}) but declared dependency could not be resolved"

    # Assemble structured evidence notes
    note = (
        f"Mapping: {'; '.join(map_notes)}. "
        f"Workflow: {c2_note}. "
        f"Install: {c3_note}. "
        f"Lock: {c4_note}. "
        f"Version: {c5_note}."
    )

    results.append({
        'audit_id': aid,
        'repository': repo,
        'commit_sha': commit,
        'repository_mapping_supported': c1_label,
        'workflow_file_present': c2_label,
        'install_directive_observed': c3_label,
        'lockfile_present': c4_label,
        'dependency_version_supported': c5_label,
        'evidence_notes': note
    })

# Write to review CSV with CRLF
fieldnames = ['audit_id', 'repository', 'commit_sha', 
              'repository_mapping_supported', 'workflow_file_present', 
              'install_directive_observed', 'lockfile_present', 
              'dependency_version_supported', 'evidence_notes']

with OUTPUT_CSV.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\r\n')
    writer.writeheader()
    writer.writerows(results)

print(f"Successfully audited {len(results)} endpoints.")
print("Summary of label counts:")
for field in ['repository_mapping_supported', 'workflow_file_present', 
              'install_directive_observed', 'lockfile_present', 
              'dependency_version_supported']:
    counts = {}
    for r in results:
        v = r[field]
        counts[v] = counts.get(v, 0) + 1
    print(f"  {field}: {counts}")
