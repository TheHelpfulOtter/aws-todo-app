FROM python:3.10.11-slim-bullseye
COPY ./app ./app
COPY ./requirements.txt ./requirements.txt
RUN pip install -r ./requirements.txt
ENV HOST="0.0.0.0"
ENV PORT=5000
ENTRYPOINT uvicorn api.app:app --host ${HOST} --port ${PORT}