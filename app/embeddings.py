"""Use the same local embedding model for documents and questions."""
from app.config import EMBED_MODEL
from app.ollama_client import post


def embed_texts(texts, is_query=False):
    # Nomic recommends distinct task prefixes for retrieval.
    prefix = "search_query: " if is_query else "search_document: "
    inputs = [prefix + text for text in texts] if EMBED_MODEL.startswith("nomic-embed-text") else texts
    return post("embed", {"model": EMBED_MODEL, "input": inputs,
                          "truncate": False})["embeddings"]
