import json
from pathlib import Path

INTERIM = Path(r"C:\DS_ML\machine-learning-engineer\inflation-intelligence\data\interim")
INTERIM.mkdir(parents=True, exist_ok=True)

def save_docs(docs, path):
    with open(path, "w", encoding="utf-8") as f:
        for doc in docs.values():
            record = {
                "doc_id": doc["doc_id"],
                "doc_type": doc["doc_type"],
                "meeting_date": doc["meeting_date"],
                "text": doc["cleaned"],
                "report": doc["report"],
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

def load_docs(path):
    with open(path, encoding="utf-8") as f:
        return {r["doc_id"]: r for r in map(json.loads, f) if r}

def save_records(records, path):
    """Write a list of records to JSONL, one record per line."""
    with open(path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")


def load_records(path):
    """Read a JSONL file back into a list of records."""
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records