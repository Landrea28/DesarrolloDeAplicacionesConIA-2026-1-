import csv
import json
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT_DIR))

from rag_app import rag_service


def load_questions(file_path: Path) -> list[str]:
    with file_path.open("r", encoding="utf-8") as handle:
        questions = []
        for line in handle.readlines():
            cleaned = line.strip()
            if not cleaned or cleaned.startswith("#"):
                continue
            questions.append(cleaned)
        return questions


def evaluate_questions(questions: list[str], docs_dir: Path) -> list[dict]:
    documents = rag_service.load_documents_from_dir(docs_dir)
    if not documents:
        raise RuntimeError("No se encontraron documentos en la carpeta indicada.")

    vector_store, chunk_count = rag_service.build_vector_store_in_memory(documents)
    results = []

    for question in questions:
        context, docs = rag_service.retrieve_context(vector_store, question)
        answer, meta = rag_service.run_guarded_answer(question, context)
        source = docs[0].page_content if docs else ""
        results.append(
            {
                "question": question,
                "answer": answer,
                "doc_is_cybersecurity": meta.get("doc_is_cybersecurity"),
                "question_is_cybersecurity": meta.get("question_is_cybersecurity"),
                "answer_in_context": meta.get("answer_in_context"),
                "source": source,
                "chunks_indexed": chunk_count,
            }
        )
    return results


def write_outputs(results: list[dict], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "rubric_results.json"
    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(results, handle, ensure_ascii=False, indent=2)

    csv_path = output_dir / "rubric_results.csv"
    fieldnames = [
        "question",
        "answer",
        "doc_is_cybersecurity",
        "question_is_cybersecurity",
        "answer_in_context",
        "chunks_indexed",
        "source",
    ]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)


def main() -> None:
    docs_dir = Path(os.getenv("RUBRIC_DOCS_DIR", "docs"))
    questions_path = Path(os.getenv("RUBRIC_QUESTIONS_FILE", "docs/rubric_questions.txt"))

    if not questions_path.exists():
        raise FileNotFoundError(
            "No se encontro rubric_questions.txt. Coloca alli las 10 preguntas de la rubrica."
        )

    questions = load_questions(questions_path)
    if len(questions) < 10:
        raise RuntimeError("Se requieren al menos 10 preguntas en rubric_questions.txt.")

    results = evaluate_questions(questions, docs_dir)
    write_outputs(results, Path("reports"))
    print("Evaluacion completada. Resultados en reports/.")


if __name__ == "__main__":
    main()
