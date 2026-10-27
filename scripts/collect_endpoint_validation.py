#!/usr/bin/env python3
"""Prepare and summarize commit-pinned endpoint evidence via a GitHub tool bridge.

GitHub requests are exported for the connected GitHub fetch tool. Registry requests
use the public version-specific npm endpoint. No package payload is executed.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import csv
import hashlib
import json
from pathlib import Path
import re
import urllib.error
import urllib.parse
import urllib.request

from journal_revision_common import ROOT, OUT, dump, sha, stamp
from research_observations import parse_github_repository

AUDIT = OUT / 'endpoint_audit'
RESP = AUDIT / 'github_responses'
REG = AUDIT / 'registry'
SAMPLE = ROOT/'manuscript_q1/protocols/endpoint_audit_sample.json'


def read_response(key):
    p=RESP/f'{key}.json'
    if not p.exists():return None
    obj=json.loads(p.read_text())
    if obj.get('is_error'):return None
    body=obj.get('content')
    if isinstance(body,str):
        try:return json.loads(body)
        except ValueError:return body
    return body


def registry_key(pkg,version):
    return hashlib.sha256((pkg+'@'+version).encode()).hexdigest()[:24]


def fetch_registry(mapping):
    pkg,version=mapping['package'],mapping['version']
    key=registry_key(pkg,version);path=REG/f'{key}.json'
    if path.exists():return
    url='https://registry.npmjs.org/'+urllib.parse.quote(pkg,safe='')+'/'+urllib.parse.quote(version,safe='')
    record={'package':pkg,'version':version,'requested_url':url,'observed_at_utc':stamp()}
    for attempt in range(2):
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'npm-research-endpoint-validation/1'})
            with urllib.request.urlopen(req,timeout=15) as res:
                raw=res.read(4000000);status=res.status
            obj=json.loads(raw)
            record.update(http_status=status,response_sha256=hashlib.sha256(raw).hexdigest(),
                          repository=obj.get('repository'),observed_name=obj.get('name'),
                          observed_version=obj.get('version'),dependencies=obj.get('dependencies',{}))
            break
        except urllib.error.HTTPError as e:
            record['http_status']=e.code
            if e.code not in [429,500,502,503,504]:break
        except (ValueError,TimeoutError,urllib.error.URLError) as e:
            record['error_type']=type(e).__name__
    dump(path,record)


def commit(row):
    obj=read_response(row['audit_id']+'__commit')
    return obj[0] if isinstance(obj,list) and obj and isinstance(obj[0],dict) else None


def safe_path(path):
    return isinstance(path,str) and not path.startswith('/') and '..' not in path.split('/')


def prepare(stage):
    rows=json.loads(SAMPLE.read_text());requests=[]
    def add(key,url,**metadata):
        if not (RESP/f'{key}.json').exists():requests.append({'key':key,'url':url,**metadata})
    for row in rows:
        aid,key=row['audit_id'],row['repository']
        if stage=='commits':
            add(aid+'__commit',f'https://api.github.com/repos/{key}/commits?per_page=1')
            continue
        c=commit(row)
        if not c:continue
        ref=c['sha']
        match=re.search(r'github.com/([^/]+/[^/]+)/commit/',c.get('html_url',''))
        resolved=match[1] if match else key
        if stage=='directories':
            add(aid+'__root',f'https://api.github.com/repos/{resolved}/contents?ref={ref}')
            add(aid+'__workflows',f'https://api.github.com/repos/{resolved}/contents/.github/workflows?ref={ref}')
        elif stage=='files':
            candidates={'package.json'}
            for mapping in row['original_mappings']:
                p=REG/f"{registry_key(mapping['package'],mapping['version'])}.json"
                obj=json.loads(p.read_text()) if p.exists() else {}
                repo=obj.get('repository')
                directory=repo.get('directory','') if isinstance(repo,dict) else ''
                if directory and safe_path(directory):candidates.add(directory.rstrip('/')+'/package.json')
            root=read_response(aid+'__root')
            if isinstance(root,list):
                for f in root:
                    if f.get('name') in ['package-lock.json','npm-shrinkwrap.json','yarn.lock','pnpm-lock.yaml']:
                        if f.get('size',0)<=2000000:candidates.add(f['path'])
            workflows=read_response(aid+'__workflows')
            files=sorted([f['path'] for f in workflows if f.get('type')=='file' and f['path'].endswith(('.yml','.yaml'))])[:20] if isinstance(workflows,list) else []
            for path in [*sorted(candidates)[:12],*files]:
                if safe_path(path):
                    keyfile=aid+'__file_'+hashlib.sha256(path.encode()).hexdigest()[:16]
                    add(keyfile,f'https://raw.githubusercontent.com/{resolved}/{ref}/'+urllib.parse.quote(path,safe='/'),
                        audit_id=aid,repo=resolved,commit_sha=ref,path=path)
    dump(AUDIT/f'requests_{stage}.json',requests)
    print(json.dumps({'stage':stage,'requests':len(requests),'path':str(AUDIT/f'requests_{stage}.json')}))


def collected_files(row):
    files={}
    for p in RESP.glob(row['audit_id']+'__file_*.json'):
        obj=json.loads(p.read_text())
        meta=obj.get('request',{})
        if not obj.get('is_error') and isinstance(obj.get('content'),str):
            files[meta.get('path','')]={'text':obj['content'],'response_file':str(p.relative_to(ROOT)),
                                      'sha256':hashlib.sha256(obj['content'].encode()).hexdigest(),
                                      'commit_sha':meta.get('commit_sha')}
    return files


def summarize():
    import yaml
    sample=json.loads(SAMPLE.read_text());results=[];mapping_results=[]
    for row in sample:
        aid=row['audit_id'];c=commit(row);files=collected_files(row)
        packages={};workflow_evidence=[];unresolved_actions=[];jobs=[]
        for path,e in files.items():
            if path.endswith('package.json'):
                try:
                    obj=json.loads(e['text']);packages[path]=obj
                except ValueError:pass
            if path.startswith('.github/workflows/'):
                try:obj=yaml.safe_load(e['text'])
                except yaml.YAMLError:continue
                if not isinstance(obj,dict):continue
                for jobid,job in (obj.get('jobs') or {}).items():
                    if not isinstance(job,dict):continue
                    defaults=job.get('defaults',obj.get('defaults',{})) or {}
                    for step in job.get('steps',[]) or []:
                        if not isinstance(step,dict):continue
                        if 'uses' in step:unresolved_actions.append({'workflow':path,'uses':step['uses']})
                        run=step.get('run')
                        if not isinstance(run,str):continue
                        lines=[l.strip() for l in run.splitlines() if not l.lstrip().startswith('#')]
                        observed=[l for l in lines if re.search(r'(?<![\w-])(?:npm\s+(?:ci|install|i)\b|pnpm\s+(?:install|i)\b|yarn(?:\s+(?:install|--frozen-lockfile)|\s*$))',l)]
                        if observed:
                            workflow_evidence.append({'workflow':path,'job':str(jobid),
                                'step':step.get('name'),'commands':observed,
                                'working_directory':step.get('working-directory',defaults.get('run',{}).get('working-directory','.')),
                                'condition':step.get('if',job.get('if')),'sha256':e['sha256']})
        target_names={m['package'] for m in row['original_mappings']}
        matching=[p for p,v in packages.items() if v.get('name') in target_names]
        per_mapping=[]
        for m in row['original_mappings']:
            rr=REG/f"{registry_key(m['package'],m['version'])}.json"
            reg=json.loads(rr.read_text()) if rr.exists() else {}
            observed_repo=parse_github_repository(reg.get('repository'))
            matches=[p for p,v in packages.items() if v.get('name')==m['package']]
            rrkey='/'.join(observed_repo) if all(observed_repo) else None
            state='supported_static' if matches and rrkey==row['repository'] else 'unknown_requires_review'
            per_mapping.append({'audit_id':aid,**m,'registry_repository_key':rrkey,
                                'manifest_paths':matches,'automated_mapping_state':state})
        mapping_results.extend(per_mapping)
        locks=[p for p in files if p.endswith(('package-lock.json','npm-shrinkwrap.json','yarn.lock','pnpm-lock.yaml'))]
        lock_versions=[]
        for p in locks:
            if p.endswith(('package-lock.json','npm-shrinkwrap.json')):
                try:lock=json.loads(files[p]['text'])
                except ValueError:continue
                for manifest in matching:
                    for dep in packages[manifest].get('dependencies',{}):
                        entry=(lock.get('packages') or {}).get('node_modules/'+dep,{})
                        if isinstance(entry,dict) and isinstance(entry.get('version'),str):
                            lock_versions.append({'manifest':manifest,'dependency':dep,'version':entry['version'],'lockfile':p})
        aligned_install=[]
        for evidence in workflow_evidence:
            wd=evidence['working_directory']
            for manifest in matching:
                folder=str(Path(manifest).parent)
                if wd in [folder,'./'+folder] or (wd=='.' and manifest=='package.json'):
                    aligned_install.append(evidence)
        labels={
            'repository_mapping_supported':'supported_static' if per_mapping and all(m['automated_mapping_state']=='supported_static' for m in per_mapping) else 'unknown_requires_review',
            'workflow_file_present':'supported_static' if any(p.startswith('.github/workflows/') for p in files) else 'unknown_requires_review',
            'install_directive_observed':'supported_static' if aligned_install else 'unknown_requires_review',
            'lockfile_present':'supported_static' if locks else 'unknown_requires_review',
            'dependency_version_supported':'supported_static' if lock_versions else 'unknown_requires_review'}
        result={**row,'observed_commit_sha':c.get('sha') if c else None,
                'commit_observation':str((RESP/f'{aid}__commit.json').relative_to(ROOT)),
                'time_scope':'current commit-pinned static evidence; not historical installation validation',
                'automated_labels':labels,'matching_manifest_paths':matching,
                'workflow_install_evidence':workflow_evidence,'aligned_install_evidence':aligned_install,
                'unresolved_action_references':unresolved_actions,'lockfiles':locks,
                'dependency_version_examples':lock_versions[:20],
                'evidence_files':{p:{k:v for k,v in e.items() if k!='text'} for p,e in files.items()},
                'human_review_status':'pending_independent_authors'}
        results.append(result)
    dump(AUDIT/'automated_evidence.json',results);dump(AUDIT/'mapping_evidence.json',mapping_results)
    review=ROOT/'manuscript_q1/review_packets';review.mkdir(exist_ok=True)
    fields=['audit_id','repository','commit_sha','repository_mapping_supported','workflow_file_present',
            'install_directive_observed','lockfile_present','dependency_version_supported','evidence_notes']
    for name in ['Shahriar_Hasan','Md_Ashikul_Islam']:
        p=review/f'{name}_independent_labels.csv'
        if not p.exists():
            with p.open('w',newline='') as f:
                w=csv.DictWriter(f,fields);w.writeheader()
                for r in results:w.writerow({'audit_id':r['audit_id'],'repository':r['repository'],
                                             'commit_sha':r['observed_commit_sha'] or ''})
    lines=['# Endpoint audit evidence packet','',
           'Both authors agreed to review independently. Initial label sheets contain no automated suggestions. '
           'Use supported / unsupported / unknown for each label and cite evidence paths in notes. '
           'Do not discuss initial labels until both sheets are saved. Automated evidence remains provisional.',
           '', 'Current-time static evidence does not establish old HEAD validity, workflow execution, or historical publisher authority.','']
    lines += ['## Label rubric','',
        '- `repository_mapping_supported`: every listed package/version mapping has registry repository evidence and a matching named package manifest at the inspected commit. Ambiguous monorepo paths and redirects remain unknown.',
        '- `workflow_file_present`: an actual workflow YAML file is present at the pinned commit.',
        '- `install_directive_observed`: a relevant workflow run step contains an installation command in the package path, or a reusable workflow/action has been resolved to equivalent evidence. Echoed examples, comments and unrelated paths do not count. Record conditions. This never claims a run succeeded.',
        '- `lockfile_present`: an inspected lockfile applies to the named package path or enclosing workspace. Record the relationship.',
        '- `dependency_version_supported`: a manifest dependency has a specific corresponding version entry in the relevant lockfile. Record at least one dependency/version pair; this does not validate every graph path.',
        '- `unsupported`: inspected evidence contradicts the criterion, with a cited reason. `unknown`: evidence is missing, ambiguous or unresolved. Blank means not reviewed.',
        '', 'Save initial labels independently. Human results require both complete sheets and resolution of disagreements. Do not copy automated labels into the independent sheets.','']
    for r in results:
        lines += [f"## {r['audit_id']} — {r['repository']}",'',f"Commit: `{r['observed_commit_sha']}`.",
                  'Original package/version mappings: '+', '.join(m['package']+'@'+m['version'] for m in r['original_mappings']),
                  '', 'Evidence:']
        for path,e in r['evidence_files'].items():
            link=f"https://github.com/{r['repository']}/blob/{r['observed_commit_sha']}/{path}"
            lines.append(f'- [{path}]({link}); retained response `{e["response_file"]}`')
        if not r['evidence_files']:lines.append('- Acquisition unresolved; record unknown unless independently documented.')
        lines.append('')
    (review/'ENDPOINT_REVIEW_INSTRUCTIONS.md').write_text('\n'.join(lines))
    summary={'created_at_utc':stamp(),'sample_size':len(results),
             'commits_acquired':sum(bool(r['observed_commit_sha']) for r in results),
             'labels':{label:{state:sum(r['automated_labels'][label]==state for r in results)
                              for state in ['supported_static','unknown_requires_review']} for label in fields[3:-1]},
             'human_review_completed':False,'human_agreement':None,
             'source_sample_sha256':sha(SAMPLE),'script_sha256':sha(__file__)}
    dump(AUDIT/'summary.json',summary)
    print(json.dumps(summary,indent=2))


def main():
    for p in [AUDIT,RESP,REG]:p.mkdir(parents=True,exist_ok=True)
    parser=argparse.ArgumentParser();parser.add_argument('action',choices=['registry','commits','directories','files','summarize'])
    args=parser.parse_args()
    if args.action=='registry':
        mappings={registry_key(m['package'],m['version']):m for r in json.loads(SAMPLE.read_text()) for m in r['original_mappings']}
        with ThreadPoolExecutor(max_workers=6) as pool:
            jobs=[pool.submit(fetch_registry,m) for m in mappings.values()]
            for i,f in enumerate(as_completed(jobs),1):
                f.result()
                if i%20==0:print('registry records',i,flush=True)
        print('Registry evidence complete:',len(mappings))
    elif args.action=='summarize':summarize()
    else:prepare(args.action)


if __name__=='__main__':main()
