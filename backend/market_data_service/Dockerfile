FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Build context is the repo root. See infra/docker-compose.yml.
COPY libs/py_common /app/libs/py_common
COPY backend/market_data_service/pyproject.toml /app/backend/market_data_service/pyproject.toml
RUN pip install /app/libs/py_common \
 && pip install fastapi>=0.115 'uvicorn[standard]>=0.30' httpx>=0.27

COPY config /app/config
COPY backend/market_data_service/app /app/app

ENV BOT_CONFIG_PATH=/app/config/bot.json \
    PYTHONPATH=/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
