# Citana

A self-hostable booking chatbot — FastAPI backend, MCP server, and (later)
a WhatsApp front door. Built so end customers can book appointments
through a conversational interface without filling out forms.

## About the name

**Citana** is pronounced **see-TAH-nah** — three syllables, stress on
the middle one (*ci-**ta**-na*).

The name is built from the Spanish word *cita* ("appointment", also
"date") with a soft, name-like ending. The intent is for Citana to feel
like a persona rather than a piece of infrastructure — the friendly
assistant who keeps your agenda and lets the people you care about
reach into it. Spanish-rooted, easy to pronounce in English, and short
enough to fit on a WhatsApp avatar.

## Overview

Three components, deployable independently:

- **Backend** (FastAPI + PostgreSQL) — REST API for appointments, services,
  resources, customers; admin auth via JWT.
- **MCP server** (FastMCP) — exposes a curated subset of the backend as MCP
  tools (`check_availability`, `book_appointment`, …) for any
  MCP-compatible chat client.
- **Chat client** — any open-source MCP-aware client during development
  (opencode, LibreChat, LobeChat, Dive). WhatsApp via Evolution API or
  WhatsApp Cloud API later.

## Quick Start

### Prerequisites

- Docker and Docker Compose

### Run with Docker

```bash
git clone https://github.com/jcarranz97/citana.git
cd citana
docker compose up --build
```

### Access the Application

- **API**: <http://localhost:8001>
- **API Docs**: <http://localhost:8001/docs>
- **Documentation**: <http://localhost:2012>

## Tech Stack

- **Backend**: FastAPI (Python 3.13), SQLAlchemy 2.0, Pydantic 2
- **Database**: PostgreSQL 15
- **MCP server**: FastMCP (planned, separate component)
- **Documentation**: MkDocs Material
- **Containerization**: Docker & Docker Compose

## Documentation

For detailed information, visit the official documentation at
<https://jcarranz97.github.io/citana/>, or run a local copy with:

```bash
docker compose up docs   # served at http://localhost:2012
# or, outside Docker:
mkdocs serve
```

The source lives under `docs/`. Start with `docs/ideas/overview.md`.

## Contributing

This is a personal project. See the
[development guide](https://jcarranz97.github.io/citana/development/)
for setup, conventions, and the validation checklist.

## License

MIT License — see the [LICENSE](LICENSE) file for details.

---

**[View Full Documentation](https://jcarranz97.github.io/citana/)** |
**[Development Guide](https://jcarranz97.github.io/citana/development/)** |
**[Issues](https://github.com/jcarranz97/citana/issues)**
