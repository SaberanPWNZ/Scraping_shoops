FROM python:3.9-slim


WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    ca-certificates \
    --no-install-recommends && \
    apt-key adv --keyserver keyserver.ubuntu.com --recv-keys A4B469963BF863CC && \
    wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && apt-get install -y google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*


COPY . /app
COPY requirements.txt /app/
COPY .env /app/.env


RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt


ENV PATH="/usr/local/bin:${PATH}"


EXPOSE 8000


CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8000"]
