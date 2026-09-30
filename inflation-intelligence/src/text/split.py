"""Assign sentences to train / dev / test."""


def assign_splits(sentences, *, test_from, dev_frac=0.33, seed=20260929):
    """Populate `split` on every sentence."""
    raise NotImplementedError


def verify_no_leakage(sentences) -> None:
    """Raise if the split violates any of its own constraints."""
    raise NotImplementedError


def split_summary(sentences) -> dict[str, object]:
    """Counts per split: sentences, clusters, documents, date range."""
    raise NotImplementedError
