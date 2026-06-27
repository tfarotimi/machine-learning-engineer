# Toy RAG Build — Inflation Forecasting Corpus

**Goal of v1:** Build a crude, end-to-end RAG over ~20 inflation/forecasting papers and *watch it succeed and fail*. The point is NOT a polished system — it's to hit embeddings, retrieval, and chunking as real obstacles, and to use your domain expertise to judge retrieval quality.

**Stack target:** corpus small enough that you can manually inspect every chunk and retrieval result. ~20 docs is the ceiling for v1 (you must be able to *see* what's happening). Don't scale up for the sake of it.

**Where:** local, conda env, Git repo from day one. This is a real artifact, not a throwaway.

---

## The pipeline — 5 stages

### Stage 1: Load & extract
- Pull text out of ~20 PDFs.
- Library: `pypdf` or `pymupdf`.
- **Expected obstacle:** PDF text extraction is messy — headers, footers, broken columns, equations turning to garbage. This is normal. Don't over-clean in v1.

### Stage 2: Chunk
- Split each paper into pieces.
- **Expected obstacle:** how big? With or without overlap? This IS the chunking concept becoming concrete. Start simple (fixed-size, e.g. ~500 chars or ~100 words, with small overlap), see what breaks.

### Stage 3: Embed
- Turn each chunk into a vector.
- Library: `sentence-transformers` (runs local, free, no API key).
- **Expected obstacle:** which model? what dimension? This is "embedding" stopping being abstract.

### Stage 4: Retrieve  ← MOST IMPORTANT
- Embed a question, compute cosine similarity against all chunk vectors, take top-k.
- Do this **by hand in numpy** — NO vector database for 20 docs. Keep the mechanism visible.
- **Expected obstacle:** retrieval sometimes returns irrelevant chunks. This is where your domain expertise earns its keep — you can SEE when a retrieved chunk is off-topic in a way a non-expert can't. Study the failures.

### Stage 5: Generate
- Stuff retrieved chunks into a prompt, ask an LLM to answer using them.
- **Optional for v1:** you can skip generation at first and just inspect retrieval. Add generation once retrieval feels sane.
- **Expected obstacle:** did the model actually use the context, or hallucinate? Note when it ignores the chunks.

---

## Minimal stack
- `pypdf` / `pymupdf` — extraction
- `sentence-transformers` — embeddings (local, free)
- `numpy` — cosine similarity by hand
- An LLM API — generation step (or defer)

## Deliberately EXCLUDED from v1 (parked — do not build these yet)
These are v2. Building them now turns a weekend into a month and hides the mechanism:
- Vector database (Chroma, FAISS, etc.) — unnecessary at 20 docs
- LangChain / LlamaIndex — learn the raw mechanism first
- Reranking
- Chunking optimization
- **Evaluation framework** — this is the big v2, and it's your moat. Comes after v1 works.

---

## Reading
- Do NOT read ahead in Huyen to "prepare." Build first.
- When Stage 4 retrieval misbehaves → THEN skip to Huyen's RAG chapter. It'll click because you'll have a concrete broken thing to fix.
- Read the eval chapter when you start v2 (the eval framework).

---

## Definition of done for v1
1. All 5 stages run end-to-end (generation optional).
2. You can ask a question and see which chunks were retrieved.
3. You've looked at several retrieval results and can articulate *why* some are good and some are bad.
4. Repo committed, short README.

That's it. When v1 is done, v2 is the eval framework — the scarce, hireable skill.

---

## Discipline note
The pull to "learn one more fundamental first" or "add one more feature" is the comfortable-shelf reflex. v1's job is small and specific: see retrieval work and fail. Resist scope creep. The building is the learning.
