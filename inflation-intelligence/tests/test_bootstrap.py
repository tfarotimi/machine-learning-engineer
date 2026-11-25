"""Bootstrap behaviour on small constructed cases."""

import unittest

import numpy as np

from evaluation.bootstrap import bootstrap_ci, bootstrap_indices, paired_bootstrap


def acc(t, p):
    return float(np.mean(np.asarray(t) == np.asarray(p)))


class IndexTests(unittest.TestCase):
    def test_shape_range_and_reproducible(self):
        idx = bootstrap_indices(400, 50, seed=1)
        self.assertEqual(idx.shape, (50, 400))
        self.assertTrue(((idx >= 0) & (idx < 400)).all())
        np.testing.assert_array_equal(idx, bootstrap_indices(400, 50, seed=1))

    def test_about_37_percent_left_out(self):
        idx = bootstrap_indices(400, 200, seed=0)
        left_out = np.mean([1 - len(np.unique(r)) / 400 for r in idx])
        self.assertAlmostEqual(left_out, np.exp(-1), delta=0.02)


class CITests(unittest.TestCase):
    def test_interval_contains_point_and_perfect_model_has_no_spread(self):
        t = ["x"] * 30 + ["y"] * 30
        p = ["x"] * 25 + ["y"] * 5 + ["y"] * 30
        point, lo, hi = bootstrap_ci(t, p, acc)
        self.assertLessEqual(lo, point)
        self.assertLessEqual(point, hi)
        self.assertEqual(bootstrap_ci(t, t, acc)[1:], (1.0, 1.0))


class PairedTests(unittest.TestCase):
    def test_tie_from_disjoint_errors_is_not_significant(self):
        # The 3-sentence example, repeated: A and B equally good, wrong on different sentences.
        t = ["x", "x", "x"] * 50
        a = ["x", "x", "y"] * 50
        b = ["y", "x", "x"] * 50
        r = paired_bootstrap(t, a, b, acc)
        self.assertAlmostEqual(r["diff"], 0.0)
        self.assertLess(r["ci_low"], 0)
        self.assertGreater(r["ci_high"], 0)

    def test_clearly_better_method_is_detected(self):
        t = ["x"] * 200
        a = ["x"] * 190 + ["y"] * 10
        b = ["x"] * 140 + ["y"] * 60
        r = paired_bootstrap(t, a, b, acc)
        self.assertGreater(r["ci_low"], 0)
        self.assertGreater(r["share_a_better"], 0.99)


if __name__ == "__main__":
    unittest.main()
