"""Bootstrap confidence intervals and paired method comparisons.

Predictions are fixed: each method predicts every test sentence once. A
bootstrap resample draws n sentence indices with replacement (same size as
the test set), so sentences count 0, 1, 2, ... times; the metric is
recomputed on those re-weighted fixed predictions. Paired comparisons score
both methods on the same indices in every resample, so sentence difficulty
cancels out of the difference.

``metric`` is any f(y_true, y_pred) -> float, e.g.
``functools.partial(metrics.macro_f1, task="stance")``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

Metric = Callable[[Sequence[str], Sequence[str]], float]


def bootstrap_indices(n: int, n_boot: int, seed: int) -> np.ndarray:
    """Array of shape (n_boot, n): row indices sampled with replacement."""
    rng = np.random.default_rng(seed)
    return rng.integers(0, n, size=(n_boot, n))


def _scores(y_true: np.ndarray, y_pred: np.ndarray, metric: Metric, idx: np.ndarray) -> np.ndarray:
    """Metric on each resample (one row of idx per resample)."""
    return np.array([metric(y_true[row], y_pred[row]) for row in idx])


def _interval(values: np.ndarray, alpha: float) -> tuple[float, float]:
    """Percentile interval holding the middle (1 - alpha) of values."""
    lo, hi = np.percentile(values, [100 * alpha / 2, 100 * (1 - alpha / 2)])
    return float(lo), float(hi)


def bootstrap_ci(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    metric: Metric,
    n_boot: int = 1000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Point estimate and (1 - alpha) percentile interval of metric."""
    t, p = np.asarray(y_true), np.asarray(y_pred)
    if len(t) != len(p):
        raise ValueError("y_true and y_pred differ in length")
    idx = bootstrap_indices(len(t), n_boot, seed)
    lo, hi = _interval(_scores(t, p, metric, idx), alpha)
    return float(metric(t, p)), lo, hi


def paired_bootstrap(
    y_true: Sequence[str],
    pred_a: Sequence[str],
    pred_b: Sequence[str],
    metric: Metric,
    n_boot: int = 1000,
    alpha: float = 0.05,
    seed: int = 0,
) -> dict[str, float]:
    """Observed metric(a) - metric(b), its percentile interval, and share of resamples where a > b."""
    t, a, b = np.asarray(y_true), np.asarray(pred_a), np.asarray(pred_b)
    if not len(t) == len(a) == len(b):
        raise ValueError("y_true, pred_a and pred_b differ in length")
    idx = bootstrap_indices(len(t), n_boot, seed)  # shared by both methods
    diffs = _scores(t, a, metric, idx) - _scores(t, b, metric, idx)
    lo, hi = _interval(diffs, alpha)
    return {
        "diff": float(metric(t, a) - metric(t, b)),
        "ci_low": lo,
        "ci_high": hi,
        "share_a_better": float(np.mean(diffs > 0)),
    }
