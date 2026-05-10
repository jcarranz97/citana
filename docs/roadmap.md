# Project Roadmap

This roadmap outlines the planned development phases for Citana. Items
move down the list as they ship.

## Phase 1: Foundation 🚧

- [x] Set up repository structure
- [x] Configure mkdocs-material
- [x] Scaffold FastAPI backend (mirroring colony patterns)
- [x] Scaffold auth domain (admin auth, JWT)
- [x] Scaffold appointments domain (one example)
- [ ] Wire docker-compose and verify all services come up healthy
- [ ] CI pipeline (ruff + pyright + pytest, docs deploy)

## Phase 2: Booking Domain 📅

- [ ] Customers domain (phone-number-keyed, no account required)
- [ ] Services domain (catalog: name, duration, price, optional resource
  requirement)
- [ ] Resources domain (generic — staff member, table, room)
- [ ] Availability domain (working hours per resource, blackouts)
- [ ] Conflict detection on appointment create
- [ ] List customer's upcoming appointments by phone

## Phase 3: MCP Server 🔮

- [ ] FastMCP scaffold under `mcp/`
- [ ] Tools: `list_services`, `check_availability`, `book_appointment`,
  `cancel_appointment`, `list_my_appointments`
- [ ] Authentication strategy (service-to-service token vs per-user)
- [ ] Test from opencode CLI and from LibreChat

## Phase 4: WhatsApp Front Door 🔮

- [ ] Evaluate Evolution API for prototype
- [ ] Webhook → agent loop → MCP tool calls → WhatsApp reply
- [ ] Migrate to WhatsApp Cloud API for production
- [ ] Conversation state / session memory

## Phase 5: Polish 💫

- [ ] Admin web UI (or Retool-like) for managing the catalog
- [ ] Reminders (24h before appointment, via WhatsApp)
- [ ] Analytics dashboard (no-show rate, busy hours)
- [ ] Multi-tenant support if/when needed

---

**Legend:**

- ✅ Completed
- 🚧 In Progress
- 📅 Planned
- 🔮 Future Consideration
- 💫 Polish Phase
