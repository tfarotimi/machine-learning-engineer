"""Score one method's predictions against gold labels.

Usage:
    python scripts/evaluate.py --method zero_shot --split dev
    python scripts/evaluate.py --method zero_shot --split dev --save

Reads  data/gold/<split>_labels.jsonl and data/predictions/<method>/<split>.jsonl.
--save writes data/evaluation/<method>/<split>.json (never into data/gold/).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from evaluation.data import load_aligned
from evaluation.metrics import HEADLINE, TaskScores, score_task
from inflation_intelligence.config import load_settings
from text.labels import NA, SPLITS

TASKS = ("stance", "sentiment")


def format_task(s: TaskScores) -> str:
    """Human-readable block: headline, per-class table, confusion matrix, na counts."""
    lines = [
        f"== {s.task} (n={s.n}) ==",
        f"macro-F1 over {list(HEADLINE[s.task])}: {s.macro_f1:.3f}",
        f"accuracy (all sentences): {s.accuracy:.3f}",
        "",
        f"{'class':<22}{'P':>7}{'R':>7}{'F1':>7}{'true':>7}{'pred':>7}",
    ]
    for i, c in enumerate(s.labels):
        lines.append(
            f"{c:<22}{s.precision[i]:>7.3f}{s.recall[i]:>7.3f}{s.f1[i]:>7.3f}"
            f"{s.support[i]:>7d}{s.predicted[i]:>7d}"
        )
    w = max(len(c) for c in s.labels) + 2
    lines += ["", "confusion (rows = true, cols = predicted):", " " * w + "".join(f"{c[:8]:>10}" for c in s.labels)]
    for i, c in enumerate(s.labels):
        lines.append(f"{c:<{w}}" + "".join(f"{v:>10d}" for v in s.confusion[i]))
    lines.append("")
    lines.append(
        f"{NA}: predicted on {s.na_predicted} sentences; "
        f"{s.na_correct} of {s.na_true} true {NA} correct (not in headline)"
    )
    if s.never_predicted:
        lines.append(f"WARNING: never predicted {list(s.never_predicted)} -> precision/F1 set to 0")
    return "\n".join(lines)


def to_json(s: TaskScores) -> dict:
    """Serializable version of TaskScores."""
    return {
        "n": s.n,
        "labels": list(s.labels),
        "headline_labels": list(HEADLINE[s.task]),
        "macro_f1": s.macro_f1,
        "accuracy": s.accuracy,
        "per_class": {
            c: {
                "precision": float(s.precision[i]),
                "recall": float(s.recall[i]),
                "f1": float(s.f1[i]),
                "support": int(s.support[i]),
                "predicted": int(s.predicted[i]),
            }
            for i, c in enumerate(s.labels)
        },
        "confusion": s.confusion.tolist(),
        "never_predicted": list(s.never_predicted),
        "na": {"predicted": s.na_predicted, "true": s.na_true, "correct": s.na_correct},
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--method", required=True)
    ap.add_argument("--split", required=True, choices=SPLITS)
    ap.add_argument("--save", action="store_true", help="write JSON to data/evaluation/")
    args = ap.parse_args()

    data_dir = load_settings().data_dir
    aligned = load_aligned(data_dir, args.method, args.split)
    scores = {t: score_task(aligned.true[t], aligned.pred[t], t) for t in TASKS}

    print(f"method={args.method} split={args.split}\n")
    print("\n\n".join(format_task(scores[t]) for t in TASKS))

    if args.save:
        out = data_dir / "evaluation" / args.method / f"{args.split}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            json.dumps({"method": args.method, "split": args.split, **{t: to_json(scores[t]) for t in TASKS}}, indent=2),
            encoding="utf-8",
        )
        print(f"\nsaved {out}")


if __name__ == "__main__":
    main()
