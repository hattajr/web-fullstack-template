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

```bash
# Create the database (if it doesn't exist)
dbmate create

# Run all pending migrations
dbmate up

# Create a new migration
dbmate new create_users_table

# Rollback the last migration
dbmate down

# Check migration status
dbmate status
```

### Environment Variables

Database connection is configured via `DATABASE_URL` environment variable:
- Development: `.env.dev` (uses `{{ cookiecutter.project_name }}_dev` database)
- Production: `.env.prod`

### Migration Files

For detailed migration examples, syntax, and best practices, see [migrations/README.md](migrations/README.md)

{% endif %}
## Development

{% if cookiecutter.database_url %}
### 1. Initialize database (first time setup)

See [migrations/README.md](migrations/README.md) for detailed migration instructions.

```bash
# Create your first migration
dbmate new create_initial_tables

# Edit the migration file, then apply it
dbmate up
```

{% endif %}
### {% if cookiecutter.database_url %}2. {% endif %}Start dev server
```bash
uv run --env-file .env.dev -- app/main.py
```
