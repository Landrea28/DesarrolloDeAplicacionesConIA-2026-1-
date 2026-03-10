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
    contents="TAREA= Escribe un correo para un cliente que no ha pagado"
    "FORMATO=Formato formal, cortesía, respetuoso"
    "TEMA = Recordatorio de pago pendiente"
    "TONO = Profesional, amable"
    "CONTEXTO = El cliente ha recibido el producto pero no ha realizado el pago dentro del plazo acordado."
    "REQUISITOS = Incluir una solicitud de pago, ofrecer opciones de pago, y expresar disposición para resolver cualquier duda o inconveniente que el cliente pueda tener." \
    "CONDICIONALES = El correo debe ser claro, conciso y no debe contener lenguaje amenazante o agresivo."
    "ELEMENTOS OPCIONALES = Incluir un número de contacto o dirección de correo electrónico para que el cliente pueda comunicarse fácilmente."
)

# Imprimir la respuesta
print(response.text)