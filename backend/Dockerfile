FROM python:3.8.13-slim-buster as builder

ENV PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
ARG APP_NAME=my-model
ARG MODEL_CONTAINER_PATH=/model
ARG MODEL_FILENAME=model.pkl

RUN mkdir /app && mkdir /model
RUN groupadd -r mymodel && useradd -r -s /bin/false -g mymodel mymodel
RUN chown -R mymodel:mymodel /app && chown -R mymodel:mymodel /model

FROM builder as model
WORKDIR /app
USER root

COPY ./app /app
COPY ./requirements_api.txt /tmp/requirements_api.txt
RUN pip install --upgrade pip && pip install -r /tmp/requirements_api.txt

FROM model as prod
USER mymodel
WORKDIR /app

CMD ["uvicorn", "proxy:app", "--host", "0.0.0.0", "--port", "8080"]