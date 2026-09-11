"""Standalone model check; does not depend on the RAG pipeline."""
from app.config import EMBED_MODEL, GENERATION_MODEL
from app.ollama_client import post

if __name__ == "__main__":
    result = post("embed", {"model": EMBED_MODEL, "input": "Hello world"})
    print(f"{EMBED_MODEL}: {len(result['embeddings'][0])} dimensions")
    result = post("generate", {"model": GENERATION_MODEL, "prompt": "Say hello in one sentence.",
                              "stream": False, "options": {"num_predict": 40}})
    print(f"{GENERATION_MODEL}: {result['response']}")
