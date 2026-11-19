import json
import pypdf
from pathlib import Path

MINUTES = Path(r"C:\DS_ML\machine-learning-engineer\inflation-intelligence\data\raw\feasibility_2026-09-10\rpm_minutes")
COMUNICADOS = Path(r"C:\DS_ML\machine-learning-engineer\inflation-intelligence\data\chile_banco_central")

PAGE_BREAK = "\f"   # form feed: marks where one page ends and the next begins
CATALOG = Path(r"C:\DS_ML\machine-learning-engineer\inflation-intelligence\data\catalog")

def load_dates(doc_type):
    """Map each PDF file name to its date, using the audit catalogs."""
    if doc_type == "minutes":
        entries = json.loads((CATALOG / "text_inventory.json").read_text(encoding="utf-8"))
        return {
            Path(e["path"]).name: e["meeting_date"]
            for e in entries
            if e["collection"] == "rpm_minutes"
        }
    if doc_type == "comunicado":
        entries = json.loads((CATALOG / "rpm_local_inventory.json").read_text(encoding="utf-8"))
        return {Path(e["path"]).name: e["publication_date"] for e in entries}
    raise ValueError(f"unknown doc_type: {doc_type!r}")


def get_content(folder, doc_type):
    files = sorted(folder.glob("*.pdf"))

    doc_dict = {}
    meeting_dates = load_dates(doc_type)

        #for each comunicado in the file, create a pdf reader object and get each page,
        # for each page, extract text and add it to a string containing text from previous pages
        # store contents for each comunicado in a dictionary
    for i, file in enumerate(files):
        doc = Path(file)
        reader = pypdf.PdfReader(doc)
        pages = reader.pages
        
        doc_name = doc.stem
        doc_contents = ""
        meeting_date = meeting_dates[doc_name+".pdf"]
        doc_id = f"{doc_type}_{meeting_date.replace('-', '_')}"

        for j, page in enumerate(pages):
            page_content = page.extract_text()
            # Keep a separator between pages. Without it the last line of one
            # page and the first line of the next are glued together
            # ("...en 2,5%.Antecedentes"), and running page headers end up in
            # the middle of sentences.
            if j > 0:
                doc_contents += PAGE_BREAK
            doc_contents += page_content

        

        doc_dict[doc_id] = {"text":doc_contents, "doc_id":doc_id, "doc_type":doc_type, "meeting_date":meeting_date}

    return doc_dict