"""Persist explicit embeddings in Chroma and search with cosine distance."""
import chromadb
from chromadb.config import Settings
from app.config import DB_DIR, COLLECTION, EMBED_MODEL


def get_collection():
    client = chromadb.PersistentClient(path=str(DB_DIR), settings=Settings(anonymized_telemetry=False))
    collection = client.get_or_create_collection(
        COLLECTION, embedding_function=None,
        metadata={"hnsw:space": "cosine", "embedding_model": EMBED_MODEL})
    if collection.metadata.get("embedding_model") != EMBED_MODEL:
        raise ValueError("Embedding model changed. Restore EMBED_MODEL or use a new DB_DIR.")
    return collection


def save_chunks(collection, chunks, vectors):
    collection.upsert(ids=[c["id"] for c in chunks],
                      documents=[c["text"] for c in chunks], embeddings=vectors,
                      metadatas=[{"source": c["source"], "chunk": c["chunk"]} for c in chunks])
    # Remove stale chunks when source files have changed or been deleted.
    current_ids = {c["id"] for c in chunks}
    stale = [i for i in collection.get()["ids"] if i not in current_ids]
    if stale:
        collection.delete(ids=stale)


def search(collection, vector, top_k=3):
    if collection.count() == 0:
        raise ValueError("The index is empty. Run: poetry run python -m app.main --index")
    result = collection.query(query_embeddings=[vector], n_results=min(top_k, collection.count()),
                              include=["documents", "metadatas", "distances"])
    return [{"id": result["ids"][0][i], "text": text,
             **result["metadatas"][0][i], "distance": result["distances"][0][i]}
            for i, text in enumerate(result["documents"][0])]
