# A RAG pipeline for querying Central Bank Communiqués from the Bank of Chile

## The Problem

The Banco Central de Chile conducts recurring meetings during which macroeconomic conditions of the economy are discussed and decisions are taken on the evolution of the Monetary Policy Rate. The project aims to configure a pipeline to query the corpus of communiqués in order to answer questions about monetary policy.

## Data

The corpus consists of press releases from Banco Central de Chile between the years 2016 and 2026.

## Methodology
The process employed to build the pipeline involved the following:
1. Building and Preparing the Corpus
2. Content Retrieval and Evaluation
3. Response Generation

### 1. Building and Preparing the Corpus

In this first phase of the project, I gathered approximately 93 pdf documents into a file folder and loaded into the Jupyter Notebook. I then loaded an embedder in order to represent the text contents of the pdfs into the vector space. Before embedding, the text contents had to be parsed from the PDF documents and cleaned in order to remove formatting, punctuation and boilerplate content. The contents of each document were divided into the chunks that would be embedded into the vector space.

Concerns in this phase:
* The length of each chunk was set to be the maximum sequence length allowed by the embedding model.
* In order to not lose meaning due to the cutting off each chunk from its surrounding context, each successive chunk overlapped with the previous chunk by the amount of 60% of the maximum number of tokens.
* Because the corpus is in Spanish, while queries and responses in the pipeline will be in English, I chose the 'sentence-transformers/paraphrase-multilingual-mpnet-base-v2' embedding model, a model trained to handle cross-language embedding into the vector space. 

### 2. Content Retrieval and Evaluation

The retrieval module is responsible for the accurate and thorough collecting of the relevant chunks for a query in order for synthesis and response generation. Because of its criticality to the effectiveness of the pipeline, the retrieval module was written and evaluated iteratively in order to improve the metrics of the system. Before discussing the development of the retrieval process, it makes sense to explain how the system is evaluated.

#### Evaluation

The evaluation of the RAG system consists of writing a 'gold' set of queries and mapping them to the correct chunks of the corpus that are relevant for generating an accurate response to the query. A set of 15 queries were written, divided into the following difficulty categories: Irrelevant, Easy, Medium, and Hard. 
Ideally, the construction of a gold set consists of manual review of the entire corpus to identify the relevant chunks. Because of the tedium of this process, I devised some strategies in order to minimize the effort involved.
First, because many queries in the gold set are time-bound, it made sense to organize the documents by month and year of the meeting. This categorization allowed us to map each query to an expected set of papers. (e.g. query: What was the monetary policy rate in June 2020?),expected papers: 2020_junio)

Next, I further filter the subset of chunks for each query by calculating and ranking the semantic closeness (via cosine similarity of its vector embeddings) between the query and the chunks in its expected comunicados. I then take the top n chunks by hybrid ranking (to be discussed in the retrieval step), where n is set to 3 times the number of expected papers for the query. This allows us to scale the size of the candidate chunks according to the number of expected comunicados. The size of n also allows the set of candidate chunks to be permissive. 

The resulting set of candidate chunks is much easier to manually review, and to reduce to the final set of relevant chunks for the query, also known as the "gold IDs".

It is against these gold IDs, that I evaluate the results of the built retrieval. The relevant metrics are:

* Precision - The share of retrieved chunks that are in the set of gold IDs. 
* Recall - The share of gold IDs for the query that were retrieved (retrieved IDs). 
* Mean Reciprocal Rank - The mean, across queries, of 1 divided by the rank of the first gold ID among the retrieved IDs.

#### Retrieval

Building the retrieval is the most involved part of the RAG. In this case, I iterated on the design of the module with the aim of improving the resulting metrics.

*Version 1: Cosine Similarity*

In the first iteration of the retriever, the retriever simply calculated the cosine similarity score between the vector embeddings for the query and each chunk and ranked the chunks accordingly, with the top k (default = 15) chunks being the final retrieved chunks.
Two additional issues were evident that contributed to poor scores on the concerned metrics:
* Semantic closeness was not enough to distinguish the chunks because of the boilerplate nature of most of the text in the comunicado. Chunks tend to contain text noting "an increase in the interest rate of....", "by x points", "inflation expectations", etc. This also meant that chunks from relevant papers were ranked low enough that the document was effectively shut out of the retrieved IDs. To mitigate this, a fix was applied in order to make sure each document contributed a certain amount of chunks (e.g. 3) to the candidate chunks before their final ranking. This was done by ranking the chunks first within each document before a final ranking on the entire set. The fix is standard in all subsequent versions. 
* For time-bound queries, it was easy for comunicados from irrelevant time periods to rank highly.
  
The next iterations would attempt to solve these issues: 

*Version 2: Cosine Similarity + Date Filter*
In this iteration, I implemented a function to parse queries for years and months and filter the chunks by the relevant time periods.
* In the case that the queries contained multiple years or months, the candidate set of chunks would be filtered by the range in between the years or months mentioned.
* In the case of no month or year mentioned, the filter was not applied, allowing the candidate set of chunks to contain comunicados from every month and year. 
The result was improved retrieval on time-bound queries. However, non-time bound queries continued to perform poorly.

*Version 3: Date Filter + Hybrid Ranking based on cosine similarity and BM25 scoring*
The next idea was to combine the semantic closeness with a score based on the presence in the chunks of important keywords in the query. A simple keyword match between query and chunk would not be sophisticated enough and might include common words. To this end therefore, I implemented the BM25 algorithm for text-based retrieval. BM25 assigns a score for each chunk by weighting the count of each keyword in the query along with the inverse frequency of the word in the corpus. This allows the score to be influenced largely by the occurence of query keywords in the chunk that are relatively rare in the corpus. Relatively rare words in the corpus are more likely to be relevant than more frequently occuring words. Finally, BM25 normalizes the scores to account for varying chunk lengths. It also computes saturation so as to decrease the marginal increase due to additional occurence of each keyword. Also important for BM25 is that the queries had to be translated into Spanish in order for the queries and chunks to match.
Finally, all chunks are ranked separately on semantic score and BM25 score. Each chunk is then given a final score that combines both rankings.

*Version 4: Cosine Similarity + Date Filter + Hybrid Ranking + Cross-Encoder Reranker*
While easy and medium queries scored relatively well on the relevant metrics, the challenge remained to retrieve the correct chunks for hard queries particularly where time periods were implicit (e.g during the pandemic). In this version, I employed a cross-encoder that combined the query and each chunk for embedding, instead of each separately. The cross-encoder reranked the subset of retrieved IDs after the Hybrid Ranking step. This version made precision and recall worse. Further investigation revealed that the cross-encoder reranker did not solve the implicit dating issue, as it had no awareness of dates. In one case, it promoted boilerplate chunks from 2024 and 2025 for a 2021 query, due to the continued similarity of the chunks even when query is included. 

*Version 5: Date Filter + Blended Scoring (Hybrid Rank + Cross-Encoder Reranker)*
In this version, instead of updating the ranking with the results of the Cross-Encoder, the rank of each chunk with respect to the reranker score was added as another input to the hybrid ranking.
This version showed a marked improvement. Blending allows us to keep the hybrid rank ordering instead of letting the cross-encoder override it. 

In a final attempt to improve scores for the hard queries without explicit dates, I employed an LLM to parse the query for the implicit start and end periods where no dates existed. This enhancement to the date filter resulted in higher scores downstream in all the versions of the retrieval module.

However, despite all the improvements to retrieval, it was impossible to surface the most relevant chunks for a single hard query. The query "When did the Council begin raising rates after the pandemic-era cuts, and why?" has its most relevant chunk in '2021_julio_0'. Because this chunk was never a candidate for gold IDs, it had to be added by hand to the gold corpus, and still failed to surface in retrieval. The issue was discovered because every configuration produced a well-sourced answer that could not name the date.

The results for retrieving k=15 chunks appear below: 

P

tier                easy  medium   hard
config                                 
cos_sim_only       0.000   0.050  0.150
plus_date_filter   0.838   0.588  0.550
plus_hybrid        0.838   0.588  0.600
plus_rerank        0.838   0.588  0.567
plus_rerank_blend  0.838   0.588  0.633 

R 

tier                easy  medium   hard
config                                 
cos_sim_only       0.000   0.208  0.197
plus_date_filter   0.917   0.917  0.445
plus_hybrid        0.917   0.917  0.472
plus_rerank        0.917   0.917  0.451
plus_rerank_blend  0.917   0.917  0.532 

MRR 

tier               easy  medium   hard
config                                
cos_sim_only        0.0   0.091  0.583
plus_date_filter    1.0   1.000  1.000
plus_hybrid         1.0   1.000  1.000
plus_rerank         1.0   1.000  1.000
plus_rerank_blend   1.0   1.000  1.000

Notes
* Abstention scores were recorded for the case of irrelevant queries. However, because nothing exists to prevent retrieval even when there are no gold IDs, IDs are always retrieved. This is an issue for addressing in further work on the system.
* Beyond the cosine similarity only, all versions have the best possible MRR score of 1, because the improved date filter narrows down the corpus to a few chunks from one or two comunicados.
* Precision is computed over the number of chunks returned rather than over k. Because the date filter can legitimately reduce the candidate pool below k — the March 2016 query returns 4 chunks in total — dividing by k would penalise correct behaviour.


### 3. Response Generation
