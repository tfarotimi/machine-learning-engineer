"""Strip boilerplate and normalise whitespace in extracted PDF text.

Ported unchanged from monetary-policy-rag/lib/clean.py, where it was written
and debugged against the comunicados.

TODO before labeling the minutes: the rules below are comunicado-specific.
The minutes carry different boilerplate -- an attendance list of Consejeros
and staff, a numbered-paragraph structure, and a different closing formula.
Removing the wrong thing here deletes labelable content; leaving boilerplate
in inflates the `na` class. Inspect two or three minutes by hand before
deciding, and branch on doc_type rather than widening the comunicado rules.
"""

import regex as re

def clean_content(text):


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