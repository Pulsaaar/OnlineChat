# Базовый образ
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем рабочую директорию
WORKDIR /app

ENV DB_HOST=postgres
ENV DB_PORT=5432
ENV DB_NAME=chat
ENV DB_USER=postgres
ENV DB_PASS=postgres
ENV AUTH_SECRET=5SpxMnjOUeT4zTLKmikTSoovwMY6NbfDyNY6CNUGLsU
ENV VER_SECRET=ESxXRfHQGfZcWiau83TrGtk0R43NaQUOSMJX6qKtT0E

# Скопируем файл зависимостей
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы проекта в контейнер
COPY . .

# Команда для выполнения миграций Alembic
RUN alembic upgrade head

# Открываем порт для FastAPI
EXPOSE 8000

# Команда для запуска FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
