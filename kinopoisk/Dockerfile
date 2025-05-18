FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    curl \
    postgresql-client \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home/app

COPY ./req.txt /req.txt

RUN pip install --upgrade pip
RUN pip install -r /req.txt

COPY . /home/app

RUN chmod +x entrypoint.sh