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