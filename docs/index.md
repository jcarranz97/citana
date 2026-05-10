# Citana Documentation

Welcome. Citana is a self-hostable booking assistant: end
customers describe what they want in natural language, and an LLM
(connected to your business data via the Model Context Protocol) creates
the appointment. The first chat surface is any open-source MCP-aware
client; the long-term target is WhatsApp.

## What's in this site

This documentation is split into three big sections plus an **Ideas**
area where early design notes live before they harden into formal
architecture docs.

<div class="grid cards" markdown>

-   💡 **[Ideas](ideas/overview.md)**

    ---

    Early design notes — vision, architecture sketch, MCP tool list, chat
    client comparison, WhatsApp options, tech-stack rationale.

-   🏗️ **[Architecture](architecture/backend.md)**

    ---

    Hardened design docs for the backend, the MCP server, the database
    schema, the API, and deployment.

-   🛠️ **[Development](development/index.md)**

    ---

    Local setup, code-quality conventions, contributor workflow.

-   🗺️ **[Roadmap](roadmap.md)**

    ---

    What's planned, in progress, and shipped.

</div>

## Components

| Component | Tech | Status |
|-----------|------|--------|
| Backend API | FastAPI + PostgreSQL | Skeleton scaffolded |
| MCP server | FastMCP (Python) | Placeholder — not yet implemented |
| Chat client | Any open-source MCP client (opencode / LibreChat / …) | External |
| WhatsApp gateway | Evolution API → Cloud API later | Future iteration |

!!! info "Project status"
    This is an early-stage personal project. The first iteration sets up
    the repo skeleton and the docs you are reading. Real booking
    endpoints, the MCP server, and the WhatsApp integration will land in
    later iterations — see the [roadmap](roadmap.md).

## Getting started

- Clone the repo and run `docker compose up --build`.
- Visit <http://localhost:8001/docs> for the API and
  <http://localhost:2012> for these docs.
- Read [Local Setup](development/setup.md) for the full dev workflow.
