FROM python:3.13.16-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code
COPY "pyproject.toml" ".python-version" "uv.lock" ./

RUN uv sync --locked

COPY pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]