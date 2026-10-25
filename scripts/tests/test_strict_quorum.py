"""Boundary and exhaustive small-universe tests for the explicit strict metric."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from study_q1_quorum_and_oct2026 import strict_counted

class StrictQuorumTests(unittest.TestCase):
    def test_exhaustive_set_oracle(self):
        for source in range(64):
            sources = {i for i in range(6) if source & (1 << i)}
            for selected in range(64):
                hardened = {i for i in range(6) if selected & (1 << i)}
                for k in (1, 2, 3, 5):
                    remaining = sources - hardened
                    expected = bool(sources) and (not remaining or (len(sources) >= k and len(remaining) < k))
                    self.assertEqual(strict_counted(source, selected, k), expected)
                    self.assertFalse(strict_counted(source, 0, k))
                    self.assertEqual(strict_counted(source, selected, 1), bool(sources) and not remaining)
                    if expected:
                        self.assertTrue(sources & hardened)
                        if len(sources) < k:
                            self.assertFalse(remaining)
                        for extra in range(6):
                            self.assertTrue(strict_counted(source, selected | (1 << extra), k))

    def test_compact_formula_is_not_equivalent(self):
        # n=2, remaining=1, k=3: the proposed compact expression says True.
        self.assertTrue(1 < min(3, 2))
        self.assertFalse(strict_counted(0b11, 0b01, 3))

    def test_k_is_not_monotone(self):
        self.assertTrue(strict_counted(0b11, 0b01, 2))
        self.assertFalse(strict_counted(0b11, 0b01, 3))

    def test_single_source_and_empty_source(self):
        for k in (1, 2, 3, 5):
            self.assertFalse(strict_counted(0, 0, k))
            self.assertFalse(strict_counted(1, 0, k))
            self.assertTrue(strict_counted(1, 1, k))

if __name__ == '__main__':
    unittest.main()
