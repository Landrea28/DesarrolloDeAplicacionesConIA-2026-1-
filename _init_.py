import os
import json
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
  "tema_principal": respuesta clara y concisa sobre el tema principal del problema tecnico,
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
1. Usa el historial dentro de <<<HISTORIAL>>> y <<<FIN_HISTORIAL>>> para mantener continuidad.
2. Lee la consulta actual entre <<<CONSULTA_USUARIO>>> y <<<FIN_CONSULTA>>>.
3. Responde segun el contexto acumulado de la conversacion.
4. Si el usuario responde tus preguntas, continua desde ahi sin reiniciar el caso.
2. Si hay contexto tecnico suficiente, usa estado="aceptado" y entrega una respuesta practica.
3. Si falta contexto critico, usa estado="requiere_aclaracion" y escribe preguntas concretas en "respuesta".
4. tema_principal siempre debe ser correspondiente a los temas y problemas escritos, debe ser claro y no en numeros.
5. Si requiere aclaracion y no hay suficiente contexto, usa tema_principal=10.
6. No agregues campos adicionales.
[/requirements/constraints]

[few_shot]
Entrada: "Instale el agente, pero al abrirlo aparece missing runtime y se cierra"
Salida esperada: tema_principal= instalacion, estado=aceptado, respuesta con pasos de validacion de runtime.

Entrada: "No me deja iniciar sesion en la intranet"
Salida esperada: tema_principal= autenticacion, estado=aceptado, respuesta con pasos de credenciales y bloqueo.

Entrada: "Me ayudas?"
Salida esperada: tema_principal= otro, estado=requiere_aclaracion, respuesta con preguntas puntuales.
[/few_shot]
""".strip()


def build_prompt(history: list[dict[str, str]], user_text: str) -> str:
  history_lines = []
  for item in history:
    role = item.get("role", "desconocido").upper()
    content = item.get("content", "").strip()
    history_lines.append(f"{role}: {content}")

  history_text = "\n".join(history_lines) if history_lines else "(sin historial previo)"

  return (
    f"{SYSTEM_PROMPT}\n\n"
    "<<<HISTORIAL>>>\n"
    f"{history_text}\n"
    "<<<FIN_HISTORIAL>>>\n\n"
    "[input_delimited]\n"
    "<<<CONSULTA_USUARIO>>>\n"
    f"{user_text.strip()}\n"
    "<<<FIN_CONSULTA>>>\n"
    "[/input_delimited]"
  )


def generate_support_response(prompt: str) -> str:
  response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt,
  )

  if not response.text:
    return '{"tema_principal": otro, "estado": "requiere_aclaracion", "respuesta": "No pude generar respuesta. Intenta nuevamente con mas detalle tecnico."}'

  return response.text.strip()


def format_output_for_console(raw_text: str) -> str:
  try:
    parsed = json.loads(raw_text)
    return json.dumps(parsed, ensure_ascii=False, indent=2)
  except json.JSONDecodeError:
    return raw_text


def main() -> None:
  if not API_KEY:
    print("No se encontro GENAI_API_KEY. Configurala en el archivo .env")
    return

  print("Asistente de soporte tecnico iniciado.")
  print("Escribe tu consulta. Cuando quieras terminar, escribe 'salir'.")

  history: list[dict[str, str]] = []

  while True:
    user_input = input("\nTu consulta: ").strip()

    if user_input.lower() == "salir":
      print("Saliendo del programa.")
      return

    if not user_input:
      print("Escribe una consulta o 'salir'.")
      continue

    prompt = build_prompt(history, user_input)

    try:
      answer = generate_support_response(prompt)
    except Exception as err:
      error_text = str(err)
      if "API key was reported as leaked" in error_text:
        print(
          "Error de autenticacion: tu API key fue reportada como filtrada. "
          "Genera una nueva key y actualiza GENAI_API_KEY en .env"
        )
      elif "403" in error_text:
        print("Error 403: permisos insuficientes o API key invalida.")
      else:
        print(f"Error al consultar el modelo: {error_text}")
      continue

    print("\nRespuesta IA:")
    print(format_output_for_console(answer))

    history.append({"role": "usuario", "content": user_input})
    history.append({"role": "asistente", "content": answer})

    # Limita el historial para evitar prompts demasiado largos.
    if len(history) > 20:
      history = history[-20:]

if __name__ == "__main__":
  main()