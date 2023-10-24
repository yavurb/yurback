FROM python:3.11-alpine

RUN apk update \
    && apk add gcc musl-dev \
    && apk add libpq-dev \
    && apk add libffi-dev

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /usr/src/app

COPY ["pyproject.toml", "pdm.lock", "./"]
RUN pdm sync

COPY . .

EXPOSE 8001
CMD [ "pdm", "run", "start" ]