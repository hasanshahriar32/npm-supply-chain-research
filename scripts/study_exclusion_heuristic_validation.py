#!/usr/bin/env python3
"""Executed ablations and exact candidate-restricted P benchmarks."""
from collections import Counter
import csv
import itertools
import json
import random
import resource
import time

from journal_revision_common import ROOT, OUT, baseline, dump, exclusion_order, metric, sha, stamp, ssi

BUDGETS = [1, 5, 10, 25, 50, 100]


def csvout(path, rows):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, list(rows[0])); w.writeheader(); w.writerows(rows)


def exact_p(candidates, sources, budget):
    allowed = sum(1 << m for m in candidates)
    grouped = Counter(s for s in sources if s and not s & ~allowed)
    eligible = [(s, n) for s, n in grouped.items() if s.bit_count() <= budget]
    best, best_order, evaluated = -1, None, 0
    for choice in itertools.combinations(sorted(candidates), budget):
        selected = sum(1 << m for m in choice)
        score = sum(n for s, n in eligible if s & selected == s)
        evaluated += 1
        if score > best:
            best, best_order = score, list(choice)
    return best, best_order, evaluated


def synthetic(seed):
    rng = random.Random(seed)
    sources = []
    for _ in range(100):
        n = rng.choice([1,1,2,2,3,5,8,12])
        sources.append(sum(1 << m for m in rng.sample(range(20), n)))
    masks = [sum(1 << r for r, s in enumerate(sources) if s & (1 << m)) for m in range(20)]
    return masks, sources


def main():
    out = OUT / 'heuristic'; out.mkdir(parents=True, exist_ok=True)
    protocol = json.loads((ROOT/'manuscript_q1/protocols/revision_validation_protocol.json').read_text())
    data = baseline()
    masks = [int(x, 16) for x in data['maintainer_masks']]
    sources = [int(x['source_mask'], 16) for x in data['endpoints']]
    rows, selections = [], {}
    variants = [('full_cap10', {}), ('immediate_only', {'immediate_only': True}),
                ('no_reciprocal', {'reciprocal': False}), ('no_coverage_tie', {'coverage_tie': False})]
    variants += [(f'cap_{cap if cap is not None else "all"}', {'cap':cap})
                 for cap in [1,5,20,None]]
    variants += [(f'random_tie_{seed:02}', {'tie_seed': seed}) for seed in range(30)]
    for label, params in variants:
        order, timing = exclusion_order(masks, sources, 100, **params)
        selections[label] = order
        for b in BUDGETS:
            rows.append({'variant':label, 'budget':b, **metric(order[:b],masks,sources,len(sources)),
                         **timing, 'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss})
        print(label, 'P100=', rows[-1]['P'], 'seconds=',round(timing['wall_seconds'],3),flush=True)
    # Equivalence gate against the previously retained exact ordered selection.
    retained = json.loads((ROOT/'manuscript_q1/results/quorum_reproducibility.json').read_text())['selections']
    old = retained[r'Direct Supermodular $P(S)$']
    if isinstance(old, dict):
        old = old.get('ordered_indices', old.get('selected_indices', old.get('indices',old)))
    # The retained manifest uses usernames rather than exposing numeric ordering assumptions.
    if old and isinstance(old[0], (str,list)):
        lookup={name:i for i,name in enumerate(data['maintainers'])}
        old=[lookup[x[0] if isinstance(x,list) else x] for x in old]
    assert selections['full_cap10'] == old, 'Shared rule changed the frozen original order'
    assert rows[5]['P']==1022 and rows[5]['C']==5020
    csvout(out/'ablations.csv',rows);dump(out/'selections.json',selections)
    print('Original-order equivalence passed; starting exact benchmarks',flush=True)
    exact_rows, instances = [], []
    low = [s for s in sources if 1 <= s.bit_count() <= 5]
    ranked = sorted(range(len(masks)),key=lambda m:(-masks[m].bit_count(),m))
    rng=random.Random(2026102702)
    for instance in range(32):
        if instance < 20:
            pool=set()
            for s in rng.sample(low,min(30,len(low))):
                group=set(ssi.bit_indices(s))
                if len(pool|group)<=20:pool|=group
            for m in ranked:
                if len(pool)==20:break
                pool.add(m)
            cand=sorted(pool); mm,ss=masks,sources;kind='empirical_candidate_restricted'
        else:
            mm,ss=synthetic(2026102800+instance);cand=list(range(20));kind='synthetic'
        spec={'instance':instance,'kind':kind,'candidates':cand,
              'source_count':len(ss),'sources_hex':[hex(s) for s in ss] if kind=='synthetic' else None,
              'complete_source_sets_preserved':True}
        instances.append(spec)
        direct,_=exclusion_order(mm,ss,5,candidates=cand)
        union=sorted(cand,key=lambda m:(-mm[m].bit_count(),m))[:5]
        greedy,_=ssi.lazy_greedy(mm,cand,list(range(len(mm))),5)
        for b in [1,3,5]:
            start=time.perf_counter(); optimum,best,n=exact_p(cand,ss,b)
            for method,order in [('direct_p',direct),('exact_union',union),('greedy_coverage',greedy)]:
                res=metric(order[:b],mm,ss,len(ss))
                assert res['P']<=optimum
                exact_rows.append({'instance':instance,'kind':kind,'budget':b,'method':method,
                                   'candidate_count':len(cand),'exact_P':optimum,'achieved_P':res['P'],
                                   'absolute_gap':optimum-res['P'],'ratio':res['P']/optimum if optimum else None,
                                   'combinations':n,'exact_wall_seconds':time.perf_counter()-start})
        print('exact instance',instance,'complete',flush=True)
    csvout(out/'exact_comparison.csv',exact_rows);dump(out/'exact_instances.json',instances)
    tie=[r for r in rows if r['budget']==100 and r['variant'].startswith('random_tie')]
    direct=[r for r in exact_rows if r['method']=='direct_p']
    summary={'completed_at_utc':stamp(),'original_order_equivalence':True,'ablations':len(variants),
             'tie_P100_min':min(r['P'] for r in tie),'tie_P100_max':max(r['P'] for r in tie),
             'exact_instances':32,'exact_comparisons':len(exact_rows),
             'direct_exact_hits':sum(r['absolute_gap']==0 for r in direct),'direct_benchmarks':len(direct),
             'direct_worst_absolute_gap':max(r['absolute_gap'] for r in direct),
             'population_optimality_claim':False,'protocol_sha256':sha(ROOT/'manuscript_q1/protocols/revision_validation_protocol.json'),
             'source_archive_sha256':data['archive_sha256'],'script_sha256':sha(__file__),
             'rows':rows,'exact_rows':exact_rows}
    dump(out/'summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k not in ['rows','exact_rows']},indent=2))


if __name__=='__main__':
    main()
