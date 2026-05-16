import tiktoken

ENCODER = tiktoken.get_encoding("cl100k_base")
CHUNK_SIZE = 512
CHUNK_OVERLAP = 64


def chunk_text(text: str) -> list[str]:
    tokens = ENCODER.encode(text)
    chunks = []
    start = 0
    while start < len(tokens):
        end = min(start + CHUNK_SIZE, len(tokens))
        chunks.append(ENCODER.decode(tokens[start:end]))
        if end == len(tokens):
            break
        start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks
