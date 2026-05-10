# Citana Backend

FastAPI backend for Citana, a self-hostable booking
chatbot. Python 3.13+, SQLAlchemy 2.0, Pydantic 2.0, PostgreSQL,
JWT auth.

---

## Running Commands

```bash
# Start everything (recommended)
docker compose up --build           # API at http://localhost:8000

# Backend only (no Docker)
cd backend
uv sync
uv run fastapi dev                  # hot reload

# Tests — PYTHONPATH=. is required; without it, system packages can
# leak into the path and cause import errors at pytest startup.
PYTHONPATH=. uv run pytest                      # all tests
PYTHONPATH=. uv run pytest tests/auth/          # single domain
PYTHONPATH=. uv run pytest -k test_name         # single test

# Linting & formatting
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .

# Type checking
PYTHONPATH=. uv run pyright .
```

Pre-commit runs Hadolint, markdownlint, and YAML/JSON validators on
every commit — don't bypass with `--no-verify`. Ruff and Pyright are
**not** pre-commit hooks; run them directly via `uv run`.

---

## Project Layout

```text
backend/
├── app/
│   ├── main.py          # FastAPI factory, CORS, router include, exception handlers
│   ├── config.py        # Settings (env vars via Pydantic BaseSettings)
│   ├── database.py      # SQLAlchemy engine, SessionLocal, get_db()
│   ├── exceptions.py    # AppExceptionError base + global exception handlers
│   ├── dependencies.py  # Re-exports: CurrentActiveUser, CurrentUser, get_db
│   ├── models.py        # BaseModel (id UUID, created_at, updated_at, active bool)
│   ├── schemas.py       # Global Pydantic schemas (AppBaseModel)
│   └── <domain>/        # auth | appointments (Phase 1) | future: customers, services, resources, availability
├── tests/               # pytest suite (mirrors domain layout)
└── pyproject.toml
```

### Domain Module Layout

Every domain has exactly this structure — follow it when adding a new
domain:

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

---

## Code Conventions

- **Type hints** on every function — no untyped code.
- **Google-style docstrings** on public functions.
- **88-character** line limit (Ruff enforces).
- **Double quotes** everywhere.
- **Dependency injection** via `Annotated[X, Depends(Y)]` pattern.
- All routes prefixed `/api/v1/`.
- JWT Bearer token in `Authorization` header.

### Router Pattern

```python
@router.post("/", response_model=FooResponse, status_code=201)
async def create_foo(
    payload: FooCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: CurrentActiveUser,
) -> FooResponse:
    return FooService.create_foo(db, payload, current_user.id)
```

- Routers are thin — no business logic, only call service methods.
- Always use `CurrentActiveUser` (not `CurrentUser`) unless the
  endpoint explicitly serves inactive users.
- Use `CurrentAdminUser` for admin-only endpoints.

### Service Pattern

```python
class FooService:
    @staticmethod
    def create_foo(db: Session, payload: FooCreate) -> Foo:
        # business logic here
        db.add(obj)
        db.commit()
        db.refresh(obj)
        return obj
```

- Static methods only — no `self` / `cls` state.
- Raise domain exceptions, never HTTP exceptions.
- Always `db.commit()` + `db.refresh(obj)` after writes.

---

## Error Handling

All exceptions inherit from `AppExceptionError` (defined in
`app/exceptions.py`). Global handlers in `main.py` convert every
`AppExceptionError` to the standard JSON envelope automatically.

```python
# app/exceptions.py — base class
class AppExceptionError(Exception):
    def __init__(self, error_code, message, status_code=400, details=None): ...

# domain exceptions.py
class FooNotFoundExceptionError(AppExceptionError):
    def __init__(self, foo_id: UUID):
        super().__init__(
            error_code=ErrorCode.FOO_NOT_FOUND,
            message=f"Foo {foo_id} not found.",
            status_code=404,
        )
```

Standard error response (never construct manually):

```json
{
  "success": false,
  "error": { "code": "FOO_NOT_FOUND", "message": "...", "details": {} }
}
```

Rules:

- **Never** raise `HTTPException` directly inside service methods.
- **Always** raise a domain-specific exception and let the global
  handler convert it.
- `ErrorCode` enums live in `constants.py`. Status codes: 400
  validation, 401 auth, 403 forbidden, 404 not found, 409 conflict,
  422 unprocessable.

---

## Database Patterns

### Base Model

Every ORM model inherits `BaseModel` from `app/models.py`:

```python
class Foo(BaseModel):
    __tablename__ = "foos"
    name: Mapped[str] = mapped_column(String(100))
```

Key rules:

- **UUID primary keys** — always, inherited from BaseModel.
- **Soft deletes** — set `active = False`; never `db.delete()`.
- **Timestamps** — `created_at` and `updated_at` are auto-managed.

### Migrations

Phase 1 uses `Base.metadata.create_all()` at startup — fine while the
schema is moving. Alembic is added in Phase 2 when the booking domains
land.

---

## Authentication

```python
from app.dependencies import CurrentActiveUser, CurrentAdminUser

async def endpoint(current_user: CurrentActiveUser): ...
```

- `CurrentUser` — resolves JWT → raises 401 if invalid (allows
  inactive).
- `CurrentActiveUser` — resolves JWT → raises 401/403 if
  invalid/inactive.
- `CurrentAdminUser` — resolves JWT and asserts `role == "admin"`.
- Passwords hashed with Argon2ID via `pwdlib`.
- JWT signed with `SECRET_KEY` from config; `ALGORITHM` is HS256 by
  default.
- Auth uses **username + password** (no email). A default admin user
  is created automatically on first deploy from
  `DEFAULT_ADMIN_USERNAME` and `DEFAULT_ADMIN_PASSWORD` env vars
  (defaults: `admin` / `citana-admin`).
- JWT `sub` claim holds the username.

---

## Testing

### Fixtures (backend/tests/conftest.py)

```python
db      # Session — fresh tables per test (create_all → test → drop_all)
client  # TestClient with get_db overridden to use the test session
```

Each domain has its own `tests/<domain>/conftest.py` with
domain-specific fixtures (users, etc.).

### Conventions

- Test files mirror domain layout: `tests/<domain>/test_<layer>.py`.
- Class per feature: `class TestCreateFoo:` with `def test_*` methods.
- Every new endpoint needs at least:
  - `test_requires_auth` — 401 without token.
  - `test_<happy_path>` — 200/201 with valid data.
  - `test_not_found` — 404 for unknown ID.
  - `test_<conflict>` — 409 if the domain has uniqueness constraints.
- Use `client.post/get/put/delete("/api/v1/<route>", headers=auth_headers)`.
- Auth headers helper:

```python
def get_auth_headers(client: TestClient, user: User) -> dict:
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": user.username, "password": RAW_PASSWORD},
    )
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
```

- Do not mock the database — tests use a real PostgreSQL test
  database.
- Do not use `db.delete()` in tests — use the service's soft-delete
  method.
- Never delete existing tests.

---

## Adding a New Domain

Follow this checklist in order:

1. Create `app/<domain>/` with all 7 files: `router.py`, `schemas.py`,
   `models.py`, `service.py`, `dependencies.py` (if needed),
   `exceptions.py`, `constants.py`. Add `__init__.py`.
2. Inherit the ORM model from `app.models.BaseModel`.
3. Define `ErrorCode` enum in `constants.py` first — name values as
   `DOMAIN_CONDITION` (e.g., `APPOINTMENT_NOT_FOUND`).
4. Write exceptions in `exceptions.py` inheriting `AppExceptionError`.
5. Write service methods — static methods only, no HTTP types.
6. Write Pydantic schemas with
   `model_config = ConfigDict(from_attributes=True)` on response
   models.
7. Write the router using the existing domain routers as templates.
8. Register the router in `app/main.py`:

   ```python
   from app.<domain>.router import router as <domain>_router
   app.include_router(<domain>_router, prefix="/api/v1")
   ```

9. Create `tests/<domain>/` with `__init__.py`, `conftest.py`, and at
   least one `test_router.py`.

---

## Cross-Domain Rules

Domains do not import from each other's `service.py`. If you need
shared logic, add a local `_helper` function in the calling domain's
`service.py`.

---

## Validation Checklist Before Finishing

```bash
cd backend
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .
PYTHONPATH=. uv run pyright .
PYTHONPATH=. uv run pytest
```

From repo root, also:

```bash
pre-commit run --files backend/app/<changed-files>
```

Pyright is strict — add type annotations to every function you write
or touch, including return types. Never use `Any` unless there is no
alternative and you add a comment explaining why.

---

## What NOT to Do

- Do not import `HTTPException` in service files.
- Do not use `db.delete()` anywhere — soft deletes only.
- Do not share service classes across domains.
- Do not add business logic to router functions.
- Do not skip `db.refresh(obj)` after `db.commit()` when the caller
  needs up-to-date computed values.
- Do not add endpoints without auth unless explicitly public (only
  `/auth/login`, `/health`, `/<domain>/health`).
- Do not use `Any` in type annotations without a comment.
- Do not hard-code user IDs or secrets — use fixtures and config.
