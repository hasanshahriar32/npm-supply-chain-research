#!/usr/bin/env python3
"""Verify active paper tables, endpoint units, source fields and figure bindings.

Scientific consistency gate, independent of PDF formatting and archive locks.
"""
from pathlib import Path
import csv,hashlib,json,math,re,sqlite3,tempfile,zipfile,shutil,sys
ROOT=Path(__file__).resolve().parents[1]
METHODS=['portfolio','sum_package_reach','max_package_reach','exact_union','greedy_coverage']
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def budget_rows(baseline):
 out=[]
 for b in (1,5,10,25,50,100):
  rnd=next(r for r in baseline['random_summary']if r['endpoint']=='workflow_repositories'and r['budget']==b)
  for label,key,factor in [('C (\\%)','coverage_fraction_observed',100),('H (\\%)','scenario_exposure_reduction_fraction',100),('P','fully_protected_endpoints',1)]:
   rows=[next(r for r in baseline['deterministic_curves']if r['endpoint']=='workflow_repositories'and r['budget']==b and r['method']==m)for m in METHODS]
   vals=[f'{factor*r[key]:.2f}'if factor==100 else f"{r[key]:,}"for r in rows]
   out.append([str(b),label,*vals,f"{factor*rnd[key+'_mean']:.2f} $\\pm$ {factor*rnd[key+'_sd']/math.sqrt(rnd['trials']):.2f}"])
 return out
def validate_budget_table(content,baseline):
 actual=[[c.strip().removesuffix(r'\\').strip()for c in line.split('&')]for line in content.splitlines()if re.match(r'^\d+ & ',line)]
 expected=budget_rows(baseline)
 if actual!=expected:
  bad=[i+1 for i,(a,b)in enumerate(zip(actual,expected))if a!=b]
  raise AssertionError(f'Active budget table mismatch in rows {bad}; {len(actual)} rows, expected 18')
 return 90+36

def verify(root=ROOT):
 baseline=json.loads((root/'manuscript/results/structural_interventions/results.json').read_text())
 evidence=json.loads((root/'manuscript_q1/results/full_revision_evidence.json').read_text())
 for rel,expected in evidence['source_sha256'].items():assert sha(root/rel)==expected,f'Stale reconciliation source: {rel}'
 sec5=(root/'manuscript_q1/sections/05_empirical_results_rq1_to_rq3.tex').read_text()
 assert r'\input{tables/q1_multi_budget_table}'in sec5,'Generated budget table is not active'
 assert r'\begin{tabular}'not in sec5,'Duplicated handwritten result table in active section'
 count=validate_budget_table((root/'manuscript_q1/tables/q1_multi_budget_table.tex').read_text(),baseline)
 # Direct archive reads establish focal membership and independent BFS endpoint sets.
 sys.path.insert(0,str(root/'scripts'));import study_structural_interventions as ssi
 with tempfile.TemporaryDirectory(prefix='paper-evidence-')as tmp:
  db=Path(tmp)/'data.db'
  with zipfile.ZipFile(root/'data/npm_ecosystem.db.zip')as z,z.open('npm_ecosystem.db')as src,db.open('wb')as dst:shutil.copyfileobj(src,dst)
  conn=sqlite3.connect(f'file:{db}?mode=ro&immutable=1',uri=True)
  names,ids,port,pm,adj,wf,ch,rn,wn,sn,pop=ssi.load_data(conn)
  comp,mem,edges,topo=ssi.scc_condensation(adj);reach=ssi.propagate_endpoint_bits(comp,mem,edges,topo,wn);ep=ssi.endpoint_data(reach,port)
  assert ep['total_pairs']==baseline['diagnostics']['workflow_repositories']['total_identity_endpoint_pairs']
  ix={name:m for m,(name,_)in enumerate(ids)};order=sorted(range(len(ids)),key=lambda m:(-ep['sizes'][m],m));ranks={m:i+1 for i,m in enumerate(order)}
  greedy,_=ssi.lazy_greedy(ep['masks'],range(len(ids)),range(len(ids)),100);gr={m:i+1 for i,m in enumerate(greedy)}
  for user,fact in evidence['focal_maintainers'].items():
   m=ix[user];seen=set(port[m]);pending=list(seen)
   while pending:
    node=pending.pop()
    for v in adj[node]-seen:seen.add(v);pending.append(v)
   bfs=ssi.union(wn[p]for p in seen)
   assert bfs.bit_count()==fact['workflow_name_reach'],f'Wrong endpoint universe for {user}'
   assert ranks[m]==fact['ranks']['union']and len(port[m])==fact['portfolio_size']
  incidents=json.loads((root/'manuscript_q1/results/incident_workflow_reconciliation.json').read_text());table=(root/'manuscript_q1/tables/q1_incident_case_study_table.tex').read_text()
  per={r['package_name']:r for r in csv.DictReader((root/'manuscript/results/graph_validity/per_package.csv').open())}
  for row in incidents:
   label=row['package'];pkg=label.split(' ')[0];m=ix[row['primary_maintainer']]
   assert row['union_name_rank']==ranks[m]and row['greedy_rank']==gr.get(m,'>100'),label
   assert int(row['reach_name'])==int(per[pkg]['workflow_repository_reach'])and int(row['reach_vc'])==int(per[pkg]['version_continuous_workflow_repository_reach']),label
   lines=[line for line in table.splitlines()if line.startswith(r'\texttt{'+label+'}')];assert len(lines)==1,label
   cells=[c.strip().removesuffix(r'\\').strip()for c in lines[0].split('&')]
   assert cells[2:4]==[f"{int(row['reach_name']):,}",f"{int(row['reach_vc']):,}"],label
   rank=lambda x:r'\#'+(f'{x:,}'if isinstance(x,int)else x)
   assert cells[4:]==[rank(row[k])for k in ['portfolio_rank','greedy_rank','union_name_rank','pareto_p50_rank']],label
 # Shared macros prevent both papers drifting back to linked endpoints.
 f=evidence['focal_maintainers']['qix'];values={'QixPortfolio':str(f['portfolio_size']),'QixNameReach':f"{f['workflow_name_reach']:,}",'QixVersionReach':f"{f['workflow_version_reach']:,}",'QixUnionRank':str(f['ranks']['union']),'QixVersionRank':str(f['ranks']['version_union']),'QixHybridRank':str(f['ranks']['hybrid']),'QixOutsideSindresorhus':str(f['not_reached_by_sindresorhus'])}
 for rel in ['manuscript/results/reconciliation_numbers.tex','manuscript_q1/config/reconciliation_numbers.tex']:
  content=(root/rel).read_text()
  for k,v in values.items():assert '\\newcommand{\\'+k+'}{'+v+'}'in content,(rel,k)
 for rel,base in [('manuscript/main.tex','results'),('manuscript_q1/main_q1.tex','config'),('manuscript_q1/main_q1_anonymous.tex','config')]:assert '\\input{'+base+'/reconciliation_numbers}'in(root/rel).read_text()
 # Count recorded attempts; do not reinterpret skipped expansions as successful.
 edges=list(csv.DictReader((root/'platform/research/74_bounded_recursive_registry_semver_graph_edges.csv').open()))
 resolved=sum(r['target_resolution_status']=='resolved_cutoff_semver_range'for r in edges);ratio=100*resolved/len(edges)
 assert evidence['temporal']['resolved']==resolved and evidence['temporal']['recorded_attempts']==len(edges)
 assert abs(evidence['temporal']['attempted_share_pct']-ratio)<1e-10
 temporal=(root/'manuscript_q1/tables/q1_temporal_reconstruction_table.tex').read_text();assert f'{ratio:.2f}\\%'in temporal and f'{resolved:,}'in temporal
 authority=(root/'manuscript_q1/tables/q1_release_authority_table.tex').read_text()
 assert 'Embedded Maintainer Signatures'not in authority and 'unknown' in authority.lower()
 available=json.loads((root/'platform/research/95_release_authority_metadata_availability_audit.json').read_text())['summary']
 fields=['exactPreEventSourceSnapshots','predecessorAvailable','repositoryDescriptorComparisonAvailable','gitHeadComparisonAvailable','publishConfigComparisonAvailable','selectedDistIntegrityPresent','selectedEmbeddedMaintainersPresent']
 arows=[line for line in authority.splitlines() if re.search(r' & \d+ & ',line)]
 assert len(arows)==len(fields)
 for line,field in zip(arows,fields):
  cells=[c.strip().removesuffix(r'\\').strip()for c in line.split('&')]
  assert cells[1:]==[str(available[field]),f"{100*available[field]/45:.1f}\\%"],field
 assert evidence['scc']==json.loads((root/'manuscript/results/graph_validity/summary.json').read_text())['scc']
 access=json.loads((root/'platform/research/97_official_npm_provenance_attestation_access_assessment.json').read_text());assert access['counts']['attestationStatesClassified']==0
 prose='\n'.join(p.read_text()for p in(root/'manuscript_q1/sections').glob('*.tex'))
 for bad in ['99.89','31.8\\%','14.2\\%','1.8\\%','0.15\\%','3.12','182$','fully protected repositories','verified, active','pre-registered','Total Absence of Public Cryptographic Provenance','registry PGP signatures']:
  assert bad not in prose,f'Reintroduced unsupported claim: {bad}'
 # Bind every added active visual to inputs and both identical exported copies.
 for rel,figure_root in [('manuscript/results/review_figure_data.json','manuscript/figures'),('manuscript_q1/results/journal_figure_data.json','manuscript_q1/figures')]:
  record=json.loads((root/rel).read_text())
  for source,h in record['source_sha256'].items():assert sha(root/source)==h,source
  renderer='scripts/render_review_figures.py'if 'review_figure' in rel else'manuscript_q1/scripts/render_q1_figures.py'
  assert sha(root/renderer)==record['renderer_sha256']
  for stem,outputs in record['figures'].items():
   for ext,h in outputs.items():
    presentation_path=root/'manuscript_q1/results/emse_figure_presentation.json'
    presentation=json.loads(presentation_path.read_text()) if presentation_path.exists() else None
    if figure_root=='manuscript_q1/figures' and presentation and stem in presentation['inputs']:
     assert sha(root/figure_root/'editorial_inputs'/f'{stem}.{ext}')==h,(stem,ext,'original')
     assert sha(root/figure_root/f'{stem}.{ext}')==presentation['figures'][stem][ext],(stem,ext,'presentation')
    else:assert sha(root/figure_root/f'{stem}.{ext}')==h,(stem,ext)
  if 'review_figure'in rel:
   for label,mat in record['representation_matrices'].items():
    method,key=label.split('/')
    assert len(mat)==2 and all(len(row)==2 for row in mat)
    version_rows=baseline['version_representation_curves']
    reps=sorted({r['selection_representation'] for r in version_rows})
    name_rep=next(r for r in reps if r!='version_continuous');reps=[name_rep,'version_continuous']
    for iy,ev in enumerate(reps):
     for ix,sel in enumerate(reps):
      found=[r for r in version_rows if r['endpoint']=='workflow_repositories' and r['method']==method and r['budget']==100 and r['selection_representation']==sel and r['evaluation_representation']==ev]
      if not found and sel==ev==name_rep:
       found=[r for r in baseline['deterministic_curves'] if r['endpoint']=='workflow_repositories' and r['method']==method and r['budget']==100]
      assert len(found)==1
      assert abs(mat[iy][ix]-found[0][key]*(100 if key=='scenario_exposure_reduction_fraction' else 1))<1e-9
 for path in(root/'manuscript_q1/sections').glob('*.tex'):
  for stem in re.findall(r'\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}',path.read_text()):assert(root/'manuscript_q1/figures'/stem).exists(),stem
 return {'budget_numeric_values_checked':count,'incident_rows_checked':len(incidents),'focal_workflow_sets_independently_checked':3,'temporal_resolved_rows':resolved,'temporal_attempted_rows':len(edges),'attestation_states_assessed':0,'pass':True}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
