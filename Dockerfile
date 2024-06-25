FROM python:3.9-slim

WORKDIR /app/Scraping_shoops


RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    gnupg \
    unzip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*


RUN pip install chromedriver-py==114.0.5735.90


COPY . /app/Scraping_shoops


COPY requirements.txt /app/Scraping_shoops/
COPY .env /app/Scraping_shoops/.env

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


ENV PATH="/usr/local/bin:${PATH}"

EXPOSE 80

CMD ["python", "main.py"]
