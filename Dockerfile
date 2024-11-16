FROM python:3.13-slim

# Install uv.
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# Install the application dependencies.
# Copy the lockfile and `pyproject.toml` into the image
COPY uv.lock /app/uv.lock
COPY pyproject.toml /app/pyproject.toml
RUN  uv sync --frozen  --no-dev

# Copy the application code into the container
COPY isbnchile /app

# Use the environment.
ENV PATH="/app/.venv/bin:$PATH"

# Run the application.
ENTRYPOINT ["python" , "run.py"]