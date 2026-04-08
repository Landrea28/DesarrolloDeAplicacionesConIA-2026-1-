# # 🪸 RECUERDE QUE ESTA EN LA RAMA: TF-IDF
## Rama "main": https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/tree/main?tab=readme-ov-file 

Este proyecto implementa un motor de búsqueda básico en Python utilizando el algoritmo **TF-IDF (Term Frequency - Inverse Document Frequency)**. Su propósito es encontrar los artículos o reglamentos académicos más relevantes dentro de una colección de documentos, basándose en una consulta de texto proporcionada por el usuario.

## Descripción del Proyecto ✨

El script `# tf-idf.py` contiene una lista de documentos (artículos de un reglamento universitario) y una consulta predefinida. El algoritmo calcula la relevancia de cada documento para la consulta dada siguiendo estos pasos:

1. **TF (Frecuencia de Término):** Calcula con qué frecuencia aparece cada palabra de la consulta en un documento específico.
2. **IDF (Frecuencia Inversa de Documento):** Mide la importancia de la palabra en el conjunto total de documentos. Las palabras comunes en todos los documentos reciben un peso menor, mientras que las raras obtienen un peso mayor.
3. **Score Final:** Multiplica TF por IDF para cada palabra y suma los resultados para obtener la puntuación total del documento.

## Requisitos Previos 🛠️

Para ejecutar este proyecto, necesitas tener instalado Python y la biblioteca `numpy` (utilizada para calcular el logaritmo natural en la fórmula del IDF).

Puedes instalar la dependencia ejecutando:

```bash
pip install numpy
```

## Instrucciones de Ejecución 👩‍🏫

1. Abre una terminal o línea de comandos.
2. Navega hasta el directorio donde se encuentra el archivo `# tf-idf.py`.
3. Ejecuta el script con Python:

```bash
python tf_idf.py
```

## Explicación del Código ⚡

Dentro del script, puedes modificar la variable `consulta` para realizar diferentes búsquedas. Por ejemplo:

```python
# Puedes descomentar y probar diferentes consultas:
# consulta = "registro y cancelación de asignaturas"
# consulta = "requisitos exigidos por los reglamentos y estatutos"
consulta = "perfil de ingreso y criterios del Ministerio de Educación"
```

El programa limpiará los signos de puntuación, dividirá la consulta en palabras y calculará los puntajes mostrando los documentos ordenados de mayor a menor relevancia.

## Ejemplos de Ejecución 🪄

Al ejecutar el script con la consulta `"perfil de ingreso y criterios del Ministerio de Educación"`, la salida en consola será similar a esta:

```text
1 - Documento 1: TF-IDF Score = 0.5123 - 'ARTÍCULO 14: La Institución se reserva el derecho de seleccionar a los estudiantes y define...'
2 - Documento 6: TF-IDF Score = 0.2854 - 'ARTÍCULO 39: Se denomina estudiante regular a aquel que se ha matriculado en cualquiera...'
...
```

### Imágenes de Prueba 🖨️

#### Consulta 1
![Consulta 1](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/blob/TF-IDF/IMAGENES/Consulta1.png)

#### Consulta 2
![Consulta 2](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/blob/TF-IDF/IMAGENES/Consulta2.png)

#### Consulta 3
![Consulta 3](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/blob/TF-IDF/IMAGENES/Consulta3.png)
