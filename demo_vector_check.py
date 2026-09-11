"""Standalone check: embed a question and print the top three database hits."""
import sys
from embeddings import embed_texts
from retriever import format_chunks
from vector_store import get_collection, search

if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "How do I set up company email on a mobile device?"
    chunks = search(get_collection(), embed_texts([question], is_query=True)[0], 3)
    print(f"Question: {question}\n\n{format_chunks(chunks)}")
