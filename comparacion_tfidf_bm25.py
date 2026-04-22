import re
import numpy as np
from tabulate import tabulate

# Corpus de 6 documentos
docs = [
    # Documento A (Normal): Uso natural de "inteligencia"
    "La inteligencia artificial es una rama de la informática. Sistemas de inteligencia avanzada buscan emular el razonamiento humano.",
    
    # Documento B (Keyword Stuffing): Repetición abusiva de "inteligencia"
    "Inteligencia, inteligencia, inteligencia. La inteligencia artificial necesita mucha inteligencia. Todo es inteligencia y pura inteligencia, sin inteligencia no hay nada.",
    
    # Documento C (Corto y directo): Uso de "algoritmo" 1 vez, al grano
    "Un algoritmo es un conjunto ordenado de instrucciones finitas para resolver un problema de forma precisa.",
    
    # Documento D (Largo y tangencial): 90 palabras, usa "algoritmo" 1 sola vez perdida en el texto
    "La historia de las matemáticas es vasta y muy compleja. Desde tiempos antiguos, los humanos desarrollaron muchas herramientas distintas para contar, medir y lograr comprender mejor las leyes del universo. En la edad media, estudiosos preservaron manuscritos clásicos invaluables. Dentro de la resolución de ciertas ecuaciones algebraicas extremadamente complejas, a veces se puede emplear un algoritmo de aproximación sucesiva. Sin embargo, la mayor parte del conocimiento matemático clásico se centra más bien en demostraciones formales, postulados lógicos y teoremas abstractos que trascienden el mero cálculo rutinario de datos numéricos diarios.",
    
    # --- Documentos Extra para estabilizar el cálculo IDF de BM25 ---
    "La cocina italiana moderna es conocida por su uso de ingredientes frescos como el tomate, el aceite de oliva y la albahaca. Las recetas se transmiten de generación en generación.",
    "El clima en la zona ecuatorial se caracteriza por altas temperaturas y lluvias constantes durante todo el año, lo que favorece el crecimiento de selvas tropicales densas y biodiversas."
]

nombres_docs = ["Doc A (Normal)", "Doc B (Spam/Stuffing)", "Doc C (Corto)", "Doc D (Largo)", "Doc Extra 1", "Doc Extra 2"]

def limpiar_texto(texto: str) -> str:
    # Convertimos a minúsculas y eliminamos signos de puntuación para que el .split() funcione perfecto
    texto = texto.lower()
    return re.sub(r'[^\w\s]', '', texto)

# Aplicar limpieza al corpus para el procesamiento
docs_limpios = [limpiar_texto(doc) for doc in docs]

# =====================================================================
# FUNCIONES PROPORCIONADAS
# =====================================================================

def calculo_idf(termino_buscado: str, documentos: list) -> float:
    N = len(documentos) # Número total de documentos
    df = sum(1 for doc in documentos if termino_buscado in doc.split())
    idf = np.log(N / df) if df > 0 else 0
    return idf

def calculo_tf(termino_buscado: str, documento: str) -> float:
    palabras = documento.split()
    if not palabras: return 0
    return palabras.count(termino_buscado) / len(palabras)

def calculo_tf_idf(termino_buscado: str, documento: str, idf: float) -> float:
    tf = calculo_tf(termino_buscado, documento)
    return tf * idf

def promedio_documentos(documentos: list) -> float:
    total_palabras = sum(len(doc.split()) for doc in documentos)
    return total_palabras / len(documentos) if documentos else 0

def calcular_BM25(termino_buscado: str, documento: str, idf: float, avg_doc_length: float, k1=1.5, b=0.75) -> float:
    tf = calculo_tf(termino_buscado, documento)
    doc_length = len(documento.split())
    if doc_length == 0: return 0
    bm25_score = idf * ((tf * (k1 + 1)) / (tf + k1 * (1 - b + b * (doc_length / avg_doc_length))))
    return bm25_score


# =====================================================================
# EJECUCIÓN
# =====================================================================

def calcular_y_mostrar(query, descripcion):
    print(f"\n{'='*70}")
    print(f"CONSULTA: '{query}' ({descripcion})")
    print(f"{'='*70}")
    
    query = limpiar_texto(query).strip()
    avg_dl = promedio_documentos(docs_limpios)
    
    resultados = []
    
    for i, doc in enumerate(docs_limpios):
        score_tfidf_total = 0
        score_bm25_total = 0
        
        # Soportar múltiples palabras en la consulta
        for termino in query.split():
            idf = calculo_idf(termino, docs_limpios)
            score_tfidf_total += calculo_tf_idf(termino, doc, idf)
            score_bm25_total += calcular_BM25(termino, doc, idf, avg_doc_length=avg_dl)
            
        resultados.append([
            nombres_docs[i],
            round(score_tfidf_total, 4),
            round(score_bm25_total, 4)
        ])
        
    print(tabulate(resultados, headers=["Documento", "Score TF-IDF", "Score BM25"], tablefmt="grid"))

if __name__ == "__main__":
    print("\n--- COMPARACIÓN TF-IDF vs BM25 (Custom Implementation) ---")
    calcular_y_mostrar("inteligencia", "Punto 1: TF-IDF vs BM25 debido a 'Keyword Stuffing'")
    calcular_y_mostrar("algoritmo", "Punto 2: BM25 vs TF-IDF debido a 'Penalización por Longitud'")
