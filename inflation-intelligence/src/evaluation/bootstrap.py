"""Bootstrap confidence intervals and paired method comparisons.

Written by the annotator. ``metric`` is any f(y_true, y_pred) -> float, e.g.
``functools.partial(metrics.macro_f1, task="stance")``.
"""

from __future__ import annotations

from collections.abc import Callable, Sequence

import numpy as np

Metric = Callable[[Sequence[str], Sequence[str]], float]


def bootstrap_indices(n: int, n_boot: int, seed: int) -> np.ndarray:
    """Array of shape (n_boot, n): row indices sampled with replacement."""
    raise NotImplementedError


def bootstrap_ci(
    y_true: Sequence[str],
    y_pred: Sequence[str],
    metric: Metric,
    n_boot: int = 1000,
    alpha: float = 0.05,
    seed: int = 0,
) -> tuple[float, float, float]:
    """Point estimate and (1 - alpha) percentile interval of metric."""
    raise NotImplementedError


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
    raise NotImplementedError
