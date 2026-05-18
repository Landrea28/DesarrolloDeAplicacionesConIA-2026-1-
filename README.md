# Asistente RAG de Ciberseguridad

**Un asistente inteligente interactivo impulsado por IA, diseñado para clasificar y responder dudas de ciberseguridad basándose en documentación local.**

---

## 1. Introducción

Este proyecto es un **Asistente de Ciberseguridad** por consola (CLI) que utiliza la arquitectura **RAG** (Retrieval-Augmented Generation). 
Resuelve el problema de buscar información en manuales extensos: en lugar de leer PDFs completos, el usuario hace una pregunta, el sistema busca los fragmentos más relevantes en los documentos locales y utiliza inteligencia artificial para generar una respuesta estructurada, precisa y basada **únicamente** en la documentación proporcionada.

---

## 2. Glosario Técnico

Si eres nuevo en el mundo de la Inteligencia Artificial o el desarrollo, aquí tienes los conceptos clave:

*   **RAG (Retrieval-Augmented Generation):** Técnica que mejora las respuestas de una IA dándole documentos específicos para que los lea antes de responder.
*   **LLM (Large Language Model):** El "cerebro" de la IA (en este caso, *Llama 3* de Groq) que entiende el texto y redacta respuestas.
*   **Vectorización / Embeddings:** Proceso de convertir palabras en números (coordenadas) para que la computadora pueda medir qué tan similares son dos textos.
*   **FAISS (Vector Database):** Una base de datos especial que guarda los números (embeddings) y permite búsquedas ultrarrápidas.
*   **API Key:** Una "contraseña" secreta que permite a tu aplicación conectarse a los servidores de Groq.
*   **Entorno Virtual (venv):** Una carpeta aislada donde se instalan las librerías del proyecto para no afectar al resto de tu computadora.

---

## 3. Tecnologías y Herramientas

### Tecnologías Principales
*   **Python:** Lenguaje de programación principal del proyecto.
*   **LangChain:** Framework (caja de herramientas) que orquesta todo: lee los PDFs, los corta y conecta la base de datos con la IA.
*   **Groq Cloud API:** Proveedor del LLM (`llama-3.3-70b-versatile`). Procesa las preguntas a velocidades ultrarrápidas usando chips LPU.
*   **HuggingFace Embeddings:** Modelo local (`all-MiniLM-L6-v2`) que convierte el texto en vectores sin necesidad de internet.
*   **FAISS:** Base de datos vectorial creada por Meta, que se guarda localmente en tu disco duro.

### Herramientas Recomendadas
Puedes usar cualquier herramienta de tu preferencia:
*   **Editor de código:** VS Code, Cursor, PyCharm o Bloc de Notas.
*   **Terminal:** PowerShell o CMD (Windows), Terminal nativa (macOS/Linux).

---

## 4. Estructura del Proyecto

```text
📁 ProyectoFinal/
├── 📄 _init_.py          # Archivo principal: Ejecuta el chat y conecta con la IA.
├── 📄 ingest.py          # Motor de indexación: Lee tus PDFs/MDs y crea la base de datos.
├── 📁 docs/              # Carpeta donde TÚ debes colocar tus manuales (.pdf, .md, .txt).
├── 📁 db/                # Se crea sola. Guarda la base de datos vectorial (FAISS).
├── 📄 requirements.txt   # Lista de dependencias (librerías) necesarias.
└── 📄 .env               # Archivo oculto (que debes crear) con tus claves secretas.
```

---

## 5. Requisitos Previos

Antes de empezar, asegúrate de tener:
1.  **Python 3.9 o superior:** [Descárgalo aquí](https://www.python.org/downloads/). (Al instalar en Windows, asegúrate de marcar la casilla *"Add Python to PATH"*).
2.  **Conexión a Internet:** Para descargar librerías y conectarse a Groq.
3.  **Cuenta en Groq:** (Totalmente gratuita, se explica en la sección 7).

---

## 6. Guía de Instalación y Ejecución (Paso a Paso)

No importa si no tienes experiencia, sigue estos pasos al pie de la letra.

### Paso 6.1: Abrir el proyecto en la terminal
1. Descarga el proyecto y extrae la carpeta.
2. Abre tu terminal (Busca "CMD" o "PowerShell" en Windows, o "Terminal" en macOS/Linux).
3. Navega hasta la carpeta del proyecto usando el comando `cd` (Change Directory).
   ```bash
   cd ruta/hacia/la/carpeta/del/proyecto
   ```

### Paso 6.2: Crear el Entorno Virtual
Esto creará una carpeta llamada `env` para aislar tu proyecto.

*   **En Windows, Linux y macOS:**
    ```bash
    python -m venv env
    ```
    *Resultado esperado: Una pausa de unos segundos y luego vuelve a aparecer la línea para escribir. Aparecerá una nueva carpeta `env/`.*

### Paso 6.3: Activar el Entorno Virtual
Debes "encender" el entorno virtual para instalar cosas dentro de él.

*   **En Windows (CMD):** `env\Scripts\activate.bat`
*   **En Windows (PowerShell):** `.\env\Scripts\Activate.ps1`
*   **En macOS / Linux:** `source env/bin/activate`

*Resultado esperado: Verás la palabra `(env)` al inicio de la línea de tu terminal.*

### Paso 6.4: Instalar las dependencias
Ahora descargaremos las herramientas de terceros necesarias (LangChain, Groq, FAISS, etc.).
```bash
pip install -r requirements.txt
```
*   **Qué hace:** Lee `requirements.txt` y descarga todo de internet.
*   **Resultado esperado:** Verás barras de carga. Tarda un par de minutos.

---

## 7. Configuración de Credenciales (Groq)

El proyecto necesita permiso para usar la IA de Groq.
1. Ve a [console.groq.com](https://console.groq.com) e inicia sesión.
2. En el menú, busca **"API Keys"** y haz clic en **"Create API Key"**.
3. Copia el texto largo que empieza por `gsk_...`
4. En la carpeta del proyecto, crea un archivo de texto y llámalo **exactamente** `.env` (asegúrate de que no se llame `.env.txt`).
5. Abre el archivo y pega esto (reemplazando tu clave):
   ```env
   GROQ_API_KEY=gsk_tu_clave_copiada_aqui_12345
   ```
6. Guarda y cierra el archivo.

---

## 8. Ejecución del Sistema

El proyecto funciona en dos fases distintas.

### Fase 1: Ingesta de Documentos (Crear el "Cerebro")
1. Coloca manuales, políticas de ciberseguridad o guías técnicas (archivos `.pdf`, `.txt` o `.md`) dentro de la carpeta `docs/`. Sin embargo ya hay unos de  base.
2. En tu terminal (con el entorno activado), ejecuta:
   ```bash
   python ingest.py
   ```
*   **Qué hace:** Lee tus documentos, los divide en pedazos pequeños, los "vectoriza" y los guarda en la carpeta `db/` usando FAISS. 
*   **Cuándo usarlo:** Solo la primera vez, o cuando agregues nuevos archivos a `docs/`.

### Fase 2: Ejecutar el Chat (Consultas)
1. En tu terminal ejecuta:
   ```bash
   python _init_.py
   ```
*   **Qué hace:** Inicia el asistente interactivo.
*   **Uso:** Simplemente escribe tu pregunta. El sistema buscará en la base de datos local `db/`, enviará el contexto a Groq, y te devolverá una respuesta en formato JSON puro.
*   **Para salir:** Escribe `salir`.

---

## 9. Arquitectura y Componentes Implementados (Detalle Técnico)

Para cumplir con el rigor de la ingeniería de software, el sistema se divide funcionalmente en los siguientes componentes implementados a nivel de código:

### A. Subsistema de Ingestión (`ingest.py`)
*   **Document Loaders (`PyPDFLoader` y `TextLoader`):** Módulos extraídos de `langchain_community` encargados de leer el sistema de archivos local (`docs/`) para extraer el texto plano tanto de binarios PDF como de archivos de texto (Markdown y TXT).
*   **Text Splitter (`RecursiveCharacterTextSplitter`):** Componente que toma los textos crudos y los divide en "chunks" (fragmentos) manejables de 1000 caracteres, aplicando un `chunk_overlap` (solapamiento) de 200 caracteres para asegurar que no se pierdan frases o contextos en el límite de un corte.
*   **Modelo de Embeddings (`HuggingFaceEmbeddings`):** Se instanció el modelo `all-MiniLM-L6-v2` el cual corre localmente en el procesador. Transforma los "chunks" de texto humano en vectores densos (coordenadas matemáticas en alta dimensionalidad) que representan su significado.
*   **Vector Store (`FAISS`):** El componente de base de datos (`FAISS.from_documents`). Almacena los vectores generados y los guarda persistentemente en disco (`vector_store.save_local`) dentro de la carpeta `db/`.

### B. Subsistema de Inferencia y Chat (`_init_.py`)
*   **Retriever (Recuperador `vector_store.similarity_search`):** Componente que evalúa matemáticamente la "distancia" entre el vector de la pregunta del usuario y los vectores de la base de datos local (FAISS), retornando los 3 fragmentos (k=3) más similares o relevantes al problema.
*   **Ingeniería de Prompts (Constructor Dinámico):** Un ensamblador estricto (`build_prompt`) que inyecta el `SYSTEM_PROMPT` (reglas, taxonomía temática y format JSON), los fragmentos recuperados (`context`), el historial de la conversación y la duda en turno. 
*   **Motor LLM (Cliente `Groq`):** Sustituye la computación local para ganar velocidad extrema (LPUs). Se utiliza el SDK oficial para enviar el prompt consolidado hacia el modelo `llama-3.3-70b-versatile` en la nube.
*   **Formateador de Salida Estructurada (`response_format`):** A nivel de API, el componente le exige a Groq devolver la clasificación estrictamente tipada: `{"type": "json_object"}`. Luego, el script intercepta el JSON bruto y lo presenta de manera legible en la consola mediante `json.dumps()`.

---

## 10. Reglas de Seguridad

*   **NUNCA** subas el archivo `.env` a internet, GitHub o foros públicos. Tu API Key es personal.
*   El archivo `.gitignore` ya está configurado para omitir las carpetas `env/` y `db/`, así como el `.env`. 

---

## 11. Errores Comunes y Soluciones

| Error Visualizado | Causa y Solución |
| :--- | :--- |
| `ModuleNotFoundError: No module named '...'` | Olvidaste activar el entorno virtual o instalar las dependencias (Paso 6.3 y 6.4). |
| `Error: La variable de entorno GROQ_API_KEY no esta configurada` | Te falta crear el archivo `.env` o escribiste mal el nombre de la variable (Paso 7). |
| `No se encontro la base de datos vectorial` | Intentaste iniciar el chat sin antes "ingestar" los documentos. Ejecuta `python ingest.py` primero. |
| `python no se reconoce como un comando` | Python no está instalado o no está en el PATH de Windows. Reinstala Python marcando "Add to PATH". |

---

## 12. Checklist de Soporte Rápido
Si algo no funciona, verifica esto en orden:
1. [ ] ¿Aparece `(env)` en la terminal? (Entorno activado).
2. [ ] ¿Está tu clave correctamente pegada en un archivo `.env`?
3. [ ] ¿Ejecutaste `python ingest.py` y se creó la carpeta `db/`?
4. [ ] ¿Tienes archivos dentro de `docs/`?

---

## 13. Evidencias

A continuación, se presentan las evidencias de ejecución del sistema que comprueban el correcto funcionamiento tanto de los algoritmos como de la indexación:

<figure>
    <img src="IMAGENES/consulta.png" alt="Ejecución y resultados obtenidos">
</figure>

### Mi retroalimentación
En los documentos del proyecto se plantearon distintos escenarios para analizar el comportamiento de los algoritmos TF-IDF y BM25 frente a consultas específicas. Cada documento fue diseñado con una intención diferente para evaluar cómo reaccionan ambos métodos ante casos como keyword stuffing, relevancia temática y longitud del contenido.

El **Documento A** es un texto normal que habla sobre inteligencia artificial de manera coherente y contextualizada. Aunque utiliza la palabra “inteligencia”, el término aparece de forma natural dentro del contenido.

El **Documento B** fue creado como un caso de *spam* o *keyword stuffing*. Básicamente repite muchas veces la palabra “inteligencia” sin desarrollar realmente un tema relacionado. El objetivo es demostrar cómo un documento puede aparentar relevancia únicamente por repetir constantemente la palabra clave.

El **Documento C** es un documento corto cuyo tema principal son los algoritmos. Aunque el texto es breve, está completamente enfocado en ese concepto.

El **Documento D** es un texto mucho más largo, aproximadamente de 90 palabras, relacionado principalmente con matemáticas. Sin embargo, menciona “algoritmo” una sola vez y utiliza términos relacionados con conteo y medición. Este documento se incluyó para evaluar si el modelo reconoce cierta relación semántica parcial, aun cuando el tema principal no son los algoritmos.

Finalmente, el **Documento Extra** habla sobre cocina italiana y clima ecuatorial, sin relación con inteligencia artificial, matemáticas o algoritmos. Este documento sirve como referencia irrelevante para estabilizar el cálculo del IDF y comprobar que los algoritmos no asignen relevancia a textos completamente fuera del contexto de búsqueda.

En la primera tabla, correspondiente a la consulta **“inteligencia”**, se puede observar un comportamiento importante. El Documento A, que realmente desarrolla el tema de inteligencia artificial de forma coherente, obtiene un score TF-IDF cercano a **0.12** y un score BM25 cercano a **0.28**.

Por otro lado, el Documento B obtiene valores mucho más altos: aproximadamente **0.44** en TF-IDF y **0.76** en BM25. A simple vista podría parecer el documento más relevante, pero en realidad esto ocurre porque repite excesivamente la palabra “inteligencia”. Es decir, ambos algoritmos están otorgando prioridad a la frecuencia del término dentro del documento.

Aquí se evidencia el problema del *keyword stuffing*: un texto puede recibir una puntuación alta no por ser útil o informativo, sino simplemente por repetir demasiadas veces la palabra consultada.

Sin embargo, BM25 y TF-IDF no funcionan exactamente igual. Aunque ambos favorecen al Documento B, BM25 intenta controlar parcialmente este problema mediante una saturación de frecuencia. Esto significa que repetir una palabra muchas veces deja de aumentar el score de forma proporcional después de cierto punto. TF-IDF, en cambio, es más sensible a la repetición directa del término, por lo que puede verse más afectado por documentos spam.

En la segunda tabla, correspondiente a la consulta **“algoritmo”**, el comportamiento cambia considerablemente.

Los Documentos A y B obtienen puntuaciones cercanas a cero porque no están relacionados con algoritmos. En cambio, el Documento C obtiene el mayor score tanto en TF-IDF como en BM25, ya que es el único cuyo tema principal son los algoritmos.

El Documento D también obtiene cierta relevancia, pero menor. Esto ocurre porque menciona el término “algoritmo” y además contiene vocabulario relacionado con matemáticas y procesos de cálculo. Aun así, el tema principal del documento no son los algoritmos, por lo que ambos modelos le asignan una puntuación inferior frente al Documento C.

Aquí es donde BM25 muestra una diferencia importante respecto a TF-IDF.

TF-IDF se basa principalmente en:

* frecuencia del término,
* frecuencia inversa en los documentos,
* y peso estadístico de la palabra.

Pero BM25 añade además una penalización por longitud del documento. Esto significa que un documento demasiado largo no obtiene automáticamente mayor relevancia solo por contener la palabra buscada.

Por esa razón, el Documento C —aunque es más corto— obtiene mejor puntuación que el Documento D. BM25 interpreta que el Documento C es más específico y directo respecto al tema “algoritmo”, mientras que el Documento D diluye el término dentro de mucho más contenido.

En otras palabras, BM25 favorece documentos más concretos y especializados, mientras que TF-IDF puede verse más influenciado por la frecuencia bruta de palabras.

En conclusión, las pruebas muestran que ambos métodos pueden detectar relevancia léxica, pero también evidencian limitaciones importantes. TF-IDF tiende a ser más vulnerable al *keyword stuffing*, mientras que BM25 mejora parcialmente este problema gracias a la normalización por longitud y la saturación de frecuencia. Aun así, ninguno de los dos comprende realmente el significado del texto; ambos trabajan principalmente con estadísticas de aparición de palabras.

---

## 14. Autores

*   **Lina Andrea Bello Ballen** - *Ingeniería de Sistemas (2026)*.
