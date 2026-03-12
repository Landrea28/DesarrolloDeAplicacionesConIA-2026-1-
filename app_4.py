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
    contents="[task= Escribe una explicacion de blog detallada sobre las ventajas de usar microservicios.] [format=blog] [topic=ventajas de microservicios] [tone=informal] [context=desarrollo de software moderno] [requirements/constraints=debe ser entre 500 y 1000 palabras] [optional elements=ejemplos prácticos]"
)

# Imprimir la respuesta
print(response.text)
