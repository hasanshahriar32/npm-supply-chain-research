"""Regression cases for the active-table discrepancies found in review."""
import json,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'scripts'))
from verify_reconciled_papers import validate_budget_table
class BudgetEvidenceTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  cls.baseline=json.loads((ROOT/'manuscript/results/structural_interventions/results.json').read_text())
  cls.table=(ROOT/'manuscript_q1/tables/q1_multi_budget_table.tex').read_text()
 def test_complete_generated_grid_passes(self):
  self.assertEqual(validate_budget_table(self.table,self.baseline),126)
 def test_old_budget_one_greedy_coverage_is_rejected(self):
  corrupted=self.table.replace('35.46 & 35.46','35.46 & 23.65',1)
  self.assertNotEqual(corrupted,self.table)
  with self.assertRaises(AssertionError):validate_budget_table(corrupted,self.baseline)
 def test_analytical_expectation_cannot_replace_sample_mean(self):
  corrupted=self.table.replace('0.80 $\\pm$ 0.03','0.82 $\\pm$ 0.03')
  self.assertNotEqual(corrupted,self.table)
  with self.assertRaises(AssertionError):validate_budget_table(corrupted,self.baseline)
 def test_missing_budget_row_is_rejected(self):
  corrupted='\n'.join(line for line in self.table.splitlines()if not line.startswith('5 & P &'))
  with self.assertRaises(AssertionError):validate_budget_table(corrupted,self.baseline)
if __name__=='__main__':unittest.main()
