# 🛡️ Asistente RAG de Ciberseguridad

**Un asistente inteligente interactivo impulsado por IA, diseñado para clasificar y responder dudas de ciberseguridad basándose exclusivamente en documentación local y privada.**

---

## 🚀 1. Guía Rápida de Ejecución

El sistema opera en **dos fases obligatorias**. Es fundamental realizar la Fase 1 al menos una vez antes de poder iniciar el asistente interactivo (Fase 2).

### Fase 1: Ingesta de Documentos (Alimentar la IA)
Este paso convierte tus PDFs y manuales de la carpeta `docs/` en una base de datos matemática local.

1.  Abre tu terminal en la raíz del proyecto.
2.  Asegúrate de que el entorno virtual esté activado (`(env)` visible).
3.  Ejecuta el siguiente comando:
    ```bash
    python ingest.py
    ```
> **💡 ¿Cuándo usar este comando?:** Solo debes ejecutarlo la primera vez que configuras el proyecto o cada vez que añadas, elimines o modifiques un archivo dentro de la carpeta `docs/`.

### Fase 2: Conversar con el Asistente
Este comando inicia la consola interactiva donde puedes interactuar con el asistente para resolver tus dudas.

1.  En la misma terminal (con el entorno activado), ejecuta:
    ```bash
    python _init_.py
    ```
2.  Escribe tu consulta cuando aparezca el mensaje `Tu consulta:`. El sistema te devolverá un formato JSON estructurado basado en los documentos leídos.
3.  Para salir, simplemente escribe la palabra `salir`.

> **💡 ¿Cuándo usar este comando?:** Siempre que quieras encender el chat interactivo para buscar ayuda o consultar la documentación.

---

## 2. Introducción

Este proyecto es un **Asistente de Ciberseguridad** por consola (CLI) que utiliza la arquitectura **RAG** (Retrieval-Augmented Generation). 
Resuelve el problema de buscar información de mitigación en manuales extensos: en lugar de leer PDFs completos o depender de la memoria inestable de una IA general, el sistema busca los fragmentos relevantes en los documentos locales y utiliza inteligencia artificial para generar una respuesta estructurada, rápida y sin inventar datos (sin "alucinar").

---

## 3. Requisitos Previos

Antes de proceder con la instalación técnica, asegúrate de contar con lo siguiente en tu sistema:
1.  **Python 3.9 o superior:** [Instalador oficial de Python](https://www.python.org/downloads/). (Durante la instalación en Windows, marca la casilla obligatoria *"Add Python to PATH"*).
2.  **Conexión a Internet:** Para descargar los modelos y conectarse a la API de Groq.
3.  **Cuenta en Groq:** Totalmente gratuita, necesaria para obtener las credenciales del modelo LLM.

---

## 4. Estructura del Proyecto

El repositorio está organizado funcionalmente de la siguiente manera:

```text
📁 ProyectoFinal/
├── 📄 _init_.py          # [FASE 2] Archivo principal interactivo (Chat LLM).
├── 📄 ingest.py          # [FASE 1] Motor de indexación vectorial (Lectura de documentos).
├── 📁 docs/              # Carpeta para colocar manuales y normativas (.pdf, .md, .txt).
├── 📁 db/                # (Autogenerada) Almacena la base de datos vectorial local.
├── 📄 requirements.txt   # Listado estricto de dependencias de Python.
└── 📄 .env               # Archivo de configuración (creado por ti) para la API Key.
```

---

## 5. Instalación del Entorno Local

Sigue estrictamente estos pasos si es la primera vez que configuras el proyecto.

### 5.1 Crear y activar el Entorno Virtual
Para no causar conflictos con otras librerías en tu sistema operativo, aislaremos el proyecto en un entorno virtual.

*   **Creación del entorno (Windows / macOS / Linux):**
    ```bash
    python -m venv env
    ```

*   **Activación en Windows (CMD):**
    ```cmd
    env\Scripts\activate.bat
    ```
*   **Activación en Windows (PowerShell):**
    ```powershell
    .\env\Scripts\Activate.ps1
    ```
*   **Activación en macOS / Linux:**
    ```bash
    source env/bin/activate
    ```
> Si funcionó correctamente, verás un prefijo `(env)` al inicio de la línea de tu terminal.

### 5.2 Instalar las Dependencias
Con el entorno `(env)` encendido, procede a instalar los componentes del sistema (LangChain, FAISS, Embeddings, Groq, etc.):
```bash
pip install -r requirements.txt
```

---

## 6. Configuración de Credenciales de IA

El proyecto utiliza un LLM avanzado en la nube (Llama 3 de Groq) que requiere autorización.

1. Regístrate o inicia sesión en [console.groq.com](https://console.groq.com).
2. Dirígete a la sección de **"API Keys"** y genera una clave nueva. Cópiala (empezará con `gsk_`).
3. En la raíz de la carpeta del proyecto, crea un archivo que se llame **exactamente** `.env`.
4. Ábrelo con el bloc de notas y añade tu clave con el siguiente formato:
   ```env
   GROQ_API_KEY=gsk_tu_clave_super_secreta_pegada_aqui
   ```
5. Guarda el archivo. *Nota: Este archivo está ignorado por Git, por lo que nunca se subirá a repositorios públicos.*

---

## 7. Arquitectura y Componentes Implementados (Detalle Técnico)

A nivel de ingeniería de software, el sistema se divide funcionalmente en los siguientes componentes:

### A. Subsistema de Ingestión (`ingest.py`)
*   **Document Loaders (`PyPDFLoader` y `TextLoader`):** Módulos extraídos de `langchain_community` encargados de leer el sistema de archivos local (`docs/`) para extraer el texto plano de manuales y documentos.
*   **Text Splitter (`RecursiveCharacterTextSplitter`):** Componente que toma los textos crudos y los divide en "chunks" (fragmentos) manejables de 1000 caracteres, aplicando un `chunk_overlap` de 200 caracteres para asegurar que no se pierdan frases en el límite de un corte.
*   **Modelo de Embeddings (`HuggingFaceEmbeddings`):** Instancia local del modelo neuronal `all-MiniLM-L6-v2`. Transforma cada fragmento de texto humano en un vector denso (coordenadas matemáticas).
*   **Vector Store (`FAISS`):** Base de datos optimizada de Meta (`FAISS.from_documents`). Almacena los vectores generados y los persiste localmente en disco (`vector_store.save_local`) en la ruta `db/`.

### B. Subsistema de Inferencia y Chat (`_init_.py`)
*   **Retriever (Búsqueda Vectorial):** Componente que evalúa matemáticamente la "distancia" entre el vector de la pregunta del usuario y los guardados en FAISS, retornando de inmediato los 3 fragmentos (k=3) más relevantes.
*   **Ensamblador de Prompts:** Constructor dinámico que inyecta el `SYSTEM_PROMPT` estricto, los fragmentos recuperados localmente (`context`), la memoria de corto plazo y la duda del analista. 
*   **Motor LLM (Cliente SDK `Groq`):** Delega la inferencia computacional a LPUs en la nube para ganar velocidad extrema utilizando el modelo `llama-3.3-70b-versatile`.
*   **Salida Tipada (`response_format`):** Regla impuesta al cliente para interceptar un JSON puro: `{"type": "json_object"}`. El script finalmente parsea este JSON y lo presenta al analista.

---

## 8. Errores Comunes (Troubleshooting)

Si algo falla, verifica la siguiente tabla:

| Problema o Error | Causa y Solución Comprobada |
| :--- | :--- |
| `ModuleNotFoundError` o comando no existe | Olvidaste encender el entorno virtual (Paso 5.1) o instalar los requerimientos (Paso 5.2). |
| `La variable de entorno GROQ_API_KEY no esta configurada` | Te falta crear el archivo `.env` o lo guardaste mal (por ejemplo `.env.txt`). Revisa el Paso 6. |
| `No se encontro la base de datos vectorial` | Intentaste hacer una consulta interactiva en `_init_.py` sin antes construir la base. Ejecuta `python ingest.py` primero. |
| `UnicodeDecodeError: 'charmap'` durante `ingest.py` | Existe un documento con caracteres especiales. El script ya posee `encoding="utf-8"` integrado, asegúrate de tener la última versión del repositorio. |

---

## 9. Autores

*   **Lina Andrea Bello Ballen** - *Ingeniería de Sistemas (2026)*.