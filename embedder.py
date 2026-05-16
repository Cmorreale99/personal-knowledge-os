from openai import OpenAI

client = OpenAI()
EMBEDDING_MODEL = "text-embedding-3-small"
BATCH_SIZE = 100


def embed(texts: list[str]) -> list[list[float]]:
    embeddings = []
    for i in range(0, len(texts), BATCH_SIZE):
        batch = texts[i : i + BATCH_SIZE]
        response = client.embeddings.create(model=EMBEDDING_MODEL, input=batch)
        embeddings.extend(item.embedding for item in response.data)
    return embeddings
