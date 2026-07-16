import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}

def test_root():
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "message" in data
    assert "redis_hits" in data
    assert "postgres_records" in data

def test_root_returns_json():
    """Test that root returns JSON"""
    response = client.get("/")
    assert response.headers["content-type"] == "application/json"

def test_health_returns_json():
    """Test that health returns JSON"""
    response = client.get("/health")
    assert response.headers["content-type"] == "application/json"

def test_redis_hits_increment():
    """Test that redis hits increment on each request"""
    response1 = client.get("/")
    hits1 = response1.json()["redis_hits"]
    
    response2 = client.get("/")
    hits2 = response2.json()["redis_hits"]
    
    assert hits2 > hits1
