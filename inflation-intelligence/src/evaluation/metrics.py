"""Classification metrics for one task (stance or sentiment), built on sklearn.

Evaluation rules (see data/gold/README.md, "Evaluation rules"):
- Headline = macro-F1 averaged only over ``average_over`` (excludes ``na``,
  which has one test sentence); every sentence is still scored.
- Zero division -> 0: a class a method never predicts gets precision 0.
"""

from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_recall_fscore_support,
)

from text.labels import NA, SENTIMENT, STANCE

# Classes the headline macro-F1 averages over.
HEADLINE: dict[str, tuple[str, ...]] = {
    "stance": tuple(c for c in STANCE if c != NA),
    "sentiment": tuple(c for c in SENTIMENT if c != NA),
}
# Full label order for confusion matrices and per-class tables.
LABELS: dict[str, tuple[str, ...]] = {"stance": STANCE, "sentiment": SENTIMENT}


def macro_f1(y_true: Sequence[str], y_pred: Sequence[str], task: str) -> float:
    """Headline macro-F1 for a task; the function the bootstrap resamples."""
    return float(
        f1_score(y_true, y_pred, labels=list(HEADLINE[task]), average="macro", zero_division=0)
    )


@dataclass(frozen=True)
class TaskScores:
    task: str
    labels: tuple[str, ...]
    n: int
    accuracy: float
    macro_f1: float
    precision: np.ndarray  # per class, in ``labels`` order
    recall: np.ndarray
    f1: np.ndarray
    support: np.ndarray  # true count per class
    predicted: np.ndarray  # predicted count per class
    confusion: np.ndarray  # rows = true, cols = predicted, in ``labels`` order
    never_predicted: tuple[str, ...]  # headline classes with zero predictions
    na_predicted: int
    na_true: int
    na_correct: int


def score_task(y_true: Sequence[str], y_pred: Sequence[str], task: str) -> TaskScores:
    """All metrics for one task on aligned true/predicted label lists."""
    if len(y_true) != len(y_pred):
        raise ValueError(f"length mismatch: {len(y_true)} true vs {len(y_pred)} predicted")
    labels = LABELS[task]
    unknown = set(y_pred) - set(labels)
    if unknown:
        raise ValueError(f"{task}: predicted labels not in vocabulary: {sorted(unknown)}")

    cm = confusion_matrix(y_true, y_pred, labels=list(labels))
    p, r, f, support = precision_recall_fscore_support(
        y_true, y_pred, labels=list(labels), zero_division=0
    )
    predicted = cm.sum(axis=0)
    na_i = labels.index(NA)
    return TaskScores(
        task=task,
        labels=labels,
        n=len(y_true),
        accuracy=float(accuracy_score(y_true, y_pred)),
        macro_f1=macro_f1(y_true, y_pred, task),
        precision=p,
        recall=r,
        f1=f,
        support=support,
        predicted=predicted,
        confusion=cm,
        never_predicted=tuple(
            c for c in HEADLINE[task] if predicted[labels.index(c)] == 0
        ),
        na_predicted=int(predicted[na_i]),
        na_true=int(support[na_i]),
        na_correct=int(cm[na_i, na_i]),
    )
