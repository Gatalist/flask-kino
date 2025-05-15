FROM python:3.12

RUN apt-get update && apt-get install -y curl build-essential

# RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/root/poetry python3 -
RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

WORKDIR /home/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml poetry.lock* /home/app/

RUN poetry config virtualenvs.create false \
    && poetry add setuptools \
    && poetry install --no-interaction --no-ansi

COPY . /home/app