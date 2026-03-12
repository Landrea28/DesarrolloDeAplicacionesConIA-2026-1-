CREACION: martes, 10 de febrero de 2026, 20:30

# 🪸 RECUERDE QUE ESTA EN LA RAMA: Conexion_a_la_API
## Rama "main": https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/tree/main?tab=readme-ov-file

# Integración Básica con Gemini API

Este proyecto corresponde a la entrega de la práctica de **Desarrollo de Aplicaciones con IA**.

## 📋 Contenido del Repositorio
Se incluyen los scripts solicitados en la guía de la práctica:
1. `pruebaEntorno.py`: Script de validación del entorno (citado en la guía como `prueba_entorno.py`).
2. `app_gemini.py`: Script principal de conexión con Google Gemini.
3. `requirements.txt`: Archivo con las dependencias necesarias.
4. `.gitignore`: Configuración para excluir archivos sensibles y temporales.

## 🚀 Guía de Ejecución (Paso a Paso)

Para probar este código localmente, siga estos pasos estandarizados para replicar el entorno de desarrollo:

### 1. Creación del Entorno Virtual (VENV)
El entorno virtual no se incluye en el repositorio por buenas prácticas. Debe crearse localmente:

```bash
# Crear el entorno virtual
python -m venv venv

# Activar el entorno (Windows):
.\venv\Scripts\activate

# Activar el entorno (macOS/Linux):
source venv/bin/activate
```

### 2. Configuración en VS Code (Requerido)
Para asegurar que VS Code use el intérprete correcto creado en el paso anterior:
1.  Presione `Ctrl + Shift + P`.
2.  Busque: **"Python: Select Interpreter"**.
3.  Seleccione la opción asociada a la carpeta `venv` (ej: `.\venv\Scripts\python.exe`).

### 3. Instalación de Dependencias
Instale todas las librerías necesarias (`google-genai`, `python-dotenv`, `requests`) de una sola vez:

```bash
pip install -r requirements.txt
```

### 4. Configuración de Credenciales
Por seguridad, la API Key no está en el repositorio.
1.  Cree un archivo `.env` en la raíz.
2.  Agregue su clave de Google AI Studio:

```env
GEMINI_API_KEY=SU_CLAVE_API_AQUI
```

---

## 🧪 Verificación y Pruebas

### Paso A: Validar Entorno
Ejecute este script para confirmar que las librerías base funcionan correctamente:

```bash
python pruebaEntorno.py
```
**Resultado esperado:** Mensaje confirmando "Entorno Virtual ACTIVO".

### Paso B: Ejecutar Consulta a Gemini
Ejecute el script principal para conectar con la IA:

```bash
python app_gemini.py
```

**Resultado esperado:**
La terminal mostrará el saludo inicial, conectará con la API y devolverá una presentación generada por el modelo `gemini-3-flash-preview` simulando ser un programador Full Stack.

## 📸 Evidencia de Ejecución

![Captura de pantalla de la terminal mostrando la respuesta de Gemini](./img/demo_resultado.png)
*(Nota: La imagen esta en la carpeta 'img' del repositorio)*
