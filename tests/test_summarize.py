from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_summarize_valid():
    response = client.post("/v1/summarize", json={
        "text": "Climate change is one of the most pressing issues of our time. Rising global temperatures are causing ice caps to melt, sea levels to rise, and extreme weather events to become more frequent. Scientists have warned that without immediate action to reduce carbon emissions, the consequences could be catastrophic. Governments around the world are struggling to agree on meaningful policies, while activists are pushing for faster change. Renewable energy sources like solar and wind are growing rapidly but still only account for a small fraction of global energy production."
    })
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "summary" in data
    assert "bullets" in data
    assert "latency_ms" in data
    assert len(data["bullets"]) > 0

def test_summarize_empty_text():
    response = client.post("/v1/summarize", json={"text": ""})
    assert response.status_code == 400

def test_summarize_too_short():
    response = client.post("/v1/summarize", json={"text": "Too short"})
    assert response.status_code == 400

def test_summarize_too_long():
    response = client.post("/v1/summarize", json={"text": "a" * 10001})
    assert response.status_code == 400
