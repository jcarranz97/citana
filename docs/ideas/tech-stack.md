# Tech Stack Rationale

Why each piece, and what it would take to swap.

## Backend — FastAPI + PostgreSQL + SQLAlchemy 2.0

- **FastAPI** for the REST API. Mature, async-first, auto-generated
  OpenAPI, Pydantic validation built in.
- **PostgreSQL 15** as the database. Native JSONB for recurrence
  configs, mature timezone support (we'll need it for working hours).
- **SQLAlchemy 2.0** ORM in **sync** mode. Async ORM is a tax we
  don't need to pay for booking volumes; sync is simpler and the
  performance ceiling is far above what a single-business deployment
  ever sees. (Mirrors colony's deliberate choice.)
- **Pydantic-settings** for config from env vars. Standard.
- **Argon2ID** (via `pwdlib`) for passwords; **PyJWT** for tokens.

## MCP server — FastMCP

- **FastMCP** is the Pythonic MCP framework that the official MCP
  Python SDK is built on. Declarative tool registration, automatic
  schema derivation from Python type hints.
- Run as a separate process (own `pyproject.toml`, own Dockerfile).
  Trust boundary, deployability, language flexibility — even though
  we're Python everywhere now.

## Tooling

- **uv** for Python dependency management. Fast, reproducible, drop-in
  for pip/poetry.
- **Ruff** for lint + format (ruff replaces black, flake8, isort).
- **Pyright** for strict type checking. Strict mode — we want the
  errors before runtime.
- **Pytest** with a real PostgreSQL test database (no SQLite, no
  mocks). Mirrors colony's choice; integration parity > test speed.

## Container / deploy

- **Docker** + **docker-compose** for local. One command to come up.
- **Helm** chart shape reserved (placeholder dir). Will populate when
  there's an actual K8s deploy.
- **MkDocs Material** for these docs. Zero JS framework needed; static
  site, deployed to GitHub Pages on `main`.

## What we're not using (and why)

- **Async SQLAlchemy / databases** — overkill at this scale.
- **Next.js / React** — no frontend in v1. The "frontend" is the chat
  client (someone else's UI). If an admin dashboard becomes painful
  via OpenAPI, revisit.
- **GraphQL** — REST is enough; the MCP layer already gives the LLM
  exactly the tools it needs.
- **Alembic from day one** — for v1 we use `Base.metadata.create_all()`
  during the schema-flux phase. Add Alembic when the schema stabilizes
  and a real production deploy exists.
- **Celery / Redis queue** — no async work yet. Add when reminders or
  WhatsApp inbound queueing show up in Phase 4/5.
