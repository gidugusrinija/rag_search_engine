from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import shutil
import os
from app.ingestion import ingest_file
from app.vector_store import get_vector_db
from app.llm import get_llm_client

router = APIRouter()

class SearchRequest(BaseModel):
    query: str

class SearchResponse(BaseModel):
    answer: str
    sources: list[str]

@router.post("/ingest")
async def ingest_document(file: UploadFile = File(...)):
    file_location = f"data/{file.filename}"
    os.makedirs("data", exist_ok=True)
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    try:
        num_chunks = ingest_file(file_location)
        return {"message": f"Successfully ingested {file.filename}", "chunks": num_chunks}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search(query: str):
    vector_db = get_vector_db()
    results = vector_db.search(query)
    
    documents = results['documents'][0]
    metadatas = results['metadatas'][0]
    
    llm_client = get_llm_client()
    answer = llm_client.generate_answer(query, documents)
    
    return {
        "answer": answer,
        "sources": [m['source'] for m in metadatas],
        "context": documents
    }
