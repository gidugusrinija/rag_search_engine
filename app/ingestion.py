import os
from pypdf import PdfReader
from app.vector_store import get_vector_db

def load_text_file(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def load_pdf_file(file_path: str) -> str:
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def ingest_file(file_path: str):
    if file_path.endswith(".pdf"):
        text = load_pdf_file(file_path)
    else:
        text = load_text_file(file_path)
    
    chunks = chunk_text(text)
    vector_db = get_vector_db()
    vector_db.add_documents(chunks, metadatas=[{"source": os.path.basename(file_path)} for _ in chunks])
    return len(chunks)

def ingest_directory(directory: str):
    total_chunks = 0
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            try:
                total_chunks += ingest_file(file_path)
            except Exception as e:
                print(f"Error ingesting {filename}: {e}")
    return total_chunks
