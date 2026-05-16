import sys
from pathlib import Path
from sqlalchemy.orm import Session
from db import engine, init_db, Chunk
from chunker import chunk_text
from embedder import embed


def ingest_file(path: str):
    source = Path(path).name
    text = Path(path).read_text(encoding="utf-8")

    chunks = chunk_text(text)
    print(f"[{source}] chunked into {len(chunks)} pieces")

    embeddings = embed(chunks)
    print(f"[{source}] embeddings generated")

    with Session(engine) as session:
        for i, (content, embedding) in enumerate(zip(chunks, embeddings)):
            session.add(Chunk(source=source, chunk_index=i, content=content, embedding=embedding))
        session.commit()

    print(f"[{source}] done — {len(chunks)} chunks stored")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python ingest.py <file> [file ...]")
        sys.exit(1)

    init_db()
    for path in sys.argv[1:]:
        ingest_file(path)
