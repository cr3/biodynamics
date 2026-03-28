FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY uv.lock pyproject.toml ./
RUN uv sync --frozen --no-install-project

COPY . ./

ENV SETUPTOOLS_SCM_PRETEND_VERSION=0.1.0
RUN uv sync --frozen --no-editable

ENTRYPOINT ["uv", "run", "--no-sync"]
