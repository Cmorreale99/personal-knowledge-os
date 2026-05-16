import sys
from qa import answer


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: python ask.py \"your question here\"")
        sys.exit(1)

    question = " ".join(sys.argv[1:])
    result = answer(question)

    print(f"\n{result['answer']}\n")

    if result["sources"]:
        print("Sources:")
        for s in result["sources"]:
            print(f"  {s['source']} · chunk {s['chunk_index']} · score {s['score']}")
