FROM python:3.9-slim


WORKDIR /app

COPY requirements.txt /app/
COPY . /app
COPY .env /app/.env


RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH="${PYTHONPATH}:/app"


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
