## 🪸 RECUERDE QUE ESTA EN LA RAMA: Conexion_a_la_API
Rama "main": https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/tree/main?tab=readme-ov-file

CREACION: sabado, 14 de marzo de 2026, 11:44

# Proyecto 1 - Integracion con Gemini para Soporte Tecnico

Este proyecto corresponde al Proyecto 1 de la materia. Implementa un asistente de soporte tecnico en Python que usa Google Gemini para clasificar consultas y responder en formato JSON.

## 🤖 Explicacion del asistente que se crea en este proyecto

El asistente recibe consultas tecnicas por consola y mantiene contexto de conversacion con historial.
Su comportamiento principal es:

1. Clasificar el tema principal de la consulta (instalacion, configuracion, autenticacion, conectividad, etc.).
2. Determinar el estado de la respuesta: `aceptado` o `requiere_aclaracion`.
3. Entregar una respuesta util y concreta en JSON valido.

La logica del asistente esta definida en [_init_.py](_init_.py), usando un prompt de sistema con reglas y ejemplos de salida.

## 📁 Estructura actual del proyecto

- [_init_.py](_init_.py): script principal del asistente.
- [requeriments.txt](requeriments.txt): dependencias del proyecto.
- [.env](.env): variables de entorno (no compartir en publico).
- [README.md](README.md): documentacion.

## 📦 Librerias instaladas (verificadas)

Se revisaron las librerias instaladas en el entorno virtual del proyecto y coinciden con el enfoque actual (Gemini por consola, sin Django). Principales paquetes:

- `google-genai`
- `python-dotenv`
- `requests`
- `httpx`
- `pydantic`
- `tenacity`

Tambien hay dependencias de soporte/transitivas como `anyio`, `websockets`, `cryptography`, entre otras.

## 🛠️ Tecnologias utilizadas

- Python
- Google GenAI (modelo `gemini-2.5-flash`)
- python-dotenv
- JSON para salida estructurada

## 🚀 Instrucciones de instalacion y ejecucion

### 🧭 Flujo recomendado (resumido)

#### 1) 💻 Abrir terminal en VS Code

- Atajo usado en clase: `Ctrl + ñ`

#### 2) 🧪 Crear y activar entorno virtual

Crear entorno:

```bash
python -m venv env
```

Windows:

```bash
.\env\Scripts\Activate
```

macOS/Linux:

```bash
source env/bin/activate
```

#### 3) 🧠 Seleccionar interprete en VS Code

1. Presionar `Ctrl + Shift + P`.
2. Buscar `Python: Select Interpreter`.
3. Elegir el interprete del entorno virtual, por ejemplo `./env/Scripts/python.exe`.
4. Referencia usada en clase: Python 3.13.12 (Microsoft Store).

#### 4) 📦 Instalar librerias (elige una opcion)

Opcion A - Instalacion manual:

```bash
python.exe -m pip install --upgrade pip
pip install requests
pip install google-genai
pip install python-dotenv
```

Opcion B - Instalar todo desde archivo:

```bash
pip install -r requeriments.txt
```

#### 5) 🔐 Configurar credenciales

En el archivo `.env`, definir:

```env
GENAI_API_KEY=TU_API_KEY_AQUI
```

Nota: en este proyecto la variable usada por el codigo es `GENAI_API_KEY`.

#### 6) ▶️ Ejecutar el asistente

```bash
python _init_.py
```

Para salir del programa, escribir `salir`.

## 🧾 Formato de salida esperado

El asistente responde en JSON con esta estructura:

```json
{
	"tema_principal": "configuracion",
	"estado": "aceptado",
	"respuesta": "..."
}
```

## 🖼️ Seccion visual (espacio para evidencias)



- Ejecucion del asistente
- Clasificacion de una consulta
- Caso con `requiere_aclaracion`

## 📌 Notas importantes

- No publicar claves API.
- Mantener el archivo `.env` fuera del control de versiones.
- Si cambias dependencias, actualizar [requeriments.txt](requeriments.txt).

## 👩‍💻 Autor

Lina Andrea Bello Ballen  
Ingenieria de Sistemas  
2026