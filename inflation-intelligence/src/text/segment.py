"""Split cleaned document text into sentences."""

import regex as re
SENTENCE_BREAK = re.compile(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚÑ¿])")

def to_records(minutes):
    records = []
    for doc_id, doc in minutes.items():
        for i, s in enumerate(SENTENCE_BREAK.split(doc["text"])):
            records.append({
                "doc_id": doc_id,
                "doc_type": doc["doc_type"],
                "meeting_date": doc["meeting_date"],
                "sent_idx": i,
                "sentence": s,
                "cluster": None, "split": None, "stance": None, "sentiment": None,
            })

    return records