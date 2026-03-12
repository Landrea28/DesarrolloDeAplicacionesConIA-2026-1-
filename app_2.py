import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def procesar_articulo(texto, tarea):
    """
    Procesa un texto según la tarea especificada: 'resumir' o 'profesionalizar'.
    Utiliza una system_instruction de 'Editor Editorial de prestigio'.
    """
    
    API_KEY = os.getenv("GENAI_API_KEY")
    if not API_KEY:
        return "Error: API Key no encontrada en variables de entorno."

    client = genai.Client(api_key=API_KEY)

    # Configuración con la restricción solicitada
    # System instruction define el rol de la IA
    sys_instruction = "Eres un Editor Editorial de prestigio."

    model_config = types.GenerateContentConfig(
        system_instruction=sys_instruction,
        temperature=0.3
    )
    
    # Construcción del prompt según la tarea
    if tarea.lower() == "resumir":
        prompt = f"Tu tarea es generar un resumen ejecutivo del siguiente texto:\n\n{texto}"
    elif tarea.lower() == "profesionalizar":
        prompt = f"Tu tarea es editar el siguiente texto para que suene formal y técnico:\n\n{texto}"
    else:
        return "Error: Tarea no reconocida. Use 'resumir' o 'profesionalizar'."

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt,
            config=model_config
        )
        
        return response.text
    except Exception as e:
        return f"Error al procesar la solicitud: {str(e)}"

# Bloque de prueba
if __name__ == "__main__":
    texto_ejemplo = """
    La cosa es que la inteligencia artificial se está poniendo muy loca. 
    Ayer vi una herramienta que hace videos de la nada y me quedé. 
    Esto va a cambiar todo de cómo trabajamos, seguro.
    """

    print("--- Prueba 1: Resumir ---")
    resultado_resumen = procesar_articulo(texto_ejemplo, "resumir")
    print(resultado_resumen)
    
    print("\n--- Prueba 2: Profesionalizar ---")
    resultado_profesional = procesar_articulo(texto_ejemplo, "profesionalizar")
    print(resultado_profesional)
