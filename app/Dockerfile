FROM python:3.10.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY ./requirements.txt .
COPY ./api ./api 

RUN pip install -r ./requirements.txt

ENV HOST="0.0.0.0"
ENV PORT=5000

ENTRYPOINT uvicorn api.main:app --host ${HOST} --port ${PORT}