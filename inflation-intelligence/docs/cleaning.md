# Cleaning: RPM minutes

Applies to `clean(text, "minutes")` in `src/text/clean.py`. Checked on all 94
minutes (2016-01 to 2026-07) by reading every removed line.

## Rules, in order

| # | Rule | Why |
|---|---|---|
| 1 | Strip the running header at the top of each page, matched with that page's number | Headers sit mid-sentence otherwise: "...monetaria.BANCO CENTRAL DE CHILE Reunión de Política Monetaria 3Los mercados..." |
| 1b | Strip "MINUTA REUNIÓN DE POLÍTICA MONETARIA ..." at the end of a page | Footer / back cover in 2022+ minutes |
| 2 | Cut from the page containing "Este documento es preparado / considera" | Chart annex of the nine 2018–2020 quarterly minutes (41–72 pages each) |
| 3 | Start at the first line beginning "1." | Drops cover, session line and attendance list |
| 4 | Put glued headings and subtitles back on their own line | Extraction sometimes loses the line break: "...de la TPM.4. Decisión de política monetaria" |
| 5 | Re-join words hyphenated across lines | Before rule 6, so a word fragment is not taken for a heading |
| 6a | Drop lines starting with a 1–2 digit number, a period and a capital | Section headings. Not 4 digits: "2018. Con todo, ..." is a wrapped sentence |
| 6b | Drop short lines (≤ 5 words) with no final period that start with a capital and follow the end of a sentence or a heading | Subtitles ("Escenario internacional"). The last two conditions stop it deleting mid-sentence fragments created by italics ("shocks y de sus efectos") |
| 6c | Drop lines containing "Ä" | Undecodable font, see below |
| 7 | Ligatures, redaction marker, whitespace; join lines | |

## Results

- Removed lines across the corpus are all section headings or subtitles (checked by hand).
- No running headers, annex text or heading text remain in any output.
- Annex cut in all nine long minutes (22–40k characters each).

## Known problems

- **2024-01-31 and 2024-04-02** have paragraphs in a font without a Unicode
  map: "+@ÄHMÇ@BH¹M" is "La inflación", and digits are lost entirely. Both
  pypdf and pdftotext fail. About 40% and 70% of their text is unreadable, and
  what remains is broken sentences. **Excluded from the Phase 1 corpus.**
  Recoverable later with OCR (Spanish model) if needed. Neither falls in the
  test period.
- Extraction splits some words ("Ante cedentes", "po lítica"). Left as is.
