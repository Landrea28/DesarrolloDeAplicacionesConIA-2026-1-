## 🪸 RECUERDE QUE ESTA EN LA RAMA: ProyectoFinal
Rama "main": https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/tree/main?tab=readme-ov-file

CREACION 1: sabado, 14 de marzo de 2026, 11:44
CREACION 2: sabado, 2 de mayo de 2026, 16:00

# Proyecto - Asistente RAG de Ciberseguridad (100% Local)

Este proyecto desarrolla un asistente de ciberseguridad basado en la arquitectura RAG (Retrieval-Augmented Generation) operando completamente en local para preservar la privacidad de los datos.

## 🛠️ Explicación de la Arquitectura

1. **Base de Conocimiento (FAISS)**: El sistema lee archivos `.pdf` y `.md` ubicados en la carpeta `docs/`, dividiéndolos en fragmentos e indexándolos mediante embeddings de HuggingFace (`all-MiniLM-L6-v2`) a una base de datos local rápida (FAISS).
2. **Modelo LLM Local (Ollama)**: Reemplazamos Google Gemini por modelos de lenguaje Open Source (como Mistral o Llama 3) corriendo localmente mediante `Ollama`.
3. **Respuesta Estructurada**: El LLM recibe el fragmento de la documentación más relevante, la historia del chat y la pregunta actual para generar una respuesta en formato estrictamente JSON.

## 📂 Estructura actual del proyecto

- `_init_.py`: script principal del asistente RAG y chat.
- `ingest.py`: motor de indexación (convierte los documentos de `docs/` a vectores en `db/`).
- `docs/`: carpeta donde se deben ubicar los manuales en PDF, Markdown o TXT.
- `db/`: carpeta generada automáticamente con la base de datos vectorial FAISS.
- `requirements.txt`: dependencias del proyecto.
- `.env`: variables de entorno.

## 🚀 Tecnologías utilizadas

- Python
- Ollama (Modelos Open Source locales como `mistral` o `llama3`)
- LangChain (Orquestación RAG y partición de texto)
- FAISS (Vector Database local por Meta)
- HuggingFace Embeddings (Modelos ligeros locales de vectorización)

## 🔧 Instrucciones de instalación y ejecución

### 1) Crear y activar entorno virtual

Crear entorno:
```bash
python -m venv env
```
Activar (Windows):
```bash
.\env\Scripts\Activate
```

### 2) Instalar librerías
```bash
pip install -r requirements.txt
```

### 3) Instalar y Configurar Ollama
1. Descarga e instala [Ollama](https://ollama.com/). 
	O puedes usar un comando...
		En Windows: irm https://ollama.com/install.ps1 | iex
		En Linux y En macOS: curl -fsSL https://ollama.com/install.sh | sh
2. Abre una terminal normal en tu equipo y descarga el modelo base ejecutando:
```bash
ollama run mistral
```
*(Puedes salir de esa terminal luego o dejarla corriendo de fondo).*

### 4) Ingesta de Documentos (Fase 2)
Coloca todos los manuales, leyes o guías en la carpeta `docs/`. Luego ejecuta:
```bash
python ingest.py
```
Esto leerá los documentos y creará la base de datos vectorial en `db/`.

### 5) Ejecutar el asistente (Fase 3)
```bash
python _init_.py
```
El asistente leerá el historial, recuperará el contexto de la base de datos y le pedirá a Ollama una respuesta estructurada en formato JSON.

## 🧾 Formato de salida esperado

El asistente responde en JSON con esta estructura:

```json
{
	"tema_principal": "configuracion",
	"estado": "aceptado",
	"respuesta": "..."
}
```

## 📌 Notas importantes

- No publicar claves API.
- Mantener el archivo `.env` fuera del control de versiones.
- Si cambias dependencias, actualizar [requeriments.txt](requeriments.txt).

## 👩‍💻 Autor

Lina Andrea Bello Ballen  
Ingenieria de Sistemas  
2026