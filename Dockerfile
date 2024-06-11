
FROM python:3.9-slim


WORKDIR /app/Scraping_shoops

# Install git and any other dependencies
RUN apt-get update && apt-get install -y git

# Copy the current directory contents into the container at /app
COPY . /app/Scraping_shoops

COPY requirements.txt /app/Scraping_shoops/


COPY .env /app/Scraping_shoops/.env


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 80

ENV NAME World


CMD ["python", "bot.py"]
