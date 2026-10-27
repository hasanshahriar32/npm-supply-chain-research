"""Boundary tests for new source-set and human-review semantics."""
import csv
import itertools
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import journal_revision_common as common
import study_exclusion_heuristic_validation as heuristic
import study_validated_endpoints as audit


class RevisionEvidenceTests(unittest.TestCase):
    def test_outside_candidate_sources_are_not_erased(self):
        # Account 0 alone cannot complete a two-source endpoint, even when 1 is ineligible.
        sources=[0b11,0b10];masks=[0b01,0b11]
        order,_=common.exclusion_order(masks,sources,1,candidates=[0])
        self.assertEqual(common.metric(order,masks,sources)['P'],0)
        optimum,_,_=heuristic.exact_p([0],sources,1)
        self.assertEqual(optimum,0)
        self.assertEqual(sources,[0b11,0b10])

    def test_exact_candidate_benchmark_matches_independent_subsets(self):
        sources=[0b001,0b011,0b110,0b100,0]
        best,order,n=heuristic.exact_p([0,1,2],sources,2)
        counts=[]
        for choice in itertools.combinations([0,1,2],2):
            selected=set(choice)
            counts.append(sum(bool(s) and {i for i in range(3) if s&(1<<i)}<=selected for s in sources))
        self.assertEqual(best,max(counts));self.assertEqual(n,3)

    def test_zero_source_endpoint_never_counts_as_excluded(self):
        result=common.metric([0],[1],[1,0],2)
        self.assertEqual(result['P'],1)
        self.assertEqual(result['endpoint_total'],2)
        self.assertEqual(result['source_reachable_endpoints'],1)

    def test_random_ties_reproduce_and_selection_is_unique(self):
        sources=[1,2,4,8];masks=[1,2,4,8]
        a,_=common.exclusion_order(masks,sources,4,tie_seed=11)
        b,_=common.exclusion_order(masks,sources,4,tie_seed=11)
        self.assertEqual(a,b);self.assertEqual(len(set(a)),4)

    def test_blank_human_sheets_do_not_become_unknown_completed_labels(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'manuscript_q1/review_packets';folder.mkdir(parents=True)
            sample=[{'audit_id':'A001','repository':'owner/repo'}]
            for author in ['Shahriar_Hasan','Md_Ashikul_Islam']:
                with (folder/f'{author}_independent_labels.csv').open('w',newline='') as f:
                    w=csv.DictWriter(f,['audit_id','repository',*audit.LABELS]);w.writeheader();w.writerow(sample[0])
            with patch.object(audit,'ROOT',root),patch.object(audit,'OUT',root/'results'):
                status,rows=audit.review_status(sample)
            self.assertFalse(status['human_review_complete_and_adjudicated'])
            self.assertEqual(status['independent_rows_complete'],0)
            self.assertEqual(rows[0][audit.LABELS[0]],'pending')

    def test_human_disagreement_keeps_adjudication_pending_and_reports_kappa(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);folder=root/'manuscript_q1/review_packets';folder.mkdir(parents=True)
            sample=[{'audit_id':'A001','repository':'owner/one'},{'audit_id':'A002','repository':'owner/two'}]
            for index,author in enumerate(['Shahriar_Hasan','Md_Ashikul_Islam']):
                with (folder/f'{author}_independent_labels.csv').open('w',newline='') as f:
                    w=csv.DictWriter(f,['audit_id','repository',*audit.LABELS,'evidence_notes']);w.writeheader()
                    for i,row in enumerate(sample):
                        value='unsupported' if index==1 and i==1 else 'supported'
                        w.writerow({**row,**{label:value for label in audit.LABELS},'evidence_notes':'Inspected recorded evidence'})
            with patch.object(audit,'ROOT',root),patch.object(audit,'OUT',root/'results'):
                status,rows=audit.review_status(sample)
            self.assertFalse(status['human_review_complete_and_adjudicated'])
            self.assertEqual(status['raw_agreement'],.5)
            self.assertEqual(status['initial_agreement_by_label'][audit.LABELS[0]]['cohen_kappa'],0)
            self.assertTrue((folder/'adjudication.csv').exists())


if __name__=='__main__':unittest.main()
