ARG python=python:3.11-alpine

FROM ${python} as build

RUN apk update \
    && apk add gcc musl-dev \
    && apk add libpq-dev \
    && apk add libffi-dev

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /app

COPY ["pyproject.toml", "pdm.lock", "./"]
RUN pdm sync --prod --no-editable

FROM ${python}

RUN apk add libpq-dev

WORKDIR /app

COPY --from=build --chown=python:python /app/.venv .venv
COPY ["start.sh", ".env", "./"]
COPY src/ src/

CMD ["sh", "start.sh"]
