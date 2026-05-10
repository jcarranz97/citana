# Citana

A self-hostable booking chatbot. FastAPI backend + MCP server, designed
to be reachable from open-source MCP-aware chat clients today and from
WhatsApp later via a gateway. See `backend/AGENTS.md` and `mcp/AGENTS.md`
for component-specific instructions.

## Quick Start

```bash
docker compose up --build
# API   → http://localhost:8001
# Docs  → http://localhost:2012
```

## Commands

### Backend

```bash
cd backend
uv run fastapi dev                          # hot reload
PYTHONPATH=. uv run pytest                  # all tests
PYTHONPATH=. uv run pytest tests/auth/      # single domain
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .
PYTHONPATH=. uv run pyright .
```

### Pre-commit (from repo root)

```bash
# List only the files you changed — do NOT use --all-files (OOM risk):
pre-commit run --files backend/app/appointments/service.py
pre-commit run markdownlint --files AGENTS.md
```

Ruff and Pyright are **not** pre-commit hooks — run them directly via
`uv run`.

## Structure

```
backend/app/      # FastAPI domains: auth, appointments
mcp/              # MCP server (placeholder; FastMCP, future iteration)
docs/             # MkDocs Material — ideas, architecture, development
helm/             # Kubernetes manifests (placeholder)
scripts/          # Repo-level scripts (placeholder)
```

## Key Constraints

- **PYTHONPATH=.** required for all backend pytest/ruff/pyright invocations.
- **Soft deletes only** — set `active = False`; never `db.delete()`.
- **Domain isolation** — domains do not import each other's `service.py`.
- **No `HTTPException` in services** — raise domain exceptions (inherit
  `AppExceptionError`); global handler converts to JSON envelope.
- **80-char prose limit** on `.md` files outside `docs/` (markdownlint
  MD013). Code blocks and table rows are exempt.

## Validation Checklist

```bash
cd backend
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .
PYTHONPATH=. uv run pyright .
PYTHONPATH=. uv run pytest
pre-commit run --files <changed files>
```

## Default Admin

`admin` / `citana-admin` (configurable via `DEFAULT_ADMIN_USERNAME` /
`DEFAULT_ADMIN_PASSWORD` env vars on deploy).

## Docs

- `docs/ideas/` — early design notes (overview, architecture, MCP design,
  chat client options, WhatsApp integration, tech stack).
- `docs/architecture/backend.md` — backend architecture.
- `docs/architecture/mcp.md` — MCP server design.
- `docs/architecture/database-schema.md` — DB design.
- `docs/architecture/api-specification.md` — API endpoints.
- `docs/development/setup.md` — dev setup.
- `docs/development/code-quality.md` — code standards.
- `docs/requirements.md` — functional + non-functional requirements.
