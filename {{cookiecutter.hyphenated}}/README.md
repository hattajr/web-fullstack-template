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
```bash
uv run --env-file .env.dev -- app/main.py
```
