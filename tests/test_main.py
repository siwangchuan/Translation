import pytest
from fastapi.testclient import TestClient
from backend.main import app


@pytest.fixture
def client():
    """Create a test client"""
    with TestClient(app) as test_client:
        yield test_client

def test_root(client):
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert data["message"] == "AI Translation Assistant API"

def test_health(client):
    """Test the health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_translate_missing_api_key(client, monkeypatch):
    """Test translation endpoint without API key"""
    # Remove ALIYUN_API_KEY if it exists
    monkeypatch.delenv("ALIYUN_API_KEY", raising=False)
    
    response = client.post(
        "/translate",
        json={
            "text": "Hello world",
            "source_lang": "en",
            "target_lang": "zh"
        }
    )
    assert response.status_code == 500
    assert "ALIYUN_API_KEY not configured" in response.json()["detail"]

def test_translate_with_api_key(client, monkeypatch):
    """Test translation endpoint with API key"""
    monkeypatch.setenv("ALIYUN_API_KEY", "test-key")
    
    response = client.post(
        "/translate",
        json={
            "text": "Hello world",
            "source_lang": "en",
            "target_lang": "zh"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "translated_text" in data
    assert "source_lang" in data
    assert "target_lang" in data
