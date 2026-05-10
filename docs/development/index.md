# Development Guide

Welcome. This section covers everything you need to work on Citana
locally.

## Project structure

```
citana/
├── backend/         # FastAPI application
│   ├── app/         # Domain modules
│   ├── scripts/
│   ├── tests/
│   └── Dockerfile
├── mcp/             # MCP server (placeholder; Phase 3)
├── docs/            # MkDocs Material — what you're reading
├── helm/            # Kubernetes chart (placeholder)
├── scripts/         # Repo-level scripts (placeholder)
├── .github/         # CI workflows
└── docker-compose.yml
```

See `AGENTS.md` at each level for component-specific conventions:

- Repo root `AGENTS.md` — repo-wide rules (PYTHONPATH, soft-delete,
  domain isolation).
- `backend/CLAUDE.md` — backend domain pattern, testing, error handling.
- `mcp/CLAUDE.md` — MCP server scope (placeholder until Phase 3).

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (only if developing without Docker)
- `uv` (only if developing without Docker) — `pip install uv`
- `pre-commit` — `pip install pre-commit && pre-commit install`

## Workflow

1. Create a feature branch.
2. Make your change. Follow the conventions in the relevant `AGENTS.md`
   / `CLAUDE.md`.
3. Run the validation checklist (see [Code Quality](code-quality.md)).
4. Commit (pre-commit hooks run automatically).
5. Open a PR.

## Next steps

- [Local Setup](setup.md) — set up your dev environment.
- [Code Quality](code-quality.md) — code standards, linting, type
  checking, pre-commit hooks.
