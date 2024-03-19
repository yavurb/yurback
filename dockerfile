ARG python=python:3.12-alpine

FROM ${python} as build

RUN apk add --no-cache \
    build-base \
    libpq-dev \
    libffi-dev

RUN pip install -U pip setuptools wheel
RUN pip install pdm

WORKDIR /app

COPY ["pyproject.toml", "pdm.lock", "./"]
RUN pdm sync --prod --no-editable

FROM ${python}

RUN apk add --no-cache libpq-dev

WORKDIR /app

COPY --from=build --chown=python:python /app/.venv .venv
COPY ["start.sh", ".env", "./"]
COPY src/ src/

CMD ["sh", "start.sh"]
