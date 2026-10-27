#!/usr/bin/env python3
"""Dynamic-population comparisons on the newly acquired, bounded root cohort."""
from collections import defaultdict
import argparse
import csv
import json
import random
import re
import sqlite3
import statistics

from journal_revision_common import ROOT, OUT, baseline, dump, exclusion_order, metric, sha, stamp, ssi
from collect_replication_cohort import metadata

FOLDER=OUT/'replication'


def response(key):
    p=FOLDER/'github_responses'/f'{key}.json'
    if not p.exists():return None
    o=json.loads(p.read_text())
    if o.get('is_error'):return None
    c=o.get('content')
    if isinstance(c,str):
        try:return json.loads(c)
        except ValueError:return None
    return c


def prepare():
    requests=[]
    for item in json.loads((FOLDER/'requests_commits.json').read_text()):
        obj=response(item['key'])
        if not isinstance(obj,list) or not obj:continue
        c=obj[0];ref=c['sha']
        m=re.search(r'github.com/([^/]+/[^/]+)/commit/',c.get('html_url',''))
        repo=m[1] if m else item['repository']
        key=item['key'].replace('__commit','__workflows')
        if not (FOLDER/'github_responses'/f'{key}.json').exists():
            requests.append({'key':key,'root':item['root'],'repository':repo,'commit_sha':ref,
                             'url':f'https://api.github.com/repos/{repo}/contents/.github/workflows?ref={ref}'})
    dump(FOLDER/'requests_workflows.json',requests)
    print('Pinned workflow requests:',len(requests))


def orders(masks,portfolios,sources,candidates=None):
    candidates=list(range(len(masks))) if candidates is None else list(candidates)
    portfolio=sorted(candidates,key=lambda m:(-len(portfolios[m]),m))[:100]
    union=sorted(candidates,key=lambda m:(-masks[m].bit_count(),m))[:100]
    greedy,_=ssi.lazy_greedy(masks,candidates,list(range(len(masks))),100)
    direct,_=exclusion_order(masks,sources,100,candidates=candidates)
    simple,_=exclusion_order(masks,sources,100,immediate_only=True,candidates=candidates)
    return {'portfolio':portfolio,'exact_union':union,'greedy_coverage':greedy,'direct_p':direct,'immediate_only':simple}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--prepare-workflows',action='store_true');args=ap.parse_args()
    if args.prepare_workflows:prepare();return
    graph=json.loads((FOLDER/'graph.json').read_text())
    nodes=[tuple(x) for x in graph['nodes']];names=sorted({x[0] for x in nodes});ni={p:i for i,p in enumerate(names)}
    memberships=defaultdict(set);metadata_status=[]
    for p,v in nodes:
        if '>' in p:continue
        obs=metadata(p,v);memberships[p].update(obs.get('maintainers',[]))
        metadata_status.append({'package':p,'version':v,'http_status':obs.get('http_status'),
                                'maintainer_count':len(obs.get('maintainers',[]))})
    people=sorted(set().union(*memberships.values()));mi={m:i for i,m in enumerate(people)}
    pm=[{mi[m] for m in memberships[p]} for p in names]
    portfolios=[set() for _ in people]
    for p,src in enumerate(pm):
        for m in src:portfolios[m].add(p)
    successful={r['root'] for r in graph['root_bounds'] if r['root_request_succeeded']}
    root_obs=[];keys=set()
    for req in json.loads((FOLDER/'requests_commits.json').read_text()):
        key=req['key'].replace('__commit','__workflows');listing=response(key)
        c=response(req['key']);repo=req['repository']
        if isinstance(c,list) and c:
            mm=re.search(r'github.com/([^/]+/[^/]+)/commit/',c[0].get('html_url',''))
            if mm:repo=mm[1].casefold()
        positive=isinstance(listing,list)
        eligible=positive and req['root'] in successful
        root_obs.append({'root':req['root'],'repository':repo,'directory_observed':positive,
                         'dependency_graph_acquired':req['root'] in successful,'eligible':eligible})
        if eligible:keys.add(repo)
    repo_names=sorted(keys);ri={r:i for i,r in enumerate(repo_names)}
    wn=[0 for _ in names]
    for r in root_obs:
        if r['eligible']:wn[ni[r['root']]]|=1<<ri[r['repository']]
    adj=[set() for _ in names]
    conn=sqlite3.connect(':memory:')
    conn.execute('CREATE TABLE dependencies(from_package,from_version,to_package,to_version)')
    conn.execute('CREATE TABLE package_versions(package_name,version)')
    conn.executemany('INSERT INTO dependencies VALUES(?,?,?,?)',graph['edges'])
    conn.executemany('INSERT INTO package_versions VALUES(?,?)',nodes)
    for a,av,b,bv in graph['edges']:adj[ni[b]].add(ni[a])
    comp,mem,dag,topo=ssi.scc_condensation(adj)
    reaches=ssi.propagate_endpoint_bits(comp,mem,dag,topo,wn)
    ep=ssi.endpoint_data(reaches,portfolios)
    _,vreaches,_,vmeta=ssi.version_continuous_representation(conn,names,pm,wn)
    vep=ssi.endpoint_data(vreaches,portfolios)
    conn.close()
    def source_sets(masks):
        ss=[0]*len(repo_names)
        for m,mask in enumerate(masks):
            for r in ssi.bit_indices(mask):ss[r]|=1<<m
        return ss
    ns,vs=source_sets(ep['masks']),source_sets(vep['masks'])
    assert len(people)>100 and repo_names
    nm=orders(ep['masks'],portfolios,ns);vm=orders(vep['masks'],portfolios,vs)
    rows=[]
    for sel,oo in [('name',nm),('version',vm)]:
        for ev,ee,ss in [('name',ep,ns),('version',vep,vs)]:
            for method,order in oo.items():
                for b in [1,5,10,25,50,100]:
                    rows.append({'selection_representation':sel,'evaluation_representation':ev,
                                 'method':method,'budget':b,**metric(order[:b],ee['masks'],ss,len(repo_names))})
    rng=random.Random(2026102703);rand=[]
    for i in range(200):
        order=rng.sample(range(len(people)),100)
        for b in [1,5,10,25,50,100]:
            rand.append({'seed_order':i,'budget':b,**metric(order[:b],ep['masks'],ns,len(repo_names))})
    # Common endpoints/accounts; full source sets survive candidate restriction.
    old=baseline();oldrepo={r['repository']:r for r in old['endpoints']}
    common_repo=sorted(set(repo_names)&set(oldrepo))
    union_people=sorted(set(old['maintainers'])|set(people));ui={m:i for i,m in enumerate(union_people)}
    common_people=set(old['maintainers'])&set(people);candidates=sorted(ui[m] for m in common_people)
    oldm=[0]*len(union_people);newm=[0]*len(union_people);oldsrc=[];newsrc=[]
    for i,repo in enumerate(common_repo):
        os=int(oldrepo[repo]['source_mask'],16);ss=ns[ri[repo]];oa=na=0
        for m in ssi.bit_indices(os):
            j=ui[old['maintainers'][m]];oldm[j]|=1<<i;oa|=1<<j
        for m in ssi.bit_indices(ss):
            j=ui[people[m]];newm[j]|=1<<i;na|=1<<j
        oldsrc.append(oa);newsrc.append(na)
    common_rows=[];overlaps=[]
    for label,mm,ss in [('original',oldm,oldsrc),('new_cohort',newm,newsrc)]:
        oo=orders(mm,[set() for _ in mm],ss,candidates)
        for method in ['exact_union','greedy_coverage','direct_p']:
            for b in [1,5,10,25,50,100]:
                common_rows.append({'dataset':label,'method':method,'budget':b,
                                    'eligible_common_accounts':len(candidates),**metric(oo[method][:b],mm,ss,len(common_repo))})
        if label=='original':previous=oo
        else:
            for method in ['exact_union','greedy_coverage','direct_p']:
                for b in [10,25,50,100]:
                    a=set(previous[method][:b]);bb=set(oo[method][:b])
                    overlaps.append({'method':method,'budget':b,'intersection':len(a&bb),
                                     'jaccard':len(a&bb)/len(a|bb) if a|bb else None})
    for fn,rr in [('comparisons.csv',rows),('random_orders.csv',rand),('common_population.csv',common_rows),('selection_overlap.csv',overlaps)]:
        with (FOLDER/fn).open('w',newline='') as f:
            w=csv.DictWriter(f,list(rr[0]));w.writeheader();w.writerows(rr)
    dump(FOLDER/'incidence.json',{'maintainers':people,'repositories':repo_names,
         'name_masks':[hex(x) for x in ep['masks']],'version_masks':[hex(x) for x in vep['masks']],
         'name_sources':[hex(x) for x in ns],'version_sources':[hex(x) for x in vs],
         'orders_name':nm,'orders_version':vm,'root_observations':root_obs,'metadata_status':metadata_status})
    summary={'completed_at_utc':stamp(),'roots_selected':100,'root_repo_observations':len(root_obs),
             'roots_with_directory':sum(r['directory_observed'] for r in root_obs),
             'roots_eligible':sum(r['eligible'] for r in root_obs),'workflow_repository_endpoints':len(repo_names),
             'ordinary_or_context_identifiers':len(names),'exact_version_nodes':len(nodes),'maintainers':len(people),
             'name_pair_mass':ep['total_pairs'],'version_pair_mass':vep['total_pairs'],
             'pair_decrease_pct':100*(1-vep['total_pairs']/ep['total_pairs']),
             'metadata_versions_acquired':sum(r['http_status']==200 for r in metadata_status),
             'metadata_versions_attempted':len(metadata_status),'common_endpoints':len(common_repo),
             'common_accounts':len(candidates),'results':rows,'common_results':common_rows,'overlaps':overlaps,
             'script_sha256':sha(__file__),'graph_sha256':sha(FOLDER/'graph.json'),
             'interpretation':'New bounded acquisition of 100 roots from original ordinary-name frame; endpoint population and acquisition differ. Not a registry-wide or independent-time-population estimate. No significance tests across two acquisitions.'}
    dump(FOLDER/'study_summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['results','common_results','overlaps']},indent=2))


if __name__=='__main__':main()
