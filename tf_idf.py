# tf-idf
import numpy as np

documents = [
    "ARTÍCULO 3: El número de créditos de cada asignatura es determinado por el Consejo Académico, previo estudio del Comité de Currículo del Programa.",
    "ARTÍCULO 4: El número de créditos académicos de una actividad circunscrita en el plan de estudios será aquel que resulte de dividir por 48 el número total de horas que deba emplear el estudiante para cumplir satisfactoriamente los resultados del aprendizaje.",
    "ARTÍCULO 5: La Institución, dentro de su autonomía y de acuerdo con la naturaleza del programa, distinguirá entre créditos académicos obligatorios y electivos. Cra 9 Bis No. 62.43 PBX - (571) 347 2311 - F. (571) 347 2311 ext. 131 Bogotá D.C., Colombia juridico@konradlorenz.edu.co - www.konradlorenz.edu.co",
    "ARTÍCULO 6: El Consejo Académico podrá adoptar diferentes períodos calendario (bimestre, trimestre, semestre, anualidad u otro) para el desarrollo de los programas académicos.",
    "ARTÍCULO 7: Cada período académico tendrá una duración definida en semanas, conforme lo reglamente el Consejo Académico, teniendo en cuenta las características de los planes de estudio de los programas académicos, las resoluciones de registro calificado asociadas a cada uno de estos y la normativa nacional vigente. PARÁGRAFO: La hora académica con acompañamiento directo del docente (sincrónico presencial y/o remoto, según el caso) tiene una duración de 45 minutos efectivos, sin que ello impida la programación de bloques de dos o más horas continuas académicas, dependiendo de la naturaleza de la asignatura o espacio formativo (por ejemplo, en el caso de las prácticas profesionales).",
    "ARTÍCULO 13: Los aspirantes que no sean admitidos o que habiéndolo sido no se matriculen, así como aquellos que se retiren definitivamente, pueden retirar sus documentos en el Departamento de Registro Académico, previa solicitud escrita.",
    "ARTÍCULO 14: El Consejo Académico fija los criterios de selección para las diferentes carreras y determina el conjunto de las pruebas internas y demás procedimientos de selección. PARÁGRAFO: Para el primer período académico del programa correspondiente, el Director de Programa selecciona a los aspirantes que obtengan los mayores puntajes, dentro del límite de cupos fijados por el Consejo Académico y de acuerdo con las políticas establecidas por el Consejo Superior.",
    "ARTÍCULO 15: Una vez culminado el proceso de admisión, el Departamento de Promoción y Divulgación informa los resultados del proceso al aspirante.",
    "ARTÍCULO 18: Los aspirantes extranjeros están sujetos a los mismos requisitos de inscripción y matrícula exigidos para los aspirantes colombianos, de acuerdo con las leyes vigentes. CAPÍTULO IV DE LAS TRANSFERENCIAS",
    "ARTÍCULO 19: Se entiende por transferente al aspirante que, habiendo cursado estudios superiores en otra institución debidamente reconocida por el Estado, es aceptado como estudiante regular en uno de los programas académicos de la Institución."
]   

# Consultas de ejemplo (descomentar la que se desee probar):
consulta = "créditos académicos obligatorios y electivos"
#consulta = "duración del período académico en semanas"
#consulta = "requisitos de inscripción para aspirantes extranjeros"
palabras_consulta = consulta.replace(',', '').lower().split()

# total de documentos
N = len(documents)

# calcular tf-idf para cada documento sumando los scores de cada palabra
scores = []
for i, doc in enumerate(documents):
    # Limpiamos el documento para contar palabras correctamente (sin comas ni dos puntos)
    palabras_doc = doc.replace(',', '').replace('.', '').replace(':', '').lower().split()
    total_palabras_doc = len(palabras_doc)
    
    score_final = 0
    for palabra in palabras_consulta:
        # Calcular TF: frecuencia_palabra / total_palabras_doc
        frecuencia_palabra = palabras_doc.count(palabra)
        tf = frecuencia_palabra / total_palabras_doc if total_palabras_doc > 0 else 0
        
        # Calcular IDF: log(Total_Docs / Docs_con_la_palabra)
        # Contamos en cuántos documentos aparece exactamente la palabra
        docs_con_la_palabra = sum(1 for d in documents if palabra in d.replace(',', '').replace('.', '').replace(':', '').lower().split())
        idf = np.log(N / docs_con_la_palabra) if docs_con_la_palabra > 0 else 0
        
        # Calcular Score Final: Sumar el TF-IDF de cada palabra de la consulta
        score_final += tf * idf
        
    # almacenar el índice del documento, el puntaje final calculado y el documento original
    scores.append((i+1, score_final, doc))  

# ordenar por puntaje acumulado de mayor a menor
scores.sort(key=lambda x: x[1], reverse=True)  

#mostrar resultados
print(f"Consulta: '{consulta}'\n")
for i, (doc_id, score_final, doc) in enumerate(scores, 1):
    print(f"{i} - Documento {doc_id}: Score = {score_final:.4f} - '{doc}'")
