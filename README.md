# 🪸 RECUERDE QUE ESTA EN LA RAMA "RAG"
  Para ir a la rama main: https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-.git
# Evaluación de Pipeline RAG con RAGAS y Gemini

Este proyecto implementa y evalúa el desempeño de un pipeline RAG (Retrieval-Augmented Generation) utilizando documentos PDF (programas de asignatura). Se hace uso de **LangChain** para la orquestación, **HuggingFace** para la generación de embeddings locales, **ChromaDB** como base de datos vectorial y el modelo **Gemini** de Google como LLM. Finalmente, la evaluación de las respuestas se realiza con el framework **RAGAS**.

---

## 🚀 Guía de Instalación y Ejecución

Si tienes el enlace de este repositorio en GitHub, sigue estos pasos cuidadosamente para ejecutar el proyecto en tu máquina local.

### Paso 1: Clonar el repositorio y acceder a la rama correcta
Este repositorio está dividido por ramas (branches) para cada proyecto o actividad. Este proyecto específico se encuentra en la rama **`RAG`**.

1. Ve al repositorio en GitHub, haz clic en el botón verde que dice **`<> Code`** y copia la URL HTTPS.
2. Abre una terminal en tu computadora y ejecuta el siguiente comando para clonar directamente la rama `RAG`:
   ```bash
   git clone -b RAG <URL_DEL_REPOSITORIO>
   ```
   *(Reemplaza `<URL_DEL_REPOSITORIO>` con el enlace que copiaste).*

### Paso 2: Abrir el proyecto en Visual Studio Code
Navega hacia la carpeta del proyecto que acabas de clonar y ábrela en VS Code:
```bash
cd <NOMBRE_DE_LA_CARPETA>
code .
```

### Paso 3: Crear y activar un entorno virtual
Para no generar conflictos con otras versiones de Python en tu computadora, es crucial aislar las librerías en un entorno virtual. Abre la terminal integrada de VS Code (`Ctrl + ñ` o `Cmd + J`) y ejecuta:

**Crear el entorno virtual:**
```bash
python -m venv env
```

**Activar el entorno virtual:**
- En **Windows**:
  ```bash
  .\env\Scripts\activate
  ```
- En **Mac/Linux**:
  ```bash
  source env/bin/activate
  ```
*(Sabrás que funcionó porque aparecerá `(env)` al inicio de tu línea de comandos en la terminal).*

### Paso 4: Instalar las dependencias
Con el entorno virtual activado, debes instalar todas las librerías necesarias. Copia y pega este comando completo (es bastante largo para asegurar que todo el entorno funcione a la perfección):

```bash
pip install pandas datasets tabulate ragas langchain-google-genai langchain-huggingface langchain-chroma pypdf python-dotenv sentence-transformers
```

### Paso 5: Configurar la variable de entorno
Este proyecto utiliza la API de Google Gemini, por lo que necesitas tu propia clave de acceso.
1. En la raíz del proyecto (al mismo nivel que la carpeta `docs` y el script), crea un archivo llamado **`.env`**.
2. Ábrelo y escribe tu clave de Google de la siguiente manera:
   ```env
   GOOGLE_API_KEY="AQUI_VA_TU_API_KEY_DE_GOOGLE"
   ```

### Paso 6: Ejecutar el proyecto
Una vez esté todo configurado y las librerías instaladas, ejecuta el script principal de evaluación:

```bash
python -u evaluacion_ragas.py
```
*(Nota: El uso del flag `-u` sirve para mostrar el progreso en tiempo real en consola, dado que el script realiza pausas estratégicas para no agotar la capa gratuita de la API de Gemini).*

Al finalizar, el proyecto te mostrará una tabla en la terminal y generará un archivo `resultados_evaluacion.md` con los análisis y métricas detalladas.

---

## 🧠 Tecnologías y Componentes del Proyecto

Para entender lo que sucede detrás de este código, aquí tienes una explicación de las tecnologías y conceptos clave implementados:

*   **RAG (Retrieval-Augmented Generation):** Es una arquitectura que mejora a los modelos de lenguaje (LLMs) conectándolos con bases de conocimiento externas. En lugar de que el LLM responda solo con lo que "recuerda" de su entrenamiento, RAG primero **recupera** fragmentos de documentos relevantes (los PDFs de las asignaturas) y luego usa esa información exacta como contexto para **generar** una respuesta precisa, reduciendo drásticamente las "alucinaciones" (respuestas inventadas).
*   **LangChain:** Es un framework diseñado para simplificar la creación de aplicaciones impulsadas por LLMs. Actúa como el "pegamento" que conecta nuestros PDFs (mediante el `PyPDFLoader`), el segmentador de texto (`RecursiveCharacterTextSplitter`), la base de datos vectorial y el modelo generativo en un flujo de trabajo unificado.
*   **Embeddings de HuggingFace (`all-MiniLM-L6-v2`):** Los embeddings son representaciones numéricas (vectores) del texto. Este proyecto utiliza un modelo ligero, rápido y local provisto por la comunidad de HuggingFace para convertir los fragmentos de los PDFs en vectores de números sin depender de APIs de pago, optimizando así los recursos.
*   **ChromaDB:** Es una base de datos vectorial local. Su función es almacenar los vectores generados por el modelo de embeddings. Cuando hacemos una pregunta, ChromaDB busca qué fragmentos de texto (vectores almacenados) están matemáticamente más "cerca" de la pregunta y se los devuelve al LLM.
*   **Google Gemini (ChatGoogleGenerativeAI):** Es el Motor Generativo (LLM) que recibe la pregunta del usuario junto con el contexto recuperado de ChromaDB, para leer la información y redactar una respuesta fluida y coherente.
*   **RAGAS (RAG Assessment):** Es el corazón de este archivo de evaluación. Es un framework diseñado para evaluar objetivamente aplicaciones RAG sin necesidad de supervisión humana (LLM-as-a-judge). En este proyecto evaluamos tres métricas principales:
    *   *Faithfulness (Fidelidad):* Mide si la respuesta generada se deriva estrictamente del contexto dado y no tiene información inventada.
    *   *Answer Relevancy (Relevancia):* Evalúa si la respuesta realmente contesta lo que el usuario preguntó, sin desvíos o información redundante.
    *   *Context Precision (Precisión del Contexto):* Analiza si el retriever (ChromaDB) fue capaz de traer los fragmentos correctos de los PDFs al principio de la búsqueda.

---

## 👩‍💻 Autor

*   **Nombre:** Lina Andrea Bello Ballen
*   **Código:** 506241153
*   **Fecha de creación:** 07 de marzo de 2026
*   **Asignatura:** Desarrollo de Aplicaciones con IA