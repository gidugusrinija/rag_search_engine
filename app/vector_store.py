import chromadb
from chromadb.config import Settings as ChromaSettings
from app.core import get_settings
from app.embeddings import get_embedding_model
import uuid

settings = get_settings()

class VectorDB:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMA_DB_DIR)
        self.collection = self.client.get_or_create_collection(name="documents")
        self.embedding_model = get_embedding_model()

    def add_documents(self, documents: list[str], metadatas: list[dict] = None):
        if not documents:
            return
        
        embeddings = self.embedding_model.encode(documents)
        ids = [str(uuid.uuid4()) for _ in range(len(documents))]
        
        if metadatas is None:
            metadatas = [{"source": "unknown"} for _ in range(len(documents))]

        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def search(self, query: str, n_results: int = 5):
        query_embedding = self.embedding_model.encode([query])
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=n_results
        )
        return results

_vector_db_instance = None

def get_vector_db():
    global _vector_db_instance
    if _vector_db_instance is None:
        _vector_db_instance = VectorDB()
    return _vector_db_instance
