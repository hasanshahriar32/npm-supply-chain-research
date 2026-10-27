#!/usr/bin/env python3
"""Paired transport of frozen selections; human and automated labels stay distinct."""
import argparse
import csv
import json
import math

from journal_revision_common import ROOT, OUT, baseline, dump, metric, sha, stamp

LABELS=['repository_mapping_supported','workflow_file_present','install_directive_observed',
        'lockfile_present','dependency_version_supported']


def review_status(sample):
    folder=ROOT/'manuscript_q1/review_packets'
    sheets=[]
    for who in ['Shahriar_Hasan','Ashikul_Islam']:
        p=folder/f'{who}_independent_labels.csv'
        if not p.exists():
            folder.mkdir(parents=True,exist_ok=True)
            evidence_path=OUT/'endpoint_audit/automated_evidence.json'
            commits={r['audit_id']:r.get('observed_commit_sha','') for r in json.loads(evidence_path.read_text())} if evidence_path.exists() else {}
            with p.open('w',newline='') as f:
                fields=['audit_id','repository','commit_sha',*LABELS,'evidence_notes']
                w=csv.DictWriter(f,fields);w.writeheader()
                for r in sample:w.writerow({'audit_id':r['audit_id'],'repository':r['repository'],'commit_sha':commits.get(r['audit_id'],'')})
        with p.open() as f:rows=list(csv.DictReader(f))
        assert len(rows)==len(sample) and {r['audit_id'] for r in rows}=={r['audit_id'] for r in sample}
        assert len({r['audit_id'] for r in rows})==len(rows)
        sheets.append({r['audit_id']:r for r in rows})
    completed=0;agreements=0;comparisons=0;unresolved=[];consensus=[]
    for s in sample:
        aid=s['audit_id'];row={'audit_id':aid,'repository':s['repository']}
        assert all(sheet[aid]['repository']==s['repository'] for sheet in sheets), 'Review row repository mismatch'
        complete=True
        for label in LABELS:
            a,b=[sheet[aid][label].strip().lower() for sheet in sheets]
            assert a in ['','supported','unsupported','unknown'] and b in ['','supported','unsupported','unknown']
            if not a or not b:
                complete=False;row[label]='pending';continue
            comparisons+=1;agreements+=a==b
            row[label]=a if a==b else 'requires_adjudication'
            if a!=b:unresolved.append({'audit_id':aid,'label':label,'reviewer_1':a,'reviewer_2':b,'adjudicated_label':'','reason':''})
        if complete and not all(sheet[aid].get('evidence_notes','').strip() for sheet in sheets):
            complete=False
        completed+=complete
        consensus.append(row)
    adjudication=folder/'adjudication.csv'
    if unresolved and not adjudication.exists():
        with adjudication.open('w',newline='') as f:
            w=csv.DictWriter(f,list(unresolved[0]));w.writeheader();w.writerows(unresolved)
    if adjudication.exists():
        with adjudication.open() as f:decisions=list(csv.DictReader(f))
        lookup={(r['audit_id'],r['label']):r for r in decisions}
        for row in consensus:
            for label in LABELS:
                if row[label]=='requires_adjudication':
                    decision=lookup.get((row['audit_id'],label),{})
                    value=decision.get('adjudicated_label','').strip().lower()
                    if value in ['supported','unsupported','unknown'] and decision.get('reason','').strip():row[label]=value
    finished=completed==len(sample) and all(r[k] in ['supported','unsupported','unknown'] for r in consensus for k in LABELS)
    status={'authors_expected':2,'independent_rows_complete':completed,'sample_rows':len(sample),
            'completed_label_comparisons':comparisons,'initial_agreements':agreements,
            'raw_agreement':agreements/comparisons if comparisons else None,
            'human_review_complete_and_adjudicated':finished,'no_labels_inferred_from_blank_cells':True}
    dump(OUT/'endpoint_audit/human_review_status.json',status)
    if finished:dump(OUT/'endpoint_audit/labels_adjudicated.json',consensus)
    return status,consensus


def retained_orders(data):
    obj=json.loads((ROOT/'manuscript_q1/results/quorum_reproducibility.json').read_text())['selections']
    lookup={name:i for i,name in enumerate(data['maintainers'])}
    return {k:[lookup[x[0]] for x in v] for k,v in obj.items()}


def weighted_metrics(rows,selected,eligible):
    # Horvitz-Thompson endpoint totals and descriptive Hajek pair-mass ratio.
    c=p=num=den=n=0.0
    for r in rows:
        if r['audit_id'] not in eligible:continue
        src=int(r['source_mask'],16);w=r['design_weight'];removed=(src&selected).bit_count()
        n+=w;c+=w*bool(removed);p+=w*(bool(src) and src&selected==src)
        num+=w*removed;den+=w*src.bit_count()
    return {'weighted_C':c,'weighted_P':p,'weighted_endpoint_total':n,
            'weighted_pair_total':den,'weighted_H_pct':100*num/den if den else None}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--label-source',choices=['automated','human'],default='human')
    args=parser.parse_args()
    sample=json.loads((ROOT/'manuscript_q1/protocols/endpoint_audit_sample.json').read_text())
    status,human=review_status(sample)
    if args.label_source=='human' and not status['human_review_complete_and_adjudicated']:
        print(json.dumps({'status':'pending_human_review',**status},indent=2));return
    if args.label_source=='automated':
        evidence=json.loads((OUT/'endpoint_audit/automated_evidence.json').read_text())
        labels={r['audit_id']:{k:('supported' if v=='supported_static' else 'unknown') for k,v in r['automated_labels'].items()} for r in evidence}
    else:labels={r['audit_id']:r for r in human}
    data=baseline();masks=[int(x,16) for x in data['maintainer_masks']];orders=retained_orders(data)
    strata={s:[r for r in sample if r['stratum']==s] for s in ['1','2-5','6-50','>50']}
    estimates={}
    for label in LABELS:
        point=variance=unknown=0.0
        for frame in strata.values():
            n=len(frame);N=frame[0]['stratum_population'];v=[labels[r['audit_id']][label]=='supported' for r in frame]
            p=sum(v)/n;weight=N/7158;point+=weight*p
            if n>1:variance+=weight**2*(1-n/N)*(sum((x-p)**2 for x in v)/(n-1))/n
            unknown+=weight*sum(labels[r['audit_id']][label]=='unknown' for r in frame)/n
        estimates[label]={'weighted_documented_support_fraction':point,
                          'weighted_unknown_fraction':unknown,
                          'descriptive_normal_interval_lower':max(0,point-1.96*math.sqrt(variance)),
                          'descriptive_normal_interval_upper':min(1,point+1.96*math.sqrt(variance)),
                          'identification_interval_assigned_unknowns':[point,min(1,point+unknown)],
                          'interval_note':'Approximate stratified sampling interval for documented support only; uncertainty about unknown labels is separate. Boundary cases need caution.'}
    results=[]
    definitions={'mapping':['repository_mapping_supported'],
                 'mapping_workflow':['repository_mapping_supported','workflow_file_present'],
                 'mapping_workflow_install':['repository_mapping_supported','workflow_file_present','install_directive_observed']}
    for label,needed in definitions.items():
        supported={r['audit_id'] for r in sample if all(labels[r['audit_id']][k]=='supported' for k in needed)}
        unresolved={r['audit_id'] for r in sample if not any(labels[r['audit_id']][k]=='unsupported' for k in needed)}-supported
        for scenario,eligible in [('documented',supported),('unresolved_included',supported|unresolved)]:
            subset=[r for r in sample if r['audit_id'] in eligible]
            endpoint_mask=sum(1<<r['index'] for r in subset)
            restricted=[m&endpoint_mask for m in masks]
            sources=[int(r['source_mask'],16) for r in subset]
            for method,order in orders.items():
                for budget in [1,5,10,25,50,100]:
                    chosen=order[:budget];selected=sum(1<<m for m in chosen)
                    results.append({'definition':label,'unknown_scenario':scenario,'method':method,'budget':budget,
                                    'label_source':args.label_source,'sample_eligible':len(subset),'sample_unresolved':len(unresolved),
                                    **metric(chosen,restricted,sources,len(subset)),
                                    **weighted_metrics(sample,selected,eligible)})
    out=OUT/'endpoint_transport';out.mkdir(exist_ok=True)
    dump(out/f'{args.label_source}_results.json',results)
    with (out/f'{args.label_source}_results.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,list(results[0]));w.writeheader();w.writerows(results)
    dump(out/f'{args.label_source}_summary.json',{'label_source':args.label_source,'human_status':status,
         'estimates':estimates,'interpretation':'Current-time static audit; automated labels are provisional evidence candidates, not independent human validation.',
         'population':'original 7158 endpoint frame, not all npm','scenario_warning':'H all-in/all-out scenarios are not sharp bounds',
         'created_at_utc':stamp(),'script_sha256':sha(__file__)})
    print(json.dumps({'label_source':args.label_source,'rows':len(results),'human_review_complete':status['human_review_complete_and_adjudicated'],'estimates':estimates},indent=2))


if __name__=='__main__':main()
