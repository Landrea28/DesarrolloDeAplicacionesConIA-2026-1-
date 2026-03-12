import os
from wsgiref import types
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar el cliente con la API Key
client = genai.Client(api_key=API_KEY)

# Definir la instrucción del sistema y la consulta
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=
    """Contexto: Eres un asistente de triaje de correos electrónicos de soporte de una plataforma de cursos en línea.
        Instrucciones: Se te proporcionará un texto delimitado por \"\"\".
        SI el texto contiene una queja sobre un pago o factura:
        Clasifícalo como "URGENTE-FINANZAS".
        Extrae el número de factura si existe.
        SI NO, si el texto es una duda técnica general:
        Clasifícalo como "SOPORTE-ESTÁNDAR".
        Responde: "Gracias, un técnico lo revisará".
        SI NO es ninguna de las anteriores:
        Responde simplemente: "Categoría no identificada".
        Texto del Usuario: \"\"\" Hola, no puedo acceder al curso de SQL; la página se queda cargando desde ayer. \"\"\"
        """

)

# Imprimir la respuesta
print(response.text)