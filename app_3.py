import os
from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()  # Load environment variables from .env file  
API_KEY = os.getenv("GENAI_API_KEY")
# Inicializar el cliente
client = genai.Client(api_key=API_KEY)

# 1. Configuración: Rol de Vendedor
sys_instruct = "Eres un vendedor amable de una tienda de tecnología. Ayuda a los clientes a elegir productos y da especificaciones claras."

# 2. Contexto (Few-shot)
history = [
    types.Content(
        role="user",
        parts=[types.Part(text="Hola, ¿tienes laptops para diseño gráfico?")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="¡Hola! Sí, claro. Te recomiendo la ProArt Studiobook. Tiene pantalla OLED 4K, tarjeta gráfica RTX 4070 y 32GB de RAM, ideal para renderizado y diseño preciso.")]
    ),
    types.Content(
        role="user",
        parts=[types.Part(text="¿Y qué tal unos audífonos con buena cancelación de ruido?")]
    ),
    types.Content(
        role="model",
        parts=[types.Part(text="Los Sony WH-1000XM5 son excelentes para eso. Tienen la mejor cancelación de ruido del mercado, 30 horas de batería y sonido de alta fidelidad.")]
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

print("--- Chat Tienda de Tecnología ---")
print("(Escribe 'finalizar' para terminar)\n")

while True:
    user_input = input("Cliente: ")
    if user_input.lower() == "finalizar":
        print("Vendedor: ¡Gracias por tu visita! Hasta luego.")
        break
    
    try:
        response = chat.send_message(user_input)
        print(f"Vendedor: {response.text}\n")
    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")