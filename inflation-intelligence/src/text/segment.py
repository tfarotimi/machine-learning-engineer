"""Split cleaned document text into sentences."""


def split_sentences(text: str) -> list[str]:
    """Split one cleaned document's text into sentence strings, in order."""
    raise NotImplementedError


def to_records(text, *, doc_id, doc_type, meeting_date):
    """Segment one document and wrap each sentence in a Sentence record."""
    raise NotImplementedError


def length_summary(sentences: list[str]) -> dict[str, float]:
    """Length distribution of the segmented sentences."""
    raise NotImplementedError
