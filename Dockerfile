FROM python:3.9-slim

RUN apt-get update && apt-get install -y git

WORKDIR /app/Scraping_shoops/


RUN git clone https://github.com/SaberanPWNZ/Scraping_shoops.git .

COPY requirements.txt .
COPY .env .env
RUN pip install --upgrade pip


RUN pip install --no-cache-dir -r requirements.txt


CMD ["python", "bot.py"]