# Citana MCP Server

This directory will hold the **MCP server** — a separate process that
exposes a curated subset of the backend's booking functionality as MCP
tools, callable by any MCP-compatible LLM client (opencode, LibreChat,
LobeChat, …).

> **Status: placeholder. Do not implement yet.**
>
> The MCP server is scheduled for **Phase 3** (see
> `../docs/roadmap.md`). The current iteration is intentionally just the
> directory skeleton plus this file. The design lives in:
>
> - `../docs/architecture/mcp.md` — target architecture.
> - `../docs/ideas/mcp-design.md` — draft tool list and open questions.

## Planned tools

The MCP server will expose **only** customer-facing operations. Admin
operations (catalog management, working hours, deleting records) stay
REST-only on the backend.

| Tool | Purpose |
|---|---|
| `list_services` | Public read of the active service catalog. |
| `check_availability` | Compute open slots for a service over a date range. |
| `book_appointment` | Create an appointment, creating the customer record on first booking. |
| `cancel_appointment` | Customer-scoped cancel — phone must match the appointment's customer. |
| `list_my_appointments` | Returns the caller's upcoming appointments (filtered by phone). |

See `../docs/ideas/mcp-design.md` for argument shapes and the explicit
list of operations that will *not* be exposed.

## Planned tech

- **FastMCP** (`pip install fastmcp` — built on the official MCP Python
  SDK).
- Same Python 3.13, same tooling (uv, ruff, pyright) as the backend.
- Own `pyproject.toml`, own Dockerfile — runnable as a standalone
  process.
- Talks to the backend over HTTP using a service-to-service token (or
  per-customer ephemeral token; see open questions in
  `../docs/ideas/mcp-design.md`).

## Trust boundary (the important part)

The MCP server is **public-facing** — it's the surface the LLM (and
ultimately, the customer's WhatsApp message) hits. Treat it as
untrusted input. Specifically:

- Every customer-scoped tool must verify ownership (e.g.
  `cancel_appointment` checks that the supplied `customer_phone`
  matches the appointment's customer record) **inside the MCP layer**,
  before forwarding to the backend.
- No tool may ever return data across customers.
- No tool may ever bypass admin-only operations.

If you find yourself wanting to expose something to the LLM that feels
sensitive, that's a sign it should stay REST-only.

## When implementation starts

Use the colony backend conventions as the template (7-file domain
pattern doesn't apply directly here, but the style choices do):

- Strict type hints on every function.
- Google-style docstrings.
- 88-char line length, double quotes.
- `uv` for deps, ruff + pyright for QA, pytest for tests.
- Tests against a real backend instance (no mocking — same philosophy
  as colony's "real Postgres test DB" stance).
