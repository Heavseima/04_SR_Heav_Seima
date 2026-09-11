from config import TOP_K
from embeddings import embed_texts
from vector_store import search


def retrieve(question, collection):
    return search(collection, embed_texts([question], is_query=True)[0], TOP_K)


def format_chunks(chunks):
    return "\n\n".join(f"[{i}] {c['source']} (chunk {c['chunk']}, cosine distance {c['distance']:.4f})\n{c['text']}"
                       for i, c in enumerate(chunks, 1))
