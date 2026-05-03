import os
import json
import ollama
from dotenv import load_dotenv
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()  # Load environment variables from .env file

DB_DIR = "db"
OLLAMA_MODEL = "mistral" # Puedes cambiar esto por "llama3" u otro que tengas instalado en ollama

SYSTEM_PROMPT = """
[task]
Eres un Analista de Ciberseguridad. Tu objetivo es clasificar y responder de forma util basandote estrictamente en la documentacion proporcionada,
sin inventar informacion y sin asumir archivos adjuntos.
[/task]

[format]
Responde UNICAMENTE en JSON valido, sin markdown, sin texto extra y sin explicaciones.
Usa exactamente este esquema:
{
  "tema_principal": respuesta clara y concisa sobre el tema principal del problema tecnico o de ciberseguridad,
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
10=malware
11=phishing
12=vulnerabilidades
13=otro
[/topic]

[requirements/constraints]
1. Usa el historial dentro de <<<HISTORIAL>>> y <<<FIN_HISTORIAL>>> para mantener continuidad.
2. Lee la consulta actual entre <<<CONSULTA_USUARIO>>> y <<<FIN_CONSULTA>>>.
3. IMPORTANTE: Basa tu respuesta PRINCIPALMENTE en la informacion dentro de <<<DOCUMENTACION_RELEVANTE>>> y <<<FIN_DOCUMENTACION>>>. Si la respuesta no esta alli, indicalo o pide aclaracion.
4. Responde segun el contexto acumulado de la conversacion.
5. Si el usuario responde tus preguntas, continua desde ahi sin reiniciar el caso.
6. Si hay contexto tecnico suficiente, usa estado="aceptado" y entrega una respuesta practica.
7. Si falta contexto critico, usa estado="requiere_aclaracion" y escribe preguntas concretas en "respuesta".
8. tema_principal siempre debe ser correspondiente a los temas y problemas escritos, debe ser claro y no en numeros.
9. Si requiere aclaracion y no hay suficiente contexto, usa tema_principal=13.
10. No agregues campos adicionales.
[/requirements/constraints]

[few_shot]
Entrada: "He notado actividad inusual en el puerto 443"
Salida esperada: tema_principal= vulnerabilidades, estado=aceptado, respuesta con pasos de mitigacion de la documentacion.

Entrada: "No me deja iniciar sesion en la VPN"
Salida esperada: tema_principal= autenticacion, estado=aceptado, respuesta con pasos de credenciales y bloqueo.

Entrada: "Me ayudas?"
Salida esperada: tema_principal= otro, estado=requiere_aclaracion, respuesta con preguntas puntuales sobre el incidente.
[/few_shot]
""".strip()


def build_prompt(history: list[dict[str, str]], user_text: str, context: str) -> str:
  history_lines = []
  for item in history:
    role = item.get("role", "desconocido").upper()
    content = item.get("content", "").strip()
    history_lines.append(f"{role}: {content}")

  history_text = "\n".join(history_lines) if history_lines else "(sin historial previo)"

  return (
    f"{SYSTEM_PROMPT}\n\n"
    "<<<DOCUMENTACION_RELEVANTE>>>\n"
    f"{context}\n"
    "<<<FIN_DOCUMENTACION>>>\n\n"
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
  try:
    response = ollama.generate(model=OLLAMA_MODEL, prompt=prompt, format='json')
    return response['response'].strip()
  except Exception as e:
    print(f"Error comunicandose con Ollama: {e}")
    print("Asegurate de que Ollama esta corriendo (ollama run mistral)")
    return '{"tema_principal": "otro", "estado": "requiere_aclaracion", "respuesta": "Error de conexion con modelo local."}'


def format_output_for_console(raw_text: str) -> str:
  try:
    parsed = json.loads(raw_text)
    return json.dumps(parsed, ensure_ascii=False, indent=2)
  except json.JSONDecodeError:
    return raw_text

def get_vector_store():
  if not os.path.exists(DB_DIR):
    print("No se encontro la base de datos vectorial. Ejecuta 'python ingest.py' primero.")
    return None
  print("Cargando base de datos vectorial local...")
  embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
  vector_store = FAISS.load_local(DB_DIR, embeddings, allow_dangerous_deserialization=True)
  return vector_store


def main() -> None:
  print("Iniciando componentes...")
  vector_store = get_vector_store()
  if not vector_store:
    return

  print(f"Asistente RAG de Ciberseguridad (Local con {OLLAMA_MODEL}) iniciado.")
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

    print("Buscando en la documentacion local...")
    # Retrieve relevant documents
    docs = vector_store.similarity_search(user_input, k=3)
    context = "\n\n".join([d.page_content for d in docs])
    
    prompt = build_prompt(history, user_input, context)

    print("Generando respuesta con el LLM...")
    answer = generate_support_response(prompt)

    print("\nRespuesta IA:")
    print(format_output_for_console(answer))

    history.append({"role": "usuario", "content": user_input})
    history.append({"role": "asistente", "content": answer})

    # Limita el historial para evitar prompts demasiado largos.
    if len(history) > 20:
      history = history[-20:]

if __name__ == "__main__":
  main()
