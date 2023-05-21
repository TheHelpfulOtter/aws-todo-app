# https://docs.aws.amazon.com/lambda/latest/dg/images-create.html
FROM public.ecr.aws/lambda/python:3.10

ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app

COPY ./requirements.txt .
COPY ./api ${LAMBDA_TASK_ROOT}

RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD [ "api.main.handler" ]