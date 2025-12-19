# Database Migrations

This directory contains database migration files managed by [dbmate](https://github.com/amacneil/dbmate).

## Quick Start

### 1. Create a new migration
```bash
dbmate --env-file .env.dev new create_users_table
```

This creates a timestamped file like `20250119120000_create_users_table.sql`

### 2. Write your migration
```sql
-- migrate:up
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down
DROP TABLE IF EXISTS users;
```

### 3. Apply migrations
```bash
# Run all pending migrations (development)
dbmate --env-file .env.dev up

# Rollback last migration
dbmate --env-file .env.dev down

# Check migration status
dbmate --env-file .env.dev status
```

## Environment

- **Development**: `.env.dev` → `{{ cookiecutter.underscored }}_dev` database
- **Production**: `.env.prod` → `{{ cookiecutter.underscored }}` database

Both files are auto-generated with:
- `DATABASE_URL` (includes `?sslmode=disable`)
- `DBMATE_MIGRATIONS_DIR=./migrations`
- `DBMATE_SCHEMA_FILE=migrations/schema.sql`

Always use `--env-file` flag:
```bash
dbmate --env-file .env.dev up
```

## Files

- `schema.sql` - Auto-generated complete database schema (commit to git)
- `YYYYMMDDHHMMSS_*.sql` - Your migration files

## Tips

- Always test migrations with `dbmate --env-file .env.dev up` then `down`
- Keep migrations small and focused
- Never modify executed migrations - create new ones
- `schema.sql` is auto-updated by dbmate (don't edit manually)
- Use `.env.dev` for local development, `.env.prod` for production
