from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app
from app.db import init_db

init_db()  # create tables before tests run

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_summarize_valid():
    mock_result = {
        "title": "Test Title",
        "summary": "Test summary sentence here.",
        "bullets": ["Point 1", "Point 2", "Point 3"]
    }
    with patch("app.routes.summarize.get_summary", return_value=mock_result):
        response = client.post("/v1/summarize", json={
            "text": "Climate change is one of the most pressing issues of our time. Rising global temperatures are causing ice caps to melt, sea levels to rise, and extreme weather events to become more frequent. Scientists have warned that without immediate action."
        })
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "summary" in data
    assert "bullets" in data
    assert "latency_ms" in data

def test_summarize_empty_text():
    response = client.post("/v1/summarize", json={"text": ""})
    assert response.status_code == 400

def test_summarize_too_short():
    response = client.post("/v1/summarize", json={"text": "Too short"})
    assert response.status_code == 400

def test_summarize_too_long():
    response = client.post("/v1/summarize", json={"text": "a" * 10001})
    assert response.status_code == 400
