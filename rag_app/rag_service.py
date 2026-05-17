import json
import os
import re
import shutil
from functools import lru_cache
from pathlib import Path

from django.conf import settings
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}
EMBEDDING_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150

NON_CYBER_RESPONSE = (
    "Lo siento soy un modelo entrenado para resolver dudas concretas "
    "de documentos concretos de CIBERSEGURIDAD"
)
NO_CONTEXT_RESPONSE = "No encuentro esa información en el reglamento"

CYBER_KEYWORDS = {
    "ciber", "ciberseguridad", "seguridad", "malware", "phishing", "ransomware",
    "vulnerabilidad", "vulnerabilidades", "exploit", "intrusion", "intrusiones",
    "firewall", "vpn", "ddos", "botnet", "pentest", "pentesting", "siem",
    "ids", "ips", "forense", "cifrado", "encriptacion", "hash", "contraseña",
    "autenticacion", "amenaza", "amenazas", "riesgo", "mitigacion", "patch",
    "actualizacion", "incidente", "backdoor", "log", "logs",
}

SYSTEM_PROMPT = """
Eres un verificador estricto para un asistente RAG de ciberseguridad.
Debes seguir estas reglas de oro en este orden:

1) Determina si la MUESTRA_DOCUMENTO trata sobre ciberseguridad.
   Si no es claro o no hay evidencia, responde false.
2) Determina si la PREGUNTA es sobre ciberseguridad.
3) Determina si el CONTEXTO contiene la respuesta exacta.

Tu salida debe ser SOLO JSON valido, sin markdown ni texto extra, con estas claves exactas:
- doc_is_cybersecurity (boolean)
- question_is_cybersecurity (boolean)
- answer_in_context (boolean)
- answer (string)

Reglas de respuesta estrictas:
- Si doc_is_cybersecurity es false O question_is_cybersecurity es false, answer debe ser EXACTAMENTE:
  "Lo siento soy un modelo entrenado para resolver dudas concretas de documentos concretos de CIBERSEGURIDAD"
- Si answer_in_context es false, answer debe ser EXACTAMENTE:
  "No encuentro esa información en el reglamento"
- Si answer_in_context es true y las otras son true, answer debe ser breve, en espanol y basada SOLO en el CONTEXTO.

No inventes informacion ni agregues campos adicionales.
""".strip()

load_dotenv()


@lru_cache(maxsize=1)
def get_embeddings() -> HuggingFaceEmbeddings:
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)


def ensure_session_key(request) -> str:
    if not request.session.session_key:
        request.session.save()
    return request.session.session_key


def get_session_dir(session_key: str) -> Path:
    base_dir = Path(settings.MEDIA_ROOT) / "rag_sessions" / session_key
    base_dir.mkdir(parents=True, exist_ok=True)
    return base_dir


def save_uploaded_file(uploaded_file, session_dir: Path) -> Path:
    file_path = session_dir / uploaded_file.name
    with file_path.open("wb") as file_handle:
        for chunk in uploaded_file.chunks():
            file_handle.write(chunk)
    return file_path


def load_documents(file_path: Path):
    suffix = file_path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(file_path))
    elif suffix in {".txt", ".md"}:
        loader = TextLoader(str(file_path), encoding="utf-8")
    else:
        raise ValueError("Tipo de archivo no soportado.")
    return loader.load()


def load_documents_from_dir(docs_dir: Path):
    documents = []
    for file_path in docs_dir.rglob("*"):
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            documents.extend(load_documents(file_path))
    return documents


def split_documents(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
        length_function=len,
    )
    return splitter.split_documents(documents)


def build_vector_store(documents, session_dir: Path) -> tuple[Path, int]:
    chunks = split_documents(documents)
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)

    index_path = session_dir / "faiss_index"
    if index_path.exists():
        shutil.rmtree(index_path, ignore_errors=True)
    vector_store.save_local(str(index_path))
    return index_path, len(chunks)


def build_vector_store_in_memory(documents):
    chunks = split_documents(documents)
    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store, len(chunks)


def load_vector_store(index_path: Path) -> FAISS:
    embeddings = get_embeddings()
    return FAISS.load_local(
        str(index_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )


def retrieve_context(vector_store: FAISS, query: str, k: int = 4):
    docs = vector_store.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in docs])
    return context, docs


@lru_cache(maxsize=1)
def get_llm() -> ChatGroq:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("Falta la variable de entorno GROQ_API_KEY.")
    model_name = os.getenv("GROQ_MODEL", "llama3-8b-8192")
    return ChatGroq(
        model=model_name,
        temperature=0.2,
        max_tokens=700,
        groq_api_key=api_key,
    )


def generate_answer(question: str, context: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            (
                "human",
                "PREGUNTA: {question}\n\nMUESTRA_DOCUMENTO:\n{doc_hint}\n\nCONTEXTO:\n{context}",
            ),
        ]
    )
    chain = prompt | get_llm()
    response = chain.invoke({"question": question, "context": context, "doc_hint": context[:1200]})
    return response.content.strip()


def run_guarded_answer(question: str, context: str) -> tuple[str, dict]:
    raw = generate_answer(question, context)
    parsed = extract_json(raw)

    doc_is_cyber = bool(parsed.get("doc_is_cybersecurity"))
    question_is_cyber = bool(parsed.get("question_is_cybersecurity"))
    answer_in_context = bool(parsed.get("answer_in_context"))
    answer = str(parsed.get("answer", "")).strip()

    if not doc_is_cyber or not question_is_cyber:
        return NON_CYBER_RESPONSE, parsed

    if not answer_in_context:
        return NO_CONTEXT_RESPONSE, parsed

    return answer, parsed


def extract_json(payload: str) -> dict:
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", payload, re.DOTALL)
        if not match:
            raise
        return json.loads(match.group(0))
