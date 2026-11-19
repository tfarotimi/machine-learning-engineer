"""Add an English translation to every sentence in one or more sample files.

Usage, from the inflation-intelligence folder:

    python scripts/translate.py data/interim/sample_train.jsonl data/interim/sample_dev.jsonl data/interim/sample_test.jsonl

Each record gets two new fields: `sentence_en`, and `context_en` when the
record has a `context`. The files are rewritten in place.

Why this is safe for the blind test set: a translation carries no label. It
changes how fast you read, not what you decide. The Spanish stays the
authority; when the two seem to disagree, label from the Spanish and note the
case in the codebook's pilot log.

Translations are cached in data/interim/translations.json, keyed by the
Spanish text. Two consequences:
  * rerunning the script, or stopping halfway, never pays for the same
    sentence twice;
  * a sentence that appears both as one record's `sentence` and another
    record's `context` is translated once.

Needs the `anthropic` package and ANTHROPIC_API_KEY in the environment.
"""

import argparse
import json
import os
import sys
from pathlib import Path

import anthropic

CACHE_PATH = Path("data/interim/translations.json")
BATCH_SIZE = 20

# The translation has one job: preserve what the labeling rules depend on.
# The codebook separates "will" from "could" (direction vs risk), and past from
# future (stance), so modality and tense matter more than elegant English.
SYSTEM_PROMPT = """You translate sentences from Banco Central de Chile monetary policy documents from Spanish into English.

Rules:
- Translate faithfully and fairly literally. Do not summarise, interpret or smooth.
- Preserve modality exactly: "podría" = "could", "se estima/estimaba" = "is/was estimated", "se espera" = "is expected", "debería" = "should".
- Preserve tense and conditional mood exactly; reported speech in the minutes often uses the imperfect or conditional ("estaban", "permanecerían") and that must remain visible.
- Keep hedges and intensifiers ("algo", "acotado", "significativamente", "más bien").
- Keep standard abbreviations as they are: TPM, IPC, IPoM, EEE, EOF, PIB, Imacec.

You receive a JSON array of strings. Return ONLY a JSON array of the same length, with the translations in the same order. No commentary, no code fences."""


# --- files -----------------------------------------------------------------


def load_records(path):
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def save_records(records, path):
    # Temporary file, then swap: a crash mid-write leaves the original intact.
    tmp = str(path) + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    os.replace(tmp, path)


def load_cache():
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}


def save_cache(cache):
    tmp = str(CACHE_PATH) + ".tmp"
    Path(tmp).write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    os.replace(tmp, CACHE_PATH)


# --- translation -----------------------------------------------------------


def translate_batch(client, model, texts):
    """Translate a list of Spanish strings; return English strings in order."""
    response = client.messages.create(
        model=model,
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": json.dumps(texts, ensure_ascii=False)}],
    )
    # The response is a list of content blocks, and the first one is not
    # always text: the model may return a thinking block before its answer.
    # So collect the text blocks by type instead of assuming position 0.
    raw = "".join(block.text for block in response.content if block.type == "text").strip()
    translations = json.loads(raw)

    # Fail loudly at the boundary rather than silently misaligning sentences:
    # if the model dropped or merged one item, every translation after it
    # would be attached to the wrong Spanish sentence.
    if not isinstance(translations, list) or len(translations) != len(texts):
        raise ValueError(
            f"expected {len(texts)} translations, got "
            f"{len(translations) if isinstance(translations, list) else type(translations)}"
        )
    return translations


def texts_needing_translation(records, cache):
    """Every distinct Spanish string (sentence or context) not yet cached."""
    needed = []
    seen = set()
    for record in records:
        for text in (record["sentence"], record.get("context")):
            if text and text not in cache and text not in seen:
                seen.add(text)
                needed.append(text)
    return needed


def main():
    parser = argparse.ArgumentParser(description="Add English translations to sample files.")
    parser.add_argument("files", nargs="+", help="JSONL sample files to translate in place")
    parser.add_argument("--model", default="claude-sonnet-5-5")
    args = parser.parse_args()

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    cache = load_cache()
    files = {path: load_records(path) for path in args.files}

    all_records = [r for records in files.values() for r in records]
    needed = texts_needing_translation(all_records, cache)
    print(f"{len(cache)} cached, {len(needed)} to translate")

    for start in range(0, len(needed), BATCH_SIZE):
        batch = needed[start : start + BATCH_SIZE]
        try:
            translations = translate_batch(client, args.model, batch)
        except (ValueError, json.JSONDecodeError) as error:
            # Save what we have; rerunning picks up from here.
            print(f"batch at {start} failed: {error}. Rerun to retry.", file=sys.stderr)
            continue
        cache.update(zip(batch, translations))
        save_cache(cache)
        print(f"  {min(start + BATCH_SIZE, len(needed))}/{len(needed)}")

    missing = 0
    for path, records in files.items():
        for record in records:
            record["sentence_en"] = cache.get(record["sentence"])
            context = record.get("context")
            record["context_en"] = cache.get(context) if context else None
            missing += record["sentence_en"] is None
        save_records(records, path)
        print(f"wrote {path}")

    if missing:
        print(f"{missing} sentences still untranslated; rerun the script.", file=sys.stderr)


if __name__ == "__main__":
    main()
