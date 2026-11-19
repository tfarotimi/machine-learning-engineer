"""Group near-duplicate sentences into clusters.

Two sentences are duplicates when they are the same after `normalize`, which
blanks out the details that change from meeting to meeting while the sentence
stays the same: numbers, months, Consejeros' names and their gendered titles.
`normalize` only builds a comparison key; the sentences themselves are never
changed.
"""

import regex as re

CAPITAL = "A-ZÁÉÍÓÚÑ"

# --- names ------------------------------------------------------------------

# A capitalized word right after "señor/señora/señores/señoras" is a name.
# Collecting these across the whole corpus gives the list of Consejeros, which
# also catches names in lists: "los Consejeros señores Vial, García y Marcel".
NAME_AFTER_TITLE = re.compile(rf"\bseñor(?:a|es|as)?\s+([{CAPITAL}][\w’'-]+)")


def collect_names(sentences):
    """Every capitalized word that follows señor/señora anywhere."""
    names = set()
    for sentence in sentences:
        names.update(NAME_AFTER_TITLE.findall(sentence))
    return names


def build_name_pattern(names):
    """One pattern matching any of the names, capitalized, as whole words.

    Matched BEFORE lowercasing on purpose: several surnames are ordinary
    words in lowercase ("a costa de", "es claro que", "infraestructura vial").
    """
    longest_first = sorted(names, key=len, reverse=True)
    alternatives = "|".join(re.escape(n) for n in longest_first)
    return re.compile(rf"\b(?:{alternatives})\b")


# --- normalization rules ------------------------------------------------------

# Any number, including Spanish formats: 5, 4,2, 1.200, 2.500,75
NUMBER = re.compile(r"\d+(?:[.,]\d+)*")
# Anything that isn't a letter, digit, whitespace or the # placeholder
PUNCT = re.compile(r"[^\w\s#]")
# The titles themselves: señor, señora, señores, señoras
TITLE_NAME = re.compile(r"\bseñor(?:a|es|as)?\b")
# "el presidente", "la presidenta", "el vicepresidente", "la vicepresidenta"
TITLE = re.compile(r"\b(?:el|la)\s+(vice)?president[ea]\b")
# The policy rate written out in full -> its abbreviation
TPM_LONG = re.compile(r"\btasa de interés de política monetaria\b")
# Basis points written out -> abbreviation: "puntos base", "punto base",
# "puntos básicos", "pbs" -> "pb"
BASIS_POINTS = re.compile(r"\b(?:puntos?\s+b[aá]s(?:e|icos?)|pbs)\b")
MONTH = re.compile(
    r"\b(?:enero|febrero|marzo|abril|mayo|junio|julio|agosto|"
    r"septiembre|setiembre|octubre|noviembre|diciembre)\b"
)


def normalize(sentence, names=None):
    """Comparison key for deduplication.

    "La Presidenta señora Costa y los Consejeros votaron por mantener la TPM en 5,25%."
    -> "presidente y los consejeros votaron por mantener la tpm en #"

    `names` is the pattern from `build_name_pattern`; without it, names are
    left in and sentences differing only by Consejero won't group.
    """
    text = sentence
    if names is not None:
        text = names.sub(" ", text)        # before lowercasing, see build_name_pattern
    text = text.lower()
    text = TITLE_NAME.sub(" ", text)
    text = TITLE.sub(r"\1presidente", text)
    text = TPM_LONG.sub("tpm", text)
    text = BASIS_POINTS.sub("pb", text)
    text = MONTH.sub("mes", text)
    text = NUMBER.sub(" # ", text)          # spaces around: footnote numbers glued to words ("banco1")
    text = PUNCT.sub(" ", text)
    return " ".join(text.split())          # collapse repeated spaces


def assign_clusters(records, names):
    """First pass: sentences with the same normalized key share a cluster."""
    seen = {}                                   # normalized key -> cluster number
    for record in records:
        key = normalize(record["sentence"], names)
        if key not in seen:
            seen[key] = len(seen)               # new key: next unused number
        record["cluster"] = seen[key]
    return records


def merge_near_duplicates(records, names, threshold=0.85):
    """Second pass: merge clusters whose keys have Jaccard >= threshold.

    Catches near-duplicates exact matching misses: a typo ("en en"), one
    changed word ("ancladas a / en la meta"). Merging is transitive: if A
    matches B and B matches C, all three end up in one cluster (union-find).

    Returns the records (cluster numbers updated in place) and the list of
    merged pairs, so every merge can be read and checked.
    """
    # One normalized key per cluster, as a set of words.
    words_of = {}
    for record in records:
        if record["cluster"] not in words_of:
            words_of[record["cluster"]] = set(normalize(record["sentence"], names).split())

    # Sorted by size: Jaccard can never exceed small/large, so once the size
    # ratio drops below the threshold, no larger key can match and we stop.
    items = sorted(words_of.items(), key=lambda item: len(item[1]))

    parent = {cluster: cluster for cluster in words_of}

    def find(cluster):
        while parent[cluster] != cluster:
            parent[cluster] = parent[parent[cluster]]
            cluster = parent[cluster]
        return cluster

    merges = []
    for i, (cluster_a, a) in enumerate(items):
        if not a:
            continue
        for cluster_b, b in items[i + 1:]:
            if len(a) < threshold * len(b):
                break
            score = len(a & b) / len(a | b)
            if score >= threshold:
                root_a, root_b = find(cluster_a), find(cluster_b)
                if root_a != root_b:
                    parent[max(root_a, root_b)] = min(root_a, root_b)
                    merges.append((round(score, 2), " ".join(sorted(a)), " ".join(sorted(b))))

    for record in records:
        record["cluster"] = find(record["cluster"])
    return records, merges
