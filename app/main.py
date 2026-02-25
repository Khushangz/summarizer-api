from fastapi import FastAPI
from app.routes.summarize import router as summarize_router
from app.db import init_db

app = FastAPI(
    title="Summarizer API",
    description="Production-grade text summarization powered by LLMs",
    version="1.0.0"
)

@app.on_event("startup")
def startup():
    init_db()

app.include_router(summarize_router, prefix="/v1")

@app.get("/health")
def health():
    return {"status": "ok"}
