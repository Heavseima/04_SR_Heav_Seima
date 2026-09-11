"""Load UTF-8 text/Markdown documents from one folder."""
from app.config import DATA_DIR


def load_documents(folder=DATA_DIR):
    documents = []
    for path in sorted(folder.iterdir()):
        if path.is_file() and path.suffix.lower() in {".txt", ".md"}:
            text = path.read_text(encoding="utf-8").strip()
            if text:
                documents.append({"source": path.name, "text": text})
    if not documents:
        raise ValueError(f"No non-empty .txt or .md documents in {folder}")
    return documents
