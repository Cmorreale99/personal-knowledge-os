import sys
from retriever import retrieve


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python query.py \"your question here\"")
        sys.exit(1)

    query = " ".join(sys.argv[1:])
    results = retrieve(query)

    if not results:
        print("no results found")
        sys.exit(0)

    for i, r in enumerate(results, 1):
        print(f"\n--- [{i}] {r['source']} · chunk {r['chunk_index']} · score {r['score']} ---")
        print(r["content"])
