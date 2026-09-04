### api call
import anthropic
import dotenv
from dotenv import load_dotenv
import os

def generate_response(embedder, query, top_n, model="claude-sonnet-5", max_tokens=2000):

    SYSTEM_PROMPT = (
    "You are a research assistant answering questions about central bank policy "
    "using central bank press releases. Answer ONLY using the sources provided in the "
    "user's message. If the sources don't contain enough information to answer, say so "
    "explicitly rather than guessing or drawing on outside knowledge. "
    "When you use a source, cite it by its bracketed label, e.g. [Source: comunicado_name, chunk_id]."
)
    prompt = assemble_prompt(embedder, query, top_n, max_content_tokens=4000)

    if prompt is None:
        return "I don't have relevant information in the corpus to answer that." 


    load_dotenv()

    client = anthropic.Anthropic()

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[{"role":"user", "content":prompt}]
    )

    for block in response.content:
        if block.type == "text":
            return block.text

    return None 



def assemble_prompt(embedder, query, top_n, max_content_tokens=4000):
    #Assemble prompt from returned chunks for API call to send 

    if not top_n:
        return None

    if len(top_n) == 0:
        return None

    
    blocks = []
    running_tokens=0
    for n in top_n:
        block = (
            f"[Source: {n['name']}, chunk {n['chunk_id']}, similarity {n['score']:.2f}]\n"
            f"{n['decoded']}"
        )
        
        tok = embedder.tokenizer

        block_tokens=len(tok.encode(block))
        if running_tokens + block_tokens > max_content_tokens:
            print("limit reached")
            break
        blocks.append(block)
        running_tokens += block_tokens

    context = "\n\n---\n\n".join(blocks)
    prompt = (
        f"SOURCES:\n{context}\n"
        f"QUESTION: {query}"
    )

    return prompt
