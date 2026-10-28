#!/usr/bin/env python3
"""Independent numeric and provenance gates for the journal validation revision."""
from collections import Counter
import csv
from datetime import datetime
import json
from pathlib import Path
import tempfile
from unittest.mock import patch

import journal_revision_common as common
from journal_revision_common import ROOT, OUT, dump, metric, sha, stamp, ssi
from study_exclusion_heuristic_validation import exact_p, synthetic


def verify(raw_evidence=True):
    protocol=ROOT/'manuscript_q1/protocols/revision_validation_protocol.json'
    proto=json.loads(protocol.read_text())
    sample_path=ROOT/'manuscript_q1/protocols/endpoint_audit_sample.json'
    sample=json.loads(sample_path.read_text())
    assert sha(sample_path)==proto['sample_sha256']
    assert len(sample)==120 and len({r['audit_id'] for r in sample})==120
    assert len({r['repository'] for r in sample})==120
    assert Counter(r['stratum'] for r in sample)=={'1':30,'2-5':30,'6-50':30,'>50':30}
    for row in sample:
        assert row['inclusion_probability']==row['stratum_sample']/row['stratum_population']
        assert row['design_weight']==row['stratum_population']/row['stratum_sample']
    data=common.baseline()
    # Rebuild every incidence mask from the immutable archive under a fresh cache.
    with tempfile.TemporaryDirectory(prefix='verify-revision-') as tmp:
        with patch.object(common,'OUT',Path(tmp)):
            independent=common.baseline()
    for key in ['maintainers','maintainer_masks','scores','total_pairs','endpoints']:
        assert data[key]==independent[key],f'Baseline cache differs from archive-derived {key}'
    masks=[int(x,16) for x in data['maintainer_masks']]
    sources=[int(x['source_mask'],16) for x in data['endpoints']]
    heuristic=json.loads((OUT/'heuristic/summary.json').read_text())
    assert heuristic['source_archive_sha256']==data['archive_sha256']
    assert heuristic['script_sha256']==sha(ROOT/'scripts/study_exclusion_heuristic_validation.py')
    choices=json.loads((OUT/'heuristic/selections.json').read_text())
    for r in heuristic['rows']:
        order=choices[r['variant']][:r['budget']]
        assert len(set(order))==len(order)==r['budget']
        actual=metric(order,masks,sources,len(sources))
        for key in ['C','P','H_pct','C_pct','pair_denominator']:
            assert actual[key]==r[key],(r['variant'],key)
    instances=json.loads((OUT/'heuristic/exact_instances.json').read_text())
    exact_checked=0
    for spec in instances:
        ss=sources if spec['kind']=='empirical_candidate_restricted' else [int(x,16) for x in spec['sources_hex']]
        for b in [1,3,5]:
            optimum,selection,count=exact_p(spec['candidates'],ss,b)
            rr=[r for r in heuristic['exact_rows'] if r['instance']==spec['instance'] and r['budget']==b]
            for r in rr:
                assert r['exact_P']==optimum and r['combinations']==count
                assert 0<=r['achieved_P']<=optimum
                assert r['absolute_gap']==optimum-r['achieved_P']
                assert r['ratio']==(r['achieved_P']/optimum if optimum else None)
                exact_checked+=1
    evidence=json.loads((OUT/'endpoint_audit/automated_evidence.json').read_text())
    assert {r['audit_id'] for r in evidence}=={r['audit_id'] for r in sample}
    frozen=datetime.fromisoformat(proto['frozen_at_utc'])
    observation_count=0
    for p in (OUT/'endpoint_audit/github_responses').glob('*.json'):
        record=json.loads(p.read_text())
        assert datetime.fromisoformat(record['observed_at_utc'])>=frozen
        observation_count+=1
    for r in evidence:
        assert r['human_review_status']=='pending_independent_authors'
        for path,meta in r['evidence_files'].items():
            if not raw_evidence:
                continue
            source=json.loads((ROOT/meta['response_file']).read_text())
            import hashlib
            assert hashlib.sha256(source['content'].encode()).hexdigest()==meta['sha256']
            assert source['request']['commit_sha']==r['observed_commit_sha']
    repl=json.loads((OUT/'replication/study_summary.json').read_text())
    graph=json.loads((OUT/'replication/graph.json').read_text())
    incidence=json.loads((OUT/'replication/incidence.json').read_text())
    assert repl['graph_sha256']==sha(OUT/'replication/graph.json')
    assert repl['script_sha256']==sha(ROOT/'scripts/study_replication_cohort.py')
    assert len(graph['nodes'])==repl['exact_version_nodes']==1641
    assert len(incidence['repositories'])==repl['workflow_repository_endpoints']==66
    assert sum(x['eligible'] for x in incidence['root_observations'])==70
    assert sum(x['root_request_succeeded'] for x in graph['root_bounds'])==94
    for r in repl['results']:
        mm=[int(x,16) for x in incidence[r['evaluation_representation']+'_masks']]
        ss=[int(x,16) for x in incidence[r['evaluation_representation']+'_sources']]
        order=incidence['orders_'+r['selection_representation']][r['method']][:r['budget']]
        actual=metric(order,mm,ss,66)
        for key in ['C','P','H_pct','C_pct','pair_denominator']:
            assert actual[key]==r[key],(r['method'],key)
    publication=json.loads((OUT/'publication_artifacts.json').read_text())
    assert publication['renderer_sha256']==sha(ROOT/'scripts/render_journal_validation.py')
    for p,h in publication['source_sha256'].items():assert sha(ROOT/p)==h,p
    presentation_path=ROOT/'manuscript_q1/results/emse_figure_presentation.json'
    presentation=json.loads(presentation_path.read_text()) if presentation_path.exists() else None
    for stem,outputs in publication['figures'].items():
        for ext,h in outputs.items():
            folder='editorial_inputs/' if presentation and stem in presentation['inputs'] else ''
            assert sha(ROOT/f'manuscript_q1/figures/{folder}{stem}.{ext}')==h
            if presentation:
                assert sha(ROOT/f'manuscript_q1/figures/{stem}.{ext}')==presentation['figures'][stem][ext]
    if presentation:
        assert sha(ROOT/'scripts/prepare_emse_figures.py')==presentation['renderer_sha256']
    for name,h in publication['tables'].items():assert sha(ROOT/'manuscript_q1/tables'/name)==h
    return {'status':'PASS','checked_at_utc':stamp(),'baseline_masks_independently_rebuilt':len(masks),
            'sample_units':120,'github_observation_records':observation_count,
            'ablation_metric_rows':len(heuristic['rows']),'exact_comparisons_recomputed':exact_checked,
            'fresh_cohort_metric_rows':len(repl['results']),'human_review_pending':True,
            'protocol_sha256':sha(protocol),'audit_raw_source_files_verified':raw_evidence}


if __name__=='__main__':
    result=verify();dump(OUT/'verification.json',result);print(json.dumps(result,indent=2))
