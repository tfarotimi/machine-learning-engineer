def chunk_content(embedder, text, overlap_ratio=0.06):

    #tokenize, chunk by max sequence length of model, and decode back to text

    tok = embedder.tokenizer
    max_tokens = embedder.max_seq_length
    overlap_tokens = int(overlap_ratio * max_tokens)

    all_token_ids = tok.encode(text)
    n = len(all_token_ids)

    chunked = {}
    chunk_id = 0
    start = 0

    while start < n:
        end = min(start + max_tokens, n)
        window_ids = all_token_ids[start:end]
        chunked[chunk_id] = tok.decode(window_ids)
        chunk_id += 1 

        start = end - overlap_tokens 

        if end == n:
            break 

    return chunked

