from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from app.routes.summarize import router as summarize_router
from app.db import init_db

app = FastAPI(
    title="Summarizer API",
    description="Production-grade text summarization powered by LLMs",
    version="1.0.0"
)

templates = Jinja2Templates(directory="app/templates")

@app.on_event("startup")
def startup():
    init_db()

app.include_router(summarize_router, prefix="/v1")

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
def health():
    return {"status": "ok"}
