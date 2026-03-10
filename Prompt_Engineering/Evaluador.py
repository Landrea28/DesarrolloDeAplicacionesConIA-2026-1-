import os
from dotenv import load_dotenv
from google import genai

load_dotenv()  # Load environment variables from .env file

API_KEY = os.getenv("GENAI_API_KEY")

# Inicializar el cliente con la API Key
client = genai.Client(api_key=API_KEY)

# Prompt estructurado para el evaluador académico
prompt = """
ROL: Eres un evaluador académico especializado en análisis y crítica de ensayos.

ENTRADA: 
Evalúa el siguiente ensayo:

"Desde su publicación en 1915, La metamorfosis de Franz Kafka ha sido considerada una de las narraciones más enigmáticas y representativas del siglo XX. La historia de Gregorio Samsa, un hombre que despierta convertido en insecto, trasciende lo fantástico y se convierte en una metáfora de la alienación, la incomunicación y la fragilidad de la existencia moderna.
En el relato la transformación física de Gregorio contrasta con la indiferencia y el rechazo de su familia. Mientras él intenta adaptarse a su nueva condición, su entorno lo margina, tratándolo como una carga. El verdadero horror de la obra no radica en el monstruo en que se ha convertido, sino en la frialdad con la que sus seres queridos lo relegan hasta desear su desaparición.
La crítica ha ofrecido diversas lecturas. Algunos intérpretes, como Stanley Corngold, destacan que la metamorfosis representa el choque entre individuo y sociedad, subrayando la incapacidad de la familia de aceptar lo distinto. Otros, como Günther Anders, consideran que Kafka retrata la mecanización de la vida moderna, donde el hombre, reducido a engranaje laboral, pierde su identidad hasta volverse desechable.
Más de un siglo después, la obra de Kafka conserva su vigencia. En un mundo atravesado por el aislamiento, la precariedad laboral y la presión social, Gregorio Samsa encarna la soledad de quienes no logran responder a las expectativas de productividad.
Tal vez, La metamorfosis no sea únicamente la historia de un hombre convertido en insecto, sino la denuncia de un sistema que, aún hoy, convierte en invisibles a los que no encajan."

CONDICIONALES:
1. Primero, cuenta el número de palabras en el ensayo.
2. Si tiene menos de 100 palabras: RECHÁZALO y solicita más contenido (mínimo 100 palabras).
3. Si tiene 100 palabras o más: Evalúalo bajo estos criterios:
   - Ortografía: Verifica errores gramaticales y de puntuación (0-10)
   - Coherencia: Analiza la estructura lógica y fluidez del texto (0-10)
   - Argumentación: Evalúa la solidez y relevancia de los argumentos presentados (0-10)

SALIDA: 
Responde ÚNICAMENTE en formato JSON con la siguiente estructura:
{
  "palabras_totales": número,
  "estado": "aceptado" o "rechazado",
  "nota_final": número (promedio de los tres criterios) o null si fue rechazado,
  "criterios": {
    "ortografia": número,
    "coherencia": número,
    "argumentacion": número
  },
  "comentarios": "texto con análisis detallado"
}
"""

# Realizar la solicitud a la API
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents=prompt
)

# Imprimir la respuesta
print(response.text)