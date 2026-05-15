import json
from pathlib import Path
from django.shortcuts import render
from django.http import JsonResponse

from . import rag_service

def index(request):
    """Renderiza la página principal."""
    return render(request, 'rag_app/index.html')

def upload_document(request):
    """Maneja la subida de un documento y su indexación temporal."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido.'}, status=405)

    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return JsonResponse({'error': 'No se proporcionó ningún archivo.'}, status=400)

    try:
        session_key = rag_service.ensure_session_key(request)
        session_dir = rag_service.get_session_dir(session_key)

        file_path = rag_service.save_uploaded_file(uploaded_file, session_dir)
        if file_path.suffix.lower() not in rag_service.SUPPORTED_EXTENSIONS:
            return JsonResponse({'error': 'Tipo de archivo no soportado.'}, status=400)

        documents = rag_service.load_documents(file_path)
        index_path, chunk_count = rag_service.build_vector_store(documents, session_dir)

        request.session['rag_index_path'] = str(index_path)
        request.session['rag_file_name'] = uploaded_file.name
        request.session['rag_chunks'] = chunk_count

        return JsonResponse(
            {
                'message': f'Documento "{uploaded_file.name}" indexado correctamente.',
                'chunks': chunk_count,
            }
        )
    except Exception as exc:
        return JsonResponse({'error': str(exc)}, status=500)

def chat(request):
    """Maneja las preguntas del usuario y retorna respuestas generadas por Groq."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
            
            if not question:
                return JsonResponse({'error': 'Pregunta vacía.'}, status=400)
            
            index_path = request.session.get('rag_index_path')
            if not index_path:
                return JsonResponse({'error': 'Primero sube un documento.'}, status=400)

            vector_store = rag_service.load_vector_store(Path(index_path))
            context, docs = rag_service.retrieve_context(vector_store, question)
            answer, meta = rag_service.run_guarded_answer(question, context)
            source_preview = docs[0].page_content if docs else ''

            if (
                not meta.get('doc_is_cybersecurity')
                or not meta.get('question_is_cybersecurity')
                or not meta.get('answer_in_context')
            ):
                source_preview = ''

            return JsonResponse({'answer': answer, 'source': source_preview, 'meta': meta})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Método no permitido.'}, status=405)
