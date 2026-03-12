CREACION: martes, 24 de febrero de 2026, 21:07

# Prompt Engineering con Google Gemini

Ejemplos de técnicas de Prompt Engineering usando la API de Google Gemini (google-genai) en Python.

## Archivos

| Archivo | Descripción |
|---|---|
| `Few_Shot.py` | Clasificador de sentimientos usando ejemplos few-shot |
| `Estructura.py` | Generación de respuestas con estructura definida |
| `Evaluador.py` | Evaluación de respuestas con criterios específicos |
| `Condicional.py` | Prompts con lógica condicional |

---

## Requisitos previos

- Python 3.10 o superior
- Una API Key de Google Gemini → [Obtenerla aquí](https://aistudio.google.com/app/apikey)

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd Prompt_Engineering
```

### 2. Crear y activar el entorno virtual

```bash
# Crear el entorno virtual
python -m venv env

# Activar en Windows (CMD)
env\Scripts\activate.bat

# Activar en Windows (PowerShell)
env\Scripts\Activate.ps1

# Activar en Linux/Mac
source env/bin/activate
```

### 3. Instalar las dependencias

```bash
pip install -r requeriments.txt
```

### 4. Configurar la API Key

Crear un archivo `.env` en la carpeta `Prompt_Engineering/` con el siguiente contenido:

```
GENAI_API_KEY=tu_api_key_aqui
```

> **Importante:** El archivo `.env` no se sube al repositorio (está en `.gitignore`). Cada persona debe crear el suyo propio.

---

## Ejecución

Con el entorno virtual activado, ejecutar cualquiera de los scripts:

```bash
python Few_Shot.py
python Estructura.py
python Evaluador.py
python Condicional.py
```

---

## Solución de problemas

- **Error `ModuleNotFoundError`**: Asegúrate de haber activado el entorno virtual antes de correr el script.
- **Error de API Key**: Verifica que el archivo `.env` existe y que la variable se llama exactamente `GENAI_API_KEY`.
- **PowerShell no permite ejecutar scripts**: Ejecuta `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y luego activa el entorno virtual de nuevo.

