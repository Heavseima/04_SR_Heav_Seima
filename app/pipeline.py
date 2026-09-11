from app.chunking import recursive_text_split
from app.config import CHUNK_SIZE, CHUNK_OVERLAP
from app.embeddings import embed_texts
from app.generator import generate
from app.ingestion import load_documents
from app.retriever import retrieve
from app.vector_store import save_chunks


def build_index(collection):
    documents = load_documents()
    chunks = []
    for document in documents:
        for number, text in enumerate(recursive_text_split(document["text"], CHUNK_SIZE, CHUNK_OVERLAP), 1):
            chunks.append({"id": f"{document['source']}:{number}", "source": document["source"],
                           "chunk": number, "text": text})
    vectors = embed_texts([chunk["text"] for chunk in chunks])
    save_chunks(collection, chunks, vectors)
    return len(documents), len(chunks)


def answer_question(question, collection):
    if not question.strip():
        raise ValueError("Please enter a question.")
    chunks = retrieve(question, collection)
    return generate(question, chunks), chunks
