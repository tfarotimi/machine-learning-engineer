import numpy as np
import re
from itertools import product
import textwrap
import nltk
nltk.download('punkt')
nltk.download('stopwords')

from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer

from lib.generate import generate_response

import regex as re

#create dict to map month names to integers
MONTHS = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4,
    "mayo": 5, "junio": 6, "julio": 7, "agosto": 8,
    "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
    "january": 1, "february": 2, "march": 3, "april":  4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}



meses_pattern = "|".join(MONTHS) # "enero|febrero|marzo|....."
 
#regex pattern for finding month names in chunks
pattern = rf"({meses_pattern})\s+de\s+(\d{{4}})"



def retrieve_chunks(embedder, query, query_es, embeddings, bm25, key_to_idx, threshold, k, k_rrf, per_comunicado_n=3):
    query_dates = parse_query_date(query)
        
    #embed query

    query_vec = embedder.encode(query, normalize_embeddings=True)

    grouped = {}

    #create a dict of chunks retrieved based on generous cos sim threshold, key is the comunicado name. 
    for comunicado in embeddings:
        

        name = comunicado['name']
        _id = comunicado['chunk_id']
        #get embedding and magnitude
        emb = comunicado['embedding']

        comunicado_year, comunicado_month_num = parse_comunicado_date(name)

        #if dates in query, check each date, if in comunicado, calculate similarity, if its not, go to next query
        #if no dates in query, just calculate similarity as normal
        #calculate similarity of query with each comunicado

        #if filtered certain query dates, only calculate cos similarity for query dates
        if len(query_dates) > 0:
            date_match = any((comunicado_year, comunicado_month_num) == d for d in query_dates)
            if not date_match:
                continue   # this continue is on the OUTER loop — skips the whole comunicado
        
        
        cos_sim = np.dot(query_vec, emb)

        if cos_sim < threshold:            
            continue


        #decode vector 
        decoded = comunicado['text']

        
        chunk_data = {'chunk_id':_id,'score':cos_sim, 'name': name, 'comunicado_year': comunicado_year, 'decoded':decoded}

        grouped.setdefault(name, []).append(chunk_data) #each comunicado now has its chunks stored in the dict, key is the comunicado name

    #flatten grouped dict into list for hybrid rank 

    all_chunks = []
    for name, chunks in grouped.items():
        all_chunks.extend(chunks) #still pointing to dict in grouped


    #pass list of chunks to get rrf score for each chunk, adds rrf to each chunk in the all_chunks, and thus grouped
    hybrid_rank(all_chunks, query_es, bm25, key_to_idx, k_rrf=k_rrf)

    all_top_chunks = []

    #for each comunicado in grouped, get the top 'per_comunicado_n'ranked by the rrf score
    for name, chunks in grouped.items():
        top_n = sorted(chunks, key=lambda c: c['rrf'], reverse=True)[:per_comunicado_n]
        all_top_chunks.extend(top_n)

        # for c in all_top_chunks:
        #     display_chunk(comunicado=c['comunicado'], chunk_id=c['chunk_id'], text=c['decoded'], score = c['score'])
    #all_top_chunks contains the top 3 for each comunicado, now we can sort the whole list by chunk rrfs
    all_top_chunks = sorted(all_top_chunks, key=lambda c: c['rrf'], reverse=True)

    #grab the highest rrf 'k'chunks
    return all_top_chunks[:k]  


        
#parse dates from comunicado names
def parse_comunicado_date(name: str) -> tuple[int, int]:
    year_str, mes_str = name.split("_")[:2]
    year = int(year_str) 
    mes = MONTHS[mes_str]
    return (year, mes)

#parse dates referenced in query 
def parse_query_date(query: str) -> list[tuple[int, int]]:
    query_lower = query.lower()

    meses_encontrados = re.findall(meses_pattern, query_lower)
    years_encontrados = re.findall(r"\d{4}", query_lower)

    mes_nums = [MONTHS[m] for m in meses_encontrados]

    if len(mes_nums) < 1 and len(years_encontrados) > 0:
        mes_nums = [1,2,3,4,5,6,7,8,9,10,11,12]
    elif(len(mes_nums) >=2):
        mes_nums=list(range(min(mes_nums), max(mes_nums) +1 ))
            
    years_int = [int(y) for y in years_encontrados]

    
    if len(years_int) >= 2:
        years = list(range(min(years_int), max(years_int) + 1))   # fill the gap: 2020,2021,2022
    elif len(years_int) == 1:
        years = years_int
    else:
        years = []

    

    pares = list(product(years, mes_nums))
    return pares

def hybrid_rank(candidates, query, bm25, key_to_idx, k_rrf=5):
    query_tokens = tokenize_stem(query.lower())
    bm25_scores = bm25.get_scores(query_tokens)

    print(query, "\n")
    for c in candidates:
        key = c['name'] + "_" + str(c['chunk_id'])
        idx = key_to_idx[key]
        c['bm25_score'] = bm25_scores[idx]        

    sim_sort = sorted(candidates, key=lambda c:c['score'], reverse=True)
    bm25_sort = sorted(candidates, key=lambda c: c['bm25_score'], reverse=True)

    for i, c in enumerate(sim_sort, start=1):
        c['semantic_rank'] = i

    for i, c in enumerate(bm25_sort, start=1):
        c['bm25_rank'] = i

    for c in candidates:
        c['rrf'] = 1/(k_rrf + c['semantic_rank']) + 1/(k_rrf + c['bm25_rank'])
        key = c['name'] + "_" + str(c['chunk_id'])


    rrf_sort = sorted(candidates, key=lambda c:c['rrf'], reverse=True)

    return rrf_sort


def tokenize_stem(text):
    stemmer = SnowballStemmer('spanish')
    spanish_stopwords = set(stopwords.words('spanish'))

    tokens = re.findall(r'\w+', text.lower())
    filtered = [t for t in tokens if t not in spanish_stopwords]
    return [stemmer.stem(t) for t in filtered]


def display_chunk(comunicado, chunk_id, text, score=None):
    print(f"\n{'='*60}")
    print(f"doc: {comunicado} chunk: {chunk_id}" + (f" | score: {score:.3f}" if score else ""))
    print(f"{'-'*60}")
    print(textwrap.fill(text, width=90))
