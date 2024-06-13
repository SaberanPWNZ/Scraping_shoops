FROM python:3.9-slim

WORKDIR /app/Scraping_shoops

# Установить git и любые другие зависимости
RUN apt-get update && apt-get install -y \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Playwright
RUN pip install playwright

# Установка браузеров для Playwright
RUN playwright install

# Установка Chromium для Playwright (если необходимо)
RUN playwright install chromium

COPY . /app/Scraping_shoops

COPY requirements.txt /app/Scraping_shoops/

COPY .env /app/Scraping_shoops/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Установка переменной окружения для Chromium
ENV PATH="/usr/lib/chromium-browser/:${PATH}"

EXPOSE 80

CMD ["python", "main.py"]
