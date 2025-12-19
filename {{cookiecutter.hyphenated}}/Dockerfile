# syntax=docker/dockerfile:1

# Use Python 3.12 slim image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim AS builder

# Set working directory
WORKDIR /app

# Enable bytecode compilation for better performance
ENV UV_COMPILE_BYTECODE=1

# Copy dependency files first for better layer caching
COPY pyproject.toml ./

# Install dependencies first (without the project itself)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-install-project --no-dev

# Copy the entire application
COPY . /app

# Install the project itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev

# Final stage - use slim Python image with uv
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code and project files
COPY --from=builder /app/app /app/app
COPY --from=builder /app/data /app/data
{% if cookiecutter.database_url %}COPY --from=builder /app/migrations /app/migrations
{% endif %}COPY --from=builder /app/pyproject.toml /app/pyproject.toml

# Add virtual environment to PATH
ENV PATH="/app/.venv/bin:$PATH"

# Set Python to run in unbuffered mode
ENV PYTHONUNBUFFERED=1

# Run the application using uv
CMD ["uv", "run", "app/main.py"]
