FROM python:3.9-slim

WORKDIR /app/Scraping_shoops

# Установка необходимых пакетов
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gnupg \
    unzip \
    libnss3 \
    libxss1 \
    libgconf-2-4 \
    fonts-liberation \
    libappindicator3-1 \
    xdg-utils \
    --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Установка Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Установка Chromedriver
RUN pip install chromedriver-autoinstaller

# Копирование файлов
COPY . /app/Scraping_shoops
COPY requirements.txt /app/Scraping_shoops/
COPY .env /app/Scraping_shoops/.env

# Установка зависимостей Python
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Определение переменных окружения
ENV PATH="/usr/local/bin:${PATH}"

# Открытие порта
EXPOSE 80

# Запуск приложения
CMD ["python", "main.py"]
