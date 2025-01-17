FROM python:3.12-alpine

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  # poetry:
  POETRY_VERSION=1.8.3 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry'

RUN apk add --no-cache \
    bash \
    && pip install --no-cache-dir "poetry==$POETRY_VERSION" \
    && poetry --version

WORKDIR /code
COPY ./poetry.lock ./pyproject.toml /code/

RUN poetry install --no-root

COPY . /code

CMD ["uvicorn", "src.api.v1.main:create_app", "--reload", "--host", "0.0.0.0", "--port", "9000", "--log-level", "info"]

