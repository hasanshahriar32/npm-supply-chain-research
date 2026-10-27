#!/usr/bin/env python3
"""Render measured scalarization, exclusion and assumed-weight figures."""
from pathlib import Path
import json,hashlib,os,shutil
os.environ.setdefault('MPLCONFIGDIR','/tmp/npm-q1-matplotlib')
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
FIG=ROOT/'manuscript_q1/figures';OUT=ROOT/'manuscript/results/q1_journal'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(fig,stem):
 for ext in ('pdf','svg','png'):
  p=FIG/f'{stem}.{ext}'
  fig.savefig(p,dpi=240,metadata={'CreationDate':None,'ModDate':None}if ext=='pdf'else{'Date':None}if ext=='svg'else None)
  shutil.copy2(p,OUT/p.name)
 plt.close(fig)
def main():
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':8,'axes.labelsize':8,'axes.titlesize':9,'legend.fontsize':7,'pdf.fonttype':42,'ps.fonttype':42,'axes.spines.top':False,'axes.spines.right':False,'svg.hashsalt':'npm-journal-review'})
 source=ROOT/'manuscript/results/q1_journal_experiments.json';d=json.loads(source.read_text());alphas=['0.0','0.1','0.25','0.5','0.75','0.9','1.0']
 fig,ax=plt.subplots(figsize=(3.45,2.85));fig.subplots_adjust(left=.18,right=.96,bottom=.19,top=.96)
 for key,label,color,marker in [('pareto_name_graph','Name projection','#285d85','o'),('pareto_version_continuous_graph','Version continuity','#00858b','s')]:
  r=[d[key][a]['100']for a in alphas];ax.plot([v['C_pct']for v in r],[v['H_pct']for v in r],marker=marker,color=color,lw=1.2,ms=3,label=label)
 mid=d['pareto_name_graph']['0.5']['100'];ax.scatter([mid['C_pct']],[mid['H_pct']],marker='*',s=65,color='#8660a8',zorder=4)
 ax.annotate('Equal weighting\n'+r'$\alpha=0.50$',(mid['C_pct'],mid['H_pct']),xytext=(62,23),arrowprops={'arrowstyle':'-','color':'#8660a8'},fontsize=7,color='#61457e')
 ax.set(xlabel='Workflow repository coverage C (%)',ylabel='Scenario exposure share H (%)',xlim=(58,80),ylim=(8,45));ax.grid(alpha=.18);ax.legend(loc='upper right',frameon=False,fontsize=6.5)
 save(fig,'q1_pareto_frontier')
 fig,ax=plt.subplots(figsize=(3.45,2.7));fig.subplots_adjust(left=.17,right=.96,bottom=.19,top=.95)
 budgets=[10,25,50,100]
 for label,values,color,mark in [('Direct exclusion',[d['direct_p_optimization'][str(b)]['P']for b in budgets],'#b57720','o'),('Greedy coverage',[d['pareto_name_graph']['1.0'][str(b)]['P']for b in budgets],'#00858b','s'),('Exact union',[d['pareto_name_graph']['0.0'][str(b)]['P']for b in budgets],'#285d85','D')]:
  ax.plot(budgets,values,color=color,marker=mark,lw=1.3,ms=3,label=label)
 ax.set(xlabel='Selected identity budget',ylabel='All-source exclusions P',xlim=(5,110),ylim=(0,1150));ax.grid(axis='y',alpha=.18);ax.legend(frameon=False,loc='upper left',fontsize=7);save(fig,'q1_supermodular_p')
 keys=['Exact Union (Unweighted)','Greedy Coverage','Pareto Hybrid (alpha=0.50)','Weight-Aware Sole Optimum','Weight-Aware Package-Sole Optimum']
 labels=['Exact union','Greedy coverage','Hybrid (0.50)','Account-sole aware','Package-sole aware']
 fields=['H_uniform_pct','H_sole_pct','H_pkg_sole_pct'];data=np.array([[d['heterogeneous_weights'][k][f]for f in fields]for k in keys])
 fig,ax=plt.subplots(figsize=(7.1,2.55));fig.subplots_adjust(left=.23,right=.98,bottom=.10,top=.72)
 ax.imshow(data,cmap='Blues',aspect='auto',vmin=0,vmax=100)
 for i in range(5):
  for j in range(3):ax.text(j,i,f'{data[i,j]:.2f}%',ha='center',va='center',fontsize=9,color='white'if data[i,j]>55 else'#17354b')
 ax.set_xticks([0,1,2],['Uniform H','Account-sole H','Package-sole H']);ax.xaxis.tick_top();ax.set_yticks(range(5),labels);ax.tick_params(length=0);ax.set_title('Exposure shares under separate assumed weightings · budget 100',pad=25,fontsize=9)
 save(fig,'q1_weight_sensitivity')
 stems=['q1_pareto_frontier','q1_supermodular_p','q1_weight_sensitivity']
 record={'source_sha256':{str(source.relative_to(ROOT)):sha(source)},'renderer_sha256':sha(Path(__file__)),'figures':{stem:{ext:sha(FIG/f'{stem}.{ext}')for ext in('pdf','svg','png')}for stem in stems}}
 (ROOT/'manuscript_q1/results/journal_figure_data.json').write_text(json.dumps(record,indent=2)+'\n')
 print('Rendered three journal figures with separate exclusion and weighting views.')
if __name__=='__main__':main()
