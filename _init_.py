import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar el cliente con la API Key
client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
[task]
Eres un Analista de Soporte Tecnico. Tu objetivo es clasificar y responder de forma util,
sin inventar informacion y sin asumir archivos adjuntos.
[/task]

[format]
Responde UNICAMENTE en JSON valido, sin markdown, sin texto extra y sin explicaciones.
Usa exactamente este esquema:
{
  "tema_principal": numero,
  "estado": "aceptado" o "requiere_aclaracion",
  "respuesta": "texto"
}
[/format]

[topic]
Catalogo de tema_principal:
1=instalacion
2=configuracion
3=autenticacion
4=conectividad
5=rendimiento
6=error_aplicacion
7=integraciones
8=seguridad
9=respaldo_recuperacion
10=otro
[/topic]

[requirements/constraints]
1. Lee solo el texto entre <<<CONSULTA_USUARIO>>> y <<<FIN_CONSULTA>>>.
2. Si hay contexto tecnico suficiente, usa estado="aceptado" y entrega una respuesta practica.
3. Si falta contexto critico, usa estado="requiere_aclaracion" y escribe preguntas concretas en "respuesta".
4. tema_principal siempre debe ser un entero entre 1 y 10.
5. Si requiere aclaracion y no hay suficiente contexto, usa tema_principal=10.
6. No agregues campos adicionales.
[/requirements/constraints]

[few_shot]
Entrada: "Instale el agente, pero al abrirlo aparece missing runtime y se cierra"
Salida esperada: tema_principal=1, estado=aceptado, respuesta con pasos de validacion de runtime.

Entrada: "No me deja iniciar sesion en la intranet"
Salida esperada: tema_principal=3, estado=aceptado, respuesta con pasos de credenciales y bloqueo.

Entrada: "Me ayudas?"
Salida esperada: tema_principal=10, estado=requiere_aclaracion, respuesta con preguntas puntuales.
[/few_shot]
""".strip()


def build_prompt(user_text: str) -> str:
  return (
    f"{SYSTEM_PROMPT}\n\n"
    "[input_delimited]\n"
    "<<<CONSULTA_USUARIO>>>\n"
    f"{user_text.strip()}\n"
    "<<<FIN_CONSULTA>>>\n"
    "[/input_delimited]"
  )


def has_enough_context(user_text: str) -> bool:
  text = user_text.strip().lower()
  if len(text) < 8:
    return False

  vague_inputs = {
    "no se",
    "nose",
    "ayuda",
    "hola",
    "no",
    "si",
    "xd",
  }

  if text in vague_inputs:
    return False

  return len(user_text.strip().split()) >= 3


def main() -> None:
  if not API_KEY:
    print("No se encontro GENAI_API_KEY. Configurala en el archivo .env")
    return

  user_input = input("Escribe la consulta tecnica: ").strip()

  while not has_enough_context(user_input):
    print(
      "Necesito una consulta mas concreta para ayudarte. "
      "Incluye sistema/modulo, error exacto y que accion realizaste."
    )
    user_input = input("Describe mejor el problema tecnico: ").strip()

  prompt = build_prompt(user_input)

  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
  )

  print(response.text)


if __name__ == "__main__":
  main()