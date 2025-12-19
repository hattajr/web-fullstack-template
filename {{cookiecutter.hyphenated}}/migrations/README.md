# Database Migrations

This directory contains database migration files managed by [dbmate](https://github.com/amacneil/dbmate).

## Quick Start

### 1. Create a new migration
```bash
dbmate new create_users_table
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
# Run all pending migrations
dbmate up

# Rollback last migration
dbmate down

# Check migration status
dbmate status
```

## Environment

- **Development**: Uses `.env.dev` → `{{ cookiecutter.project_name }}_dev` database
- **Production**: Uses `.env.prod` → `{{ cookiecutter.project_name }}` database

Set `DATABASE_URL` environment variable or use:
```bash
dbmate --env-file .env.dev up
```

## Files

- `schema.sql` - Auto-generated complete database schema (commit to git)
- `YYYYMMDDHHMMSS_*.sql` - Your migration files

## Tips

- Always test migrations with `dbmate up` then `dbmate down`
- Keep migrations small and focused
- Never modify executed migrations - create new ones
- `schema.sql` is auto-updated by dbmate (don't edit manually)
