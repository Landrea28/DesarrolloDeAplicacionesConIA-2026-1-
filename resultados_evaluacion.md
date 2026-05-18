# Resultados de Evaluación RAGAS

_Generado el 2026-05-17 17:40_

**Modelo:** Llama 3.1 8B (Groq) · **Embeddings:** all-MiniLM-L6-v2 (HuggingFace)

---

## 📊 Promedios generales

| Faithfulness | Answer Relevancy | Context Precision |
|:---:|:---:|:---:|
| **nan** | **0.416** | **0.000** |

> Las métricas van de **0 a 1**. Más cercano a 1 = mejor desempeño.

---

## 📋 Resultados por pregunta

| # | Pregunta | Faithfulness | Answer Relevancy | Context Precision | Análisis Crítico |
|:---:|---|:---:|:---:|:---:|---|
| **Q1** | ¿Cuál es el objetivo general o propósito principal de la asignatura de Desarrollo de Aplicaciones con IA según su programa? | N/A | 0.907 | N/A | Basándome en los resultados, puedo decir que el modelo RAG ha demostrado una alta relevancia en su respuesta a la pregunta, con un valor de 0.9074648458977345. Esto sugiere que la respuesta proporcionada es muy relevante para la pregunta y probablemente esté bien enfocada en el objetivo principal de la asignatura de Desarrollo de Aplicaciones con IA. Sin embargo, la falta de información sobre la fidelidad (faithfulness) y la precisión del contexto (Context Precision) hace que sea difícil evaluar la exactitud y la precisión de la respuesta en general. |
| **Q2** | ¿Cuál es la modalidad de enseñanza y el número de créditos académicos de la asignatura de Diseño de Interfaces? | N/A | 0.755 | N/A | El desempeño del RAG (Ranking Aggregated Generator) para esta pregunta es moderadamente bueno, con una relevancia del 75.46%, lo que sugiere que el modelo ha identificado con precisión la información relevante relacionada con la modalidad de enseñanza y el número de créditos académicos de la asignatura de Diseño de Interfaces. Sin embargo, la falta de información sobre la fidelidad y la precisión del contexto sugiere que el modelo puede no haber capturado con precisión la respuesta exacta o la información contextual necesaria para responder la pregunta de manera completa. |
| **Q3** | ¿Qué conocimientos previos o materias debo tener aprobadas para poder matricular Bases de Datos II? | N/A | 0.000 | N/A | El desempeño del RAG (Recurrent Neural Network-based Answer Generator) para esta pregunta es deficiente, ya que presenta valores de "Faithfulness" y "Answer Relevancy" como "nan" (no disponible) y "0.0" respectivamente. Esto sugiere que el modelo no ha sido entrenado adecuadamente para responder a esta pregunta específica o que no tiene información relevante para proporcionar una respuesta precisa y fiable. |
| **Q4** | ¿Cuáles son los textos sugeridos o material de lectura recomendada para estudiar Ecuaciones Diferenciales? | N/A | N/A | N/A | Los resultados de las métricas del RAG (Retrieval-Augmented Generation) para esta pregunta son significativamente bajos, lo que sugiere que el modelo no ha encontrado información relevante o precisa para responder a la pregunta específica sobre textos sugeridos o material de lectura recomendado para estudiar Ecuaciones Diferenciales. Esto puede deberse a que la pregunta es muy específica o que el modelo no tiene acceso a información suficiente sobre el tema. |
| **Q5** | Compara las estrategias metodológicas de Nuevas Tecnologías de Desarrollo frente a Diseño de Interfaces. ¿Qué diferencias principales existen? | N/A | 0.000 | N/A | El desempeño del RAG (Ranking and Aggregation) para esta pregunta es deficiente, ya que presenta valores de "nan" (no disponible) para la fidelidad y precisión del contexto, lo que sugiere que el modelo no ha podido generar una respuesta coherente o relevante para la pregunta. Además, la relevancia de la respuesta es 0.0, lo que indica que el modelo no ha podido identificar ninguna relación entre la pregunta y la respuesta proporcionada. Esto sugiere que el modelo necesita mejorar su capacidad para comprender la pregunta y generar respuestas relevantes y precisas. |
| **Q6** | Haz un resumen estructurado de las estrategias de evaluación para las materias de Redes de Comunicación I y Bases de Datos II. | N/A | N/A | N/A | El desempeño del RAG (Ranking-AGgregation) para la pregunta específica de "Haz un resumen estructurado de las estrategias de evaluación para las materias de Redes de Comunicación I y Bases de Datos II" es inaceptable, ya que todas las métricas (fidelidad, relevancia y precisión del contexto) están marcadas como "nan" (no disponible). Esto sugiere que el modelo no ha podido generar una respuesta relevante o precisa para la pregunta, lo que puede deberse a una falta de entrenamiento o conocimiento en el tema específico. |
| **Q7** | ¿Cuál es el nombre, correo o número de contacto del monitor de la clase de Ecuaciones Diferenciales para tutorías extra? | N/A | N/A | N/A | El desempeño del RAG (Ranking Aggregator) para esta pregunta es deficiente, ya que las métricas de Faithfulness, Answer Relevancy y Context Precision son todas "nan", lo que indica que el modelo no ha proporcionado ninguna respuesta relevante o precisa para la pregunta. Esto sugiere que el modelo no tiene suficiente conocimiento o experiencia sobre la pregunta específica o que no ha sido entrenado adecuadamente para responder a preguntas de este tipo. |
| **Q8** | ¿El profesor de Redes de Comunicación I aplica alguna sanción disciplinaria o baja puntos si se usa ChatGPT durante un examen presencial? | N/A | N/A | 0.000 | Los resultados de las métricas del RAG (Ranking, Aggregation, Generation) para esta pregunta sugieren que la respuesta proporcionada no es relevante ni precisa en el contexto de la pregunta. La falta de valor en Faithfulness (fidelidad) y Answer Relevancy (relevancia) indica que la respuesta no se ajusta a la pregunta, mientras que la Context Precision (precisión del contexto) de 0.0 sugiere que la respuesta no tiene relación con el tema o contexto de la pregunta. Esto implica que la respuesta proporcionada no es confiable ni útil para responder a la pregunta. |

---

## 📖 Leyenda de métricas

| Métrica | Qué mide |
|---|---|
| **Faithfulness** | Fidelidad: la respuesta se basa estrictamente en el contexto. Cercano a 1 = sin alucinaciones. |
| **Answer Relevancy** | Relevancia: la respuesta realmente contesta lo que se preguntó. |
| **Context Precision** | Precisión del contexto: el retriever trajo los fragmentos correctos. |