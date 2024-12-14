FROM python:3.11-slim AS backend

ARG ENVIRONMENT

ENV TZ=America/Argentina/Buenos_Aires \
    PIP_DEFAULT_TIMEOUT=100 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYDEVD_DISABLE_FILE_VALIDATION=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

ADD poetry.lock poetry.lock
ADD pyproject.toml pyproject.toml

RUN pip install poetry
RUN poetry config virtualenvs.create false

RUN if [ "$ENVIRONMENT" == "prod" ]; then poetry install --only main; else poetry install; fi

COPY src ./


CMD ["python3",  "main.py"]
