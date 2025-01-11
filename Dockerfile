FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    libglib2.0-0 libnss3 libdbus-1-3 libatk1.0-0 libcups2 \
    libdrm2 libexpat1 libx11-6 libxcomposite1 libxdamage1 libxext6 libxfixes3 \
    libxrandr2 libgbm1 libxcb1 libxkbcommon0 libpango-1.0-0 libcairo2 libasound2 \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*


WORKDIR /app


COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


RUN playwright install


COPY . /app


ENV PYTHONPATH="${PYTHONPATH}:/app"


EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
