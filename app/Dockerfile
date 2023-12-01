FROM python:3.12

RUN apt-get update && apt-get install -y curl

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/poetry python3 -

ENV PATH="${PATH}:/root/poetry/bin"

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY app poetry.lock pyproject.toml /

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi

COPY . .
