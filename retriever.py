from sqlalchemy import select
from sqlalchemy.orm import Session
from db import engine, Chunk
from embedder import embed


def retrieve(query: str, top_k: int = 5) -> list[dict]:
    query_embedding = embed([query])[0]
    distance = Chunk.embedding.cosine_distance(query_embedding).label("distance")

    with Session(engine) as session:
        rows = session.execute(
            select(Chunk, distance).order_by(distance).limit(top_k)
        ).all()

    return [
        {
            "source": chunk.source,
            "chunk_index": chunk.chunk_index,
            "content": chunk.content,
            "score": round(1 - dist, 4),
        }
        for chunk, dist in rows
    ]
