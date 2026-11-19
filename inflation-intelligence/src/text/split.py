"""Assign every sentence to train, dev or test.

Three rules, in order:

1. TIME. Meetings on or after `test_from` are test. The test set measures how
   a method does on statements written after everything it learned from.

2. WHOLE MEETINGS. Every sentence of a meeting gets that meeting's split.
   Dev is a random set of whole meetings from before `test_from`, so it
   covers several policy regimes; the rest is train.

3. CLUSTERS. Near-duplicate sentences (same `cluster`) must not sit in two
   splits, or a method could be tested on a sentence it effectively saw.
   When a cluster crosses splits, the copies in the most protected split are
   kept (test > dev > train) and the other copies are marked "excluded":
   they stay in the corpus, but are never labeled, used as examples, or used
   to train anything. This keeps the test period's vote sentences in test,
   instead of moving the whole cluster to train.
"""

import random
from collections import Counter, defaultdict

EXCLUDED = "excluded"
PRIORITY = {"test": 0, "dev": 1, "train": 2}     # lower = more protected


def assign_splits(records, test_from, dev_frac=0.2, seed=20260929):
    """Set record["split"] on every record. Returns the records."""

    # 1-2. Split by meeting.
    meetings = sorted({r["meeting_date"] for r in records})
    before = [m for m in meetings if m < test_from]

    rng = random.Random(seed)                 # same seed -> same dev meetings
    n_dev = round(len(before) * dev_frac)
    dev_meetings = set(rng.sample(before, n_dev))

    def meeting_split(date):
        if date >= test_from:
            return "test"
        if date in dev_meetings:
            return "dev"
        return "train"

    for r in records:
        r["split"] = meeting_split(r["meeting_date"])

    # 3. Clusters that cross splits: keep the most protected copies.
    splits_of = defaultdict(set)
    for r in records:
        splits_of[r["cluster"]].add(r["split"])

    for r in records:
        keep = min(splits_of[r["cluster"]], key=PRIORITY.get)
        if r["split"] != keep:
            r["split"] = EXCLUDED

    return records


def verify_no_leakage(records, test_from):
    """Raise ValueError listing every violation. Run before labeling."""
    problems = []

    allowed = set(PRIORITY) | {EXCLUDED}
    bad = [r for r in records if r.get("split") not in allowed]
    if bad:
        problems.append(f"{len(bad)} records with missing or unknown split")

    # No cluster in two usable splits.
    used = defaultdict(set)
    for r in records:
        if r["split"] in PRIORITY:
            used[r["cluster"]].add(r["split"])
    crossing = [c for c, s in used.items() if len(s) > 1]
    if crossing:
        problems.append(f"{len(crossing)} clusters in more than one split")

    # No meeting in two usable splits.
    by_meeting = defaultdict(set)
    for r in records:
        if r["split"] in PRIORITY:
            by_meeting[r["meeting_date"]].add(r["split"])
    split_meetings = [m for m, s in by_meeting.items() if len(s) > 1]
    if split_meetings:
        problems.append(f"meetings divided across splits: {split_meetings[:5]}")

    # Test is exactly the recent period.
    wrong_side = [
        r for r in records
        if (r["split"] == "test") != (r["meeting_date"] >= test_from)
        and r["split"] != EXCLUDED
    ]
    if wrong_side:
        problems.append(f"{len(wrong_side)} records on the wrong side of {test_from}")

    if problems:
        raise ValueError("split is not sound:\n  " + "\n  ".join(problems))


def split_summary(records):
    """Per split: sentences, meetings, clusters, date range."""
    summary = {}
    for name in ("train", "dev", "test", EXCLUDED):
        rs = [r for r in records if r["split"] == name]
        if not rs:
            continue
        dates = sorted({r["meeting_date"] for r in rs})
        summary[name] = {
            "sentences": len(rs),
            "meetings": len(dates),
            "clusters": len({r["cluster"] for r in rs}),
            "from": dates[0],
            "to": dates[-1],
        }
    return summary

