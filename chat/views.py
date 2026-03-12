import os
from django.shortcuts import render
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Cargar variables de entorno (Asegúrate de que tu archivo .env esté en la raíz del proyecto)
load_dotenv()
API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar cliente Gemini
client = genai.Client(api_key=API_KEY)

sys_instruct = "Eres un tutor socratico de nuevas tecnologias de desarrollo de software, TAREA: tarea es enseñarle a los estudiantes con base a filosofia de socrates 'No puedo enseñar nada a nadie, solo puedo hacerles pensar'. Para esto, debes responder a las preguntas de los estudiantes con preguntas que los guíen a descubrir la respuesta por sí mismos. Evita dar respuestas directas y fomenta el pensamiento crítico." 

# Contexto igual al de tu taller
history = [
    types.Content(role="user", parts=[types.Part(text="Ayudame a hacer un sitio web..")]),
    types.Content(role="model", parts=[types.Part(text="¡Claro! Para empezar, ¿qué tipo de sitio web...")]),
]

# Inicializamos el chat a nivel global
chat_gemini = client.chats.create(
    model="gemini-2.5-flash",
    config=types.GenerateContentConfig(
        max_output_tokens=500,
        system_instruction="Eres un tutor socrático. Evita dar respuestas directas. Tema: Desarrollo web. Si el estudiante se desvía del tema, redirígelo con una pregunta. Si la pregunta es muy general, pide que la especifique."
    ),
    history=history
)

def index(request):
    # Por defecto, no hay respuesta
    contexto = {}

    # Si el usuario mandó una pregunta a través del formulario web (Método POST)
    if request.method == "POST":
        pregunta_usuario = request.POST.get("pregunta") # Obtenemos lo que escribió
        
        try:
            # Enviamos la pregunta a Gemini
            response = chat_gemini.send_message(pregunta_usuario)
            
            # Guardamos la pregunta y la respuesta para enviarlas al HTML
            contexto = {
                "pregunta": pregunta_usuario,
                "respuesta": response.text
            }
        except Exception as e:
            contexto = {"respuesta": f"Lo siento, ocurrió un error: {str(e)}"}

    # Cargamos el HTML y le pasamos el contexto (variables)
    return render(request, "chat/index.html", contexto)
