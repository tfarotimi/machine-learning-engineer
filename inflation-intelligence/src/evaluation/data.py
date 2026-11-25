"""Load gold labels and method predictions, and join them on (doc_id, sent_idx).

Layout:
    data/gold/<split>_labels.jsonl                 human labels (read-only)
    data/predictions/<method>/<split>.jsonl        one record per sentence:
        {"doc_id": ..., "sent_idx": ..., "stance": ..., "sentiment": ...}
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from text.labels import NA, SENTIMENT, SPLITS, STANCE

Key = tuple[str, int]


def read_jsonl(path: Path) -> list[dict]:
    """Parse a JSON-lines file, skipping blank lines."""
    with path.open(encoding="utf-8") as fh:
        return [json.loads(line) for line in fh if line.strip()]


def gold_path(data_dir: Path, split: str) -> Path:
    return data_dir / "gold" / f"{split}_labels.jsonl"


def predictions_path(data_dir: Path, method: str, split: str) -> Path:
    return data_dir / "predictions" / method / f"{split}.jsonl"


def _index(records: list[dict], source: str) -> dict[Key, dict]:
    out: dict[Key, dict] = {}
    for rec in records:
        key = (rec["doc_id"], int(rec["sent_idx"]))
        if key in out:
            raise ValueError(f"{source}: duplicate key {key}")
        out[key] = rec
    return out


def _check_labels(rec: dict, source: str) -> None:
    key = (rec["doc_id"], rec["sent_idx"])
    if rec["stance"] not in STANCE:
        raise ValueError(f"{source} {key}: bad stance {rec['stance']!r}")
    if rec["sentiment"] not in SENTIMENT:
        raise ValueError(f"{source} {key}: bad sentiment {rec['sentiment']!r}")
    if (rec["stance"] == NA) != (rec["sentiment"] == NA):
        raise ValueError(f"{source} {key}: coupling rule broken (na iff na)")


@dataclass(frozen=True)
class Aligned:
    """Gold and predicted labels in the same (gold file) order."""

    keys: list[Key]
    true: dict[str, list[str]]  # task -> labels
    pred: dict[str, list[str]]


def load_aligned(data_dir: Path, method: str, split: str) -> Aligned:
    """Join one method's predictions to gold; every gold sentence must be predicted exactly once."""
    if split not in SPLITS:
        raise ValueError(f"unknown split {split!r}")
    gold_records = read_jsonl(gold_path(data_dir, split))
    pred_records = read_jsonl(predictions_path(data_dir, method, split))
    gold = _index(gold_records, "gold")
    pred = _index(pred_records, f"predictions/{method}")

    missing = gold.keys() - pred.keys()
    extra = pred.keys() - gold.keys()
    if missing or extra:
        raise ValueError(
            f"{method}/{split}: {len(missing)} gold sentences without a prediction, "
            f"{len(extra)} predictions not in gold (e.g. {sorted(missing or extra)[:3]})"
        )

    keys = [(r["doc_id"], int(r["sent_idx"])) for r in gold_records]
    for k in keys:
        _check_labels(gold[k], "gold")
        _check_labels(pred[k], f"predictions/{method}")
    tasks = ("stance", "sentiment")
    return Aligned(
        keys=keys,
        true={t: [gold[k][t] for k in keys] for t in tasks},
        pred={t: [pred[k][t] for k in keys] for t in tasks},
    )
