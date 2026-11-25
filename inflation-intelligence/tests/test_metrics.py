"""Metrics against the hand-traced toy table (2026-11-25) and edge cases."""

import unittest
from fractions import Fraction

from evaluation.metrics import macro_f1, score_task

# Toy stance table: rows = true, cols = predicted (backward, forward, na)
#   backward: 5 1 0 / forward: 2 1 0 / na: 0 0 1
TRUE = ["backward"] * 6 + ["forward"] * 3 + ["na"]
PRED = ["backward"] * 5 + ["forward"] + ["backward"] * 2 + ["forward"] + ["na"]


class ToyTableTests(unittest.TestCase):
    def setUp(self):
        self.s = score_task(TRUE, PRED, "stance")  # labels: forward, backward, na

    def test_accuracy(self):
        self.assertAlmostEqual(self.s.accuracy, 0.7)

    def test_per_class_f1_matches_hand_trace(self):
        f1 = dict(zip(self.s.labels, self.s.f1))
        self.assertAlmostEqual(f1["backward"], float(Fraction(10, 13)))
        self.assertAlmostEqual(f1["forward"], float(Fraction(2, 5)))
        self.assertAlmostEqual(f1["na"], 1.0)

    def test_forward_precision_is_column_recall_is_row(self):
        i = self.s.labels.index("forward")
        self.assertAlmostEqual(self.s.precision[i], 1 / 2)
        self.assertAlmostEqual(self.s.recall[i], 1 / 3)

    def test_headline_excludes_na(self):
        expected = (10 / 13 + 2 / 5) / 2  # not (10/13 + 2/5 + 1) / 3 = 0.723
        self.assertAlmostEqual(self.s.macro_f1, expected)
        self.assertAlmostEqual(macro_f1(TRUE, PRED, "stance"), expected)

    def test_na_counts(self):
        self.assertEqual((self.s.na_predicted, self.s.na_true, self.s.na_correct), (1, 1, 1))


class EdgeCaseTests(unittest.TestCase):
    def test_never_predicted_class_scores_zero_and_is_flagged(self):
        s = score_task(["forward", "backward"], ["backward", "backward"], "stance")
        i = s.labels.index("forward")
        self.assertEqual((s.precision[i], s.f1[i]), (0.0, 0.0))
        self.assertIn("forward", s.never_predicted)

    def test_wrong_na_prediction_still_lowers_headline(self):
        perfect = macro_f1(["forward", "backward"], ["forward", "backward"], "stance")
        with_na = macro_f1(["forward", "backward"], ["na", "backward"], "stance")
        self.assertLess(with_na, perfect)

    def test_unknown_label_rejected(self):
        with self.assertRaises(ValueError):
            score_task(["forward"], ["sideways"], "stance")


if __name__ == "__main__":
    unittest.main()
