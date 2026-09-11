"""Build the index once, then chat with your documents in the terminal."""
import argparse
from pipeline import answer_question, build_index
from retriever import format_chunks
from vector_store import get_collection


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", action="store_true", help="Rebuild the document index and exit")
    args = parser.parse_args()
    collection = get_collection()
    if args.index:
        documents, chunks = build_index(collection)
        print(f"Indexed {documents} documents as {chunks} chunks.")
        return
    if not collection.count():
        print("Run poetry run python main.py --index first.")
        return
    print("Chat with Documents | type exit to quit")
    while True:
        try:
            question = input("\nYou: ").strip()
            if question.lower() == "exit":
                break
            if not question:
                continue
            answer, chunks = answer_question(question, collection)
            print(f"\nRetrieved chunks:\n{format_chunks(chunks)}\n\nAnswer: {answer}")
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        except (RuntimeError, ValueError) as exc:
            print(f"Error: {exc}")


if __name__ == "__main__":
    try:
        main()
    except (RuntimeError, ValueError) as exc:
        raise SystemExit(str(exc))
