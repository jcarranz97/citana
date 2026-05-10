# WhatsApp Integration

The long-term distribution surface is WhatsApp. Two viable paths.

## Option A — Evolution API (unofficial, Baileys-based)

[Evolution API](https://github.com/EvolutionAPI/evolution-api) is an
open-source REST/WebSocket gateway built on top of Baileys, which talks
to WhatsApp Web's protocol.

**Pros:**

- Open source (Apache 2.0), self-hosted, no paid API.
- REST endpoints map cleanly onto our backend's needs.
- Excellent for prototyping — log in by scanning a QR code from a
  WhatsApp on your phone.

**Cons:**

- Uses **unofficial** WhatsApp Web protocol.
- Violates WhatsApp Terms of Service in production. Phone numbers can
  be banned (ranges from rare to common depending on usage volume,
  message content, and how "spammy" the traffic looks).
- Breaks whenever Meta changes the WhatsApp Web protocol — back online
  once the Baileys community updates.

**Verdict:** great for v1 prototyping. Ship a usable end-to-end demo
fast, learn what you actually need.

## Option B — WhatsApp Cloud API (official)

Meta's [WhatsApp Cloud API](https://developers.facebook.com/docs/whatsapp/cloud-api)
is the officially sanctioned way for businesses to send/receive
WhatsApp messages.

**Pros:**

- Compliant. No risk of bans.
- Free tier (~1k conversations/month for service messages).
- Stable, documented, well-supported.

**Cons:**

- Not open-source — it's a SaaS API. The system depends on Meta's
  uptime.
- Requires a verified Business account (not strictly hard, but more
  paperwork than scanning a QR code).
- Template messages have approval workflows for outbound notifications.

**Verdict:** the destination for production. Migrate when the
prototype is validated and we're done iterating quickly.

## Migration path

The good news: **Evolution API can also front the official Cloud API**.
That means the migration is mostly a config change, not a code rewrite.
Plan accordingly:

1. Build the agent loop (LLM ↔ MCP) against an HTTP webhook
   abstraction.
2. Wire Evolution API in pointing at unofficial WhatsApp Web for the
   prototype.
3. Switch Evolution API to Cloud API mode (or talk Cloud API directly)
   for production.

## Open questions

- **Conversation state.** WhatsApp messages are essentially
  unconnected. We need a session store keyed by phone so the LLM can
  thread messages. PostgreSQL is fine; LangChain-style memory is
  overkill for booking flows.
- **Inbound handling.** Webhook → queue → agent worker is the right
  shape. Don't process directly in the webhook (we lose retries).
- **Outbound proactive messages.** Reminders ("your appointment is
  tomorrow"). On Cloud API these need an approved template; that
  changes the Phase 5 design slightly.
