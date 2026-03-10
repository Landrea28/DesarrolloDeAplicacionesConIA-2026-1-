import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar el cliente con la API Key
client = genai.Client(api_key=API_KEY)

# Definir la instrucción del sistema y la consulta
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explique qué es la 'Inferencia en IA' en menos de 50 palabras."
)

# Imprimir la respuesta
print(response.text)
