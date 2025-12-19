# Web Fullstack Cookiecutter Template

A production-ready cookiecutter template for building modern web applications with FastAPI, optional PostgreSQL database, and TailwindCSS.

## How It Works

```mermaid
flowchart LR
    A[User Input<br/>project name, description<br/>database URL optional] --> B[Validate & Generate]
    B --> C[Create .env Files<br/>random ports & secrets]
    C --> D[Install Dependencies<br/>uv sync]
    D --> E{Database?}
    E -->|Yes| F[Setup Database<br/>+ migrations]
    E -->|No| G[Remove DB files]
    F --> H[Ready to Use]
    G --> H
    
    style A fill:#e1f5e1
    style H fill:#e1f5e1
    style C fill:#e1e5ff
    style F fill:#e1e5ff
```

**What happens:**
1. **Collects your inputs** - Project name, description, optional database URL
2. **Validates** - Checks database URL format if provided
3. **Generates .env files** - Random ports (8000+, 9000+) and secure secret keys
4. **Installs dependencies** - Runs `uv sync` automatically
5. **Configures database** - If URL provided: tests connection, adds to .env, creates databases
6. **Ready!** - Project is configured and ready to run

## Stack

### Backend
- **FastAPI** - Modern, fast web framework for building APIs
- **Python 3.12+** - Latest Python with modern features
- **Uvicorn** - Lightning-fast ASGI server
- **Pydantic** - Data validation using Python type annotations
- **Loguru** - Simple and powerful logging

### Frontend
- **Jinja2** - Template engine for server-side rendering
- **TailwindCSS** - Utility-first CSS framework (via pytailwindcss)
- **HTMX-ready** - Structure supports progressive enhancement

### Database (Optional)
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - SQL toolkit and ORM
- **psycopg2** - PostgreSQL adapter

### Development Tools
- **uv** - Fast Python package manager
- **Ruff** - Lightning-fast linter and formatter
- **pytest** - Testing framework (optional)

## What

This template generates a structured FastAPI web application with:
- Server-side rendered templates with Jinja2
- Static file serving (CSS, JS, images)
- Optional PostgreSQL database integration
- Environment-based configuration
- Development and production-ready setup
- Pre-configured linting and formatting
- Automatic TailwindCSS compilation

## How to Use

### Prerequisites
- Python 3.12 or higher
- uv package manager (`pip install uv` or use system package manager)
- PostgreSQL (only if using database option)

### Generate Project

```bash
# Install cookiecutter
uv tool install cookiecutter

# Generate project
uv tool run cookiecutter gh:hattajr/web-fullstack-template

# Or from local template
uv tool run cookiecutter /path/to/web-fullstack-template
```

### Configuration Prompts

You'll be prompted for:
- `project_name` - Your project name (e.g., "My Awesome App")
- `description` - Brief project description
- `github_username` - Your GitHub username
- `author_name` - Your name
- `database_url` - PostgreSQL connection string (leave empty to skip database)
  - Format: `postgresql://username:password@host:port/database`
  - Example: `postgresql://myuser:mypass@localhost:5432/mydb`

### Database URL Format

If including database support, provide a PostgreSQL connection string:

**With database name:**
```
postgresql://username:password@host:port/database_name
```

**Without database name** (will use project name):
```
postgresql://username:password@host:port
```

**Examples:**
```bash
# Using project name as database
postgresql://dev:devpass@localhost:5432

# Specifying database name
postgresql://dev:devpass@localhost:5432/myapp
```

**Note:** `?sslmode=disable` is automatically added to URLs in generated `.env` files for local development. Leave empty to generate a project without database support.

### Run Your Application

```bash
cd your-project-name

# Dependencies are already installed during generation!
# .env files are already created with random ports and secrets!

# Run development server
uv run --env-file .env.dev uvicorn app.main:app --reload

# Or for production
uv run --env-file .env.prod uvicorn app.main:app
```

Visit `http://localhost:<PORT>` (port shown in .env.dev)

## Project Structure

```
your-project/
├── app/
│   ├── main.py              # Application entry point
│   ├── core/
│   │   ├── config.py        # Settings and configuration
│   │   └── security.py      # Security utilities
│   ├── db/                  # Database (if enabled)
│   │   └── connection.py    # DB connection management
│   ├── routers/             # API routes
│   │   └── root.py          # Root routes
│   ├── schemas/             # Pydantic models
│   ├── services/            # Business logic
│   ├── static/              # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   ├── templates/           # Jinja2 templates
│   │   ├── shared/
│   │   └── home/
│   └── utils/               # Helper functions
├── data/                    # Application data
├── migrations/              # Database migrations (if enabled)
├── tests/                   # Test files
├── pyproject.toml           # Project dependencies
├── .env                     # Environment variables
└── README.md               # Project documentation
```

## Integrations

### TailwindCSS
Automatically compiled on startup via pytailwindcss. Edit `app/static/css/input.css` and classes are auto-generated.

### Database (PostgreSQL)
When database URL is provided:
- Validates connection on project creation
- Creates database if it doesn't exist
- Sets up SQLAlchemy connection pooling
- Includes migration schema template

### Session Management
Built-in session middleware using `itsdangerous` for secure session cookies.

### Static Files
Automatic static file serving from `app/static/` at `/static/` endpoint.

### Templates
Jinja2 templates with:
- Base template with common structure
- Template inheritance support
- Static file URL generation
- Context processors ready

## Dependencies

### Core Dependencies
```toml
fastapi          # Web framework
uvicorn          # ASGI server
pydantic         # Data validation
pydantic-settings # Settings management
jinja2           # Template engine
loguru           # Logging
httpx            # HTTP client
python-multipart # Form parsing
itsdangerous     # Secure sessions
pyyaml           # YAML support
ua-parser        # User agent parsing
user-agents      # User agent detection
```

### Optional Dependencies
```toml
# With database
sqlalchemy       # ORM
psycopg2-binary  # PostgreSQL driver

# Testing
pytest           # Testing framework
testcontainers   # Container-based testing
```

### Development Tools
```toml
ruff            # Linter and formatter (configured)
pytailwindcss   # TailwindCSS compiler
```

## Environment Variables

**Auto-generated during project creation:**

`.env.dev` (development):
```bash
LOG_LEVEL=DEBUG
APP_HOST=0.0.0.0
APP_PORT=8000  # Random available port
APP_WORKERS=1
APP_HOT_RELOAD=True
SECRET_KEY=<random-secure-key>

# If database provided:
DATABASE_URL=postgresql://user:pass@host:port/dbname_dev?sslmode=disable
DBMATE_MIGRATIONS_DIR=./migrations
DBMATE_SCHEMA_FILE=migrations/schema.sql
```

`.env.prod` (production):
```bash
LOG_LEVEL=INFO
APP_HOST=0.0.0.0
APP_PORT=9000  # Random available port
APP_WORKERS=3
APP_HOT_RELOAD=False
SECRET_KEY=<random-secure-key>

# If database provided:
DATABASE_URL=postgresql://user:pass@host:port/dbname?sslmode=disable
DBMATE_MIGRATIONS_DIR=./migrations
DBMATE_SCHEMA_FILE=migrations/schema.sql
```

## Testing

Run tests:
```bash
# Install test dependencies
uv sync --extra tests

# Run tests
uv run pytest
```

Test the template itself:
```bash
# From template root directory
uv run test_template.py
```

## Features

- **Type-safe configuration** - Pydantic settings with environment variable support
- **Structured logging** - Loguru with custom formatting
- **Hot reload** - Development server with auto-reload
- **Database pooling** - SQLAlchemy connection pool (when using DB)
- **Security** - Session management, CORS-ready
- **Production-ready** - Multi-worker support, proper logging
- **Modern Python** - Type hints, async/await, Python 3.12+
- **Code quality** - Pre-configured Ruff for linting and formatting

## License

Apache-2.0
