# Gold labels

Human-assigned labels. This directory is tracked in Git — unlike the rest of
`data/` — because these files are the most expensive and least reproducible
artifact in the project. Losing them means re-labeling by hand; publishing
them is what makes the results checkable by someone else.

Labels are produced with `scripts/annotate.py`, which writes to
`data/interim/<split>_labels.jsonl`. When a split is finished, that file is
copied here and committed. The copy in `data/gold/` is the official version.

## Files

| File | Sentences | How it was labeled | Status |
|---|---|---|---|
| `train_labels.jsonl` | 400 | Hand-labeled by the annotator, then reviewed by Claude; the annotator accepted or rejected each proposed correction (stance review changed 63/400, ~16%). Codebook rules were refined during this pass, and labels were re-checked against the final rules. | mutable during development |
| `dev_labels.jsonl` | 150 | Hand-labeled **blind** (no model pre-labels, no review of individual labels), 2026-11-19, in three sessions of 50. Two corrections made at the annotator's own request, logged below. | frozen; change only with a logged codebook change |
| `test_labels.jsonl` | 400 | Hand-labeled **blind** (no model pre-labels) before any model was run; finished 2026-11-25. One pre-freeze review of the `na` class only, logged below. | **frozen 2026-11-25; read-only** |

All splits: single annotator; labels assigned from the English machine
translation, with the Spanish original available on request in the tool.

## Rules

**Test is labeled blind, before any model is run.** No model prediction,
on any split, is seen before test is finished — so nothing learned from
model behaviour can influence the test labels. Test is labeled under one
frozen version of `codebook.md`. Once `test_labels.jsonl` exists it is never
edited, except by a documented second pass recorded in the codebook's
self-agreement section, and then only from the annotator's own re-judgement,
never from a model's output.

**Dev is blind too.** Every method is tuned against dev, so model-influenced
dev labels would pull all methods toward the model's interpretation of the
codebook. Dev was originally allowed to be pre-labeled and verified; on
2026-11-18 the decision was changed to blind labeling.

**Train is not blind.** It was reviewed with Claude's help. Residual error
or model influence there only adds noise to training, which is tolerable.
Note for the write-up: a method trained on train may partly learn the shared
annotator+Claude conventions, which is why dev and test (annotator only) are
the yardstick.

**Predictions never live here.** Model outputs go to a separate
predictions directory, one file per method, keyed by `(doc_id, sent_idx)`,
and are joined against gold at evaluation time. Nothing in the evaluation
path can write into this directory.

## Record format

One JSON object per line. Vocabularies (`STANCE`, `SENTIMENT`) are defined in
`src/text/labels.py`; label meanings are in `codebook.md`.

| Field | Meaning |
|---|---|
| `doc_id` | Source document, e.g. `minutes_2017_07_13` |
| `doc_type` | `minutes` or `comunicado` |
| `meeting_date` | ISO date of the meeting |
| `sent_idx` | Sentence position within the document; `(doc_id, sent_idx)` is the unique key |
| `sentence` | Spanish original |
| `cluster` | Near-duplicate cluster id from `dedup.py` (one sentence sampled per cluster) |
| `split` | `train`, `dev` or `test` |
| `stance` | `forward`, `backward` or `na` |
| `sentiment` | `hawkish`, `dovish`, `neutral`, `risk_highlighting`, `confidence_building` or `na` |
| `context` | Previous sentence in the document (Spanish), saved at sampling time |
| `sentence_en`, `context_en` | Machine translations shown in the labeling tool |

Constraint: `sentiment == "na"` if and only if `stance == "na"`.

Example (strings trimmed):

```json
{
  "doc_id": "minutes_2017_07_13",
  "doc_type": "minutes",
  "meeting_date": "2017-07-13",
  "sent_idx": 89,
  "sentence": "El Consejo acordó, con los votos del Presidente señor Marcel, ...",
  "cluster": 341,
  "split": "dev",
  "stance": "backward",
  "sentiment": "neutral",
  "context": "Por ello, consideraba que la comunicación debería indicar ...",
  "sentence_en": "The Board agreed, with the votes of the Governor Mr. Marcel, ...",
  "context_en": "For this reason, he/she considered that the communication ..."
}
```

## Change log

| Date | File | Record | Change | Reason |
|---|---|---|---|---|
| 2026-11-19 | dev | `minutes_2017_07_13` / 89 | stance forward → backward | Annotator re-judged under S2 (decision at this meeting). First applied during labeling but overwritten by the tool (see note); re-applied after copy to gold. |
| 2026-11-19 | dev | `minutes_2022_07_13` / 66 | sentiment neutral → dovish | Annotator re-judged after viewing wider document context. |
| 2026-11-25 | test | 14 records (rows 264, 273, 289, 291, 305, 349, 363, 367, 377, 381, 382, 383, 386, 394) | stance/sentiment `na`/`na` → forward/neutral (12) or backward/neutral (2) | Pre-freeze review of the `na` class, see note below. |

Note on the 2026-11-25 test review: after labeling, the annotator suspected
`na` had been used for sentences with economic content but no clear time
reference. Claude listed all 15 `na` records and pointed out which codebook
rules (the `na` definition, S1, S2, S6, S8) applied to each; the annotator
made every decision. 14 of 15 were relabeled to bring test in line with the
rules already used for train and dev; one (`minutes_2025_12_16` / 33) stays
`na`. No model predictions were involved, and no other class was reviewed.
This is a disclosed deviation from "test is never edited": it happened
before the freeze and only restored consistency with the existing codebook.
The pre-review file is kept locally as
`data/interim/test_labels.before_na_review.jsonl` (not tracked).

Note: `annotate.py`'s `save_one` writes both stance and sentiment of the
record being labeled, so an external edit to a field of that same record made
between the stance and sentiment passes is overwritten by the tool's stale
in-memory value. Until fixed, make corrections after the tool has finished
with that record.

## Checksums

Record the SHA-256 of `test_labels.jsonl` here when it is frozen, and cite
it in the results so any later run can be shown to have used the same test set.

- `test_labels.jsonl` frozen on: 2026-11-25
- Codebook version used for test: _(commit that freezes `codebook.md`)_
- SHA-256: `c5faf29b561b9777e56fa1999491904280f210ad7df4aceb5364f9024a64a304`
