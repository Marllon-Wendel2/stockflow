FROM python:3.12-slim

WORKDIR /app

ENV PYTHONPATH=/app/src

COPY pyproject.toml ./
COPY src ./src

RUN pip install --upgrade pip \
    && pip install fastapi uvicorn sqlalchemy psycopg2-binary

EXPOSE 8000

CMD ["uvicorn", "stockflow.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
