"""Derive conference sensitivities from retained source/remaining-cardinality evidence."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    provenance = ROOT / 'manuscript_q1/results/quorum_reproducibility.json'
    results = ROOT / 'manuscript_q1/results/q1_quorum_exclusion.json'
    meta = json.loads(provenance.read_text())
    strict = json.loads(results.read_text())
    assert meta['metric_version'] == 'strict_zero_anchored_v1'
    distribution = meta['source_cardinality_distribution']
    baseline = distribution['1']
    rows=[]
    for hist in meta['cardinality_histograms']:
        if hist['budget'] != 100:
            continue
        row = next(r for r in strict if r['strategy']==hist['strategy'] and r['budget']==100)
        bins=hist['counts']
        assert sum(c for n,rem,c in bins)==7158
        residual=sum(c for n,rem,c in bins if rem<2)
        strict_p2=sum(c for n,rem,c in bins if rem==0 or (n>=2 and rem<2))
        assert strict_p2==row['P_2']
        rows.append({'strategy':row['strategy'],'budget':100,'C':row['C'],'H_pct':row['H_pct'],
                     'P1':row['P_1'],'T2':residual,'delta_T2':residual-baseline,
                     'P2_strict':strict_p2,'H_eta_090_pct':0.9*row['H_pct']})
    for prefix,expected in [('Greedy',(2112,396,1145)),('Exact',(2137,421,793)),('Pareto',(2153,437,961))]:
        row=next(row for row in rows if row['strategy'].startswith(prefix))
        assert (row['T2'],row['delta_T2'],row['P2_strict'])==expected
    out={'population':{'workflow_universe':7171,'nonempty_source_endpoints':7158,'source_free_excluded':13},
         'definitions':{'T2':'nonempty source sets with remaining<2','delta_T2':'T2(S)-T2(empty)',
                        'P2_strict':'nonempty source sets with remaining=0 or (total>=2 and remaining<2)',
                        'H_eta':'hypothetical uniform efficacy multiplier, not a measured bypass rate'},
         'T2_empty':baseline,'P2_strict_empty':0,'budget100':rows,
         'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in (provenance,results,ROOT/'scripts/generate_conference_modernization.py')}}
    target=ROOT/'manuscript/results/conference_modernization.json'
    target.write_text(json.dumps(out,indent=2)+'\n')
    print('Verified residual increments and strict counts; wrote',target)

if __name__=='__main__':
    main()
