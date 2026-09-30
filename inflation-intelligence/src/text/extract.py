import pypdf as pdf

def get_content(files):

    doc_dict = {}

    #for each comunicado in the file, create a pdf reader object and get each page,
    # for each page, extract text and add it to a string containing text from previous pages
    # store contents for each comunicado in a dictionary
    for i, doc in enumerate(files):
        reader = pdf.PdfReader(doc)
        pages = reader.pages
        
        doc_name = doc.stem
        doc_contents = ""

        for j, page in enumerate(pages):
            page_content = page.extract_text()
            doc_contents += page_content

        doc_dict[doc_name] = doc_contents

    return doc_dict
