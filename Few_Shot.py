import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()  # Load environment variables from .env file  
API_KEY = os.getenv("GENAI_API_KEY")
# Inicializar el cliente
client = genai.Client(api_key=API_KEY)

# 1. Configuración: Rol de Clasificador
sys_instruct = "Eres un clasificador de sentimientos para reseñas de libros. Solo debes responder con una palabra: POSITIVO, NEUTRAL o NEGATIVO."

# 2. Contexto (Few-shot) con 3 ejemplos
history = [
    types.Content(
        role="user",
        parts=[types.Part(text="Me encantó este libro, los personajes son increíbles y la trama te atrapa desde el principio.")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="POSITIVO")]
    ),
    types.Content(
        role="user",
        parts=[types.Part(text="Es un libro pasable, tiene partes buenas pero otras muy aburridas.")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="NEUTRAL")]
    ),
    types.Content(
        role="user",
        parts=[types.Part(text="Pésimo libro, no lo recomiendo para nada, una pérdida de tiempo.")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="NEGATIVO")]
    )
]

# Inicialización del chat
chat = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        system_instruction=sys_instruct
    ),
    history=history
)

print("--- Clasificador de Sentimientos de Reseñas de Libros ---")
reseña = "Este libro empezó bien pero el final fue muy apresurado y decepcionante."
print(f"Reseña a clasificar: '{reseña}'\n")

try:
    response = chat.send_message(reseña)
    print(f"Clasificación: {response.text}")
except Exception as e:
    print(f"Error al procesar la solicitud: {e}")