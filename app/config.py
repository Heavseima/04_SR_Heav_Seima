"""Small, editable defaults for the homework."""
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_DIR = ROOT / "chroma_db"
COLLECTION = "homework"
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434").rstrip("/")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")
GENERATION_MODEL = os.getenv("GENERATION_MODEL", "llama3.2")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 80
TOP_K = 3
