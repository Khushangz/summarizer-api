from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.llm import get_summary
from app.db import log_request
import time

router = APIRouter()

class SummarizeRequest(BaseModel):
    text: str

class SummarizeResponse(BaseModel):
    title: str
    summary: str
    bullets: list[str]
    latency_ms: int

@router.post("/summarize", response_model=SummarizeResponse)
def summarize(request: SummarizeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(request.text) < 200:
        raise HTTPException(status_code=400, detail="Text too short (min 200 chars)")
    if len(request.text) > 10000:
        raise HTTPException(status_code=400, detail="Text too long (max 10,000 chars)")

    start = time.time()
    result = get_summary(request.text)
    latency_ms = int((time.time() - start) * 1000)

    log_request(
        input_text=request.text,
        title=result["title"],
        summary=result["summary"],
        bullets=result["bullets"],
        latency_ms=latency_ms
    )

    return {**result, "latency_ms": latency_ms}
