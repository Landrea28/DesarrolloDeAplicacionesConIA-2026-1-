# Comparación de Modelos TF-IDF y BM25

Este proyecto analiza y compara los algoritmos de recuperación de información **TF-IDF** y **BM25**. El objetivo principal es evaluar su comportamiento ante distintos escenarios de búsqueda utilizando un corpus de documentos controlados, con el fin de entender el impacto de prácticas como el *keyword stuffing* y la influencia de la longitud del texto en la relevancia de los resultados.

---

## 1. Introducción

Contar la frecuencia de palabras no basta para medir la relevancia de un texto. El *keyword stuffing* (repetir palabras artificialmente) y los documentos excesivamente largos pueden alterar los rankings de búsqueda, desplazando textos cortos y precisos. Se requieren métricas más inteligentes que equilibren la frecuencia con el contexto y el tamaño del documento. Este proyecto compara cómo TF-IDF y su evolución, BM25, abordan este problema.

---

## 2. Glosario Técnico

*   **Recuperación de Información (IR):** Proceso de encontrar material que satisfaga una necesidad de información dentro de grandes colecciones.
*   **Corpus:** Conjunto o colección de documentos sobre los cuales se realizan las búsquedas.
*   **Tokenización:** Proceso de dividir un texto completo en unidades más pequeñas, como palabras individuales.
*   **Ranking:** Orden en el que se presentan los documentos, del más relevante al menos relevante.
*   **TF-IDF (Term Frequency - Inverse Document Frequency):** Algoritmo que evalúa la importancia de una palabra basándose en su frecuencia en el documento, penalizándola si es demasiado común en el corpus.
*   **BM25 (Best Matching 25):** Evolución de TF-IDF que incorpora límites matemáticos (saturación de términos) para evitar que la repetición excesiva sume puntos infinitamente, y penaliza los documentos innecesariamente largos.
*   **Keyword stuffing:** Práctica de manipular los resultados repitiendo excesivamente la misma palabra clave.

---

## 3. Tecnologías y Ejecución

*   **Python:** Lenguaje principal utilizado para la implementación de los algoritmos.

### Cómo ejecutar el proyecto:

1. Clona el repositorio y asegúrate de tener Python instalado.
2. (Opcional) Instala las dependencias necesarias. El proyecto utiliza `numpy` y `tabulate`:
   ```bash
   pip install numpy tabulate
   ```
3. Ejecuta el script principal:
   ```bash
   python comparacion_tfidf_bm25.py
   ```

El sistema cargará un corpus predefinido de documentos, calculará los puntajes para consultas de prueba (`inteligencia` y `algoritmo`) y mostrará en consola una tabla comparativa de los resultados de TF-IDF y BM25.

---

## 4. Metodología y Documentos de Prueba

En los documentos del proyecto se plantearon distintos escenarios para analizar el comportamiento de los algoritmos. Cada documento fue diseñado con una intención diferente:

*   **Documento A (Normal):** Texto normal que habla sobre inteligencia artificial de manera coherente y contextualizada.
*   **Documento B (Spam/Keyword Stuffing):** Repite muchas veces la palabra "inteligencia" sin desarrollar un tema, para demostrar cómo engañar al ranking.
*   **Documento C (Corto):** Documento corto y directo, cuyo tema principal son los algoritmos.
*   **Documento D (Largo):** Texto mucho más largo (aprox. 90 palabras), tangencial, que menciona "algoritmo" una sola vez.
*   **Documentos Extra:** Textos sin relación (cocina y clima) para estabilizar el cálculo del IDF y comprobar que no asignen relevancia fuera de contexto.

---

## 5. Resultados y Análisis

### Caso 1: Consulta "inteligencia" (Keyword Stuffing)

El Documento A desarrolla el tema coherentemente, obteniendo scores moderados. Sin embargo, el **Documento B** obtiene los puntajes más altos en ambos algoritmos debido a que repite excesivamente la palabra "inteligencia".
Aquí se evidencia el problema del *keyword stuffing*. No obstante, **BM25** intenta controlar parcialmente este problema mediante una saturación de frecuencia, por lo que su incremento de puntaje no es directamente proporcional a la cantidad de repeticiones sin límite, a diferencia de TF-IDF que es más vulnerable y directo.

### Caso 2: Consulta "algoritmo" (Penalización por Longitud)

El **Documento C** obtiene el mayor puntaje en ambos algoritmos.
El **Documento D** también menciona "algoritmo" pero en un texto mucho más extenso y diluido. 
Aquí BM25 muestra su mayor ventaja frente a TF-IDF: **BM25 penaliza la longitud del documento**. Un documento largo no obtiene automáticamente mayor relevancia solo por contener la palabra buscada. BM25 interpreta que el Documento C es más específico y directo, dándole clara ventaja sobre el Documento D, mientras que TF-IDF se guía más por el peso estadístico sin importar la longitud de todo el documento.

---

## 6. Evidencias

A continuación, se presentan las evidencias de ejecución del sistema que comprueban el correcto funcionamiento tanto de los algoritmos:

<figure>
    <img src="IMAGENES/consulta.png" alt="Ejecución y resultados obtenidos">
</figure>

---

## 7. Conclusiones

*   **TF-IDF** es sensible a la repetición directa de términos y altamente vulnerable al *keyword stuffing*.
*   **BM25** es más robusto al implementar la saturación de términos y la penalización por longitud, mitigando los engaños del *keyword stuffing* y valorando adecuadamente los documentos cortos y precisos.
*   Ambos métodos son estadísticos/léxicos (basados en frecuencias de aparición de palabras) y evidencian la limitación de no comprender realmente el significado del texto, siendo deseable apoyarlos con modelos semánticos en el futuro.

---

## 8. Autores

*   **Lina Andrea Bello Ballen** - *Ingeniería de Sistemas (2026)*.
