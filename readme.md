# Basic RAG Homework: Chat with Documents

A local Python terminal application that implements the five stages of Naive RAG: ingestion, chunking, embedding, retrieval, and generation. It uses Ollama for local models and ChromaDB for persistent vector storage.

## Setup and run

Install Python 3.14, Poetry, and Ollama. Run the following commands from the project root:

```bash
poetry install
ollama pull llama3.2
ollama pull nomic-embed-text
```

Make sure Ollama is running. If needed, start `ollama serve` in a separate terminal. Check that both models respond:

```bash
poetry run python -m app.demo_ollama_check
```

Place non-empty UTF-8 `.txt` or `.md` files directly in `data/`.

Build the index, check the top three retrieval results, and start chatting:

```bash
poetry run python -m app.main --index
poetry run python -m app.demo_vector_check
poetry run python -m app.main
```

Try: `What should I do first when Microsoft Office has a problem?`

The app prints the retrieved chunks, their sources, and the generated answer. Type `exit` to quit, or press Ctrl+C or Ctrl+D. Each question is processed independently, without conversation memory. Run the indexing command again after changing files in `data/`; the index updates existing chunks and removes stale entries.

## Chunking strategy and model choices

The app uses **recursive character splitting**, trying paragraph breaks, line breaks, sentence boundaries, and spaces before splitting individual characters. Chunks contain at most **500 characters**, with up to **80 characters of overlap**. This strategy favors natural boundaries and helps keep related instructions together while limiting the amount of text passed to the model. Overlap carries some context between chunks, but is not guaranteed across recursive boundaries.

- **Embedding model:** Ollama `nomic-embed-text`, used for both chunks and questions. Inputs use `search_document:` and `search_query:` prefixes respectively.
- **Vector database:** ChromaDB in persistent mode, stored in `chroma_db/`. Retrieval uses cosine distance to select the top three chunks; smaller distances indicate closer matches.
- **Generation model:** Ollama `llama3.2`, with temperature set to 0. The prompt asks it to use only the retrieved excerpts, cite excerpt numbers, and say `I could not find this in your documents.` when the answer is unavailable. Answers and citations still need checking.

The offline flow is **load → split → embed → store**. At query time, the app **embeds the question → retrieves chunks → generates an answer**.

## Project files

All application modules are in `app/`:

| File | Responsibility |
| --- | --- |
| `ingestion.py` | Load text and Markdown files |
| `chunking.py` | Split text into overlapping chunks |
| `embeddings.py`, `ollama_client.py` | Request local embeddings and call Ollama |
| `vector_store.py` | Persist vectors and search the index |
| `retriever.py` | Embed questions and retrieve matching chunks |
| `generator.py` | Build the prompt and generate an answer |
| `pipeline.py` | Connect indexing and question-answering stages |
| `main.py` | Run indexing or the terminal chat loop |
| `config.py` | Define paths, model names, and chunking settings |
| `demo_ollama_check.py`, `demo_vector_check.py` | Check models and retrieval separately |
| `run_homework_tests.py` | Record five questions, retrieved chunks, and answers |

Defaults are in `app/config.py`. You can override `OLLAMA_URL`, `EMBED_MODEL`, and `GENERATION_MODEL` through environment variables. If changing the embedding model, select a new `DB_DIR` in the configuration and rebuild the index.

## Tests and reflection

[test_log.md](test_log.md) records five questions with their retrieved chunks and generated answers: four answerable questions and one unrelated question. [reflection.md](reflection.md) discusses what worked, a difficulty observed during testing, and a proposed re-ranking improvement.

To regenerate the log, first build the index and ensure Ollama is running, then run:

```bash
poetry run python -m app.run_homework_tests
```

Run the automated chunking, ingestion, and vector-store tests with:

```bash
poetry run python -m unittest discover -s tests
```
