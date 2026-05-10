# API Specification

Live OpenAPI is at <http://localhost:8000/docs> when the backend is
running. This page documents the stable shape; for full request/response
details (including all fields), use the live docs.

## Conventions

- All routes are prefixed `/api/v1/`.
- Success: returns the resource (or list of resources) directly.
- Error: returns the standard envelope:

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

- Auth: `Authorization: Bearer <jwt>` on every endpoint except `POST
  /auth/login` and `GET /health`.

## Endpoints (Phase 1)

### Auth

| Method | Path                    | Description                       | Auth     |
|--------|-------------------------|-----------------------------------|----------|
| POST   | `/auth/login`           | Get JWT (form-encoded body)       | None     |
| GET    | `/auth/me`              | Current user info                 | Bearer   |
| PUT    | `/auth/me`              | Update profile                    | Bearer   |
| PUT    | `/auth/me/password`     | Change own password               | Bearer   |
| POST   | `/auth/register`        | Create user (admin-only)          | Admin    |
| GET    | `/auth/users`           | List all users                    | Admin    |
| GET    | `/auth/users/{id}`      | Get user by id                    | Admin    |
| PUT    | `/auth/users/{id}`      | Admin update user                 | Admin    |
| DELETE | `/auth/users/{id}`      | Soft-deactivate user              | Admin    |
| GET    | `/auth/health`          | Auth health check                 | None     |

### Appointments (stub)

| Method | Path                       | Description                | Auth   |
|--------|----------------------------|----------------------------|--------|
| GET    | `/appointments/`           | List appointments          | Bearer |
| POST   | `/appointments/`           | Create appointment         | Bearer |
| GET    | `/appointments/{id}`       | Get appointment by id      | Bearer |
| PUT    | `/appointments/{id}`       | Update appointment         | Bearer |
| DELETE | `/appointments/{id}`       | Cancel appointment (soft)  | Bearer |
| GET    | `/appointments/health`     | Domain health check        | None   |

The Phase 1 appointment endpoints are deliberately minimal — they
exist to validate the scaffolding. Phase 2 adds the customer/service/
resource model and conflict detection.

### Health

| Method | Path        | Description              |
|--------|-------------|--------------------------|
| GET    | `/health`   | Application health check |
| GET    | `/`         | Root info                |

## Future endpoints

Phase 2 adds resource catalogs (services, resources, working_hours,
blackouts) and turns appointments into a properly normalized aggregate
with conflict checks. Phase 3 adds nothing here — the new surface is
the MCP server, documented in [MCP Server](mcp.md).
