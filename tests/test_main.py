import sys
import os
from unittest.mock import MagicMock, patch

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from fastapi.testclient import TestClient

# Мокаем redis и psycopg2 до импорта app
mock_redis = MagicMock()
mock_psycopg2 = MagicMock()

# Создаем мок для подключения
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_cursor.fetchone.return_value = (1,)
mock_conn.cursor.return_value = mock_cursor

# Настраиваем моки
mock_psycopg2.connect.return_value = mock_conn
mock_redis.Redis.return_value = mock_redis

# Патчим зависимости
with patch.dict('sys.modules', {
    'redis': mock_redis,
    'psycopg2': mock_psycopg2
}):
    # Импортируем app после моков
    from app.main import app

client = TestClient(app)


def test_health():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_root():
    """Test root endpoint with mocked dependencies"""
    # Настраиваем мок для redis incr
    mock_redis.incr.return_value = 1
    
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["redis_hits"] == 1
    assert data["postgres_records"] == 1


def test_root_multiple_requests():
    """Test that redis hits increment on each request"""
    # Настраиваем мок для последовательных вызовов incr
    mock_redis.incr.side_effect = [1, 2, 3]
    
    response1 = client.get("/")
    hits1 = response1.json()["redis_hits"]
    
    response2 = client.get("/")
    hits2 = response2.json()["redis_hits"]
    
    assert hits2 > hits1
