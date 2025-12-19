# {{ cookiecutter.project_name }}
{{ cookiecutter.description }}

{% if cookiecutter.database_url %}
## Database Setup

This project uses [dbmate](https://github.com/amacneil/dbmate) for database migrations.

### Install dbmate

**macOS:**
```bash
brew install dbmate
```

**Linux:**
```bash
sudo curl -fsSL -o /usr/local/bin/dbmate https://github.com/amacneil/dbmate/releases/latest/download/dbmate-linux-amd64
sudo chmod +x /usr/local/bin/dbmate
```

**Other platforms:** See [dbmate installation guide](https://github.com/amacneil/dbmate#installation)

### Database Commands

All dbmate commands use `--env-file` to specify the environment:

```bash
# Run migrations (development)
dbmate --env-file .env.dev up

# Create a new migration
dbmate --env-file .env.dev new create_users_table

# Rollback the last migration
dbmate --env-file .env.dev down

# Check migration status
dbmate --env-file .env.dev status

# For production, use .env.prod
dbmate --env-file .env.prod up
```

### Environment Variables

Environment files are auto-generated during project setup:
- **Development**: `.env.dev` (uses `{{ cookiecutter.underscored }}_dev` database)
- **Production**: `.env.prod` (uses `{{ cookiecutter.underscored }}` database)

Each includes:
- `DATABASE_URL` with `?sslmode=disable` appended
- `DBMATE_MIGRATIONS_DIR=./migrations`
- `DBMATE_SCHEMA_FILE=migrations/schema.sql`

### Migration Files

For detailed migration examples, syntax, and best practices, see [migrations/README.md](migrations/README.md)

{% endif %}
## Development

{% if cookiecutter.database_url %}
### 1. Initialize database (first time setup)

See [migrations/README.md](migrations/README.md) for detailed migration instructions.

```bash
# Create your first migration
dbmate --env-file .env.dev new create_initial_tables

# Edit the migration file, then apply it
dbmate --env-file .env.dev up
```

{% endif %}
### {% if cookiecutter.database_url %}2. {% endif %}Start dev server

**Option 1: Using uv (local development)**
```bash
uv run --env-file .env.dev -- app/main.py
```

**Option 2: Using Docker**
```bash
# Build and start with docker-compose (recommended)
docker-compose --env-file .env.dev up --build

# Or build and run manually
docker build -t {{ cookiecutter.hyphenated }} .
docker run -p 8000:8000 --env-file .env.dev {{ cookiecutter.hyphenated }}
# Note: Adjust port mapping (8000:8000) to match your .env.dev APP_PORT value
```

The application will be available at the port configured in your .env file (check with `grep APP_PORT .env.dev`)

## Docker Deployment

This project includes Docker support using [uv's official Docker images](https://docs.astral.sh/uv/guides/integration/docker/).

### Building the Image

```bash
docker build -t {{ cookiecutter.hyphenated }}:latest .
```

### Running with Docker Compose

The project includes a `docker-compose.yml` file for easy deployment:

```bash
# Start all services (development - loads .env.dev for container, uses shell environment for compose)
docker-compose --env-file .env.dev up -d

# Or for production
docker-compose --env-file .env.prod up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

### Environment Variables

The project automatically generates `.env.dev` and `.env.prod` files during setup with dynamically assigned ports:
- `.env.dev`: Development configuration (port auto-assigned starting from 8000)
- `.env.prod`: Production configuration (port auto-assigned starting from 9000)

Required environment variables:
- `APP_HOST`: Host to bind to (default: 0.0.0.0)
- `APP_PORT`: Port to bind to (dynamically assigned in .env files)
- `SECRET_KEY`: Secret key for session encryption
{% if cookiecutter.database_url %}- `DATABASE_URL`: PostgreSQL connection string{% endif %}
