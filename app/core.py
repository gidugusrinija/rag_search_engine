import os
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "RAG Search Engine"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"
    CHROMA_DB_DIR: str = "chroma_db"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_TOKEN: str = os.getenv("HF_TOKEN", "")
    
    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
