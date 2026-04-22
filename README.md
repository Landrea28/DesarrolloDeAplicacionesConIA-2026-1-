# # 🪸 RECUERDE QUE ESTA EN LA RAMA: Tf-Idf_BM25
## Rama "main": https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/tree/main?tab=readme-ov-file 

Este proyecto implementa un motor de búsqueda básico en Python utilizando el algoritmo **TF-IDF (Term Frequency - Inverse Document Frequency)**. Su propósito es encontrar los artículos o reglamentos académicos más relevantes dentro de una colección de documentos, basándose en una consulta de texto proporcionada por el usuario.

## Descripción del Proyecto ✨

Este proyecto tiene como objetivo principal realizar una **comparación técnica y matemática entre los algoritmos de recuperación de información TF-IDF y BM25**. A través de un script en Python (`comparacion_tfidf_bm25.py`), se evalúa el comportamiento de ambos algoritmos frente a dos escenarios críticos:
1. **Keyword Stuffing (Spam de palabras):** Donde TF-IDF es vulnerable a dar altas puntuaciones por repetición excesiva lineal, mientras que BM25 "satura" el puntaje controlando los abusos.
2. **Penalización por longitud:** Donde TF-IDF clásico puede fallar al dar puntajes altos a documentos muy largos tangenciales, mientras que BM25 premia a documentos más cortos y directos al tema de búsqueda.

## Requisitos Previos 🛠️

Para ejecutar esta comparación, necesitas tener instalado Python en tu sistema junto con las siguientes bibliotecas para los cálculos matemáticos y la visualización en tabla:

- `scikit-learn` (para el cálculo del TF-IDF puro)
- `rank_bm25` (para la implementación del algoritmo BM25)
- `tabulate` (para imprimir las tablas de resultados)

Puedes instalar las dependencias ejecutando:

```bash
pip install scikit-learn rank_bm25 tabulate
```

## Instrucciones de Ejecución 👩‍🏫

1. Abre una terminal o línea de comandos.
2. Navega hasta el directorio del repositorio donde se encuentra el archivo `comparacion_tfidf_bm25.py`.
3. Ejecuta el script con Python utilizando el siguiente comando:

```bash
python comparacion_tfidf_bm25.py
```

## Explicación del Código ⚡

Dentro del script `comparacion_tfidf_bm25.py` encontrarás dos partes fundamentales:
1. **El Corpus de Texto:** Una lista de documentos creados intencionalmente para la prueba. Incluye un documento con repetición de palabras ("spam"), documentos cortos vs largos, y documentos de relleno para estabilizar el cálculo del IDF.
2. **Cálculos e Instancias:** 
   - Se utiliza `TfidfVectorizer(norm=None)` de `sklearn` para mostrar la debilidad pura y matemática de TF-IDF sin correcciones artificiales posteriores (L2).
   - Se utiliza `BM25Okapi` de `rank_bm25` para calcular la saturación de frecuencia de términos y la normalización de la longitud del documento de forma nativa.
   
Puedes modificar la lista `docs` o agregar nuevas sentencias a la función `calcular_y_mostrar("tu palabra", "descripción")` para experimentar con diferentes escenarios.

## Ejemplos de Ejecución 🪄

Al ejecutar el script, verás la salida en consola formateada en tablas. Por ejemplo, al evaluar el caso de "Keyword Stuffing" con la palabra *inteligencia*:

```text
======================================================================
CONSULTA: 'inteligencia' (Punto 1: TF-IDF > BM25 debido a 'Keyword Stuffing')
======================================================================
+-----------------------+----------------+--------------+
| Documento             |   Score TF-IDF |   Score BM25 |
+=======================+================+==============+
| Doc A (Normal)        |         6.825  |       0.9884 |
| Doc B (Spam/Stuffing) |        27.3001 |       1.3004 |
| Doc C (Corto)         |         0      |       0      |
+-----------------------+----------------+--------------+
```
*(Se observa claramente cómo el score de TF-IDF se dispara matemáticamente por 4x, mientras que el de BM25 se satura, limitando el abuso de palabras clave).*

### Imágenes de Prueba 🖨️

#### Consulta 
![Consulta 1](https://github.com/Landrea28/DesarrolloDeAplicacionesConIA-2026-1-/blob/Tf_Idf_BM25/IMAGENES/Consulta.png)
