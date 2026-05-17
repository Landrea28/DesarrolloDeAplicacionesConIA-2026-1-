# Evaluación de Pipeline RAG con RAGAS y Groq

> Sistema de evaluación automática de un pipeline RAG (Retrieval-Augmented Generation) sobre programas de asignatura universitarios.

Este proyecto implementa un pipeline RAG que recupera información desde documentos PDF y la utiliza como contexto para responder preguntas mediante un modelo de lenguaje (LLM). Las respuestas se evalúan automáticamente con el framework **RAGAS** usando métricas objetivas (fidelidad, relevancia y precisión del contexto).

> 🪸 **Esta documentación corresponde a la rama `RAG`** del repositorio. La rama `main` contiene otros proyectos de la asignatura.

---

## 📑 Tabla de contenido

1. [Introducción](#1-introducción)
2. [Glosario](#2-glosario)
3. [Tecnologías](#3-tecnologías)
4. [Herramientas](#4-herramientas)
5. [Estructura del proyecto](#5-estructura-del-proyecto)
6. [Arquitectura](#6-arquitectura)
7. [Requisitos previos](#7-requisitos-previos)
8. [Guía de instalación y ejecución](#8-guía-de-instalación-y-ejecución)
9. [Configuración de servicios externos y credenciales](#9-configuración-de-servicios-externos-y-credenciales)
10. [Base de datos vectorial](#10-base-de-datos-vectorial)
11. [Cómo funciona el sistema](#11-cómo-funciona-el-sistema)
12. [Vectorización y embeddings](#12-vectorización-y-embeddings)
13. [Construcción del prompt aumentado](#13-construcción-del-prompt-aumentado)
14. [Reglas de seguridad y buenas prácticas](#14-reglas-de-seguridad-y-buenas-prácticas)
15. [Evaluación con RAGAS](#15-evaluación-con-ragas)
16. [Informe de resultados](#16-informe-de-resultados)
17. [Errores comunes y soluciones](#17-errores-comunes-y-soluciones)
18. [Seguridad de credenciales](#18-seguridad-de-credenciales)
19. [Soporte rápido (checklist)](#19-soporte-rápido-checklist)
20. [Autoría](#20-autoría)

---

## 1. Introducción

**¿Qué hace este proyecto?**
Lee un conjunto de PDFs (programas de asignatura), los convierte en representaciones numéricas, almacena estas representaciones en una base de datos vectorial y permite responder preguntas en lenguaje natural sobre el contenido.

**¿Cuál es su propósito?**
Demostrar y medir, con métricas objetivas, qué tan bien un sistema RAG puede responder preguntas a partir de documentos institucionales sin "alucinar" información que no está en ellos.

**¿Qué problema resuelve?**
Los modelos de lenguaje (LLMs) por sí solos no conocen documentos privados (programas de asignatura, manuales internos, etc.). Este proyecto les "enseña" temporalmente a leer esos documentos antes de responder, y luego evalúa la calidad de sus respuestas de forma automatizada.

---

## 2. Glosario

| Término | Definición | Cómo se usa aquí |
|---|---|---|
| **API** | "Application Programming Interface". Es un canal por el que un programa habla con un servicio externo. | El proyecto llama a la API de Groq para enviarle prompts y recibir respuestas. |
| **API Key** | Credencial secreta (parecida a una contraseña) que identifica quién está consumiendo una API. | Se necesita una `GROQ_API_KEY` para autorizar las llamadas al modelo Llama 3.3. |
| **Token** | Credencial similar a una API Key, normalmente para servicios que requieren permisos más granulares. | Opcionalmente se usa `HF_TOKEN` para descargar modelos privados desde HuggingFace. |
| **Variable de entorno** | Valor de configuración que vive fuera del código fuente. Permite separar los secretos del programa. | Las credenciales se leen desde un archivo `.env` para no escribirlas en el código. |
| **Entorno virtual** | Carpeta aislada con su propia copia de Python y librerías. Evita que las dependencias de un proyecto contaminen otros proyectos del computador. | Se crea una carpeta `env/` que contiene las librerías específicas de este proyecto. |
| **Dependencia** | Librería externa (escrita por terceros) que el proyecto necesita para funcionar. | Se listan en `requirements.txt` (pandas, langchain, ragas, etc.). |
| **Librería** | Conjunto reutilizable de funciones empaquetadas. | LangChain, RAGAS y pandas son librerías. |
| **Framework** | Librería con una estructura más opinada que define cómo organizar el código. | LangChain y RAGAS son frameworks. |
| **LLM** | "Large Language Model". Modelo de IA entrenado para entender y generar texto. | El proyecto usa Llama 3.3 70B servido a través de Groq. |
| **Embedding** | Vector numérico que representa un fragmento de texto en un "espacio semántico". Textos parecidos producen vectores parecidos. | Cada chunk de los PDFs se convierte en un embedding antes de guardarse. |
| **Vectorización** | Proceso de convertir texto en embeddings. | Lo hace el modelo `all-MiniLM-L6-v2` de HuggingFace. |
| **Similitud semántica** | Medida matemática (típicamente coseno) de qué tan parecidos son dos embeddings. | Permite encontrar fragmentos relevantes aunque la pregunta use otras palabras. |
| **Base vectorial** | Base de datos especializada en almacenar embeddings y buscar por similitud. | ChromaDB guarda todos los embeddings en la carpeta `chroma_db_ragas/`. |
| **Chunk** | Fragmento de un documento de tamaño manejable. | Cada PDF se trocea en chunks de 1000 caracteres con 200 de superposición. |
| **Retriever** | Componente que busca los chunks más relevantes para una pregunta. | El retriever de ChromaDB devuelve los 4 chunks más parecidos a cada pregunta. |
| **Prompt aumentado** | Prompt enriquecido con contexto recuperado antes de enviarse al LLM. | El proyecto construye un prompt que incluye los chunks recuperados + la pregunta. |
| **RAG** | "Retrieval-Augmented Generation". Patrón que combina búsqueda (retrieval) y generación (LLM). | Es el patrón central de todo el proyecto. |
| **Ground truth** | Respuesta de referencia, considerada correcta. | Se definen 8 ground truths para comparar contra las respuestas generadas. |
| **Métrica RAGAS** | Indicador numérico (0 a 1) producido por el framework RAGAS. | Se calculan tres: faithfulness, answer_relevancy y context_precision. |

---

## 3. Tecnologías

| Tecnología | Rol | Por qué se eligió |
|---|---|---|
| **Python 3.10+** | Lenguaje base del proyecto. | Estándar de facto en IA/ML, con el mejor ecosistema de librerías. |
| **LangChain** | Orquestador del pipeline: carga PDFs, los trocea, los conecta con embeddings, vector store y LLM. | Abstrae las diferencias entre proveedores y permite cambiar un componente sin reescribir todo. |
| **HuggingFace `all-MiniLM-L6-v2`** | Modelo de embeddings, se ejecuta localmente. | Es ligero (90 MB), rápido y gratuito. No consume API. |
| **ChromaDB** | Base de datos vectorial local, persistente en disco. | No requiere instalar ningún servidor. Los embeddings quedan en una carpeta del proyecto. |
| **Groq + Llama 3.3 70B** | Proveedor de inferencia LLM. | Latencia muy baja (cientos de ms) y capa gratuita amplia. Evita los rate limits de otros proveedores. |
| **RAGAS** | Framework de evaluación automática de pipelines RAG. | Calcula métricas estándar sin necesidad de supervisión humana ("LLM as a judge"). |
| **pypdf** | Lectura del contenido de archivos PDF. | Compatible con LangChain a través de `PyPDFLoader`. |
| **pandas** | Manipulación tabular de resultados. | Permite estructurar los resultados antes de exportarlos. |
| **tabulate** | Formato de tablas en consola. | Hace que los resultados sean legibles en terminal. |
| **python-dotenv** | Carga de variables de entorno desde el archivo `.env`. | Permite mantener las credenciales fuera del código fuente. |

---

## 4. Herramientas

> 💡 **Importante:** las herramientas listadas a continuación son **alternativas**. Puedes usar cualquiera de las opciones — el proyecto funciona igual con todas.

### 4.1. Editor de código

| Editor | Sistema | Recomendado para |
|---|---|---|
| **Visual Studio Code** | Windows / Linux / macOS | Principiantes. Gratuito, ligero, con terminal integrada. |
| **PyCharm Community** | Windows / Linux / macOS | Quienes prefieren un IDE específico de Python. Gratuito. |
| **Sublime Text / Notepad++** | Windows / Linux / macOS | Edición rápida sin features de IDE. |
| **Vim / Neovim** | Linux / macOS | Usuarios avanzados de terminal. |

No necesitas un editor específico — cualquiera que abra archivos `.py` y `.md` sirve.

### 4.2. Cliente Git (para descargar el proyecto)

| Opción | Tipo | Recomendado para |
|---|---|---|
| **GitHub Desktop** | Gráfica | Principiantes. Interfaz visual, todo con clicks. |
| **GitKraken** | Gráfica | Visualización avanzada de ramas. |
| **Git CLI** (`git` en terminal) | Línea de comandos | Quien ya conoce la terminal. |
| **Descargar ZIP** | Sin cliente | No requiere instalar nada. |

Si no quieres instalar Git, puedes descargar el proyecto como `.zip` directamente desde GitHub.

### 4.3. Terminal

| Terminal | Sistema |
|---|---|
| **CMD (Símbolo del sistema)** | Windows |
| **PowerShell** | Windows |
| **Windows Terminal** | Windows |
| **Terminal** | macOS |
| **GNOME Terminal / Konsole / xterm** | Linux |
| **Terminal integrada del editor** | Cualquiera |

> Si tu editor tiene terminal integrada (VS Code, PyCharm, etc.), es la opción más cómoda: ya está abierta dentro de la carpeta del proyecto.

### 4.4. Navegador web

Cualquiera moderno: Chrome, Firefox, Edge, Brave, Safari. Solo se usa para crear cuentas y copiar API Keys.

---

## 5. Estructura del proyecto

```
DesarrolloDeAplicacionesConIA-2026-1-/
│
├── docs/                          # PDFs de los programas de asignatura
│   ├── Programa de Asignatura Diseño de Interfaces.pdf
│   ├── Programa de Asignatura Bases de datos_II.pdf
│   ├── Programa de Asignatura Ecuaciones Diferenciales.pdf
│   ├── Programa de Asignatura DesarrolloAplicacionesIA.pdf
│   ├── Programa de Asignatura Nuevas Tecnologias de Desarrollo.pdf
│   └── Programa de Asignatura Redes de Comunicación_I.pdf
│
├── env/                           # Entorno virtual (se crea localmente, no se sube al repo)
│
├── chroma_db_ragas/               # Base vectorial (se genera al ejecutar el script)
│
├── evaluacion_ragas.py            # ⭐ Script principal del proyecto
├── requirements.txt               # Listado de dependencias
├── .env                           # Credenciales (el usuario lo crea, NO se sube al repo)
├── .gitignore                     # Archivos ignorados por Git
├── README.md                      # Esta documentación
└── resultados_evaluacion.md       # Se genera tras ejecutar el script
```

### ¿Qué puedo modificar?

| Archivo / Carpeta | ¿Modificable? | Notas |
|---|---|---|
| `docs/` | ✅ Sí | Puedes añadir o quitar PDFs. Borra `chroma_db_ragas/` después para reindexar. |
| `.env` | ✅ Sí | Aquí pones tus credenciales. **Nunca lo subas al repositorio.** |
| `evaluacion_ragas.py` | ⚠️ Con cuidado | Es el núcleo del proyecto. Modifícalo solo si entiendes el flujo. |
| `requirements.txt` | ⚠️ Con cuidado | Solo si agregas librerías nuevas. |
| `env/` | ❌ No | Se gestiona automáticamente. |
| `chroma_db_ragas/` | ❌ No | Se genera automáticamente. Si quieres reindexar, **bórrala completa**. |

---

## 6. Arquitectura

### 6.1. Flujo general

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USUARIO / SCRIPT                            │
└──────────────────────────────┬──────────────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────────────┐
│  FASE 1 — INDEXACIÓN (una sola vez)                                 │
│                                                                      │
│   docs/*.pdf  ──►  PyPDFLoader  ──►  Text Splitter                  │
│                                          │                           │
│                                          ▼                           │
│                                       Chunks                         │
│                                          │                           │
│                                          ▼                           │
│                              HuggingFace Embeddings (local)         │
│                                          │                           │
│                                          ▼                           │
│                                     ChromaDB                         │
│                                  (chroma_db_ragas/)                  │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  FASE 2 — INFERENCIA RAG (por cada pregunta)                        │
│                                                                      │
│   Pregunta  ──►  Embedding  ──►  Búsqueda por similitud  ──►        │
│                                  (ChromaDB retriever)                │
│                                          │                           │
│                                          ▼                           │
│                                  4 chunks más parecidos              │
│                                          │                           │
│                                          ▼                           │
│                                  Prompt aumentado                    │
│                              (contexto + pregunta)                   │
│                                          │                           │
│                                          ▼                           │
│                                Groq → Llama 3.3 70B                  │
│                                          │                           │
│                                          ▼                           │
│                                     Respuesta                        │
└─────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────┐
│  FASE 3 — EVALUACIÓN                                                 │
│                                                                      │
│   {pregunta, respuesta, contexto, ground_truth}                      │
│                                          │                           │
│                                          ▼                           │
│                                    RAGAS evaluate()                  │
│                                  (faithfulness,                      │
│                                   answer_relevancy,                  │
│                                   context_precision)                 │
│                                          │                           │
│                                          ▼                           │
│                              DataFrame + análisis crítico            │
│                                          │                           │
│                                          ▼                           │
│                            resultados_evaluacion.md                  │
└─────────────────────────────────────────────────────────────────────┘
```

### 6.2. Servicios externos

| Servicio | Tipo | Necesario | Para qué |
|---|---|---|---|
| **Groq** | API en la nube | ✅ Sí | Inferencia del LLM (genera respuestas y análisis). |
| **HuggingFace** | API en la nube | ⚠️ Opcional | Descarga del modelo de embeddings la primera vez. Tras la descarga inicial funciona offline. |

> ℹ️ El modelo de embeddings se descarga una sola vez (~90 MB) y queda cacheado localmente. Las llamadas siguientes no necesitan internet para los embeddings.

---

## 7. Requisitos previos

Antes de empezar necesitas tener instalado lo siguiente:

### 7.1. Resumen rápido

| Requisito | Versión mínima | Obligatorio |
|---|---|---|
| Python | 3.10 | ✅ |
| pip | (viene con Python) | ✅ |
| Git | cualquiera reciente | ⚠️ Solo si vas a clonar el repo |
| Editor de código | cualquiera | ⚠️ Recomendado |
| Conexión a internet | — | ✅ (al menos para la instalación inicial) |
| Cuenta en Groq | gratuita | ✅ |
| Cuenta en HuggingFace | gratuita | ⚠️ Opcional |

### 7.2. Verificar qué tienes instalado

Abre una terminal (más adelante explico cómo) y ejecuta los siguientes comandos **uno por uno**.

**Verificar Python:**
```bash
python --version
```
**Resultado esperado:** algo como `Python 3.11.5`.
**Si dice "no se reconoce" o sale versión menor a 3.10:** instala Python desde el paso 7.3.

**Verificar pip:**
```bash
pip --version
```
**Resultado esperado:** algo como `pip 23.x.x from ...`.
**Si dice "no se reconoce":** suele venir junto a Python — reinstala Python marcando la casilla "Add to PATH".

**Verificar Git (opcional):**
```bash
git --version
```
**Resultado esperado:** `git version 2.x.x`.
**Si dice "no se reconoce":** no es bloqueante — puedes descargar el proyecto como ZIP en su lugar.

### 7.3. Cómo instalar lo que falta

#### Python

| Sistema | Cómo instalarlo |
|---|---|
| **Windows** | Descarga desde [python.org/downloads](https://www.python.org/downloads/). Durante la instalación, **marca la casilla "Add Python to PATH"**. |
| **macOS** | Descarga desde [python.org](https://www.python.org/downloads/macos/) o instala con Homebrew: `brew install python@3.11`. |
| **Linux (Debian/Ubuntu)** | `sudo apt update && sudo apt install python3 python3-venv python3-pip` |
| **Linux (Fedora)** | `sudo dnf install python3 python3-pip` |
| **Linux (Arch)** | `sudo pacman -S python python-pip` |

#### Git (opcional, solo si vas a clonar)

| Sistema | Cómo instalarlo |
|---|---|
| **Windows** | [git-scm.com/download/win](https://git-scm.com/download/win) |
| **macOS** | `brew install git` o ejecuta `xcode-select --install` |
| **Linux** | `sudo apt install git` (Debian/Ubuntu) o equivalente |

---

## 8. Guía de instalación y ejecución

> Esta es la sección **más importante**. Sigue los pasos **en orden**, sin saltarte ninguno.

### 8.1. Obtener el proyecto

Tienes **dos formas** de obtener el proyecto. Elige la que prefieras.

#### Opción A — Clonar con Git (recomendada)

**Si tienes Git CLI:**
```bash
git clone -b RAG https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-.git
```
**Qué hace este comando:** descarga la rama `RAG` del repositorio dentro de una carpeta llamada `DesarrolloDeAplicacionesConIA-2026-1-` en el directorio actual.
**Resultado esperado:** una nueva carpeta con todos los archivos del proyecto.

**Si usas GitHub Desktop:**
1. Abre GitHub Desktop.
2. `File` → `Clone repository`.
3. Pega la URL `https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-.git`.
4. Elige la carpeta donde quieres guardarlo.
5. Después de clonar, cambia a la rama `RAG` desde el selector superior.

**Si usas GitKraken:**
1. `File` → `Clone Repo` → `Clone with URL`.
2. Pega la URL del repositorio.
3. Selecciona la rama `RAG` en el selector lateral.

#### Opción B — Descargar como ZIP

1. Entra al repositorio en GitHub desde el navegador.
2. Cambia el selector de rama a `RAG`.
3. Haz clic en el botón verde **`<> Code`** → `Download ZIP`.
4. Extrae el ZIP en una carpeta de tu elección (por ejemplo, `Documentos/RAG-proyecto`).

> 💡 **Recuerda la ruta donde quedó el proyecto** — la necesitarás para abrir la terminal en esa ubicación.

---

### 8.2. Abrir el proyecto

#### En Visual Studio Code

1. Abre VS Code.
2. `File` → `Open Folder` (o `Archivo` → `Abrir carpeta`).
3. Selecciona la carpeta del proyecto (la que contiene `evaluacion_ragas.py`).
4. VS Code mostrará la estructura del proyecto en el panel izquierdo.

#### En PyCharm

1. Abre PyCharm.
2. `File` → `Open`.
3. Selecciona la carpeta del proyecto.

#### En cualquier otro editor

Simplemente abre la carpeta del proyecto desde el menú del editor.

#### Identificar la raíz del proyecto

**Estás en la raíz del proyecto si ves estos archivos al mismo nivel:**

```
✅ evaluacion_ragas.py
✅ requirements.txt
✅ README.md
✅ docs/    (carpeta)
```

Si **no** ves estos archivos, probablemente entraste en una subcarpeta. Sube un nivel.

---

### 8.3. Cómo abrir la terminal

La **terminal** (también llamada *consola* o *línea de comandos*) es una ventana donde puedes escribir comandos de texto en lugar de hacer clic en botones.

#### En Windows

| Opción | Cómo abrirla |
|---|---|
| **CMD (Símbolo del sistema)** | Tecla `Windows` → escribe `cmd` → Enter. |
| **PowerShell** | Tecla `Windows` → escribe `powershell` → Enter. |
| **Terminal de VS Code** | Dentro de VS Code: `Ctrl + ñ` (o menú `Terminal` → `New Terminal`). |

#### En macOS

| Opción | Cómo abrirla |
|---|---|
| **Terminal** | `Cmd + Espacio` → escribe `Terminal` → Enter. |
| **Terminal de VS Code** | `Ctrl + ñ` o `Cmd + J`. |

#### En Linux

| Opción | Cómo abrirla |
|---|---|
| **Terminal del sistema** | `Ctrl + Alt + T` en la mayoría de distros. |
| **Terminal de VS Code** | `Ctrl + ñ`. |

#### Comandos básicos de navegación

| Comando | Windows (CMD) | macOS / Linux | Qué hace |
|---|---|---|---|
| Ver carpeta actual | `cd` | `pwd` | Muestra en qué carpeta estás. |
| Listar archivos | `dir` | `ls` | Muestra los archivos de la carpeta actual. |
| Entrar a una carpeta | `cd nombre` | `cd nombre` | Entra a la carpeta indicada. |
| Subir un nivel | `cd ..` | `cd ..` | Vuelve a la carpeta anterior. |
| Ir a una ruta absoluta | `cd C:\ruta\proyecto` | `cd /ruta/proyecto` | Va directamente a esa carpeta. |

#### Cómo llegar a la raíz del proyecto desde la terminal

**Ejemplo Windows:**
```cmd
cd C:\Users\TuUsuario\Documentos\DesarrolloDeAplicacionesConIA-2026-1-
```

**Ejemplo macOS / Linux:**
```bash
cd ~/Documentos/DesarrolloDeAplicacionesConIA-2026-1-
```

Luego ejecuta `dir` (Windows) o `ls` (macOS/Linux). **Debes ver `evaluacion_ragas.py`** entre los archivos. Si lo ves, estás en la raíz.

> 💡 **Atajo:** en VS Code, si abriste el proyecto con `Open Folder` y abres la terminal integrada (`Ctrl + ñ`), ya estás automáticamente en la raíz del proyecto. No necesitas navegar.

---

### 8.4. Crear el entorno virtual

#### ¿Qué es un entorno virtual?

Es una **carpeta aislada** con su propia copia de Python y librerías. Su propósito:

- Evita que las librerías de este proyecto **interfieran** con otros proyectos.
- Permite tener **diferentes versiones** de la misma librería para diferentes proyectos.
- Mantiene el Python "global" de tu computador **limpio**.

Sin entorno virtual, las librerías se instalan a nivel sistema y eso suele causar conflictos a futuro.

#### Comandos para crearlo

**Windows / macOS / Linux** (todos igual):
```bash
python -m venv env
```

**Qué hace este comando:** crea una carpeta llamada `env/` dentro de la raíz del proyecto con una copia aislada de Python.
**Resultado esperado:** aparece una carpeta nueva llamada `env/`. No saldrá ningún mensaje en consola.
**Errores comunes:**
- `python no se reconoce`: Python no está instalado o no está en el PATH. Reinstala Python marcando la casilla "Add to PATH".
- En algunos Linux: `The virtual environment was not created successfully because ensurepip is not available`. Solución: `sudo apt install python3-venv`.

---

### 8.5. Activar el entorno virtual

Crearlo **no es suficiente**. Hay que **activarlo** cada vez que abras una nueva terminal para trabajar en el proyecto.

| Sistema | Comando |
|---|---|
| **Windows (CMD)** | `env\Scripts\activate.bat` |
| **Windows (PowerShell)** | `.\env\Scripts\Activate.ps1` |
| **macOS / Linux** | `source env/bin/activate` |

**Resultado esperado:** verás `(env)` al inicio de la línea de la terminal. Algo así:

```
(env) C:\Users\TuUsuario\proyecto>
```

Eso indica que el entorno virtual está **activo**.

**Errores comunes:**

| Error | Causa | Solución |
|---|---|---|
| `activate no se reconoce` | Ruta incorrecta o entorno no creado. | Verifica que la carpeta `env/` existe. |
| `cannot be loaded because running scripts is disabled` (PowerShell) | Política de ejecución de Windows. | Ejecuta como administrador: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| No aparece `(env)` | No se activó. | Asegúrate de estar en la raíz del proyecto. |

> 💡 Para **desactivar** el entorno virtual en cualquier momento: comando `deactivate`.

---

### 8.6. Instalar las dependencias

Las dependencias son las librerías externas que el proyecto necesita. Están listadas en el archivo `requirements.txt`.

**Con el entorno virtual ACTIVADO**, ejecuta:

```bash
pip install -r requirements.txt
```

**Qué hace este comando:** lee el archivo `requirements.txt` y descarga e instala cada librería listada, junto con todas sus sub-dependencias.

**Resultado esperado:**
- Verás muchas líneas tipo `Collecting pandas`, `Downloading langchain-groq-0.x.x-...`, etc.
- Al final aparecerá `Successfully installed pandas-x.x.x datasets-x.x.x ...`.
- Tarda entre **2 y 10 minutos** según la velocidad de tu conexión.

**Errores comunes:**

| Error | Causa | Solución |
|---|---|---|
| `pip no se reconoce` | Entorno virtual no activado, o Python sin pip. | Activa el entorno virtual (paso 8.5). |
| `Permission denied` | Estás instalando a nivel sistema sin permisos. | Activa el entorno virtual o usa `pip install --user`. |
| `Could not find a version that satisfies the requirement` | Conexión a internet inestable o versión de Python muy antigua. | Verifica `python --version >= 3.10`. |
| `Microsoft Visual C++ 14.0 or greater is required` (Windows) | Falta el compilador de C++. | Instala [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). |

> 💡 Si la instalación de una librería específica falla, intenta instalarla individualmente para ver el error real: `pip install <nombre-de-la-librería>`.

---

### 8.7. Configurar las credenciales (`.env`)

#### ¿Qué es el archivo `.env`?

Es un archivo de texto plano que **guarda variables sensibles** (claves de API, tokens, contraseñas) **fuera del código fuente**. Esto permite:

- Compartir el código sin exponer credenciales.
- Tener credenciales diferentes en diferentes computadores.
- Evitar que las credenciales queden en el historial de Git.

Su nombre **debe ser exactamente `.env`** — empezando con un punto, sin nada más. Algunos sistemas lo ocultan por defecto al empezar con punto.

#### Crear el archivo

1. En la **raíz del proyecto** (misma carpeta donde está `evaluacion_ragas.py`), crea un archivo nuevo llamado `.env`.

   **Desde el explorador de archivos de Windows:**
   - Si Windows no te deja crear archivos que empiezan con `.`, créalo así: `.env.` (con punto al final). Windows quitará el punto final.
   - O créalo desde VS Code: clic derecho → `New File` → escribe `.env`.

   **Desde terminal (cualquier sistema):**
   ```bash
   # Windows (CMD):
   type nul > .env

   # macOS / Linux:
   touch .env
   ```

2. Abre el archivo con tu editor y pega exactamente esto:

   ```env
   GROQ_API_KEY=tu_clave_de_groq_aqui
   HF_TOKEN=tu_token_de_huggingface_aqui
   ```

3. Reemplaza `tu_clave_de_groq_aqui` por tu clave real (la obtienes en el [paso 9](#9-configuración-de-servicios-externos-y-credenciales)).

> ⚠️ **Importante:**
> - **No** uses comillas a menos que la clave contenga espacios.
> - **No** dejes espacios alrededor del `=`.
> - **Nunca** subas este archivo a GitHub (`.gitignore` ya lo excluye).

#### Verificar que el archivo se llama bien

En la terminal, dentro de la raíz del proyecto:

```bash
# Windows:
dir .env

# macOS / Linux:
ls -la .env
```

**Resultado esperado:** una línea mostrando el archivo `.env`.
**Si dice "no se encuentra":** el archivo se llama mal (revisa que no sea `.env.txt`, `env`, ni `.env.env`).

---

### 8.8. Ejecutar el proyecto

Con el entorno virtual **activado** y el `.env` **configurado**, ejecuta:

```bash
python -u evaluacion_ragas.py
```

**Qué hace este comando:**
- `python` ejecuta el intérprete.
- `-u` desactiva el buffer de salida (verás los `print` en tiempo real).
- `evaluacion_ragas.py` es el script principal.

**Resultado esperado** (en orden):

```
Inicializando modelos...
Cargando PDFs desde la carpeta docs/ ...
Dividiendo 18 páginas en chunks...
Cargando ChromaDB desde el directorio ./chroma_db_ragas...
Definiendo preguntas de prueba...
Recuperando contextos y generando respuestas...
  Procesando Q1...
  Procesando Q2...
  ...
  Procesando Q8...
Iniciando evaluación RAGAS (esto puede tomar un minuto)...
  Columnas devueltas por RAGAS: ['user_input', 'retrieved_contexts', ...]
Generando análisis crítico...

=== RESULTADOS DE EVALUACIÓN RAGAS ===
+-----------+------------+-----------------+-------------------+----------------+
| Pregunta  | Faithful.. | Answer Relev... | Context Precis... | Análisis Crít. |
+-----------+------------+-----------------+-------------------+----------------+
...
+-----------+------------+-----------------+-------------------+----------------+

[OK] Script completado. Los resultados también se guardaron en 'resultados_evaluacion.md'
```

**Tiempo estimado total:** de 1 a 3 minutos.

#### Cómo detener la ejecución

Si necesitas cancelar a la mitad: `Ctrl + C` en la terminal.

#### Cómo saber si terminó correctamente

Se considera ejecución exitosa si:

1. Se imprime la tabla final.
2. Aparece `[OK] Script completado.`
3. Se crea (o actualiza) el archivo `resultados_evaluacion.md` en la raíz.

---

## 9. Configuración de servicios externos y credenciales

### 9.1. Obtener la API Key de Groq (obligatoria)

Groq es el proveedor que ejecuta el LLM. Su capa gratuita es **suficiente** para este proyecto.

**Paso a paso:**

1. Entra a [https://console.groq.com](https://console.groq.com).
2. Crea una cuenta (puedes usar Google, GitHub o email).
3. Confirma el correo si te lo pide.
4. En el menú lateral, busca **"API Keys"** (o ve directo a [console.groq.com/keys](https://console.groq.com/keys)).
5. Clic en **"Create API Key"**.
6. Dale un nombre (por ejemplo, `proyecto-rag`).
7. **Copia la clave inmediatamente** — Groq solo te la muestra una vez.
8. Pégala en tu archivo `.env`:
   ```env
   GROQ_API_KEY=gsk_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

> ⚠️ Si pierdes la clave: vuelve a Groq, borra la anterior y crea una nueva. Recuerda actualizar el `.env`.

### 9.2. Obtener el token de HuggingFace (opcional)

Solo es necesario si quieres descargar modelos privados o tienes problemas de rate limit al descargar el modelo de embeddings la primera vez. **Para este proyecto, normalmente no es necesario.**

**Paso a paso (si decides crearlo):**

1. Entra a [https://huggingface.co/join](https://huggingface.co/join) y crea una cuenta.
2. Verifica tu correo.
3. Ve a [https://huggingface.co/settings/tokens](https://huggingface.co/settings/tokens).
4. Clic en **"New token"** (o "Create new token").
5. Asigna un nombre (ej. `rag-proyecto`) y selecciona el tipo **Read**.
6. Copia el token.
7. Pégalo en `.env`:
   ```env
   HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```

---

## 10. Base de datos vectorial

### 10.1. ¿Qué base de datos usa este proyecto?

Este proyecto **no usa una base de datos relacional tradicional** (como MySQL, PostgreSQL o SQLite). Usa una **base de datos vectorial** llamada **ChromaDB**.

### 10.2. ¿Qué es ChromaDB?

| Aspecto | Descripción |
|---|---|
| **Tipo** | Base de datos vectorial. |
| **Para qué sirve** | Almacenar embeddings (vectores numéricos) y buscar por similitud semántica. |
| **Dónde se guarda** | Localmente, en la carpeta `chroma_db_ragas/`. |
| **Requiere servidor** | ❌ No. Es completamente local. |
| **Requiere configuración** | ❌ No. Se inicializa automáticamente al correr el script. |

### 10.3. ¿Cómo se inicializa?

La primera vez que ejecutes `evaluacion_ragas.py`, el script:

1. Lee los PDFs de `docs/`.
2. Los divide en chunks.
3. Los convierte en embeddings.
4. Crea la carpeta `chroma_db_ragas/` y los guarda allí.

En ejecuciones siguientes, **vuelve a procesar los PDFs** (no es estrictamente necesario, pero garantiza datos frescos). Si quieres una indexación limpia, borra la carpeta `chroma_db_ragas/` antes de correr.

### 10.4. Borrar la base vectorial

Si cambias los PDFs o quieres reindexar desde cero:

```bash
# Windows (CMD):
rmdir /S /Q chroma_db_ragas

# Windows (PowerShell):
Remove-Item -Recurse -Force chroma_db_ragas

# macOS / Linux:
rm -rf chroma_db_ragas
```

---

## 11. Cómo funciona el sistema

A continuación, el **flujo interno** de qué ocurre cuando corres `python -u evaluacion_ragas.py`.

### 11.1. Fase 1 — Carga e indexación de documentos

1. Lee cada PDF de `docs/` con `PyPDFLoader`.
2. Divide cada PDF en chunks de **1000 caracteres** con **200 caracteres de superposición**.
3. Para cada chunk, calcula su embedding con `all-MiniLM-L6-v2`.
4. Almacena los embeddings en ChromaDB.

### 11.2. Fase 2 — Inferencia RAG

Para cada una de las **8 preguntas predefinidas**:

1. Convierte la pregunta en embedding.
2. ChromaDB busca los **4 chunks más parecidos** por similitud coseno.
3. Construye un **prompt aumentado** con el contexto recuperado + la pregunta.
4. Envía el prompt a **Llama 3.3 70B** vía Groq.
5. Guarda la respuesta junto con la pregunta, el contexto y el ground truth.

### 11.3. Fase 3 — Evaluación con RAGAS

1. Construye un `Dataset` de HuggingFace con todas las preguntas, respuestas, contextos y ground truths.
2. Llama a `evaluate()` de RAGAS con tres métricas:
   - **faithfulness:** ¿la respuesta se deriva del contexto?
   - **answer_relevancy:** ¿la respuesta responde la pregunta?
   - **context_precision:** ¿el retriever trajo contexto relevante?
3. RAGAS internamente vuelve a llamar al LLM para evaluar cada métrica.

### 11.4. Fase 4 — Análisis crítico

Para cada fila de resultados:

1. Construye un prompt que incluye la pregunta y sus métricas.
2. Pide al LLM un análisis crítico de 1-2 oraciones.
3. Agrega ese análisis al DataFrame.

### 11.5. Fase 5 — Salida

1. Imprime la tabla final con `tabulate` en consola.
2. Exporta los resultados a `resultados_evaluacion.md` en formato Markdown.

---

## 12. Vectorización y embeddings

### 12.1. ¿Qué es la vectorización?

Es el proceso de convertir texto en **vectores de números** (típicamente entre 384 y 1536 dimensiones). Cada vector se llama **embedding**.

**Idea clave:** textos con significado parecido producen vectores parecidos. Esto permite buscar por **significado**, no solo por palabras exactas.

**Ejemplo:**
- "¿cuánto cuesta el curso?"
- "¿cuál es el precio de la asignatura?"

Aunque no comparten palabras, sus embeddings son **muy cercanos** en el espacio vectorial, porque el modelo entendió que hablan de lo mismo.

### 12.2. ¿Qué modelo usa este proyecto?

| Característica | Valor |
|---|---|
| Modelo | `all-MiniLM-L6-v2` |
| Origen | HuggingFace (sentence-transformers) |
| Dimensiones | 384 |
| Tamaño | ~90 MB |
| Velocidad | Muy rápido (CPU) |
| Costo | Gratis (local) |

### 12.3. ¿Cómo se calcula la similitud?

ChromaDB utiliza **similitud coseno** entre vectores:

```
similitud(A, B) = (A · B) / (||A|| * ||B||)
```

Resultado entre `-1` (opuestos) y `1` (idénticos). Cuanto más cercano a 1, más parecidos son los textos.

---

## 13. Construcción del prompt aumentado

### 13.1. Anatomía del prompt

El prompt que se envía al LLM tiene esta estructura:

```
Basado en el siguiente contexto, responde la pregunta.
Si no sabes la respuesta, di que no se encuentra en el contexto.

Contexto:
<chunk 1>
---
<chunk 2>
---
<chunk 3>
---
<chunk 4>

Pregunta:
<la pregunta del usuario>
```

### 13.2. ¿Qué información se agrega?

| Componente | Origen | Función |
|---|---|---|
| Instrucción del sistema | Hardcodeada en el script | Restringe al LLM a responder solo desde el contexto. |
| Contexto (4 chunks) | Recuperado por ChromaDB | Fragmentos relevantes de los PDFs. |
| Pregunta | Pregunta del usuario / test | Lo que se desea responder. |

### 13.3. ¿Por qué mejora las respuestas?

- **Reduce alucinaciones:** el LLM ve los hechos antes de responder.
- **Permite responder sobre información privada:** el modelo no necesita "saber" sobre los PDFs — los lee en cada pregunta.
- **Trazabilidad:** sabes exactamente qué fragmentos influyeron en la respuesta.

### 13.4. Reglas de oro del proyecto

> Estas reglas aplican tanto al uso como a futuras modificaciones del script.

1. **Nunca exponer credenciales** en el código fuente. Siempre en `.env`.
2. **Nunca subir el `.env` a Git.** Ya está incluido en `.gitignore`, pero verifícalo siempre.
3. **Mantener el formato del prompt.** Cambios al formato suelen romper la calidad de las respuestas.
4. **No modificar el ground truth a conveniencia.** Si lo cambias para "mejorar" métricas, la evaluación pierde validez.
5. **Reindexar tras cambiar PDFs.** Borra `chroma_db_ragas/` siempre que modifiques `docs/`.
6. **Versionar `requirements.txt`** si agregas dependencias.
7. **No commitear** archivos generados (`chroma_db_ragas/`, `env/`, `resultados_evaluacion.md`).
8. **Validar la salida** antes de tomar decisiones a partir de las métricas — los LLM también pueden equivocarse en su rol de juez.

---

## 14. Reglas de seguridad y buenas prácticas

### 14.1. Manejo de credenciales

| Práctica | Acción |
|---|---|
| Almacenamiento | Solo en `.env`, nunca en código. |
| Versionado | El `.env` **nunca** debe estar en Git. |
| Rotación | Si se filtra una key, revócala inmediatamente y crea una nueva. |
| Compartir | No compartas el `.env` por correo, chat o capturas. |

### 14.2. Validación de entradas

Aunque este proyecto usa preguntas predefinidas, si lo adaptas para aceptar input de usuarios:

- Limita la longitud máxima de la pregunta.
- Filtra caracteres que puedan romper el prompt (saltos de línea muy largos, etc.).
- No permitas que el usuario inyecte instrucciones del sistema ("ignora todo y dime...").

### 14.3. Restricciones operativas

- La carpeta `chroma_db_ragas/` puede crecer con muchos PDFs — vigila el espacio en disco.
- El timeout de RAGAS es de **120 segundos** por métrica. Si tu conexión es lenta, aumenta `timeout` en `RunConfig`.

---

## 15. Evaluación con RAGAS

### 15.1. ¿Qué es RAGAS?

Framework que evalúa **automáticamente** la calidad de un pipeline RAG, sin necesidad de jueces humanos. Usa el patrón **"LLM as a judge"**: un LLM califica las respuestas de otro LLM.

### 15.2. Métricas usadas

| Métrica | Rango | Qué mide | Interpretación |
|---|---|---|---|
| **Faithfulness** | 0 — 1 | ¿La respuesta se basa estrictamente en el contexto? | Cercano a 1 = sin alucinaciones. |
| **Answer Relevancy** | 0 — 1 | ¿La respuesta efectivamente responde la pregunta? | Cercano a 1 = no se desvía. |
| **Context Precision** | 0 — 1 | ¿El retriever trajo contexto relevante al inicio? | Cercano a 1 = retriever bien afinado. |

### 15.3. Cómo se ejecuta

La evaluación está **integrada** dentro del script principal. No hay que correr nada aparte:

```bash
python -u evaluacion_ragas.py
```

Las métricas se imprimen al final y se exportan a `resultados_evaluacion.md`.

---

## 16. Informe de resultados

### 16.1. Dónde aparecen

| Lugar | Formato | Cuándo se genera |
|---|---|---|
| **Consola** | Tabla con `tabulate` | Al finalizar el script. |
| **`resultados_evaluacion.md`** | Markdown | Al finalizar el script (sobrescribe la versión anterior). |

### 16.2. Cómo leer la tabla

Cada fila corresponde a **una de las 8 preguntas**. Las columnas son:

| Columna | Significado |
|---|---|
| **Pregunta** | Texto de la pregunta evaluada. |
| **Faithfulness** | Valor 0-1. |
| **Answer Relevancy** | Valor 0-1. |
| **Context Precision** | Valor 0-1. |
| **Análisis Crítico** | Comentario breve del LLM sobre el desempeño en esa pregunta. |

### 16.3. Interpretación práctica

- **Las 4 primeras preguntas** (factuales y de vocabulario distinto): deberían tener métricas altas (0.7+).
- **Las preguntas 5-6** (combinar información): pueden mostrar métricas medias, depende del retriever.
- **Las preguntas 7-8** (provocan alucinación): si el sistema responde "no se encuentra en el contexto", las métricas siguen siendo buenas. Si se inventa una respuesta, **faithfulness baja**.

---

## 17. Errores comunes y soluciones

| Síntoma | Causa más probable | Solución |
|---|---|---|
| `python no se reconoce como un comando` | Python no está en el PATH. | Reinstala Python marcando "Add to PATH". |
| `pip no se reconoce` | Entorno virtual no activado. | Ejecuta el comando de activación de la sección 8.5. |
| `ModuleNotFoundError: No module named 'pandas'` | Dependencias no instaladas o entorno desactivado. | Activa el entorno y corre `pip install -r requirements.txt`. |
| `ModuleNotFoundError: No module named 'langchain_groq'` | Dependencia faltante. | `pip install langchain-groq` |
| `[ERROR] GROQ_API_KEY no encontrada` | Archivo `.env` no existe, mal nombrado o sin la variable. | Revisa la sección 8.7. Verifica que se llame exactamente `.env`. |
| `groq.AuthenticationError: 401` | API Key inválida o vencida. | Genera una nueva en [console.groq.com/keys](https://console.groq.com/keys). |
| `groq.RateLimitError: 429` | Excediste el rate limit gratuito de Groq. | Espera unos minutos. Si persiste, considera reducir el número de preguntas. |
| `KeyError: 'question'` (o `'faithfulness'`) | Versión nueva de RAGAS usa otros nombres de columna. | El script ya maneja esto. Si reaparece, revisa el `print` de "Columnas devueltas por RAGAS" y ajusta. |
| `cannot be loaded because running scripts is disabled` (PowerShell) | Política de ejecución restrictiva. | Ejecuta: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Microsoft Visual C++ 14.0 or greater is required` | Falta compilador C++ en Windows. | Instala [Visual C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/). |
| El script se queda colgado en "Cargando ChromaDB" | Primera descarga del modelo de embeddings. | Espera unos minutos — son ~90 MB. |
| `OSError: [Errno 28] No space left on device` | Disco lleno. | Libera espacio o borra `chroma_db_ragas/`. |
| El comando `cd` no cambia de carpeta | Ruta incorrecta o espacios sin escapar. | Envuelve la ruta entre comillas: `cd "C:\Ruta Con Espacios\proyecto"`. |
| `python: can't open file '...evaluacion_ragas.py'` | Estás parado en otra carpeta. | Ejecuta `cd` hacia la raíz del proyecto. Confirma con `dir` (Windows) o `ls`. |
| HuggingFace tarda en descargar el modelo | Conexión lenta. | Es normal la primera vez. Las siguientes son instantáneas (cache local). |

---

## 18. Seguridad de credenciales

### 18.1. Reglas absolutas

| Regla | Por qué |
|---|---|
| ❌ **Nunca subas `.env` a Git** | Cualquiera podría usar tu cuenta y consumir tu cuota. |
| ❌ **Nunca pegues API Keys en chats, foros, capturas o issues** | Quedan indexadas y son explotables al instante. |
| ✅ **Mantén `.gitignore` actualizado** | Asegúrate de que `.env`, `env/` y `chroma_db_ragas/` están listados. |
| ✅ **Rota las keys periódicamente** | Especialmente tras compartir tu equipo o trabajar en redes públicas. |
| ✅ **Revoca inmediatamente si hay sospecha de filtración** | El daño se reduce con velocidad. |

### 18.2. Verificar `.gitignore`

Abre el archivo `.gitignore` y confirma que contiene al menos:

```
.env
env/
chroma_db_ragas/
__pycache__/
*.pyc
```

> 💡 El archivo `resultados_evaluacion.md` se considera parte del entregable del proyecto, así que puedes decidir si lo subes al repositorio o no.

### 18.3. Qué hacer si filtraste una key

1. Entra a Groq y **revoca** la API Key inmediatamente.
2. Genera una **nueva** y actualiza tu `.env` local.
3. Si la key quedó en Git: usa `git filter-branch` o BFG Repo-Cleaner para purgarla del historial. (Una revocación + nueva key es **siempre** más rápido y seguro.)

---

## 19. Soporte rápido (checklist)

Si algo no funciona, recorre esta lista en orden:

```
[ ] 1. ¿Python 3.10+ instalado?         → python --version
[ ] 2. ¿pip funciona?                   → pip --version
[ ] 3. ¿Estás en la raíz del proyecto?  → dir / ls (debe verse evaluacion_ragas.py)
[ ] 4. ¿Entorno virtual creado?         → existe la carpeta env/
[ ] 5. ¿Entorno virtual activado?       → la terminal muestra (env) al inicio
[ ] 6. ¿Dependencias instaladas?        → pip list (debe verse langchain-groq, ragas, etc.)
[ ] 7. ¿Existe el .env?                 → dir .env  /  ls -la .env
[ ] 8. ¿GROQ_API_KEY tiene valor real?  → abre .env y verifica
[ ] 9. ¿Conexión a internet activa?     → abre cualquier web en el navegador
[ ] 10. ¿Suficiente espacio en disco?   → >500 MB libres
```

Si todos los puntos pasan y aún hay error, copia el mensaje de error completo y revisa la sección [17. Errores comunes y soluciones](#17-errores-comunes-y-soluciones).

---

## 20. Autoría

| | |
|---|---|
| **Autor** | Lina Andrea Bello Ballen |
| **Código** | 506241153 |
| **Fecha de creación** | 07 de marzo de 2026 |
| **Asignatura** | Desarrollo de Aplicaciones con IA |
| **Repositorio** | [Landrea28/DesarrolloDeAplicacionesConIA-2026-1-](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-) |
| **Rama** | `RAG` |

---

> 📘 Esta documentación está pensada para ser autocontenida. Si encuentras un paso confuso o un error que no está cubierto en la sección de troubleshooting, abre un issue en el repositorio.
