# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.13-slim

FROM python:${PYTHON_VERSION} AS builder

WORKDIR /app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r ./requirements.txt

COPY . .

RUN useradd --no-log-init --create-home appuser
USER appuser

CMD ["python3", "src/main.py"]
