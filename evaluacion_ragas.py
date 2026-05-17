import os
import sys
import pandas as pd
from tabulate import tabulate
from datasets import Dataset

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

import ragas
from ragas import RunConfig, evaluate
from ragas.metrics import faithfulness, answer_relevancy, context_precision
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

# --- 1. Configuración ---
load_dotenv()
API_KEY = os.getenv('GROQ_API_KEY')
if not API_KEY:
    print("[ERROR] GROQ_API_KEY no encontrada.")
    sys.exit(1)

# Configuramos LLM y Embeddings para LangChain
print("Inicializando modelos...")
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    groq_api_key=API_KEY,
    temperature=0.0,
    max_retries=5,
)

embeddings_local = HuggingFaceEmbeddings(
    model_name="all-MiniLM-L6-v2"
)

# --- 2. Cargar Documentos ---
print("Cargando PDFs desde la carpeta docs/ ...")
documentos = []
for file in os.listdir("docs"):
    if file.endswith(".pdf"):
        loader = PyPDFLoader(os.path.join("docs", file))
        documentos.extend(loader.load())

print(f"Dividiendo {len(documentos)} páginas en chunks...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
splits = text_splitter.split_documents(documentos)

# --- 3. Base Vectorial ---
print("Cargando ChromaDB desde el directorio ./chroma_db_ragas...")
vector_store = Chroma.from_documents(
    documents=splits,
    embedding=embeddings_local,
    persist_directory="./chroma_db_ragas"
)

# --- 4. Casos de Prueba ---
print("Definiendo preguntas de prueba...")
test_questions = [
    # A. La respuesta está textualmente
    "¿Cuál es el objetivo general o propósito principal de la asignatura de Desarrollo de Aplicaciones con IA según su programa?",
    "¿Cuál es la modalidad de enseñanza y el número de créditos académicos de la asignatura de Diseño de Interfaces?",
    # B. Vocabulario diferente
    "¿Qué conocimientos previos o materias debo tener aprobadas para poder matricular Bases de Datos II?",
    "¿Cuáles son los textos sugeridos o material de lectura recomendada para estudiar Ecuaciones Diferenciales?",
    # C. Combinar información
    "Compara las estrategias metodológicas de Nuevas Tecnologías de Desarrollo frente a Diseño de Interfaces. ¿Qué diferencias principales existen?",
    "Haz un resumen estructurado de las estrategias de evaluación para las materias de Redes de Comunicación I y Bases de Datos II.",
    # D. Alucinaciones
    "¿Cuál es el nombre, correo o número de contacto del monitor de la clase de Ecuaciones Diferenciales para tutorías extra?",
    "¿El profesor de Redes de Comunicación I aplica alguna sanción disciplinaria o baja puntos si se usa ChatGPT durante un examen presencial?"
]

# Definimos ground_truth básicos para Ragas (Context Precision lo requiere en algunas versiones)
ground_truths = [
    "El propósito principal de Desarrollo de Aplicaciones con IA es brindar al estudiante los conocimientos y habilidades necesarias para crear aplicaciones que integren Inteligencia Artificial.",
    "La asignatura de Diseño de Interfaces tiene una modalidad presencial y cuenta con 3 créditos académicos.",
    "Para matricular Bases de Datos II se requiere tener aprobada Bases de Datos I.",
    "Los textos sugeridos para Ecuaciones Diferenciales incluyen libros de texto clásicos sobre la materia como Zill o ecuaciones diferenciales aplicadas.",
    "En Nuevas Tecnologías de Desarrollo se enfocan en laboratorios prácticos y proyectos, mientras que en Diseño de Interfaces se enfatiza el diseño centrado en el usuario y talleres de prototipado.",
    "La evaluación de Redes de Comunicación I consta de tres cortes (30%, 30%, 40%) con exámenes teóricos y prácticos. Bases de Datos II también tiene tres cortes pero hace énfasis en proyectos de modelado.",
    "El documento de Ecuaciones Diferenciales no especifica el nombre, correo ni contacto del monitor para tutorías extra.",
    "El documento de Redes de Comunicación I no menciona sanciones específicas ni castigos por el uso de ChatGPT en exámenes."
]

# --- 5. Ejecutar RAG (Inferencia) ---
print("Recuperando contextos y generando respuestas...")
data_samples = {
    "question": [],
    "answer": [],
    "contexts": [],
    "ground_truth": []
}

retriever = vector_store.as_retriever(search_kwargs={"k": 4})

for i, q in enumerate(test_questions):
    print(f"  Procesando Q{i+1}...")
    # 1. Recuperar
    docs = retriever.invoke(q)
    contexts = [doc.page_content for doc in docs]

    # 2. Generar
    context_str = "\n---\n".join(contexts)
    prompt = f"Basado en el siguiente contexto, responde la pregunta. Si no sabes la respuesta, di que no se encuentra en el contexto.\n\nContexto:\n{context_str}\n\nPregunta:\n{q}"

    res = llm.invoke(prompt)
    answer = res.content

    data_samples["question"].append(q)
    data_samples["answer"].append(answer)
    data_samples["contexts"].append(contexts)
    data_samples["ground_truth"].append(ground_truths[i])

# --- 6. Evaluación con RAGAS ---
print("Iniciando evaluación RAGAS (esto puede tomar un minuto)...")
dataset = Dataset.from_dict(data_samples)

ragas_llm = LangchainLLMWrapper(llm)
ragas_emb = LangchainEmbeddingsWrapper(embeddings_local)

metrics = [faithfulness, answer_relevancy, context_precision]
run_config = RunConfig(timeout=120, max_retries=5, max_wait=60)
results = evaluate(
    dataset=dataset,
    metrics=metrics,
    llm=ragas_llm,
    embeddings=ragas_emb,
    run_config=run_config,
)

results_df = results.to_pandas()
print(f"  Columnas devueltas por RAGAS: {results_df.columns.tolist()}")

# RAGAS cambia los nombres de columna entre versiones: detectamos el alias correcto.
question_col = next((c for c in ['question', 'user_input'] if c in results_df.columns), None)
if question_col is None:
    print("[ERROR] No se encontró la columna de pregunta en los resultados de RAGAS.")
    sys.exit(1)

# --- 7. Generación de Tabla y Análisis ---
print("Generando análisis crítico...")

analisis_list = []
for index, row in results_df.iterrows():
    # Prompt al LLM para que haga el análisis crítico de cada fila
    prompt_analisis = f"""
    Evalúa críticamente el desempeño del RAG para una pregunta específica, dado sus métricas.

    Pregunta: {row[question_col]}
    Faithfulness (fidelidad): {row.get('faithfulness', 'N/A')}
    Answer Relevancy (relevancia): {row.get('answer_relevancy', 'N/A')}
    Context Precision (precisión del contexto): {row.get('context_precision', 'N/A')}

    Escribe un análisis crítico muy breve (1 a 2 oraciones) explicando qué significan estos resultados para esta pregunta.
    """

    res_analisis = llm.invoke(prompt_analisis)
    analisis_list.append(res_analisis.content.strip().replace('\n', ' '))

results_df['Análisis'] = analisis_list

# Limpiar dataframe para la tabla final (acceso defensivo: RAGAS puede cambiar nombres de columna entre versiones)
metric_cols = [c for c in ['faithfulness', 'answer_relevancy', 'context_precision'] if c in results_df.columns]
final_df = results_df[[question_col] + metric_cols + ['Análisis']]
final_df.columns = ['Pregunta'] + [c.replace('_', ' ').title() for c in metric_cols] + ['Análisis Crítico']

print("\n=== RESULTADOS DE EVALUACIÓN RAGAS ===")
table_str = tabulate(final_df, headers='keys', tablefmt='grid', showindex=False)
print(table_str)

with open('resultados_evaluacion.md', 'w', encoding='utf-8') as f:
    f.write("# Resultados de Evaluación RAGAS\n\n")
    f.write(final_df.to_markdown(index=False))

print("\n[OK] Script completado. Los resultados también se guardaron en 'resultados_evaluacion.md'")
