FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock* ./
RUN poetry install --no-interaction --no-ansi --no-root 2>/dev/null || \
    pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg psycopg2-binary \
    alembic pydantic pydantic-settings python-jose[cryptography] passlib[bcrypt] \
    python-multipart redis[hiredis] langchain langchain-openai langgraph openai \
    httpx websockets

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
