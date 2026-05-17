from openai import OpenAI
from retriever import retrieve

client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
MODEL = "llama3.2"

SYSTEM_PROMPT = (
    "You are a personal knowledge assistant. Answer questions using only the "
    "provided context excerpts. If the context doesn't contain enough information "
    "to answer, say so clearly. Be concise and cite which source(s) you drew from."
)


def answer(question: str, top_k: int = 5) -> dict:
    chunks = retrieve(question, top_k=top_k)

    if not chunks:
        return {"answer": "No relevant knowledge found in your notes.", "sources": []}

    context = "\n\n".join(
        f"[{c['source']} · chunk {c['chunk_index']}]\n{c['content']}"
        for c in chunks
    )

    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
        ],
    )

    return {
        "answer": response.choices[0].message.content,
        "sources": [
            {"source": c["source"], "chunk_index": c["chunk_index"], "score": c["score"]}
            for c in chunks
        ],
    }
