from fastapi import FastAPI
from app.api import router
from app.core import get_settings

settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the RAG Search Engine API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
