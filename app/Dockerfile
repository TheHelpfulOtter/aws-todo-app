FROM python:3.10.11-slim-bullseye

ENV PYTHONUNBUFFERED 1

EXPOSE 8000
WORKDIR /app

COPY ./requirements.txt .
COPY ./api ./api 

RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["pipenv", "run", "uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]