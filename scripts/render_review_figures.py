#!/usr/bin/env python3
"""Evidence-derived distributions, representation matrices, and observation units."""
from pathlib import Path
from collections import Counter
import hashlib,json,os,shutil
os.environ.setdefault('MPLCONFIGDIR','/tmp/npm-review-mpl')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
FIG=ROOT/'manuscript/figures'; QFIG=ROOT/'manuscript_q1/figures'
INPUTS=['manuscript_q1/results/quorum_reproducibility.json','manuscript/results/structural_interventions/results.json','manuscript/results/graph_validity/identifier_scope.json','manuscript/results/prospective_cohort/cohort_status.json']
COLORS={'Before selection':'#647481','Greedy coverage':'#00858b','Exact union':'#285d85','Hybrid':'#8660a8','Direct exclusion':'#b57720'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(fig,stem):
 for ext in ('pdf','svg','png'):
  target=FIG/f'{stem}.{ext}'
  fig.savefig(target,dpi=240,metadata={'CreationDate':None,'ModDate':None} if ext=='pdf' else {'Date':None} if ext=='svg' else None)
  shutil.copy2(target,QFIG/target.name)
 plt.close(fig)
def cdf(ax,counts,label,**kwargs):
 xs=sorted(counts)
 if xs[0]>0:xs=[0]+xs
 ys=np.cumsum([counts.get(x,0) for x in xs])*100/7158
 ax.step(xs,ys,where='post',label=label,**kwargs)
 ax.set_xscale('symlog',linthresh=1);ax.set_xlim(0,1600);ax.set_ylim(0,101)
 ax.set_xticks([0,1,10,100,1000],['0','1','10','100','1,000']);ax.grid(axis='y',alpha=.18);ax.set_yticks([0,25,50,75,100])
def main():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'axes.titlesize':9,'legend.fontsize':7,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'npm-review-20261027'})
 q=json.loads((ROOT/INPUTS[0]).read_text());d=json.loads((ROOT/INPUTS[1]).read_text());cohort=json.loads((ROOT/INPUTS[3]).read_text());scope=json.loads((ROOT/INPUTS[2]).read_text())
 h=[r for r in q['cardinality_histograms'] if r['budget']==100]
 baseline=Counter()
 for n,rem,c in h[0]['counts']:baseline[n]+=c
 assert sum(baseline.values())==7158 and sum(n*c for n,c in baseline.items())==462170
 residual={}
 for row in h:
  strategy=row['strategy']
  label='Greedy coverage' if strategy=='Greedy Coverage' else 'Exact union' if strategy=='Exact Union' else 'Hybrid' if strategy.startswith('Pareto') else 'Direct exclusion' if strategy.startswith('Direct') else None
  if label:
   counts=Counter()
   for n,rem,c in row['counts']:counts[rem]+=c
   assert sum(counts.values())==7158
   residual[label]=counts
 fig,axes=plt.subplots(1,2,figsize=(7.1,2.55));fig.subplots_adjust(left=.075,right=.98,bottom=.26,top=.84,wspace=.32)
 cdf(axes[0],baseline,'Before selection',color=COLORS['Before selection'],lw=1.6)
 axes[0].set(title='(a) Observed source cardinality',xlabel='Source identities per repository',ylabel='Repositories at or below count (%)')
 axes[0].text(.05,.9,'7,158 source-reachable repositories\nMean 64.57 · maximum 1,502',transform=axes[0].transAxes,fontsize=7,va='top')
 for label,counts in residual.items():cdf(axes[1],counts,label,color=COLORS[label],lw=1.3)
 axes[1].set(title='(b) Remaining sources after selection',xlabel='Unselected source identities (budget 100)')
 axes[1].legend(loc='lower right',frameon=False,fontsize=6.8)
 save(fig,'source_multiplicity')
 fig,ax=plt.subplots(figsize=(3.45,2.12));fig.subplots_adjust(left=.17,right=.97,bottom=.25,top=.94)
 for label,counts in [('Before selection',baseline),*[(k,residual[k]) for k in ['Greedy coverage','Exact union']]]:
  cdf(ax,counts,label,color=COLORS[label],lw=1.2,ls='--' if label=='Before selection' else '-')
 ax.set(xlabel='Remaining source identities',ylabel='Repositories at or below (%)');ax.legend(loc='lower right',fontsize=6,frameon=False,handlelength=1.4)
 save(fig,'source_multiplicity_compact')
 # A 2x2 selection/evaluation grid for each method and metric.
 rows=d['version_representation_curves']
 reps=['package_projected','version_continuous']
 available=sorted({r['selection_representation']for r in rows});name_rep=next(x for x in available if x!='version_continuous');reps=[name_rep,'version_continuous']
 matrices={};fig,axes=plt.subplots(2,3,figsize=(7.1,4.0));fig.subplots_adjust(left=.16,right=.98,bottom=.13,top=.89,hspace=.55,wspace=.32)
 for i,method in enumerate(['exact_union','greedy_coverage']):
  for j,(key,title)in enumerate([('covered_endpoints','C: repositories'),('scenario_exposure_reduction_fraction','H: evaluation pair mass (%)'),('fully_protected_endpoints','P: all-source exclusion')]):
   matrix=[]
   for ev in reps:
    vals=[]
    for sel in reps:
     matches=[r for r in rows if r['endpoint']=='workflow_repositories'and r['method']==method and r['budget']==100 and r['selection_representation']==sel and r['evaluation_representation']==ev]
     if not matches and sel==ev==name_rep:
      matches=[r for r in d['deterministic_curves']if r['endpoint']=='workflow_repositories'and r['method']==method and r['budget']==100]
     assert len(matches)==1,(sel,ev,method,len(matches))
     vals.append(matches[0][key]*(100 if j==1 else 1))
    matrix.append(vals)
   matrices[method+'/'+key]=matrix
   ax=axes[i,j];ax.imshow(matrix,cmap='Blues',aspect='auto',vmin=0)
   for y in range(2):
    for x in range(2):ax.text(x,y,f'{matrix[y][x]:.2f}'if j==1 else f'{matrix[y][x]:,.0f}',ha='center',va='center',fontsize=9,color='white'if matrix[y][x]>.55*np.max(matrix)else'#17354b')
   ax.set_xticks([0,1],['Name','Version']);ax.set_yticks([0,1],['Name','Version']if j==0 else[])
   if i==0:ax.set_title(title,fontsize=8)
   if j==0:ax.set_ylabel(('Exact union'if i==0 else'Greedy coverage')+'\nEvaluate on',fontsize=8)
   if i==1:ax.set_xlabel('Select on',fontsize=8)
 save(fig,'representation_matrix')
 # Separate populations avoid falsely adding overlapping missingness counts.
 fig,axes=plt.subplots(1,3,figsize=(7.1,2.65));fig.subplots_adjust(left=.02,right=.99,bottom=.08,top=.87,wspace=.14)
 pop=d['population']
 panels=[('Graph identifiers',[('Retained graph IDs',scope['graph_identifier_count']),('Ordinary-shaped names',scope['ordinary_name_count']),('Bundled contexts',scope['context_marker_identifier_count'])],'Shape does not verify registry existence.'),('Workflow endpoint map',[('Positive package names',pop['workflow_positive_packages']),('Repository keys',pop['workflow_positive_repositories']),('With observed sources',7158)],'15,233 packages map to 7,171 keys;\n13 keys have no observed source.'),('Frozen metadata pilot',[('Selected graph IDs',cohort['cohort_size']),('Ordinary-shaped names',92),('Metadata captures',cohort['successful_metadata_rows'])],'Eight contexts: HTTP 405\nTwo ordinary names: HTTP 404\nAll 100 outcomes pending.')]
 for ax,(title,items,note)in zip(axes,panels):
  ax.set_axis_off();ax.set_title(title,fontsize=9,loc='left')
  for i,(label,value)in enumerate(items):
   y=.86-i*.22
   ax.text(.02,y,label,fontsize=7.5,va='center');ax.text(.97,y,f'{value:,}',ha='right',va='center',fontsize=10,fontweight='bold',color='#285d85');ax.axhline(y-.09,xmin=.02,xmax=.98,color='#d9e2e7',lw=.7)
  ax.text(.02,.12,note,fontsize=6.5,color='#586977',va='top',linespacing=1.5)
 save(fig,'observation_scope')
 stems=['source_multiplicity','source_multiplicity_compact','representation_matrix','observation_scope']
 record={'source_sha256':{p:sha(ROOT/p)for p in INPUTS},'renderer_sha256':sha(Path(__file__)),'figures':{stem:{ext:sha(FIG/f'{stem}.{ext}')for ext in('pdf','svg','png')}for stem in stems},'source_cardinality':dict(sorted(baseline.items())),'residual_cardinality':{k:dict(sorted(v.items()))for k,v in residual.items()},'representation_matrices':matrices,'excluded_source_free_endpoints':13,'evaluation_pair_denominators':{'name':462170,'version':266016}}
 (ROOT/'manuscript/results/review_figure_data.json').write_text(json.dumps(record,indent=2)+'\n')
 print('Rendered four evidence-derived figure sets, including one compact conference variant.')
if __name__=='__main__':main()
