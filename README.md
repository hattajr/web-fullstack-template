# Web Fullstack Cookiecutter Template

Generate production-ready web apps with FastAPI, PostgreSQL, and TailwindCSS. Run one command, get a working application with tests, migrations, and Docker support.

## Stack

**Backend:** FastAPI, Python 3.12+, Uvicorn, Pydantic, Loguru

**Frontend:** Jinja2 templates, TailwindCSS (pytailwindcss), HTMX-ready

**Database:** PostgreSQL (optional), psycopg2, dbmate migrations

**Tools:** uv, Ruff, pytest, testcontainers, Docker

## Quick Start

**Prerequisites:** Python 3.12+, uv, PostgreSQL (if using database)

### Generate Project

```bash
uv tool run cookiecutter gh:hattajr/web-fullstack-template
```

Prompts: project name, description, GitHub username, PostgreSQL URL (optional: `postgresql://user:pass@host:port/db`)

Leave database URL empty to skip database setup.

### Run

```bash
cd your-project-name
uv run --env-file .env.dev app/main.py
```

Dependencies installed, .env files created with random ports and secrets. Just run.

## Structure

```
app/
  main.py            # Entry point
  core/              # Config, security
  db/                # Database connection
  routers/           # Routes
  services/          # Business logic
  templates/         # Jinja2 templates
  static/            # CSS, JS, images
tests/               # Tests with testcontainers
migrations/          # Database migrations (dbmate)
docker-compose.yml   # Docker setup
.env.dev/.env.prod   # Environment configs
```

Imports use `from core.config` not `from app.core.config`.

## Features

**TailwindCSS:** Auto-compiles on startup. Edit `app/static/css/input.css`.

**Database:** Creates database on setup, connection pooling via psycopg2, dbmate migrations.

**Sessions:** Secure cookie-based sessions via itsdangerous.

**Static Files:** Served from `/static/`.

**Templates:** Jinja2 with inheritance and static URL generation.

## Environment

Auto-generated `.env.dev` and `.env.prod` with random ports and secure keys:

```bash
APP_PORT=8000        # Random available port
SECRET_KEY=<random>  # Secure random key
DATABASE_URL=...     # If provided
```

Dev uses hot reload, single worker. Prod uses multiple workers, no reload.

## Testing

```bash
uv sync --extra tests
uv run --env-file .env.dev pytest
```

### Testcontainers

Tests with database support use testcontainers - real PostgreSQL in Docker:

**How it works:**
1. `conftest.py` starts PostgreSQL container once per test session
2. Runs all migration files from `migrations/` directory
3. Each test gets clean tables via auto-truncation
4. Container stops after tests complete

**Why:**
- Test against real database, not mocks
- Migrations tested exactly as production
- Zero configuration - Docker just needs to be running
- Tests in isolation

Write service tests that just use `get_test_connection()`. Schema already loaded from migrations. See `tests/README.md` for examples.

## Docker

```bash
docker-compose --env-file .env.dev up --build
```

Multi-stage build with uv. Minimal final image. Dynamic port mapping from .env files.

Database not included - use external PostgreSQL or add db service.

## License

Apache-2.0
