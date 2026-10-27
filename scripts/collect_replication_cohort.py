#!/usr/bin/env python3
"""Fresh bounded dependency acquisition for the 100 frozen baseline-frame roots."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.request
import urllib.error
import urllib.parse

from journal_revision_common import ROOT, OUT, dump, sha, stamp
from research_observations import parse_github_repository

OUTDIR=OUT/'replication'; OBS=OUTDIR/'observations'


def request(url):
    if os.environ.get('NPM_RESEARCH_OFFLINE')=='1':
        raise RuntimeError('Offline reproduction requested missing captured input: '+url)
    obj={'requested_url':url,'observed_at_utc':stamp(),'attempts':0}
    for attempt in range(2):
        obj['attempts']=attempt+1
        try:
            req=urllib.request.Request(url,headers={'User-Agent':'npm-research-replication/1'})
            with urllib.request.urlopen(req,timeout=20) as response:
                raw=response.read(8000000);obj['http_status']=response.status
            obj['response_sha256']=hashlib.sha256(raw).hexdigest()
            return obj,json.loads(raw)
        except urllib.error.HTTPError as e:
            obj['http_status']=e.code
            if e.code not in [429,500,502,503,504]:break
        except (ValueError,TimeoutError,urllib.error.URLError) as e:
            obj['error_type']=type(e).__name__
    return obj,None


def package_key(pkg,version):
    return hashlib.sha256((pkg+'@'+version).encode()).hexdigest()[:24]


def metadata(pkg,version='latest'):
    key=package_key(pkg,version);path=OBS/f'metadata_{key}.json'
    if path.exists():return json.loads(path.read_text())
    url='https://registry.npmjs.org/'+urllib.parse.quote(pkg,safe='')+'/'+urllib.parse.quote(version,safe='')
    obs,data=request(url)
    obs.update(requested_package=pkg,requested_version=version)
    if isinstance(data,dict):
        obs.update(name=data.get('name'),version=data.get('version'),repository=data.get('repository'),
                   maintainers=sorted({m['name'] for m in data.get('maintainers',[]) if isinstance(m,dict) and isinstance(m.get('name'),str)}),
                   dependencies=data.get('dependencies',{}))
    dump(path,obs)
    return obs


def acquire_root(pkg):
    path=OBS/f'root_{package_key(pkg,"latest")}.json'
    if path.exists():return json.loads(path.read_text())
    meta=metadata(pkg)
    obs={'root':pkg,'metadata_key':package_key(pkg,'latest'),'frozen_root_version':meta.get('version')}
    if meta.get('version'):
        url='https://api.deps.dev/v3/systems/npm/packages/'+urllib.parse.quote(pkg,safe='')+'/versions/'+urllib.parse.quote(meta['version'],safe='')+':dependencies'
        res,data=request(url);obs['dependency_request']=res
        if isinstance(data,dict):
            obs['nodes']=[{'name':n.get('versionKey',{}).get('name'),
                           'version':n.get('versionKey',{}).get('version'),
                           'bundled':n.get('bundled',False),'relation':n.get('relation'),
                           'errors':n.get('errors',[])} for n in data.get('nodes',[])]
            obs['edges']=data.get('edges',[]);obs['graph_error']=data.get('error')
    dump(path,obs)
    return obs


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prepare-github',action='store_true');args=parser.parse_args()
    OBS.mkdir(parents=True,exist_ok=True)
    roots=json.loads((ROOT/'manuscript_q1/protocols/replication_roots.json').read_text())
    if args.prepare_github:
        requests=[]
        for i,pkg in enumerate(roots):
            obj=metadata(pkg);owner,repo=parse_github_repository(obj.get('repository'))
            if owner and repo:
                requests.append({'key':f'R{i:03}__commit','url':f'https://api.github.com/repos/{owner}/{repo}/commits?per_page=1',
                                 'root':pkg,'repository':owner+'/'+repo})
        dump(OUTDIR/'requests_commits.json',requests)
        print('Root commit requests:',len(requests));return
    started=stamp()
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs=[pool.submit(acquire_root,pkg) for pkg in roots]
        for i,f in enumerate(as_completed(jobs),1):
            f.result()
            if i%10==0:print('root observations',i,flush=True)
    observations=[acquire_root(p) for p in roots]
    # Global cap counts exact (package, version) nodes. Root nodes take priority.
    nodes={(o['root'],o['frozen_root_version']) for o in observations if o.get('frozen_root_version')}
    edges=set();bounds=[]
    for obs in observations:
        nn=obs.get('nodes',[]);ee=obs.get('edges',[])
        adj={i:[] for i in range(len(nn))}
        for e in ee:
            if e.get('fromNode') in adj and e.get('toNode') in adj:adj[e['fromNode']].append(e['toNode'])
        seen=set();queue=deque([0] if nn else [])
        while queue and len(seen)<500:
            n=queue.popleft()
            if n in seen:continue
            key=(nn[n]['name'],nn[n]['version'])
            if not all(isinstance(x,str) and x for x in key):continue
            if key not in nodes and len(nodes)>=2500:continue
            seen.add(n);nodes.add(key)
            queue.extend(sorted(adj[n]))
        for e in ee:
            if e.get('fromNode') in seen and e.get('toNode') in seen:
                a,b=nn[e['fromNode']],nn[e['toNode']]
                edges.add((a['name'],a['version'],b['name'],b['version']))
        bounds.append({'root':obs['root'],'observed_nodes':len(nn),'retained_nodes':len(seen),
                       'omitted_nodes':len(nn)-len(seen),'root_request_succeeded':bool(nn),
                       'root_graph_error':obs.get('graph_error')})
    print('Fresh exact nodes:',len(nodes),'edges:',len(edges),'requesting version metadata',flush=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        jobs=[pool.submit(metadata,p,v) for p,v in sorted(nodes) if '>' not in p]
        for i,f in enumerate(as_completed(jobs),1):
            f.result()
            if i%100==0:print('version observations',i,flush=True)
    dump(OUTDIR/'graph.json',{'nodes':[list(x) for x in sorted(nodes)],'edges':[list(x) for x in sorted(edges)],'root_bounds':bounds})
    dump(OUTDIR/'acquisition_summary.json',{'started_at_utc':started,'completed_at_utc':stamp(),
          'roots_selected':100,'roots_with_dependency_graph':sum(b['root_request_succeeded'] for b in bounds),
          'roots_with_omitted_nodes':sum(b['omitted_nodes']>0 for b in bounds),
          'exact_nodes':len(nodes),'version_edges':len(edges),'root_bounds':bounds,
          'ordinary_name_frame':'original seeded graph, not npm population',
          'global_exact_node_cap':2500,'per_root_node_cap':500,'script_sha256':sha(__file__),
          'protocol_sha256':sha(ROOT/'manuscript_q1/protocols/revision_validation_protocol.json'),
          'metadata_observations':len(list(OBS.glob('metadata_*.json'))),
          'note':'New API acquisition. Root workflow observations are acquired separately. No old workflow flags copied.'})
    print('Fresh graph acquisition complete',flush=True)


if __name__=='__main__':main()
