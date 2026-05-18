# Evaluación de Pipeline RAG con RAGAS y Groq

> Pipeline RAG (Retrieval-Augmented Generation) que responde preguntas sobre programas de asignatura en PDF y evalúa la calidad de las respuestas con métricas automáticas.

> Esta documentación corresponde a la rama **`RAG`** del repositorio.

---

## Contenido

1. [Descripción General](#1-descripción-general)
2. [Glosario de Términos](#2-glosario-de-términos)
3. [Tecnologías](#3-tecnologías)
4. [Estructura del proyecto](#4-estructura-del-proyecto)
5. [Arquitectura](#5-arquitectura)
6. [Requisitos previos](#6-requisitos-previos)
7. [Guía de instalación y ejecución](#7-guía-de-instalación-y-ejecución)
8. [Cómo funciona internamente](#8-cómo-funciona-internamente)
9. [Resultados y métricas](#9-resultados-y-métricas)
10. [Solución de Problemas](#10-solución-de-problemas)
11. [Seguridad de credenciales](#11-seguridad-de-credenciales)
12. [Checklist de soporte](#12-checklist-de-soporte)
13. [Autoría](#13-autoría)

---

## 1. Descripción General

Lee los PDFs de `docs/`, los convierte en vectores numéricos, los almacena en una base vectorial local (ChromaDB) y permite responder preguntas en lenguaje natural usando un LLM (Llama 3.1 vía Groq). Finalmente, evalúa la calidad de cada respuesta con el framework **RAGAS**.

**Problema que resuelve:** Los modelos de lenguaje grandes (LLMs) carecen de conocimiento sobre datos privados o recientes. La arquitectura RAG proporciona el contexto necesario de forma dinámica, mitigando la generación de información falsa (alucinaciones) y garantizando respuestas basadas en fuentes confiables.

---

## 2. Glosario de Términos

| Término | Definición |
|---|---|
| **API Key** | Credencial secreta que autoriza llamadas a un servicio (aquí, Groq). |
| **Variable de entorno** | Valor de configuración que vive fuera del código, en el archivo `.env`. |
| **Entorno virtual** | Carpeta aislada con su propia copia de Python y librerías. Evita conflictos entre proyectos. |
| **LLM** | "Large Language Model". Modelo de IA que genera texto. Aquí: Llama 3.1 8B. |
| **Embedding** | Vector numérico que representa el significado de un texto. Textos parecidos → vectores parecidos. |
| **Vectorización** | Proceso de convertir texto en embeddings. |
| **ChromaDB** | Base de datos especializada en almacenar embeddings y buscar por similitud. |
| **Chunk** | Fragmento de un documento grande dividido en partes manejables. |
| **Prompt aumentado** | Prompt enriquecido con el contexto recuperado antes de enviarse al LLM. |
| **RAG** | Patrón que combina búsqueda (retrieval) y generación (LLM). |
| **RAGAS** | Framework que evalúa la calidad de un pipeline RAG con métricas objetivas. |

---

## 3. Tecnologías

| Tecnología | Rol |
|---|---|
| **Python 3.10+** | Lenguaje base. |
| **LangChain** | Orquesta carga de PDFs, troceo, embeddings, vector store y LLM. |
| **HuggingFace `all-MiniLM-L6-v2`** | Modelo de embeddings (local, gratis, sin API). |
| **ChromaDB** | Base vectorial local en `chroma_db_ragas/`. |
| **Groq + Llama 3.1 8B** | Proveedor del LLM. Capa gratuita amplia y latencia baja. |
| **RAGAS** | Evaluación automática del pipeline ("LLM as a judge"). |

---

## 4. Estructura del proyecto

```
DesarrolloDeAplicacionesConIA-2026-1-/
├── docs/                          # PDFs de los programas de asignatura
├── env/                           # Entorno virtual (local, no se sube)
├── chroma_db_ragas/               # Base vectorial (se genera al ejecutar)
├── evaluacion_ragas.py            # Script principal
├── .env                           # Credenciales (creado por el usuario, excluido del repositorio)
├── .gitignore                     # Exclusiones de Git
├── README.md                      # Esta documentación
└── resultados_evaluacion.md       # Se genera al terminar la evaluación
```

| Archivo / Carpeta | ¿Modificable? |
|---|---|
| `docs/` | Sí — añade o quita PDFs. Borra `chroma_db_ragas/` después para reindexar. |
| `.env` | Sí — aquí van tus credenciales. **Nunca lo subas al repo.** |
| `evaluacion_ragas.py` | Archivo central. Modificar con precaución. |
| `env/` y `chroma_db_ragas/` | No — se generan automáticamente. |

---

## 5. Arquitectura

```
┌──────────────────────────────────────────────────────────────┐
│ INDEXACIÓN                                                    │
│  PDFs → Text Splitter → Embeddings (HF) → ChromaDB           │
├──────────────────────────────────────────────────────────────┤
│ INFERENCIA RAG (por pregunta)                                 │
│  Pregunta → Embedding → ChromaDB busca 4 chunks similares    │
│            → Prompt aumentado → Groq/Llama → Respuesta       │
├──────────────────────────────────────────────────────────────┤
│ EVALUACIÓN                                                    │
│  {pregunta, respuesta, contexto, ground_truth}                │
│            → RAGAS evaluate() → faithfulness,                 │
│              answer_relevancy, context_precision              │
│            → resultados_evaluacion.md                         │
└──────────────────────────────────────────────────────────────┘
```

**Servicios externos:**
- **Groq** (obligatorio): inferencia del LLM.
- **HuggingFace** (opcional): descarga el modelo de embeddings la primera vez (~90 MB) y queda cacheado offline.

---

## 6. Requisitos previos

| Requisito | Versión | Obligatorio |
|---|---|---|
| Python | 3.10+ | Sí |
| pip | (incluido en la instalación de Python) | Sí |
| Git | cualquiera | Solo si vas a clonar |
| Cuenta en Groq | gratuita | Sí |
| Editor de código | cualquiera (VS Code, PyCharm, Sublime, etc.) | Recomendado |

**Verifica qué tienes instalado:**
```bash
python --version    # debe responder Python 3.10 o superior
pip --version       # debe responder pip x.x.x
```

**Si Python no está instalado:**
- **Windows:** descarga desde [python.org](https://www.python.org/downloads/) marcando **"Add Python to PATH"**.
- **macOS:** `brew install python@3.11` o desde [python.org](https://www.python.org/downloads/macos/).
- **Linux:** `sudo apt install python3 python3-venv python3-pip` (Debian/Ubuntu) o equivalente.

---

## 7. Guía de instalación y ejecución

### 7.1. Obtener el proyecto

**Nota importante:** A la hora de descargar y correr el proyecto, verifica en tu interfaz de clonación o entorno que estás posicionado en la rama del proyecto (`RAG`).

**Opción A — Git CLI:**
```bash
git clone -b RAG https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-.git
```

**Opción B — Cliente gráfico** (GitHub Desktop, GitKraken, etc.): pega la URL del repo y cambia a la rama `RAG`.

**Opción C — ZIP:** en GitHub, selector de rama → `RAG` → botón verde `<> Code` → `Download ZIP` → extraer.

### 7.2. Abrir una terminal en la raíz del proyecto

| SO | Cómo abrir una terminal |
|---|---|
| **Windows** | Tecla `Windows` + escribir `cmd` o `powershell` → Enter. |
| **macOS** | `Cmd + Espacio` + escribir `Terminal` → Enter. |
| **Linux** | `Ctrl + Alt + T`. |
| **Cualquier editor** | Generalmente `Ctrl + ñ` (terminal integrada). |

**Navegar hasta la carpeta del proyecto:**
```bash
cd ruta/a/DesarrolloDeAplicacionesConIA-2026-1-
```

**Verificar que estás en la raíz** (Windows: `dir`, macOS/Linux: `ls`). Debes ver `evaluacion_ragas.py` y la carpeta `docs/`.

> **Atajo:** si abriste el proyecto con "Open Folder" en VS Code y abres la terminal integrada, ya estás en la raíz.

### 7.3. Crear y activar el entorno virtual

**Crear** (igual en todos los sistemas):
```bash
python -m venv env
```

**Activar:**

| Sistema | Comando |
|---|---|
| Windows (CMD) | `env\Scripts\activate.bat` |
| Windows (PowerShell) | `.\env\Scripts\Activate.ps1` |
| macOS / Linux | `source env/bin/activate` |

La activación exitosa se confirmará mediante la aparición del prefijo `(env)` en la línea de comandos de su terminal.

> Para desactivarlo: `deactivate`.

### 7.4. Instalar las dependencias

Con el entorno virtual **activado**, ejecute el siguiente comando:

```bash
pip install pandas datasets tabulate ragas langchain-groq langchain-huggingface langchain-chroma langchain-community langchain-text-splitters pypdf python-dotenv sentence-transformers
```

**Qué se instala:**

| Librería | Función |
|---|---|
| `pandas`, `tabulate` | Manejo y visualización de tablas. |
| `datasets` | Estructura que consume RAGAS. |
| `ragas` | Framework de evaluación. |
| `langchain-groq` | Cliente LLM (Groq). |
| `langchain-huggingface` + `sentence-transformers` | Embeddings locales. |
| `langchain-chroma` | Conector con ChromaDB. |
| `langchain-community`, `langchain-text-splitters`, `pypdf` | Carga y troceo de PDFs. |
| `python-dotenv` | Lectura del archivo `.env`. |

El proceso puede demorar entre 2 y 10 minutos, dependiendo de la velocidad de conexión. Al finalizar, se mostrará el mensaje de confirmación `Successfully installed ...`.

### 7.5. Crear el archivo .env

En la raíz del proyecto, crea un archivo vacío llamado exactamente **.env** (con el punto al inicio).

> **Advertencia:** Si Windows no te deja crear archivos que empiezan con `.`, créalo desde VS Code (`New File` → escribe `.env`) o desde terminal: `type nul > .env` (Windows) / `touch .env` (macOS/Linux).

### 7.6. Obtener y configurar la API Key de Groq

Para poder ejecutar el proyecto, es obligatorio configurar tu API Key de Groq en el archivo .env que acabas de crear. La API Key es la credencial que permite comunicarse con el modelo de IA (Llama 3.1 8B). **Es gratuita** y se obtiene en menos de un minuto.

**Paso a paso:**
1. Entra a [https://console.groq.com](https://console.groq.com) y regístrate o inicia sesión.
2. Ve a la sección **"API Keys"** en el menú izquierdo (o visita [https://console.groq.com/keys](https://console.groq.com/keys)).
3. Haz clic en **"Create API Key"**, asigna un nombre y confírmalo.
4. **Copia la clave inmediatamente** (Groq solo la muestra una vez).
5. Abre el archivo .env creado en el paso 7.5 y pega la clave con este formato:

```env
GROQ_API_KEY="Your_api_key_here"
```
*(Reemplaza "Your_api_key_here" por la clave real que copiaste sin las comillas)*

**Preguntas frecuentes sobre la API Key:**

| Situación | Qué hacer |
|---|---|
| Perdí la clave | Vuelve a [console.groq.com/keys](https://console.groq.com/keys), borra la antigua y crea una nueva. Actualiza el .env. |
| Me da error 401 AuthenticationError | La clave está mal copiada o fue revocada. Verifica que no tenga espacios al inicio/final y crea una nueva si es necesario. |
| Me da error 429 RateLimitError | Llegaste al límite gratuito diario de tokens. Espera unas horas o al reset diario (medianoche UTC). |
| ¿Es gratis? | Sí, la capa gratuita de Groq incluye 500,000 tokens/día con el modelo Llama 3.1 8B, **más que suficiente** para este proyecto. |
| ¿La clave caduca? | No expira automáticamente, pero puedes revocarla cuando quieras desde la consola. |

### 7.7. Ejecutar el proyecto

Con el entorno virtual activado y el .env configurado:

```bash
python -u evaluacion_ragas.py
```

- `-u` muestra los `print` en tiempo real.
- Tiempo total estimado: **1 a 3 minutos**.

**El progreso de la ejecución se visualizará de la siguiente manera:**

```
Inicializando modelos...
Cargando PDFs desde la carpeta docs/ ...
Dividiendo X páginas en chunks...
Recuperando contextos y generando respuestas...
  Procesando Q1...
  ...
Iniciando evaluación RAGAS...
Generando análisis crítico...

=== RESULTADOS DE EVALUACIÓN RAGAS ===
[tabla con métricas]

[OK] Script completado.
```

**Para cancelar a mitad de ejecución:** `Ctrl + C`.

---

## 8. Cómo funciona internamente

### Vectorización y similitud

Cada chunk de los PDFs se convierte en un **embedding** (vector de 384 números) con el modelo `all-MiniLM-L6-v2`. ChromaDB usa **similitud coseno** para encontrar los chunks cuyo significado se parece más al de la pregunta — aunque usen otras palabras.

### Prompt aumentado

El prompt que recibe el LLM tiene esta forma:

```
Basado en el siguiente contexto, responde la pregunta.
Si no sabes la respuesta, di que no se encuentra en el contexto.

Contexto:
<chunk 1>
---
<chunk 2>
...

Pregunta:
<la pregunta>
```

Esto reduce alucinaciones porque el LLM responde **desde el contexto**, no desde lo que "recuerda".

### Reglas de oro

1. Nunca expongas credenciales en código — siempre en `.env`.
2. Nunca subas `.env` a Git (ya está en `.gitignore`).
3. Si modificas los PDFs en `docs/`, borra `chroma_db_ragas/` para reindexar.
4. No modifiques los `ground_truth` a conveniencia: invalidan la evaluación.

---

## 9. Resultados y métricas

Al terminar, el script imprime una tabla en consola y guarda los resultados en **`resultados_evaluacion.md`**.

| Métrica | Rango | Qué mide |
|---|---|---|
| **Faithfulness** | 0 — 1 | ¿La respuesta se basa estrictamente en el contexto? Cercano a 1 = sin alucinaciones. |
| **Answer Relevancy** | 0 — 1 | ¿La respuesta efectivamente contesta la pregunta? |
| **Context Precision** | 0 — 1 | ¿El retriever trajo contexto relevante al inicio? |

**Lectura esperada:**
- Preguntas factuales (Q1-Q4): métricas altas (0.7+).
- Preguntas que combinan información (Q5-Q6): métricas medias.
- Preguntas de validación (fuera de contexto) (Q7-Q8): si el sistema responde "no se encuentra en el contexto", **faithfulness se mantiene alta**. Si inventa una respuesta, baja.

---

## 10. Solución de Problemas

| Síntoma | Causa | Solución |
|---|---|---|
| `python no se reconoce` | Python no en PATH. | Reinstala marcando "Add to PATH". |
| `pip no se reconoce` | Entorno virtual no activado. | Activa el entorno (sección 7.3). |
| `ModuleNotFoundError: No module named 'X'` | Dependencias no instaladas o entorno desactivado. | Activa el entorno y reejecuta el `pip install` de la sección 7.4. |
| `[ERROR] GROQ_API_KEY no encontrada` | `.env` no existe o está mal nombrado. | Verifica que el archivo se llame exactamente `.env` (no `.env.txt`). |
| `groq.AuthenticationError: 401` | API Key inválida. | Genera una nueva en [console.groq.com/keys](https://console.groq.com/keys). |
| `groq.RateLimitError: 429` (TPD) | Excediste el límite diario de tokens del modelo. | Espera unos minutos o al reset diario. El script ya guarda resultados parciales. |
| `KeyError: 'question'` | RAGAS cambió nombres de columna. | El script ya lo maneja con detección automática. |
| `cannot be loaded because running scripts is disabled` (PowerShell) | Política de ejecución restrictiva. | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Microsoft Visual C++ 14.0 or greater is required` | Falta compilador en Windows. | Instala [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). |
| `python: can't open file '...evaluacion_ragas.py'` | Estás parado en otra carpeta. | Usa `cd` para ir a la raíz. Confirma con `dir` / `ls`. |
| Cuelgue en "Cargando ChromaDB" la primera vez | Descarga del modelo de embeddings. | Espera unos minutos (~90 MB). |

---

## 11. Seguridad de credenciales

- **Nunca** subas `.env` a Git.
- **Nunca** pegues tus API Keys en chats, capturas o foros.
- Si una key se filtra: ve a Groq, **revócala** y genera una nueva.
- Verifica que `.gitignore` contenga al menos:
  ```
  .env
  env/
  chroma_db_ragas/
  __pycache__/
  ```

---

## 12. Checklist de soporte

Si algo falla, revisa en orden:

```
[ ] 1. python --version             → 3.10 o superior
[ ] 2. pip --version                → responde
[ ] 3. Estás en la raíz             → ves evaluacion_ragas.py al hacer dir / ls
[ ] 4. Entorno virtual activado     → la terminal muestra (env)
[ ] 5. Dependencias instaladas      → pip list muestra langchain-groq, ragas, etc.
[ ] 6. .env existe                  → dir .env / ls -la .env
[ ] 7. GROQ_API_KEY tiene valor     → abre .env y verifica
[ ] 8. Hay conexión a internet
```

Si todo pasa y aún hay error, copia el mensaje completo y revisa la [sección 10](#10-solución-de-problemas).

---

## 13. Autoría

| | |
|---|---|
| **Autor** | Lina Andrea Bello Ballen |
| **Código** | 506241153 |
| **Fecha** | 07 de marzo de 2026 |
| **Asignatura** | Desarrollo de Aplicaciones con IA |
| **Repositorio** | [Landrea28/DesarrolloDeAplicacionesConIA-2026-1-](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-) — rama `RAG` |
