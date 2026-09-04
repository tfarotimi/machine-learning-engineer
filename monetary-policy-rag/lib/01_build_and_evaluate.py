#!/usr/bin/env python
# coding: utf-8

# ## Retrieval Augmented Generation (RAG) for Central Bank Monetary Policy

# ### 0. Imports

# In[2]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


import sys
from dotenv import load_dotenv
from pathlib import Path

project_root = Path.cwd().parent
sys.path.append(str(project_root))

from lib.clean import clean_content
from lib.chunk import chunk_content
from lib.embed import load_embedder, embed_chunks, export_full_corpus_doc
from lib.evaluate import evaluate_retrieval, build_candidate_review, export_candidate_review_doc
from lib.extract import get_content
from lib.generate import generate_response
from lib.retrieve import retrieve_chunks, parse_query_date, hybrid_rank, tokenize_stem
from rank_bm25 import BM25Okapi

import numpy as np
import regex as re

import anthropic





# ### 1. Build Embedded Corpus

# In[4]:


#set path for folder containing pdfs 
pdf_path = Path(r'C:\\DS_ML\\machine-learning-engineer\\monetary-policy-rag\\data\\chile_banco_central')

#get contents of each pdf
files = pdf_path.glob("*.pdf")
content = get_content(files)

#clean doc contents and divide into chunks
embedder = load_embedder()

chunked = {}
for doc in content.keys():
    cleaned = clean_content(content[doc])
    chunked[doc] = chunk_content(embedder, cleaned)

# #turn chunks from text into embeddings
corpus_embedded = embed_chunks(embedder, chunked)

#export the text of all chunks in the corpus to a Word doc
export_full_corpus_doc(corpus_embedded, filepath="chunk_review.docx")


# ### 2. Prepare Gold Queries

# In[5]:


#list of gold queries, difficulty level of retrieval for query, and comunicados we expect to contain the relevant chunks 

gold_queries = [
    # --- Irrelevant ---
    {"query": "What is the Federal Reserve's current interest rate?", "difficulty": "irrelevant", "expected_comunicados": []},
    {"query": "How does the European Central Bank set monetary policy?", "difficulty": "irrelevant", "expected_comunicados": []},
    {"query": "What is the history of the Chilean peso currency design?", "difficulty": "irrelevant", "expected_comunicados": []},

    # # --- Easy (single meeting, single fact) ---
    {"query": "What was the policy interest rate in March 2016?", "difficulty": "easy", "expected_comunicados": ["2016_marzo"]},
    {"query": "Did the Council cut or raise the rate in April 2017?", "difficulty": "easy", "expected_comunicados": ["2017_abril"]},
    {"query": "What was the inflation rate reported in the December 2018 meeting?", "difficulty": "easy", "expected_comunicados": ["2018_diciembre"]},
    {"query": "What rate did the Council set in May 2020?", "difficulty": "easy", "expected_comunicados": ["2020_mayo"]},

    # # --- Medium (single meeting, requires synthesis of context + decision) ---
    {"query": "What was the Council's reasoning for raising rates in January 2022?", "difficulty": "medium", "expected_comunicados": ["2022_enero"]},
    {"query": "What non-conventional measures did the Bank announce in March 2020?", "difficulty": "medium", 'expected_comunicados': ['2020_marzo_a', '2020_marzo_b']},
    {"query": "How did the Council describe labor market conditions in the June 2020 meeting?", "difficulty": "medium", "expected_comunicados": ["2020_junio"]},
    {"query": "What was said about copper prices in the February 2018 meeting?", "difficulty": "medium", "expected_comunicados": ["2018_febrero"]},

   # --- Hard (time-series, multi-meeting synthesis — this corpus's real strength) ---
    {"query": "How did the policy rate change from March 2020 through July 2020?", "difficulty": "hard", "expected_comunicados": ["2020_marzo_a", "2020_marzo_b", "2020_mayo", "2020_junio", "2020_julio"]},

    {"query": "When did the Council begin raising rates after the pandemic-era cuts, and why?", "difficulty": "hard", "expected_comunicados": ["2021_julio", "2021_agosto", "2021_diciembre", "2021_octubre"]},

    {"query": "How did the Council's tone on inflation expectations shift between 2020 and 2022?", "difficulty": "hard", "expected_comunicados": [
        "2020_diciembre", "2020_julio", "2020_junio", "2020_marzo_b",
        "2020_mayo", "2020_octubre", "2020_enero", "2020_septiembre",
        "2021_agosto", "2021_diciembre", "2021_enero", "2021_julio", "2021_junio",
        "2021_marzo", "2021_mayo", "2021_octubre",
        "2022_diciembre", "2022_enero", "2022_julio", "2022_junio",
        "2022_marzo", "2022_mayo", "2022_octubre", "2022_septiembre"
    ]},

    {"query": "What non-conventional pandemic support measures were introduced, then later withdrawn or maintained, across 2020 and 2021?", "difficulty": "hard", "expected_comunicados": ["2020_marzo_a", "2020_marzo_b", "2020_junio", "2021_marzo"]},
]


# In[12]:


#translate gold queries into spanish for later use

def translate_query(client, query_en):
    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": f"Translate this to Spanish. Return ONLY the translation, no preamble:\n\n{query_en}"
        }]
    )
    return response.content[0].text.strip()

client = anthropic.Anthropic() 
for item in gold_queries:
    item['query_es'] = translate_query(client, item['query'])


# ### 3. Define Gold Chunks

# 
# This is done by first conducting retrieval on the chunks to get a generous set of relevant chunks for each query.
# 
# The retrieval process uses hybrid ranking to choose the n most relevant chunks for each gold query.
# 
# Hybrid Ranking uses the combination of the cosine similarity score and the BM25 score to arrive at a ranking of all chunks from the set of expected comunicados for each query.
# 
# Cosine similarity scores each chunk based on semantic closeness between query and chunk as measured by the dot product of the respective normalized embeddings. 
# 
# BM25 scores each chunk based on the relevance of keywords common to both query and chunk. 
# 
# The process for calculating the BM25 score for a chunk is as follows:
# 
# 1. For the query, the algorithm weights:
#    a. Term Frequency (TF) - the number of times each word in the query appears in the candidate chunk
#       * A higher TF suggests more relevance of the chunk to the query and drives the score for the chunk up. e.g. (month, liquidity) 
#       * TF makes sure chunks dont score higher because they are longer and can accumulate more matches (e.g chunk is 50% longer than average chunk). 
#         * A constant b penalizes the chunk based on its length.
#       * TF also makes sure that multiple instances of the same term in a chunk do not inflate the TF score (e.g inflacion appears 10 times in chunk).
#         * A constant k1 penalizes the chunk by reducing the amount added to the TF score for each additional instance.
#    b. Inverse Document Frequency (IDF) - derived from the number of chunks in the entire corpus of chunks (in all comunicados) that contain each matching word
#       * A word found in more chunks is more common and does not contribute as much to the relevance of the chunk to the query, so it gets a lower IDF and drives the score down (e.g. month)
# 
# 2. The sum of the products of TF and IDF for each word in the query equals the BM25 score for the chunk.
# 
# $$\text{score}(q,d) = \sum_{t \in q} \underbrace{\text{IDF}(t)}_{\text{b}} \cdot \underbrace{\frac{f(t,d)\,(k_1+1)}{f(t,d) + k_1\left(1 - b + b\,\frac{|d|}{\text{avgdl}}\right)}}_{\text{a}}$$
# 
# where $f(t,d)$ is the count of term $t$ in chunk $d$, $|d|$ is the chunk length, and $\text{avgdl}$ is the average chunk length in the corpus.
# 
# Once cosine similarity and BM25 scores are calculated, the candidate chunks are ranked in descending order separately by each score. Each chunk's cosine rank and BM25 rank are then combined via Reciprocal Rank Fusion — each rank contributes 1/(k + rank), and the two contributions are summed to give the chunk's hybrid score. Ranks are used rather than raw scores because cosine similarities and BM25 scores are on incompatible scales.
# 
# The top n chunks by hybrid score are the retrieved chunks for the query. n is chosen to be relatively large so as to not filter out relevant chunks. 
# 
# After retrieval, the smaller subset of retrieved hunks for each query is then manually reviewed to identify gold ids.
# 

# #### Prepare corpus for BM25 scoring

# In[13]:


#tokenize the corpus (after stopword and stem) for BM25 scoring

tokenized_corpus = [tokenize_stem(chunk['text']) for chunk in corpus_embedded]

#create bm25 object with tokenized corpus for scoring candidate chunks based on text matching
bm25 = BM25Okapi(tokenized_corpus)

#create an index for each chunk in the corpus
key_to_idx = {
    chunk['name'] + "_" + str(chunk['chunk_id']): i
    for i, chunk in enumerate(corpus_embedded)
}


# #### Retrieve candidate chunks for gold queries

# In[30]:


#for each gold query, get top n retrieved chunks by hybrid ranking and add to query dict
candidate_review = build_candidate_review(embedder, gold_queries, corpus_embedded, bm25, key_to_idx, k_rrf=5)

#export candidates to Word doc for manual review of the candidate chunks for the final gold IDs.
export_candidate_review_doc(candidate_review, corpus_embedded, filepath="candidate_review.docx")



# In[32]:


for c in candidate_review:
    c['confirmed_related_chunks'] = list(c['candidates'])


# #### Remove irrelevant chunks

# In[33]:


# dictionary of irrelevant chunks after manual review

removals = {
    "What was the policy interest rate in March 2016?": [
        ("2016_marzo", 1),
    ],
    "What was the inflation rate reported in the December 2018 meeting?": [
        ("2018_diciembre", 0), ("2018_diciembre", 1),
        ("2018_diciembre", 2), ("2018_diciembre", 3),
    ],
    "What rate did the Council set in May 2020?": [
        ("2020_mayo", 1), ("2020_mayo", 2), ("2020_mayo", 3),
        ("2020_mayo", 4), ("2020_mayo", 5), ("2020_mayo", 6),
        ("2020_mayo", 7), ("2020_mayo", 8), ("2020_mayo", 9),
    ],
    "What non-conventional measures did the Bank announce in March 2020?": [
        ("2020_marzo_b", 0), ("2020_marzo_a", 1), ("2020_marzo_b", 3),
        ("2020_marzo_a", 7), ("2020_marzo_a", 2), ("2020_marzo_b", 2),
        ("2020_marzo_b", 1),
    ],
    "How did the Council describe labor market conditions in the June 2020 meeting?": [
        ("2020_junio", 0), ("2020_junio", 3), ("2020_junio", 2),
        ("2020_junio", 4), ("2020_junio", 11), ("2020_junio", 10),
        ("2020_junio", 8), ("2020_junio", 7), ("2020_junio", 6),
        ("2020_junio", 5), ("2020_junio", 9),
    ],
    "What was said about copper prices in the February 2018 meeting?": [
        ("2018_febrero", 0), ("2018_febrero", 1), ("2018_febrero", 7),
        ("2018_febrero", 8), ("2018_febrero", 4), ("2018_febrero", 6),
        ("2018_febrero", 9), ("2018_febrero", 5), ("2018_febrero", 10),
    ],
    "How did the policy rate change from March 2020 through July 2020?": [
        ("2020_julio", 6), ("2020_julio", 3), ("2020_julio", 9),
        ("2020_julio", 8), ("2020_junio", 8), ("2020_julio", 2),
        ("2020_julio", 5), ("2020_julio", 1), ("2020_marzo_a", 6),
        ("2020_marzo_b", 5),
    ],
    "When did the Council begin raising rates after the pandemic-era cuts, and why?": [
        ("2020_julio", 6), ("2020_julio", 1), ("2020_julio", 8),
        ("2020_julio", 2), ("2020_julio", 3), ("2022_enero", 3),
        ("2020_julio", 4), ("2021_octubre", 5),
    ],
    "How did the Council's tone on inflation expectations shift between 2020 and 2022?" : [
    ("2022_septiembre", 0), ("2022_julio", 0), ("2022_junio", 0), ("2022_marzo", 0),
    ("2020_enero", 7), ("2022_enero", 0), ("2022_mayo", 0), ("2022_enero", 8),
    ("2020_julio", 0), ("2020_diciembre", 7), ("2020_mayo", 0), ("2020_marzo_b", 0),
    ("2020_diciembre", 11), ("2020_junio", 0), ("2022_octubre", 6), ("2022_julio", 8),
    ("2020_octubre", 0), ("2020_enero", 0), ("2022_diciembre", 6), ("2020_diciembre", 0),
    ("2021_diciembre", 8), ("2020_septiembre", 0), ("2021_agosto", 9), ("2022_marzo", 8),
    ("2021_marzo", 0), ("2021_junio", 5), ("2022_mayo", 4), ("2022_enero", 5),
    ("2021_enero", 6), ("2021_marzo", 4), ("2020_marzo_b", 5), ("2021_julio", 12),
    ("2022_marzo", 5), ("2021_junio", 9), ("2022_junio", 7), ("2022_julio", 1),
    ("2021_mayo", 8), ("2020_octubre", 9), ("2022_junio", 5), ("2020_junio", 11),
    ("2022_enero", 3), ("2020_julio", 6), ("2021_julio", 11), ("2021_octubre", 12),
    ("2020_marzo_b", 8),
],
    "What non-conventional pandemic support measures were introduced, then later withdrawn or maintained, across 2020 and 2021?": [
        ("2020_junio", 2), ("2021_marzo", 4), ("2020_junio", 3),
        ("2020_marzo_b", 0), ("2020_marzo_b", 1), ("2021_marzo", 9),
        ("2020_marzo_a", 2), ("2020_marzo_b", 3),
    ],
}

import json 

def apply_removals(results, removals):
    for r in results:
        to_remove = removals.get(r["query"], [])
        if not to_remove:
            continue
        before = len(r["confirmed_related_chunks"])
        r["confirmed_related_chunks"] = [
            c for c in r["confirmed_related_chunks"]
            if (c["name"], c["chunk_id"]) not in to_remove
        ]
        after = len(r["confirmed_related_chunks"])
        if before != after:
            print(f"{r['query'][:60]}: removed {before - after} chunk(s)")
    return results

gold_queries = apply_removals(candidate_review, removals)

with open("eval/gold_queries.json", "w") as f:
    json.dump(gold_queries, f, indent=2, ensure_ascii=False)


# ### 4. Evaluate Retrieval

# The steps for evalulation are the following:
# 
# 1. Retrieve k chunks for each gold query
# 2. Calculate precision, recall and reciprocal rank when k chunks are retrieved
#    * Precision is the share of retrieved chunks that are in the set of gold chunks
#    * Recall is the share of gold chunks that were retreved
#    * Reciprocal Rank equals  1 divided by the rank of the first retrieved chunk that is
#      in the set of gold chunks — so 1.0 if the top hit is correct, 0.5 if the
#      second is, and 0 if none of the k are. Averaged across queries this is MRR.
# 3. Average each metric across the 15 gold queries to get the headline numbers
# 

# In[34]:


# Sweep parameters for retrieval tuning.

# k         = number of chunks to retrieve
# threshold = minimum cosine similarity score for a chunk to be ranked/retrieved
# k_rrf     = damping constant in Reciprocal Rank Fusion — 1/(k_rrf + rank), applied
#             to the cosine and BM25 ranks before summing.
#             Small k_rrf spreads the values out, so being ranked near the top matters
#             a lot and one strong rank can carry a chunk on its own.
#             Large k_rrf clusters the values, so rank differences matter less and a
#             chunk needs to score well on BOTH rankers to win.

params = {'k':[5,10,15,20],
          'threshold':[0.1, 0.4, 0.6, 0.9],
          'k_rrf': [1, 5, 10, 30, 60]
          }

# for k_rrf in params['k_rrf']:
#     print(f"\n*********** k_rrf = {k_rrf} ********\n")
#     precisions, recalls, rrs = evaluate_retrieval(embedder, gold_queries, corpus_embedded, bm25, key_to_idx, k=10, threshold=0.4, k_rrf=k_rrf)

# Coordinate sweep, not a full grid: k_rrf swept with k=10, threshold=0.4 held fixed.
# Best k_rrf = 5 on precision and recall (RR was better at higher k_rrf).
precisions, recalls, rrs = evaluate_retrieval(embedder, gold_queries, corpus_embedded, bm25, key_to_idx, k=15, threshold=0.4, k_rrf=5)


# ### 5. Generate Responses

# In[35]:


#generate responses

#plausible query with answers in text
query = "What was the policy of the Chilean Central Bank in may 2020 after COVID"
query_2 = "How did the Council describe labor market conditions in the June 2020 meeting?"

#irrelevant query - no answers in text
query_3 = "what is the recession gap and how does it relate to the phillips curve?"

#nonsense query - no answers in text
query_4 = "how do number of coconuts influence divorce"

query_5 = " What is the history of the Chilean peso currency design?"

#hard query

query_7 = "When did the Council begin raising rates after the pandemic-era cuts, and why?"

query_8 = "How did the Council's tone on inflation expectations shift between 2020 and 2022?"

query_9 = "What non-conventional pandemic support measures were introduced, then later withdrawn or maintained, across 2020 and 2021?"


# In[36]:


#Set Query, Translate, Retrieve k chunks using retrieval process
query = query_7
query_es = translate_query(client, query)


top_n = retrieve_chunks(embedder, query, query_es, corpus_embedded, bm25, key_to_idx, k=15, threshold=0.4, k_rrf = 5)
print(top_n)


# In[37]:


# Generate Response using retrieved chunks 
answer = generate_response(embedder, query, top_n)
print(answer)

