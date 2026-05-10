# Backend Architecture

The backend follows a modular, domain-driven structure with FastAPI,
SQLAlchemy 2.0, and PostgreSQL. The repo's `backend/` directory layout
mirrors the [colony](https://github.com/jcarranz97/colony) project's
conventions — see `backend/CLAUDE.md` for the full canonical guide.

## Architecture overview

The backend is built using **FastAPI** with a **domain-driven design**
approach: each business domain (`auth`, `appointments`, future
`services`/`resources`/…) is a self-contained module with its own
models, schemas, services, and routes.

### Key principles

- **Domain-Driven Design.** Each domain is a separate module under
  `app/`.
- **Separation of concerns.** Routes are thin; services hold business
  logic; ORM lives in `models.py`.
- **Domain isolation.** Domains do not import each other's `service.py`.
- **Soft deletes only.** Set `active = False` — never `db.delete()`.
- **Sync SQLAlchemy 2.0.** Deliberate; async adds complexity we don't
  need at booking-volume scale.

## Domain module layout

```text
app/<domain>/
├── router.py        # FastAPI routes — thin; delegates to service
├── schemas.py       # Pydantic request/response models
├── models.py        # SQLAlchemy ORM model (inherits BaseModel)
├── service.py       # All business logic; no HTTP concerns
├── dependencies.py  # Domain-level Depends() helpers (optional)
├── exceptions.py    # Domain-specific exceptions (inherit AppExceptionError)
├── constants.py     # Enums, error codes, business constants
└── utils.py         # Pure helper functions (optional)
```

## Cross-cutting modules

```text
app/main.py          # FastAPI factory, lifespan, exception handlers, router include
app/config.py        # Pydantic-settings; .env support; nested AUTH/ADMIN settings
app/database.py      # SQLAlchemy engine, SessionLocal, get_db()
app/exceptions.py    # AppExceptionError base + global exception handlers
app/dependencies.py  # Re-exports of common Depends() helpers
app/models.py        # BaseModel: id (UUID), created_at, updated_at, active
app/schemas.py       # AppBaseModel — extra="forbid" base for request schemas
```

## Authentication

- JWT bearer tokens, signed with `HS256`, secret from
  `AUTH_SECRET_KEY` env var.
- Argon2ID password hashing via `pwdlib`.
- A default admin user (`admin` / `citana-admin`) is bootstrapped
  on first startup; configurable via `DEFAULT_ADMIN_USERNAME` and
  `DEFAULT_ADMIN_PASSWORD`.

## Error handling

All exceptions inherit from `AppExceptionError`. The global handler in
`app/main.py` converts every `AppExceptionError` to a standard JSON
envelope:

```json
{
  "success": false,
  "error": {
    "code": "APPOINTMENT_NOT_FOUND",
    "message": "Appointment not found",
    "details": {}
  }
}
```

Services raise domain exceptions; never `HTTPException`. The router and
the global handler convert them.

## Migrations

Phase 1 uses `Base.metadata.create_all()` at startup — fine while the
schema is moving. Alembic is added in Phase 2 when the booking domains
land and the schema stabilizes.

## Deployment

Docker image based on `python:3.13-slim` with `uv` for dependency
management. Run as a single container; database is a separate
PostgreSQL service. See [Deployment](deployment.md) (TBD) for the
production layout.
