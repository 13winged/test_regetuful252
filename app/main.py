import os
import time
from fastapi import FastAPI
import redis
import psycopg2

app = FastAPI()

# Инициализация соединений из переменных окружения
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

DB_NAME = os.getenv("POSTGRES_DB", "devops_db")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

# Подключение к Redis
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)


# Функция для ленивой инициализации БД (ждем, пока Postgres поднимется)
def get_db_connection():
    while True:
        try:
            conn = psycopg2.connect(
                dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST
            )
            return conn
        except psycopg2.OperationalError:
            print("База данных еще недоступна, ждем 2 секунды...")
            time.sleep(2)


# Создаем таблицу при старте, если её нет
conn = get_db_connection()
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS visits (
        id SERIAL PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
''')
conn.commit()
cursor.close()
conn.close()


@app.get("/")
def read_root():
    # 1. Работаем с Redis (инкремент счетчика)
    visits_count = r.incr("hits")

    # 2. Работаем с PostgreSQL (пишем лог визита)
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO visits DEFAULT VALUES;")
    conn.commit()

    # Получаем общее число записей из SQL для проверки
    cursor.execute("SELECT COUNT(*) FROM visits;")
    total_sql_visits = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return {
        "status": "success",
        "message": "Привет! Инфраструктура DevOps Middle+ работает.",
        "redis_hits": visits_count,
        "postgres_records": total_sql_visits
    }


@app.get("/health")
def health_check():
    return {"status": "alive"}
