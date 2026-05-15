# Asistente RAG de Ciberseguridad (Django + Groq + Hugging Face)

## Introduccion

Este proyecto es un asistente de ciberseguridad basado en RAG (Retrieval-Augmented Generation). Permite cargar un documento (PDF, TXT o MD), indexarlo en memoria y responder preguntas usando exclusivamente el contenido de ese documento. La aplicacion aplica reglas de seguridad para validar que la pregunta sea de ciberseguridad y que la respuesta exista en el contexto. Si la informacion no esta en el documento, la respuesta es un mensaje fijo y verificable.

Problema que resuelve
1. Evita alucinaciones, porque las respuestas se basan en fragmentos reales del documento.
2. Facilita auditoria al mostrar el chunk exacto utilizado.
3. Simplifica consultas tecnicas de ciberseguridad para usuarios no expertos en comandos.

Lo que puede hacer el usuario
1. Subir un documento de ciberseguridad.
2. Hacer preguntas sobre ese documento.
3. Ver la fuente exacta usada en la respuesta.
4. Ejecutar una evaluacion automatica con 10 preguntas de rubrica.

---

## Tecnologias usadas (y su rol en este proyecto)

| Tecnologia | Que es | Para que se usa aqui |
|---|---|---|
| Python | Lenguaje de programacion | Backend, scripts y automatizacion |
| Django | Framework web de Python | Vistas, rutas, sesiones y templates |
| SQLite | Base de datos local | Base de datos por defecto de Django |
| Hugging Face | Hub de modelos | Descarga de embeddings multilingues |
| Groq | LLM en la nube | Genera respuestas con reglas de seguridad |
| Variables de entorno | Configuracion externa | Guarda credenciales sin exponerlas |
| API Keys | Tokens de acceso | Permiten usar Groq y Hugging Face |
| Entorno virtual | Aislamiento de dependencias | Evita conflictos entre proyectos |
| requirements.txt | Lista de dependencias | Define librerias exactas a instalar |
| pip | Instalador de paquetes | Instala dependencias del proyecto |

---

## Estructura del proyecto

```
DesarrolloDeAplicacionesConIA-2026-1-/
├─ ciber_rag/                 # Configuracion principal de Django
├─ rag_app/                   # Aplicacion principal (vistas y logica RAG)
│  ├─ templates/rag_app/       # HTML del frontend
│  ├─ rag_service.py           # Motor RAG + reglas de seguridad
├─ scripts/                   # Scripts de evaluacion
│  ├─ evaluate_rubric.py       # Script para ejecutar 10 preguntas
├─ docs/                      # Documentos PDF, TXT o MD
├─ media/                     # Subidas por sesion (se crea al ejecutar)
├─ db.sqlite3                 # Base de datos SQLite de Django
├─ manage.py                  # Comando principal de Django
├─ requirements.txt           # Dependencias del proyecto
├─ rubric_questions.txt       # 10 preguntas de rubrica
└─ README.md                  # Esta documentacion
```

---

## Requisitos previos

1. Computador con Windows, macOS o Linux.
2. Conexion a internet (descarga de dependencias y modelos).
3. Cuenta en Groq y Hugging Face para obtener API Keys.

---

## Descargar el proyecto

### Opcion 1 — Clonar el repositorio

Que es GitHub
GitHub es una plataforma para alojar proyectos de software. Un repositorio contiene todos los archivos del proyecto.

Clonar con GitKraken (interfaz grafica)
1. Instala GitKraken: https://www.gitkraken.com/download
2. Abre GitKraken y conecta tu cuenta de GitHub si aplica.
3. Haz clic en **Clone a repo**.
4. Pega la URL del repositorio.
5. Selecciona una carpeta de destino.
6. Anota la ruta final donde se creo el proyecto.

Clonar con terminal (git clone)
1. Instala Git: https://git-scm.com/downloads
2. Abre la terminal.
3. Ubicate en la carpeta donde quieres guardar el proyecto.
4. Ejecuta:
```bash
git clone URL_DEL_REPOSITORIO
```
5. Anota la ruta resultante (por ejemplo, `C:\Proyectos\DesarrolloDeAplicacionesConIA-2026-1-`).

### Opcion 2 — Descargar ZIP

1. En GitHub, entra al repositorio.
2. Haz clic en **Code**.
3. Selecciona **Download ZIP**.
4. Extrae el ZIP en una carpeta facil de recordar.
5. Esa carpeta extraida es la raiz del proyecto.

---

## Visual Studio Code

Que es VS Code
VS Code es un editor gratuito que facilita abrir carpetas de proyectos, ver archivos y usar terminal integrada.

Instalacion
1. Descarga: https://code.visualstudio.com/
2. Instala con opciones por defecto.

Abrir el proyecto
1. Abre VS Code.
2. Ve a **File > Open Folder...**
3. Selecciona la carpeta raiz (contiene `manage.py`).
4. Veras la estructura en el panel izquierdo.

Como identificar la raiz del proyecto
La carpeta raiz contiene:
1. `manage.py`
2. `requirements.txt`
3. Las carpetas `ciber_rag/` y `rag_app/`

---

## Archivo .env

Que es un archivo .env
Es un archivo de texto que guarda variables sensibles como API Keys. No se comparte porque contiene credenciales privadas.

Donde debe crearse
En la raiz del proyecto, junto a `manage.py`.

Como crear el archivo
1. En la carpeta raiz, crea un archivo llamado exactamente `.env`.
2. Verifica que no sea `.env.txt`.
3. En Windows, activa la vista de extensiones de archivo para evitar errores.

Contenido exacto esperado
```
GROQ_API_KEY=your_key_here
HF_TOKEN=your_token_here
```

---

## Como obtener las API Keys

### Groq API Key (LLM)
1. Entra a https://console.groq.com
2. Crea una cuenta o inicia sesion.
3. Ve a **API Keys**.
4. Crea una nueva key.
5. Copia la key y pegala en `.env`.

### Hugging Face Token (embeddings)
1. Entra a https://huggingface.co
2. Inicia sesion.
3. Ve a tu perfil > **Settings**.
4. En el menu izquierdo, entra a **Access Tokens**.
5. Crea un token con permisos **Read**.
6. Copia el token y pegalo en `.env`.

---

## Entorno virtual (venv)

Que es
Un entorno virtual es una carpeta aislada que contiene Python y librerias para este proyecto. Evita conflictos con otras aplicaciones.

Por que es importante
Cada proyecto puede requerir versiones especificas. El entorno virtual asegura que la instalacion sea predecible.

### Crear y activar

Windows (PowerShell)
```powershell
python -m venv env
env\Scripts\Activate.ps1
```

Linux
```bash
python3 -m venv env
source env/bin/activate
```

macOS
```bash
python3 -m venv env
source env/bin/activate
```

Como verificar que esta activo
La terminal mostrara un prefijo como `(env)` al inicio de la linea.

---

## Instalacion de dependencias

Que es `requirements.txt`
Es un listado de todas las librerias necesarias para ejecutar el proyecto.

Como instalar con pip
```bash
pip install -r requirements.txt
```

Si aparece un warning de Hugging Face
Es un aviso de que no estas autenticado. No detiene la ejecucion, pero puede limitar descargas. Se soluciona agregando `HF_TOKEN` en el `.env`.

---

## Base de datos

Que base de datos usa el proyecto
SQLite, ubicada en `db.sqlite3`.

Por que se usa SQLite
No requiere servidor ni configuracion adicional. Es ideal para entornos locales y prototipos.

Como se inicializa
Ejecuta migraciones con:
```bash
python manage.py migrate
```

---

## Como funciona el motor RAG en este proyecto

1. El usuario sube un PDF, TXT o MD.
2. El backend lo divide en chunks.
3. Se generan embeddings con Hugging Face.
4. Se crea un indice FAISS por sesion.
5. Al preguntar, se recupera el chunk mas relevante.
6. Groq genera la respuesta aplicando reglas estrictas.

Reglas de seguridad y respuestas oficiales
1. Si el documento o la pregunta no son de ciberseguridad, el sistema responde:
```
Lo siento soy un modelo entrenado para resolver dudad concretas de documentos concretos de CIBERSEGURIDAD
```
2. Si la respuesta no esta en el contexto, el sistema responde:
```
No encuentro esa información en el reglamento
```

---

## Ejecutar el proyecto (Django)

### 1. Migraciones
```bash
python manage.py migrate
```

### 2. Iniciar el servidor
```bash
python manage.py runserver
```

### 3. Abrir en el navegador
Visita:
```
http://127.0.0.1:8000/
```

### 4. Como saber si inicio correctamente
En la terminal veras algo similar a:
```
Starting development server at http://127.0.0.1:8000/
```

### 5. Como detener el servidor
En la terminal presiona:
```
Ctrl + C
```

---

## Ejecutar la evaluacion de rubrica (Fase 5)

1. Abre `rubric_questions.txt`.
2. Verifica que tenga 10 preguntas, una por linea.
3. Ejecuta:
```bash
python scripts/evaluate_rubric.py
```
4. Resultados generados:
1. `reports/rubric_results.json`
2. `reports/rubric_results.csv`

---

## Errores comunes y soluciones

### Python no reconocido
Sintoma
`python` no se reconoce como comando.

Solucion
Instala Python desde https://www.python.org/downloads/ y marca **Add Python to PATH**.

### pip no reconocido
Sintoma
`pip` no se reconoce como comando.

Solucion
Ejecuta:
```bash
python -m pip --version
```
Si falla, reinstala Python.

### Entorno virtual no activo
Sintoma
No aparece `(env)` en la terminal.

Solucion
Activa el entorno con los comandos indicados en tu sistema.

### Falta archivo .env o variables
Sintoma
Error: `Falta la variable de entorno GROQ_API_KEY`.

Solucion
Crea `.env` en la raiz y agrega `GROQ_API_KEY` y `HF_TOKEN`.

### API Key invalida
Sintoma
Errores de autenticacion o respuestas vacias.

Solucion
Verifica que la key este completa, sin espacios y que pertenezca a tu cuenta.

### Puerto ocupado
Sintoma
`Address already in use`.

Solucion
Inicia el servidor en otro puerto:
```bash
python manage.py runserver 8001
```

### Dependencias faltantes
Sintoma
`ModuleNotFoundError`.

Solucion
Ejecuta:
```bash
pip install -r requirements.txt
```

---

## Seguridad de credenciales

1. No publiques el archivo `.env`.
2. No subas API Keys a GitHub.
3. Si compartes el proyecto, elimina credenciales antes.

---

## Soporte rapido (orden recomendado de verificacion)

1. Entorno virtual activo.
2. `.env` creado con claves validas.
3. Dependencias instaladas.
4. Migraciones ejecutadas.

---

## Autor

Lina Andrea Bello Ballen
