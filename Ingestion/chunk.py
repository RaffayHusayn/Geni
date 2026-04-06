# chunk.py
import re

CHUNK_TOKEN_TARGET = 500
OVERLAP_TOKEN_TARGET = 100

# ~4 chars per token is the standard approximation for English text
CHARS_PER_TOKEN = 4
CHUNK_SIZE = CHUNK_TOKEN_TARGET * CHARS_PER_TOKEN   # ~2000 chars
OVERLAP_SIZE = OVERLAP_TOKEN_TARGET * CHARS_PER_TOKEN  # ~400 chars


def _split_sentences(text: str) -> list[str]:
    parts = text.strip().split('\n')
    return [p.strip() for p in parts if p]

def _build_chunks(sentences: list[str])->list[str]:
    chunks=[]
    start = 0
    while start < len(sentences):
        end=start
        current_chars = 0
        while end<len(sentences):
            sentence_len = len(sentences[end])+ 1
            if current_chars+sentence_len > CHUNK_SIZE and end > start:
                break
            current_chars +=sentence_len
            end +=1
        chunk_joined = " ".join(sentences[start:end])
        chunks.append(chunk_joined)

        if end == len(sentences):
            break

        # walk backwards to have an overlap window
        backward_step = end -1
        overlap_chars = 0 
        while overlap_chars < OVERLAP_SIZE and backward_step > start:
            overlap_chars +=len(sentences[backward_step])+1
            backward_step -=1

        start = backward_step + 1
    return chunks

def chunk(text: str, metadata: dict, go_id: str) -> list[dict]:

    sentences = _split_sentences(text)
    chunks= _build_chunks(sentences)

    return [
        {
            "go_id": go_id,
            "chunk_index": i,
            "content": chunk,
            "metadata": metadata,
        }
        for i, chunk in enumerate(chunks)
    ]
