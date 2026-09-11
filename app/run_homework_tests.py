"""Record actual retrieved excerpts and model answers for the five required questions."""
from datetime import datetime
from app.config import ROOT, EMBED_MODEL, GENERATION_MODEL
from app.pipeline import answer_question
from app.retriever import format_chunks
from app.vector_store import get_collection

QUESTIONS = [
    "How do I set up company email on a mobile device?",
    "What are the steps to reset a forgotten PIN?",
    "How do I configure VPN access for a remote worker?",
    "What should I do first when Microsoft Office has a problem?",
    "How do I make pancakes?",
]

if __name__ == "__main__":
    collection = get_collection()
    lines = ["# Homework test log", f"\nRun: {datetime.now().astimezone().isoformat()}",
             f"\nGeneration: {GENERATION_MODEL}; embeddings: {EMBED_MODEL}; top-k: 3.",
             "\nQuestions 1-4 are answerable; question 5 is outside the documents."]
    for number, question in enumerate(QUESTIONS, 1):
        answer, chunks = answer_question(question, collection)
        lines.extend([f"\n## Question {number}\n\n{question}",
                      f"\n### Retrieved chunks\n\n```text\n{format_chunks(chunks)}\n```",
                      f"\n### Generated answer\n\n{answer}"])
        print(f"{number}. {question}\n{answer}\n", flush=True)
    (ROOT / "test_log.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
