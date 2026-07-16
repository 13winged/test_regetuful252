import sys
import os
from unittest.mock import MagicMock, patch

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Импортируем после настройки пути
from fastapi.testclient import TestClient

# --- Создаем моки ДО импорта app ---
mock_redis = MagicMock()
mock_psycopg2 = MagicMock()

# Настраиваем мок для подключения к БД
mock_conn = MagicMock()
mock_cursor = MagicMock()
mock_cursor.fetchone.return_value = (1,)
mock_conn.cursor.return_value = mock_cursor
mock_psycopg2.connect.return_value = mock_conn

# Настраиваем мок для Redis
mock_redis.Redis.return_value = mock_redis
mock_redis.incr.return_value = 1

# --- Патчим зависимости и импортируем приложение ---
with patch.dict('sys.modules', {
    'redis': mock_redis,
    'psycopg2': mock_psycopg2
}):
    from app.main import app

client = TestClient(app)


def test_health():
    """Проверка health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_root():
    """Проверка root endpoint с моками"""
    # Настраиваем мок для последовательных вызовов incr
    mock_redis.incr.side_effect = [1, 2]

    response1 = client.get("/")
    assert response1.status_code == 200
    data1 = response1.json()
    assert data1["status"] == "success"
    assert data1["redis_hits"] == 1
    assert data1["postgres_records"] == 1

    response2 = client.get("/")
    assert response2.status_code == 200
    data2 = response2.json()
    assert data2["redis_hits"] == 2
    assert data2["postgres_records"] == 1
