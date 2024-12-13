FROM python:3.9-slim


RUN apt-get update && apt-get install -y \
    libpq-dev gcc --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY . /app


ENV PYTHONPATH="${PYTHONPATH}:/app"

EXPOSE 8000

# Используем встроенный сервер для разработки
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
