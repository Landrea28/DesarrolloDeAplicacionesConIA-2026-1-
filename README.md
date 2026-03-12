CREACION: martes, 3 de marzo de 2026, 20:38

# 🪸 RECUERDE QUE ESTA EN LA RAMA: Tutor_de_IA

# Tutor Socrático de Desarrollo Web con IA 🤖🌐

Este proyecto es una aplicación web construida con **Django** que integra la inteligencia artificial de **Google Gemini** para actuar como un tutor. Utiliza un enfoque socrático para enseñar a los estudiantes sobre desarrollo web (HTML, CSS, JavaScript, etc.), guiándolos mediante preguntas en lugar de darles las respuestas directas.

## 🛠️ Tecnologías utilizadas

* **Python** (Lenguaje principal)
* **Django** (Framework web para la interfaz y servidor)
* **Google GenAI** (Modelo de inteligencia artificial Gemini 2.5 Flash)
* **python-dotenv** (Manejo de variables de entorno y mayor seguridad)
* **HTML/CSS** (Para la interfaz visual del chat)

---

## 🚀 Instrucciones de Instalación y Ejecución

Sigue estos pasos para poder ejecutar el proyecto en tu entorno local:

### 1. Clonar o descargar el repositorio
Abre una terminal y ubícate en la carpeta raíz del proyecto.

### 2. Crear y activar un entorno virtual
Es una buena práctica ejecutar este proyecto dentro de un entorno virtual para no afectar otras instalaciones de Python.

**En Windows:**
```bash
python -m venv env
env\Scripts\activate
```

**En macOS / Linux:**
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Instalar las dependencias
Con el entorno virtual activado, instala todas las librerías necesarias ejecutando:
```bash
pip install -r requirements.txt
```

### 4. Configurar las variables de entorno
El proyecto requiere una llave de API de Google GenAI para funcionar.
1. Crea un archivo llamado `.env` en la raíz del proyecto (al lado de `manage.py`). Ya esta creado profe, solo ponga su API key. 
2. Agrega tu clave de la siguiente manera:
```env
GENAI_API_KEY="AIzaSy...TU_CLAVE_AQUI"
```

### 5. Configurar la base de datos (Migraciones)
Django requiere inicializar su base de datos local predeterminada. Ejecuta el siguiente comando:
```bash
python manage.py migrate
```

### 6. Iniciar el servidor web
Finalmente, levanta el servidor de desarrollo de Django:
```bash
python manage.py runserver
```

### 7. Probar la aplicación
Abre tu navegador web favorito y dirígete a la siguiente dirección:
👉 **http://127.0.0.1:8000/**

¡Listo! Ya puedes empezar a interactuar con el tutor de desarrollo web en la interfaz.

---
**Desarrollado para la clase de Desarrollo de Aplicaciones con IA.**

