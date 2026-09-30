"""Label vocabularies and validation for sentence-level signal extraction.

For the data, we use a dictionary to make sure each sentence in our corpus contains all the information we need for our classification process

Data schema:

 {'sentence':type str, set in "segment.py", e.g "La Tasa Politica Monetaria es 3.5% para Junio de 2019", 
          'sent_idx':type int, set in "segment.py", e.g 1       
          'doc_id': type str, set in "extract.py" e.g "banco_central_de_chile_rpm_05_2019"
          'doc_type':type str, set in "extract.py" e.g "comunicado"
          'meeting_date':ISO str(date), set in "extract.py" e.g "2019-06-01"
          'cluster':type int | none, set in "dedup.py", e.g "monetary policy setting"
          'split':type str | none, set in "split.py", e.g "train"
          'stance': type str | none, set in "label.py"
          'sentiment':type str | none , set in "label.py"
          }

"""

STANCE: tuple[str, ...] = ("forward", "backward", "na")

SENTIMENT: tuple[str, ...] = (
    "hawkish",
    "dovish",
    "neutral",
    "risk_highlighting",
    "confidence_building",
    "na",
)

NA = "na"

SPLITS: tuple[str, ...] = ("train", "dev", "test")

METHODS: tuple[str, ...] = ("zero_shot", "few_shot", "setfit", "distilled")

DOC_TYPES: tuple[str, ...] = ("minutes", "comunicado")


   


