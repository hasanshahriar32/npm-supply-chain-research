"""Detailed, native-vector study diagrams and measured result plots for Task 16."""
import hashlib
import json
from pathlib import Path
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Patch
from matplotlib.lines import Line2D
from matplotlib.ticker import FixedLocator, FuncFormatter, NullLocator

PAPER=Path(__file__).resolve().parents[1]
ROOT=PAPER.parent
FIG=PAPER/'figures'
INK='#213547'; BLUE='#28618a'; TEAL='#007f83'; GOLD='#a56b16'; PURPLE='#8054a3'; GRAY='#606f7b'; PALE='#f2f6f9'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':7.5,'axes.labelsize':7.5,'xtick.labelsize':7,
 'ytick.labelsize':7,'legend.fontsize':7,'pdf.fonttype':42,'ps.fonttype':42,'svg.fonttype':'none',
 'svg.hashsalt':'npm-task16-publication','axes.spines.top':False,'axes.spines.right':False})

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def save(fig,name):
    fig.canvas.draw()
    for ax in fig.axes:
        for txt in ax.texts:
            if txt.get_text() and not fig.bbox.contains(*txt.get_window_extent().get_points()[0]):
                raise ValueError(f'Text outside figure: {name}: {txt.get_text()}')
    for ext in ('pdf','svg','png'):
        meta={'CreationDate':None,'ModDate':None} if ext=='pdf' else {'Date':None} if ext=='svg' else None
        fig.savefig(FIG/f'{name}.{ext}',dpi=300,metadata=meta)
        if ext=='svg':
            path=FIG/f'{name}.{ext}'
            path.write_text('\n'.join(line.rstrip() for line in path.read_text().splitlines())+'\n')
    plt.close(fig)

def canvas(w,h):
    fig=plt.figure(figsize=(w,h));ax=fig.add_axes([0,0,1,1]);ax.set(xlim=(0,w),ylim=(0,h));ax.axis('off');return fig,ax

def text(ax,x,y,s,size=7.5,color=INK,weight='normal',ha='left',va='center'):
    return ax.text(x,y,s,fontsize=size,color=color,fontweight=weight,ha=ha,va=va,linespacing=1.35)

def box(ax,x,y,w,h,title,body,color=BLUE):
    ax.add_patch(FancyBboxPatch((x,y),w,h,boxstyle='round,pad=0.025,rounding_size=0.04',facecolor=PALE,edgecolor=color,lw=.9))
    text(ax,x+.08,y+h-.17,title,size=8,color=color,weight='bold')
    text(ax,x+.08,y+h-.39,body,size=7.1,va='top')

def arrow(ax,a,b,color=GRAY):
    ax.add_patch(FancyArrowPatch(a,b,arrowstyle='-|>',mutation_scale=9,lw=1,color=color,shrinkA=0,shrinkB=0))

def architecture(d):
    p=d['population'];fig,ax=canvas(7.1,2.12)
    text(ax,.03,2.00,'OBSERVATION → RETAINED EVIDENCE → TYPED GRAPH → EXACT REACH',8.7,weight='bold')
    boxes=[(.05,'1  Public observations','npm: accounts + metadata\ndeps.dev: versioned edges\nGitHub: workflow flags',BLUE),
           (1.85,'2  Frozen archive',f"{p['packages']:,} package identifiers\n{p['identities']:,} observed usernames\n{p['maintainer_package_relations']:,} membership links",BLUE),
           (3.65,'3  Exposure model',f"{p['unique_package_edges']:,} name adjacencies\nReverse exposure edges\nDeduplicate repo keys",TEAL),
           (5.45,'4  Closure engine','SCC condensation → DAG\nEndpoint-bitset unions\nCross-check source sets',TEAL)]
    for x,title,body,col in boxes:box(ax,x,.78,1.56,1.01,title,body,col)
    for x in (1.61,3.41,5.21):arrow(ax,(x,1.28),(x+.20,1.28))
    text(ax,.09,.53,'Typed relations:',7.4,weight='bold')
    text(ax,1.25,.53,'maintainer  →  package  →  dependent  →  repository',7.8,TEAL,weight='bold')
    text(ax,1.25,.31,'membership       reverse reach         lexical mapping',7.0,GRAY)
    text(ax,.09,.09,'7,171 workflow repositories • 7,158 with observed sources • directory presence ≠ executed CI',7.1,GRAY)
    save(fig,'observation_workflow')
    # Restore the user's preferred architecture exactly from the retained vector source.
    for ext in ('pdf','svg','png','drawio'):
        shutil.copy2(FIG/'original_architecture'/f'study_system.{ext}', FIG/f'study_system.{ext}')

def methodology():
    fig,ax=canvas(3.45,2.12)
    text(ax,.02,2.00,'ANALYSIS AND VALIDATION WORKFLOW',8.1,weight='bold')
    items=[(.05,1.34,'1  Build exact sets','Reverse edges; SCC / DAG\nPortfolio unions; deduplicate'),
           (1.85,1.34,'2  Fix comparisons','5 baseline rules + 200 orders\nBudgets 1, 5, 10, 25, 50, 100'),
           (1.85,.71,'3  Evaluate selection','C: distinct endpoints\nH: pair mass; P: all sources'),
           (.05,.71,'4  Test assumptions','Version continuity; mappings\nDepth, ties, identity grouping'),
           (.05,.08,'5  Check correctness','BFS + incidence + hashes\n675 roots in 60 small graphs'),
           (1.85,.08,'6  Report limits','Hybrid + threshold counts\nOutcomes still pending')]
    # Font sizes and rows are designed for a single IEEE column.
    for x,y,title,body in items:
        ax.add_patch(FancyBboxPatch((x,y),1.51,.51,boxstyle='round,pad=.018,rounding_size=.035',facecolor=PALE,edgecolor=BLUE,lw=.8))
        text(ax,x+.055,y+.38,title,7.5,BLUE,weight='bold')
        text(ax,x+.055,y+.18,body,6.8)
    arrow(ax,(1.58,1.59),(1.81,1.59));arrow(ax,(2.60,1.31),(2.60,1.25))
    arrow(ax,(1.81,.97),(1.58,.97));arrow(ax,(.80,.68),(.80,.62));arrow(ax,(1.58,.34),(1.81,.34))
    save(fig,'study_methodology')

def semantics():
    fig,ax=canvas(3.45,2.20)
    text(ax,.03,2.08,'WHY VERSION CONTINUITY CHANGES REACH',8,weight='bold')
    text(ax,.06,1.82,'(a) Name projection joins incompatible versions',7.2,weight='bold')
    for x,label in ((.18,'p'),(1.38,'d'),(2.58,'r')):
        ax.add_patch(FancyBboxPatch((x,1.38),.60,.26,boxstyle='round,pad=.015',facecolor=PALE,edgecolor=GOLD))
        text(ax,x+.30,1.51,label,8,GOLD,ha='center')
    arrow(ax,(.81,1.51),(1.34,1.51),GOLD);arrow(ax,(2.01,1.51),(2.54,1.51),GOLD)
    text(ax,.06,1.15,'(b) Exact version keys prevent the splice',7.2,weight='bold')
    nodes=[(.08,.78,'p@1'),(1.17,.78,'d@1'),(1.17,.27,'d@2'),(2.53,.27,'r@1')]
    for x,y,label in nodes:
        ax.add_patch(FancyBboxPatch((x,y),.69,.29,boxstyle='round,pad=.015',facecolor=PALE,edgecolor=TEAL))
        text(ax,x+.345,y+.145,label,7.5,TEAL,ha='center')
    arrow(ax,(.81,.92),(1.12,.92),TEAL);arrow(ax,(1.91,.41),(2.48,.41),TEAL)
    text(ax,2.12,.91,'d@1 ≠ d@2\nNo p@1 → r@1',7,GRAY,ha='left')
    text(ax,.04,.08,'Illustrative reverse-reach example; not a measured installation.',6.8,GRAY)
    save(fig,'graph_semantics')

def curves(d,extra):
    from render_analysis_figures import METHODS
    budgets=[1,5,10,25,50,100]
    rows=[r for r in d['deterministic_curves'] if r['endpoint']=='workflow_repositories']
    rand=sorted([r for r in d['random_analytic_expectations'] if r['endpoint']=='workflow_repositories'],key=lambda r:r['budget'])
    fig,axes=plt.subplots(1,2,figsize=(7.1,2.35));fig.subplots_adjust(left=.075,right=.955,bottom=.34,top=.86,wspace=.34)
    handles=[]
    for i,(ax,field,title,ylabel,upper) in enumerate(zip(axes,
        ['coverage_fraction_observed','scenario_exposure_reduction_fraction'],
        ['(a) Distinct repository coverage C','(b) Scenario exposure reduction H'],['Covered repositories (%)','Removed pair mass (%)'],[87,40])):
        ax.set_xscale('log');ax.xaxis.set_major_locator(FixedLocator(budgets));ax.xaxis.set_minor_locator(NullLocator());ax.xaxis.set_major_formatter(FuncFormatter(lambda x,_:f'{x:g}'))
        ax.set(xlim=(.85,200),ylim=(0,upper),xlabel='Maintainer budget (log scale)',ylabel=ylabel);ax.set_title(title,fontsize=8,loc='left');ax.grid(axis='y',color='.90')
        for method,(label,color,marker,ls) in METHODS.items():
            rr=sorted([r for r in rows if r['method']==method],key=lambda r:r['budget'])
            line,=ax.plot(budgets,[100*r[field] for r in rr],color=color,marker=marker,linestyle=ls,lw=1.2,ms=3,label=label)
            if i==0:handles.append(line)
            if method in ('greedy_coverage','exact_union'):
                val=100*rr[-1][field];ax.text(111,val,f'{val:.1f}',fontsize=7,color=color,va='center')
        line,=ax.plot(budgets,[100*r['expected_'+field] for r in rand],color=GRAY,ls='--',lw=1,label='Random exact mean')
        if i==0:handles.append(line)
        for prefix,col,marker,label,offset in [('Pareto',PURPLE,'*','Hybrid, budget 100',-7),('Direct',GOLD,'P','Direct P, budget 100',7)]:
            row=next(r for r in extra['budget100'] if r['strategy'].startswith(prefix));val=100*row['C']/7171 if i==0 else row['H_pct']
            ax.scatter([100],[val],color=col,marker=marker,s=40,zorder=5)
            if i==1:ax.annotate(f'{val:.1f}',(100,val),xytext=(-28,offset),textcoords='offset points',fontsize=7,color=col)
            if i==0:handles.append(Line2D([],[],color=col,marker=marker,ls='',label=label))
    fig.legend(handles=handles,loc='lower center',bbox_to_anchor=(.52,.005),ncol=4,fontsize=6.9,columnspacing=1.2,handlelength=1.8,frameon=False)
    save(fig,'objective_tradeoff')

def partition(d):
    from render_analysis_figures import METHODS
    rr={r['method']:r for r in d['deterministic_curves'] if r['endpoint']=='workflow_repositories' and r['budget']==100}
    order=['greedy_coverage','exact_union','max_package_reach','sum_package_reach','portfolio'];labels=['Greedy','Exact union','Max reach','Sum reach','Portfolio']
    fig,ax=plt.subplots(figsize=(3.45,2.45));fig.subplots_adjust(left=.23,right=.985,bottom=.42,top=.78)
    for y,m in enumerate(order):
        r=rr[m];parts=[r['fully_protected_endpoints'],r['covered_endpoints']-r['fully_protected_endpoints'],7158-r['covered_endpoints']];left=0
        for count,col in zip(parts,[GOLD,BLUE,'#dfe5ea']):
            ax.barh(y,count,left=left,color=col,height=.64)
            ax.text(left+count/2,y,f'{count:,}',ha='center',va='center',fontsize=6.9,color='white' if col==BLUE else INK)
            left+=count
    ax.set(yticks=range(5),yticklabels=labels,ylim=(4.6,-.6),xlim=(0,7158),xlabel='Repositories with an observed source',xticks=[0,2000,4000,6000]);ax.grid(axis='x',color='.92');ax.set_axisbelow(True);ax.spines['left'].set_visible(False);ax.tick_params(axis='y',length=0)
    fig.text(.02,.95,'Covered does not mean all sources selected',fontsize=8,weight='bold')
    fig.text(.02,.86,'Budget 100 · all three segments labeled by count',fontsize=7,color=GRAY)
    fig.legend(handles=[Patch(color=GOLD,label='All sources selected (P)'),Patch(color=BLUE,label='Covered, other sources remain'),Patch(color='#dfe5ea',label='Uncovered; 13 source-free endpoints excluded')],loc='lower left',bbox_to_anchor=(.01,.005),fontsize=6.8,labelspacing=.4,frameon=False)
    save(fig,'coverage_partition')

def representation(d):
    rows={r['method']:r for r in d['deterministic_curves'] if r['endpoint']=='workflow_repositories' and r['budget']==100}
    vr={r['method']:r for r in d['version_representation_curves'] if r['endpoint']=='workflow_repositories' and r['budget']==100 and r['selection_representation']==r['evaluation_representation']=='version_continuous'}
    a=d['diagnostics']['workflow_repositories']['total_identity_endpoint_pairs'];b=d['version_representation']['workflow_repositories']['total_identity_endpoint_pairs']
    fig=plt.figure(figsize=(3.45,2.65));fig.text(.02,.955,'Representation sensitivity at budget 100',fontsize=8,weight='bold')
    ax=fig.add_axes([.30,.70,.65,.13]);ax.plot([b,a],[0,0],color='#b9c7d0',lw=2);ax.scatter([a,b],[0,0],color=[GRAY,TEAL],s=25)
    for x,col in [(a,GRAY),(b,TEAL)]:ax.annotate(f'{x:,}',(x,0),xytext=(0,6),textcoords='offset points',ha='center',fontsize=7,color=col)
    ax.set(xlim=(210000,515000),ylim=(-.5,.9),yticks=[],xticks=[250000,350000,450000]);ax.xaxis.set_major_formatter(FuncFormatter(lambda v,_:f'{v/1000:g}k'));ax.spines['left'].set_visible(False)
    fig.text(.02,.87,f'(a) Pair mass: −{100*(1-b/a):.2f}%',fontsize=7.2,weight='bold')
    for bottom,field,title,lim in [(.39,'covered_endpoints','(b) Covered repositories C',(4100,5800)),(.10,'scenario_exposure_reduction_fraction','(c) Removed exposure H (%)',(5,48))]:
        ax=fig.add_axes([.30,bottom,.65,.17]);fig.text(.02,bottom+.21,title,fontsize=7.2,weight='bold')
        for y,m in enumerate(['exact_union','greedy_coverage']):
            p=rows[m][field];v=vr[m][field]
            if field!='covered_endpoints':p*=100;v*=100
            ax.plot([p,v],[y,y],color='#b9c7d0',lw=2);ax.scatter([p,v],[y,y],color=[GRAY,TEAL],s=20)
            for value,col,dy,ha in [(p,GRAY,5,'right'),(v,TEAL,-9,'left')]:
                label=f'{value:,.0f}' if field=='covered_endpoints' else f'{value:.2f}'
                ax.annotate(label,(value,y),xytext=(0,dy),textcoords='offset points',ha=ha,fontsize=6.8,color=col)
        ax.set(xlim=lim,ylim=(-.6,1.6),yticks=[0,1],yticklabels=['Exact union','Greedy']);ax.tick_params(axis='y',length=0,labelsize=7);ax.tick_params(axis='x',labelsize=6.5,pad=1);ax.spines['left'].set_visible(False);ax.grid(axis='x',color='.92')
    fig.text(.30,.015,'Gray: name projection    Teal: version continuity',fontsize=6.7,color=GRAY)
    save(fig,'representation_detail')

def main():
    sources=[PAPER/'results/structural_interventions/results.json',PAPER/'results/conference_modernization.json']
    sources += [FIG/'original_architecture'/f'study_system.{ext}' for ext in ('pdf','svg','png','drawio')]
    d=json.loads(sources[0].read_text());extra=json.loads(sources[1].read_text())
    architecture(d);methodology();semantics();curves(d,extra);partition(d);representation(d)
    stems=['study_system','observation_workflow','study_methodology','graph_semantics','objective_tradeoff','coverage_partition','representation_detail']
    record={'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sources},
            'renderer_sha256':sha(Path(__file__)),
            'figures':{stem:{'pdf':sha(FIG/f'{stem}.pdf'),'svg':sha(FIG/f'{stem}.svg'),'png':sha(FIG/f'{stem}.png')} for stem in stems},
            'semantics':'The original icon architecture is restored verbatim from its retained PDF/SVG/PNG; architecture/methodology follow the implemented pipeline; version-splice topology is illustrative; plot marks derive from retained results.'}
    analysis_path=PAPER/'results/analysis_figure_data.json'
    if analysis_path.exists():
        analysis=json.loads(analysis_path.read_text())
        analysis['renderer']=str(Path(__file__).relative_to(PAPER))
        analysis['renderer_sha256']=sha(Path(__file__))
        for stem,dims in {'objective_tradeoff':(7.1,2.35),'coverage_partition':(3.45,2.45),'representation_detail':(3.45,2.65)}.items():
            analysis['figures'][stem]['width_inches'],analysis['figures'][stem]['height_inches']=dims
            for ext in ('pdf','svg','png'):
                analysis['figures'][stem]['outputs'][ext]['sha256']=sha(FIG/f'{stem}.{ext}')
        analysis_path.write_text(json.dumps(analysis,indent=2,sort_keys=True)+'\n')
    system_path=PAPER/'results/system_figure_data.json'
    if system_path.exists():
        system=json.loads(system_path.read_text())
        system['dimensions_inches'].update({'study_system':[7.1,3.35],'observation_workflow':[7.1,2.12],'study_methodology':[3.45,2.12],'graph_semantics':[3.45,2.20]})
        system_path.write_text(json.dumps(system,indent=2)+'\n')
    for stem in stems:
        for ext in ('pdf','svg','png'):
            shutil.copy2(FIG/f'{stem}.{ext}',ROOT/'manuscript_q1/figures'/f'{stem}.{ext}')
    (PAPER/'results/publication_figure_data.json').write_text(json.dumps(record,indent=2)+'\n')
    print('Rendered six detailed vector figure sets with source hashes.')

if __name__=='__main__':main()
