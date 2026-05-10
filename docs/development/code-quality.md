# Code Quality

## Validation checklist

Run all of these before opening a PR; CI runs them too:

```bash
cd backend
PYTHONPATH=. uv run ruff check . --fix
PYTHONPATH=. uv run ruff format .
PYTHONPATH=. uv run pyright .
PYTHONPATH=. uv run pytest
```

From the repo root, also run pre-commit on the files you changed:

```bash
pre-commit run --files <changed files>
```

Do **not** use `--all-files` — it can OOM on large repos and isn't
needed for small PRs.

## Linting and formatting — Ruff

- `ruff check` — lint.
- `ruff format` — format (replaces black).
- Config lives in `backend/pyproject.toml` under `[tool.ruff]`.
- Line length: **88** (Python). Markdown is **80** (markdownlint).
- Quotes: double.
- Docstrings: Google style.
- Many lint rules enabled (E, W, F, I, B, UP, C90, N, D, S, A, ANN,
  COM, C4, DTZ, PIE, T20, PYI, PT, Q, RSE, RET, SLF, SIM, ARG, PTH,
  PL, RUF). See pyproject.toml for the full list and per-file ignores.

## Type checking — Pyright

Pyright runs in strict mode. Every function gets type annotations,
including return types. `Any` is allowed only with a comment explaining
why.

## Tests — Pytest

- Test files mirror the domain layout: `tests/<domain>/test_*.py`.
- Class per feature: `class TestCreateAppointment:`.
- Real PostgreSQL test database (no SQLite, no mocks). Fresh schema
  per test (create_all → test → drop_all).
- Auth helper:

```python
def get_auth_headers(client: TestClient, user: User) -> dict:
    resp = client.post(
        "/api/v1/auth/login",
        data={"username": user.username, "password": RAW_PASSWORD},
    )
    return {"Authorization": f"Bearer {resp.json()['access_token']}"}
```

Every new endpoint gets at least:

- `test_requires_auth` — 401 without a token.
- `test_<happy_path>` — 200/201 with valid input.
- `test_not_found` — 404 for unknown id.
- `test_<conflict>` — 409 for uniqueness/conflict cases.

## Pre-commit hooks

Run on every commit. Configured in `.pre-commit-config.yaml`:

- File hygiene: trailing whitespace, EOF newline, YAML/JSON/TOML
  validators, mixed line endings.
- `hadolint-docker` — Dockerfile lint.
- `markdownlint` — markdown lint (auto-fix; excludes `docs/`).

Ruff and Pyright are **not** pre-commit hooks — run them directly via
`uv run`.

## Markdown rules

- 80-character line length on prose (MD013 in `.markdownlint.json`).
- Code blocks and table rows are exempt.
- Files end with a newline; no trailing spaces.

## What to avoid

- `db.delete()` — use soft delete (`active = False`).
- `HTTPException` inside service files — raise domain exceptions
  inheriting `AppExceptionError`.
- Cross-domain service imports — keep domains isolated.
- Untyped functions, `Any` without justification.
- `--no-verify` to skip pre-commit.
