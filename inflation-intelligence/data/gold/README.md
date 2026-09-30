# Gold labels

Human-assigned labels. This directory is tracked in Git — unlike the rest of
`data/` — because these files are the most expensive and least reproducible
artifact in the project. Losing them means re-labeling by hand; publishing
them is what makes the results checkable by someone else.

## Files

| File | Written | Status |
|---|---|---|
| `test.jsonl` | first, blind | **read-only once written** |
| `dev.jsonl` | after test | mutable during development |
| `train.jsonl` | after test | mutable during development |

## Rules

**Test is labeled first, and blind.** No model prediction is seen for any
test sentence before it is labeled. Once `test.jsonl` exists it is never
edited — except by a documented second pass recorded in the codebook's
self-agreement section, and then only from your own re-judgement, never from
a model's output.

**Train and dev may be pre-labeled and verified.** Claude proposes, you check
every one. Residual error there only adds noise to training, which is
tolerable; the same error in test would bias the results.

**Predictions never live here.** Model outputs go to
`phase1_extraction/results/predictions/<method>.jsonl`, keyed by
`(doc_id, sent_idx)`, and are joined against gold at evaluation time. Nothing
in the evaluation path can write into this directory.

## Record format

One JSON object per line; see `src/text/labels.py` for the schema.

```json
{
  "doc_id": "rpm_minutes_2022_07",
  "doc_type": "minutes",
  "meeting_date": "2022-07-13",
  "sent_idx": 4,
  "text": "El Consejo estima que la TPM se mantendra en ...",
  "dup_cluster": 17,
  "split": "test",
  "gold": {"stance": "forward", "sentiment": "neutral"}
}
```

## Checksums

Record the SHA-256 of `test.jsonl` here when it is frozen, and cite it in the
results so any later run can be shown to have used the same test set.

- `test.jsonl` frozen on: _(date)_
- SHA-256: _(hash)_
