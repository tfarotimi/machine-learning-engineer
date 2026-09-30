"""Group near-duplicate sentences into clusters."""


def cluster_near_duplicates(sentences, *, threshold=0.95, model_name=None):
    """Assign a dup_cluster id to every sentence."""
    raise NotImplementedError


def cluster_summary(sentences) -> dict[str, float]:
    """Cluster-size distribution across the corpus."""
    raise NotImplementedError


def calibration_sample(sentences, *, threshold=0.95, margin=0.03, n=30, seed=20260929):
    """Sample sentence pairs whose similarity sits near the threshold."""
    raise NotImplementedError
