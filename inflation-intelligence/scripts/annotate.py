"""Command-line tool for hand-labeling sentences.

Usage, from the inflation-intelligence folder:

    python scripts/label.py data/sentences/demo.jsonl data/gold/demo.jsonl

The first path is the file of sentences to label. The second is where your
labels are saved. If the second file already exists, labeling resumes from it,
so you can stop at any point and pick up later.

Labeling happens in passes: every stance first, then every sentiment, so you
only think about one dimension at a time. Type the number of an option (or the
option itself), or q to quit. Every label is saved the moment you give it.
"""

import argparse
import json
import os
import sys

from text.labels import NA, SENTIMENT, STANCE

# In the sentiment pass, stance is already known not to be na, so na is not a
# valid answer. Offering only the five real sentiments makes the invalid
# combination impossible to type.
SENTIMENT_CHOICES = tuple(s for s in SENTIMENT if s != NA)


# --- files -----------------------------------------------------------------


def load_records(path):
    records = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                records.append(json.loads(line))
    return records


def save_records(records, path):
    # Write to a temporary file, then swap it in. If the program crashes
    # halfway through writing, the real file is untouched.
    tmp_path = path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    os.replace(tmp_path, path)


# --- screen ----------------------------------------------------------------


def show(record, previous):
    print()
    print("-" * 70)
    print(f"{record['doc_id']}  sentence {record['sent_idx']}")
    if previous is not None:
        print(f"  (previous) {previous['sentence']}")
    print(f"  >>> {record['sentence']}")


def print_options(options):
    for number, option in enumerate(options, start=1):
        print(f"  {number} {option}")


def read_choice(options):
    response = input("> ").strip().lower()
    if response == "q":
        print("Saved. Run the same command again to resume.")
        sys.exit(0)
    if response.isdigit() and 1 <= int(response) <= len(options):
        return options[int(response) - 1]
    return response


# --- labeling --------------------------------------------------------------


def stance_label(record, previous):
    show(record, previous)
    print("stance:")
    print_options(STANCE)
    while record["stance"] not in STANCE:
        response = read_choice(STANCE)
        if response in STANCE:
            record["stance"] = response
        else:
            print(f"{response!r} is invalid, provide a correct stance")


def sentiment_label(record, previous):
    if record["stance"] != NA:
        show(record, previous)
        print(f"stance: {record['stance']}")
        print("sentiment:")
        print_options(SENTIMENT_CHOICES)
        while record["sentiment"] not in SENTIMENT or record["sentiment"] == NA:
            response = read_choice(SENTIMENT_CHOICES)
            if response in SENTIMENT_CHOICES:
                record["sentiment"] = response
            else:
                print(f"{response!r} is invalid, provide a correct sentiment")
    else:
        record["sentiment"] = NA


def label_records(records, out_path):
    # Look up any sentence by (doc_id, sent_idx), so we can find the one
    # before it for context.
    by_key = {(r["doc_id"], r["sent_idx"]): r for r in records}

    def previous_of(record):
        return by_key.get((record["doc_id"], record["sent_idx"] - 1))

    for record in records:
        if record["stance"] is None:
            stance_label(record, previous_of(record))
            save_records(records, out_path)

    for record in records:
        if record["sentiment"] is None:
            sentiment_label(record, previous_of(record))
            save_records(records, out_path)

    for record in records:
        if (record["stance"] == NA and record["sentiment"] != NA) or (
            record["sentiment"] == NA and record["stance"] != NA
        ):
            raise ValueError(
                f"na mismatch in {record['doc_id']} sentence {record['sent_idx']}: "
                f"stance={record['stance']!r}, sentiment={record['sentiment']!r}"
            )

    print("na validations passed")
    print(f"All {len(records)} records labeled. Saved to {out_path}")


# --- entry point -----------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="Hand-label sentences.")
    parser.add_argument("sentences", help="JSONL file of sentences to label")
    parser.add_argument("output", help="JSONL file where labels are saved")
    args = parser.parse_args()

    if os.path.exists(args.output):
        print(f"Resuming from {args.output}")
        records = load_records(args.output)
    else:
        records = load_records(args.sentences)

    # Sentences straight out of segment.py have no label keys yet.
    for record in records:
        record.setdefault("stance", None)
        record.setdefault("sentiment", None)

    label_records(records, args.output)


if __name__ == "__main__":
    main()
