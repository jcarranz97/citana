# Deployment

Two paths: docker-compose for local / single-VPS, and Helm for
Kubernetes (future).

## Local / single VPS — docker-compose

```bash
docker compose up --build
```

Brings up:

| Service | Image | Host port → container | Purpose |
|---|---|---|---|
| `postgres` | `postgres:15-alpine` | `5433 → 5432` | Database |
| `backend` | local `./backend/Dockerfile` | `8001 → 8000` | FastAPI app |
| `docs` | `squidfunk/mkdocs-material:latest` | `2012 → 2011` | These docs |

Host ports are offset to avoid clashing with other local stacks (e.g.
the `colony` reference project on 5432/8000/2011). Container ports stay
at the conventional defaults.

The backend depends on postgres being `service_healthy`. The
`postgres_data` named volume persists the database across `docker
compose down` (use `-v` to wipe).

## Production considerations

For a single-VPS deploy:

- Put the backend behind **nginx / Caddy / Traefik** with TLS
  termination. Issue certs via Let's Encrypt.
- Move secrets out of `docker-compose.yml` — use an `.env` file (not
  committed) or a real secrets store.
- Set `DEFAULT_ADMIN_PASSWORD` and `AUTH_SECRET_KEY` to strong values
  before first start. The defaults are for local dev only.
- Mount Postgres data on a volume backed by SSD; schedule daily
  `pg_dump` backups (see how colony does it in the
  [colony docs](https://github.com/jcarranz97/colony) — copy that
  pattern when this scales).
- Run `docker compose up -d` (detached) and let the system manage the
  restart policies.

## MCP server (Phase 3)

When the MCP server lands it will be a separate service in the same
docker-compose, on its own port. It connects to the backend via HTTP
on the docker network. See [MCP Server](mcp.md) for the design.

## Kubernetes (later)

A `helm/` directory is reserved at the repo root. It will hold a Helm
chart for the backend + MCP server when there's a real cluster to
deploy onto. Single-VPS via docker-compose is the v1 target.

## Domain / ports recap

| Surface | Local | Production (suggested) |
|---|---|---|
| Backend API | `http://localhost:8001` | `https://api.<your-domain>` |
| API docs (Swagger) | `http://localhost:8001/docs` | restrict via auth proxy or VPN |
| MkDocs site | `http://localhost:2012` | GitHub Pages (deployed via CI) |
| MCP server | `http://localhost:9000` *(planned)* | internal-only, not exposed |
