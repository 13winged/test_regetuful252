# ============================================
# STAGE 1: Builder - сборка зависимостей
# ============================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Копируем зависимости
COPY requirements.txt .

# Устанавливаем зависимости Python
RUN pip install --no-cache-dir --user -r requirements.txt

# ============================================
# STAGE 2: Runner - минимальный образ
# ============================================
FROM python:3.11-slim AS runner

# Устанавливаем минимальные runtime-зависимости
RUN apt-get update && apt-get install -y \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Создаем пользователя
RUN useradd -m -u 1000 appuser
WORKDIR /app

# Копируем установленные библиотеки из билдера
COPY --from=builder /root/.local /home/appuser/.local

# Копируем код
COPY --chown=appuser:appuser app/ /app/app/

# Настраиваем PATH
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Переключаемся на пользователя
USER appuser

# Запускаем приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Healthcheck с urllib
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1
