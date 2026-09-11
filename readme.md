# Basic RAG homework

A local terminal app that loads documents, splits them, embeds the chunks, retrieves the top three matches, and asks Ollama to answer using those excerpts.

## Setup and run

Requires Python 3.14, Poetry, and a running Ollama service. From this folder:

```bash
poetry install
ollama pull llama3.2
ollama pull nomic-embed-text
# Run ollama serve in another terminal if Ollama is not already running.
poetry run python demo_ollama_check.py
poetry run python main.py --index
poetry run python demo_vector_check.py
poetry run python main.py
```

Ask a question such as `How do I set up company email on a mobile device?`. Type `exit` to quit; Ctrl+C and Ctrl+D also exit. Blank input is ignored. Each question is independent; there is no conversation memory.

The supplied `data/` folder contains ten IT support documents from the Doc Material for Ingest set: mobile email, PIN reset, VPN, Microsoft Office, Webex, backups, tablets, wireless networking, printers, and Android email. The ingestion code accepts any UTF-8 `.txt` or `.md` files placed directly in this folder. Run `--index` again after editing documents. Reindexing updates existing records and removes stale chunks; it does not accumulate duplicates. The database persists in `chroma_db/` between runs.

## Design

- **Ingestion:** load non-empty `.txt` and `.md` files directly inside `data/`.
- **Chunking:** the existing recursive character splitter, using paragraph, newline, sentence, word, then character boundaries. Maximum 500 characters, with up to 80 characters of whole-split overlap. Paragraphs stay together when they fit, making short notes readable and keeping related facts together. Overlap is not guaranteed across recursive boundaries.
- **Embeddings:** Ollama `nomic-embed-text`, with `search_document:` and `search_query:` prefixes.
- **Storage:** local persistent ChromaDB; explicit embeddings and cosine distance (smaller is closer).
- **Retrieval:** embed the question and return the top three chunks, including filename and chunk number.
- **Generation:** Ollama `llama3.2`, temperature 0, a context-only prompt, and numbered source references. The model is instructed to say `I could not find this in your documents.` when context cannot answer. This prompt reduces unsupported answers but cannot guarantee perfect grounding.

Defaults are in `config.py`. Optional environment variables: `OLLAMA_URL`, `GENERATION_MODEL`, `EMBED_MODEL`. If changing the embedding model, use a new `DB_DIR` in config and rebuild, so incompatible embeddings are never mixed. A missing model or unavailable Ollama service produces an explanatory error.

## Files and homework evidence

| File | Purpose |
| --- | --- |
| `ingestion.py`, `chunking.py` | Load and split documents |
| `embeddings.py`, `ollama_client.py` | Local model requests |
| `vector_store.py` | Persist and search vectors |
| `retriever.py`, `generator.py`, `pipeline.py` | Question-to-answer flow and offline indexing |
| `main.py` | Terminal chat and indexing command |
| `demo_ollama_check.py` | Standalone model smoke check |
| `demo_vector_check.py` | Standalone top-three retrieval check |
| `run_homework_tests.py` | Record five real questions and answers |
| `test_log.md` | Retrieved passages and generated answers |
| `reflection.md` | 150-300 word project reflection draft |

Regenerate the homework log with:

```bash
poetry run python run_homework_tests.py
poetry run python -m unittest discover -s tests
```

