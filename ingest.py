import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader, DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

DOCS_DIR = "docs"
DB_DIR = "db"

def load_documents():
    print(f"Cargando documentos desde {DOCS_DIR}...")
    documents = []
    
    # Cargar PDFs
    pdf_loader = DirectoryLoader(DOCS_DIR, glob="**/*.pdf", loader_cls=PyPDFLoader)
    documents.extend(pdf_loader.load())
    
    # Cargar TXTs o MDs
    text_loader = DirectoryLoader(DOCS_DIR, glob="**/*.md", loader_cls=TextLoader)
    documents.extend(text_loader.load())
    
    text_loader2 = DirectoryLoader(DOCS_DIR, glob="**/*.txt", loader_cls=TextLoader)
    documents.extend(text_loader2.load())
    
    print(f"Se cargaron {len(documents)} documentos.")
    return documents

def split_documents(documents):
    print("Dividiendo documentos en chunks...")
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Se crearon {len(chunks)} chunks.")
    return chunks

def create_vector_store(chunks):
    print("Creando embeddings y guardando en FAISS...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_documents(chunks, embeddings)
    
    # Guardar localmente
    vector_store.save_local(DB_DIR)
    print(f"Base de datos vectorial guardada en {DB_DIR}/")

def main():
    if not os.path.exists(DOCS_DIR):
        os.makedirs(DOCS_DIR)
        print(f"Por favor coloca tus PDFs o archivos MD/TXT en la carpeta '{DOCS_DIR}' y vuelve a ejecutar.")
        return
        
    documents = load_documents()
    if not documents:
        print(f"No se encontraron documentos en '{DOCS_DIR}'. Agrega algunos PDFs, MDs o TXTs.")
        return
        
    chunks = split_documents(documents)
    create_vector_store(chunks)
    print("Proceso de ingesta completado exitosamente.")

if __name__ == "__main__":
    main()
