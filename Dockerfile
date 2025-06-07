FROM python:3.13-slim

# Configure Poetry
ENV POETRY_VERSION=2.1.3
ENV POETRY_VIRTUALENVS_CREATE=false 
ENV POETRY_NO_INTERACTION=1

# Install poetry
RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry install --no-root

COPY . /app
