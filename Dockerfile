FROM python:3.12-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Copy files
COPY . /app

RUN #apt-get update && apt-get install -y libpq-dev  psycopg2-binary

WORKDIR /app
RUN uv sync --frozen --no-cache


# Set environment
ENV PYTHONUNBUFFERED=1
ENV PATH="/root/.cargo/bin:$PATH"
ENV DJANGO_SETTINGS_MODULE=config.settings.prod

RUN uv run manage.py collectstatic --noinput

# Default command
CMD ["uv", "run", "uvicorn", "config.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
