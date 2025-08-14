FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    curl \
    netcat-openbsd \
    postgresql-client \
    build-essential \
    libpq-dev \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2 \
    libcups2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./req.txt /req.txt

RUN pip install --upgrade pip
RUN pip install -r /req.txt
RUN python -m playwright install chromium
RUN apt-get install -y \
    libnss3 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libatspi2.0-0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libasound2

COPY . /app

RUN chmod +x entrypoint.sh