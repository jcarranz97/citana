# Local Setup

This guide walks through running Citana locally.

## Prerequisites

- Python 3.13+
- Docker and Docker Compose
- Git

## Initial setup

```bash
git clone https://github.com/jcarranz97/citana.git
cd citana

# Install pre-commit hooks (once)
pip install pre-commit
pre-commit install
```

## Option 1 — Docker (recommended)

```bash
docker compose up --build
# or detached
docker compose up -d --build
```

Services:

- **Backend API**: <http://localhost:8001>
- **API docs (Swagger)**: <http://localhost:8001/docs>
- **MkDocs site**: <http://localhost:2012>

The backend mounts `./backend` into the container, so saving a file
triggers FastAPI's hot reload.

The default admin (`admin` / `citana-admin`) is created
automatically on first startup. Override before the first run by
exporting `DEFAULT_ADMIN_USERNAME` and `DEFAULT_ADMIN_PASSWORD`.

### Starting fresh

`docker compose down` keeps the `postgres_data` volume so your DB
survives restarts. Use `-v` to wipe everything:

```bash
docker compose down -v
docker compose up -d --build
```

## Option 2 — Local Python (no Docker)

You still need a Postgres running somewhere; the easiest way is to
launch just the postgres service:

```bash
docker compose up -d postgres
```

Then in a separate shell:

```bash
cd backend
uv sync
uv run fastapi dev
```

### Backend dev commands

```bash
cd backend

# Hot reload
uv run fastapi dev

# Lint + format
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .

# Type check
PYTHONPATH=. uv run pyright .

# Tests (real Postgres test DB)
PYTHONPATH=. uv run pytest
PYTHONPATH=. uv run pytest tests/auth/
PYTHONPATH=. uv run pytest -k test_login
```

`PYTHONPATH=.` is required — without it, system Python paths can
shadow project imports.

### Test database

Tests use `DATABASE_URL` — defaulting to
`postgresql://citana_user:citana_password@localhost:5433/citana_test_db`
(host port 5433 maps to the container's 5432). Create the DB if it
doesn't exist:

```bash
docker exec -it citana-postgres psql -U citana_user -d citana_db \
  -c "CREATE DATABASE citana_test_db;"
```

## Managing dependencies

```bash
cd backend

# Add a runtime dep
uv add <package>

# Add a dev dep
uv add <package> --dev

# Update everything
uv sync --upgrade
```

## Documentation

```bash
# Live preview the docs locally (separate from docker-compose docs service)
pip install mkdocs-material
mkdocs serve
```

Or just rely on the `docs` service from `docker compose up`.

## Code quality

See [Code Quality](code-quality.md) for the full validation checklist
and the pre-commit configuration.

## Environment variables

| Variable | Default | Purpose |
|---|---|---|
| `DATABASE_URL` | `postgresql://citana_user:citana_password@localhost:5433/citana_db` | Connection string (host port 5433 → container 5432) |
| `AUTH_SECRET_KEY` | dev placeholder | JWT signing key — change in prod |
| `AUTH_ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | JWT lifetime |
| `DEFAULT_ADMIN_USERNAME` | `admin` | First-startup admin username |
| `DEFAULT_ADMIN_PASSWORD` | `citana-admin` | First-startup admin password |
