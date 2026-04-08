# tf-idf
import numpy as np

documents = [
    "the cat in the hat",
    "the cat sat on the mat",
    "the dog in the yard"
]   
# termino de buscvar
termino_buscado = "cat"
# total de documentos
N= len(documents)

#clcular idf
df = sum(1 for doc in documents if termino_buscado in doc) # contar en cuántos documentos aparece el término
idf = np.log(N / (df + 1))  # agregar 1 para evitar división por cero

print(f"IDF para el término '{termino_buscado}': {idf:.4f }") #:.4f para mostrar con 4 decimales

# calcular tf-idf para cada documento
scores = []
for i, doc in enumerate(documents):
    tf = doc.count(termino_buscado) / len(doc.split())  # frecuencia del término en el documento
    tf_idf = tf * idf
    scores.append((i+1, tf_idf, doc))  # almacenar el índice del documento, el puntaje tf-idf y el documento
    
    scores.sort(key=lambda x: x[1], reverse=True)  # ordenar por puntaje tf-idf de mayor a menor

#mostrar resultados
for i, (doc_id, tf_idf, doc) in enumerate(scores, 1):
    print(f"{i} - Documento {doc_id}: TF-IDF = {tf_idf:.4f} - '{doc}'")
