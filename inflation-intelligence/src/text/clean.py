"""Strip boilerplate and normalise whitespace in extracted PDF text.

`extract.py` separates pages with a form feed ("\\f"). The minutes cleaner
relies on that: running headers sit at the top of each page, and the chart
annex in the 2018-2020 quarterly minutes always starts on a fresh page.

Use `clean(text, doc_type)`. It returns the cleaned text plus a report of
what was removed, so every rule can be checked by reading what it deleted.
"""

import regex as re

PAGE_BREAK = "\f"
CAPITAL = "A-ZÁÉÍÓÚÑ"

# --- minutes: patterns ------------------------------------------------------

# The body starts at the first line beginning "1." followed by a capital.
BODY_START = re.compile(rf"^\s*1\.\s+[{CAPITAL}]", re.MULTILINE)

# Numbered section headings. One or two digits only: lines that start with a
# year ("2018. Con todo, ...") are wrapped sentences, not headings, and occur
# in at least two minutes (2017-11, 2025-12).
SECTION_HEADING = re.compile(rf"^\s*\d{{1,2}}\.\s*[{CAPITAL}]", re.MULTILINE)

# Sometimes extraction loses the line break before a heading, gluing it to
# the end of the previous sentence: "...de la TPM.4. Decisión de política".
# Every heading in the corpus starts with one of these words.
GLUED_HEADING = re.compile(r"(?<=[.:])\s*(\d{1,2}\.\s*(?:Ante|Análi|Decisi|Acuer))")

# Two minutes (2024-01, 2024-04) contain paragraphs in a font PDF readers
# cannot decode: "+@ÄHMÇ@BH¹M" is "La inflación", with digits missing. Real
# Spanish text never contains "Ä", so any line containing it is garbled.
GARBLED = "Ä"


# Running page headers, two layouts:
#   2016-2021: "BANCO CENTRAL DE CHILE Reunión de Política Monetaria 3Los ..."
#   2022-    : "MINUTA REUNIÓN DE POLÍTICA MONETARIA\nJULIO 20223\n..."
# The page number is glued to the next word (old) or to the year (new), so
# each page is matched with its own page number.
def _page_header(page_number: int) -> re.Pattern:
    n = str(page_number)
    old = rf"BANCO CENTRAL DE CHILE\s*Reuni[óo]n de Pol[íi]tica Monetaria\s*{n}"
    new = (
        rf"MINUTA REUNI[ÓO]N DE POL[ÍI]TICA MONETARIA\s*"
        rf"[{CAPITAL}\-]+\s*\d{{4}}\s*{n}"
    )
    return re.compile(rf"\A\s*(?:{old}|{new})")


# Some minutes also repeat the header at the END of a page, or on a final
# back-cover page: "MINUTA REUNIÓN DE POLITICA MONETARIA 4 DICIEMBRE 2023".
# Only capitals, digits and spaces are allowed after it, so the pattern can
# never reach into body text.
TRAILING_HEADER = re.compile(
    rf"\s*MINUTA REUNI[ÓO]N DE POL[ÍI]TICA MONETARIA[\s\d{CAPITAL}\-]*\Z"
)

# Subtitles occasionally glued to the next sentence:
# "...crudo de Irán. Escenario nacionalEn el mercado financiero local, ..."
GLUED_SUBTITLE = re.compile(rf"(Escenario (?:inter)?nacional)\s*(?=[{CAPITAL}])")


# The chart annex of the 2018-2020 quarterly minutes opens with a page that
# says "Este documento es preparado por ..." or "Este documento considera ...".
# Extraction sometimes drops spaces ("espreparado"), hence the \s*.
ANNEX_MARKER = re.compile(r"Este\s*documento\s*(?:es\s*preparado|considera)")

MAX_HEADING_WORDS = 5


# --- minutes ----------------------------------------------------------------


def clean_minutes(raw: str) -> tuple[str, dict]:
    report = {"warnings": [], "headers_removed": 0, "annex_chars": 0,
              "removed_lines": [], "garbled_lines": 0}

    # 1. Remove the running header from the top of each page.
    pages = raw.split(PAGE_BREAK)
    for number, page in enumerate(pages, start=1):
        stripped = _page_header(number).sub("", page, count=1)
        stripped = TRAILING_HEADER.sub("", stripped)
        if stripped != page:
            report["headers_removed"] += 1
        pages[number - 1] = stripped

    # 2. Cut the chart annex: from the page where the marker appears onward.
    for number, page in enumerate(pages):
        if ANNEX_MARKER.search(page):
            report["annex_chars"] = sum(len(p) for p in pages[number:])
            pages = pages[:number]
            break

    text = "\n".join(pages)

    # 3. Start at the body: the first line beginning "1.".
    m = BODY_START.search(text)
    if m:
        text = text[m.start():]
    else:
        report["warnings"].append("no '1.' heading found; kept full text")

    # 4. Put glued headings and subtitles back on their own line.
    text = GLUED_HEADING.sub(r"\n\1", text)
    text = GLUED_SUBTITLE.sub(r"\n\1\n", text)

    # 5. Re-join words hyphenated across a line break. Done before the line
    #    filter, so a short word fragment on the next line is not mistaken
    #    for a heading.
    text = text.replace("-\n", "")
    #normalize EE. UU instances to make sentence break robust 
    text = re.sub(r"EE\.\s+UU\.", "EE.UU.", text)

    # 6. Drop headings and garbled lines.
    #    A subtitle ("Escenario internacional") is a short line with no final
    #    period that starts with a capital AND follows the end of a sentence
    #    or another heading. Without the last two conditions the rule also
    #    deletes mid-sentence fragments: italic words make the PDF break
    #    lines early ("shocks y de sus efectos", "grosso modo, suponía").
    kept, removed, garbled = [], [], 0
    after_break = True          # the body starts on a fresh line
    for line in text.split("\n"):
        stripped = line.strip()
        words = stripped.split()
        if not words:
            continue
        if GARBLED in line:
            garbled += 1
            continue
        if SECTION_HEADING.match(line):
            removed.append(line)
            after_break = True
            continue
        if (
            len(words) <= MAX_HEADING_WORDS
            and not stripped.endswith(".")
            and stripped[0].isupper()
            and after_break
        ):
            removed.append(line)
            after_break = True
            continue
        kept.append(line)
        after_break = stripped.endswith((".", ":"))
    report["removed_lines"] = removed
    report["garbled_lines"] = garbled
    if garbled:
        report["warnings"].append(
            f"{garbled} garbled lines dropped (undecodable font); "
            "surrounding sentences are broken, so exclude this document"
        )

    # 7. Normalise characters and whitespace, then join the lines.
    text = "\n".join(kept)
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")
    text = text.replace("[INF*RES*AS]", " ")
    text = re.sub(r"\s+", " ", text).strip()

    return text, report


# --- comunicados ------------------------------------------------------------


def clean_content(text):
    """Comunicado cleaner, ported unchanged from monetary-policy-rag."""
    text = text.replace(PAGE_BREAK, "\n")

    #remove hyphens and newlines
    text = text.replace("-\n", "")
    text = text.replace("\n", " ")    # <- this step went missing

    #replace unicode characters with letters
    text = text.replace("ﬁ", "fi").replace("ﬂ", "fl")

    #remove dots from table of contents
    text = re.sub(r"\.{3,}", " ", text)  # collapse dot-leaders (TOC/list-of-tables) to a single space

    # strip the recurring administrative boilerplate ending
    minuta_start = text.find("La minuta correspondiente")
    if minuta_start != -1:
        text = text[:minuta_start]

    text = text.replace("[INF*RES*AS]", " ")

    text = re.sub(r"\s{2,}", " ", text)  # collapse any double-spaces left by the removals above

    text = text.replace("COMUNICADO DE PRENSA", " ")

    text = text.strip()

    return text


# --- entry point ------------------------------------------------------------


def clean(text: str, doc_type: str) -> tuple[str, dict]:
    if doc_type == "minutes":
        return clean_minutes(text)
    if doc_type == "comunicado":
        return clean_content(text), {"warnings": []}
    raise ValueError(f"unknown doc_type: {doc_type!r}")
