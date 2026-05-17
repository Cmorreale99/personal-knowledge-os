import numpy as np
from sqlalchemy import select
from sqlalchemy.orm import Session
from db import engine, Chunk
from embedder import embed


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed([query])[0]

    with Session(engine) as session:
        chunks = session.execute(select(Chunk)).scalars().all()

    scored = sorted(
        ((chunk, _cosine_similarity(query_embedding, chunk.embedding)) for chunk in chunks),
        key=lambda x: x[1],
        reverse=True,
    )

    return [
        {
            "source": chunk.source,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content,
            "score": round(score, 4),
        }
        for chunk, score in scored[:top_k]
    ]
