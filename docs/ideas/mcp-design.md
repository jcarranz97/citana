# MCP Design — Tool List Draft

The MCP server is the **narrow** contract for the LLM. It exposes only
what an end customer should be able to do, with strict argument
validation. Admin operations stay REST-only.

## Tools to expose (Phase 3)

### `list_services`

Public read. No arguments.

Returns the active service catalog: name, description, duration, price.

### `check_availability`

```text
check_availability(
    service_id: str,
    date_from: date,
    date_to: date,
    resource_id: str | None = None,
) -> list[Slot]
```

Returns available time slots in the given range. Optionally narrowed
to a specific resource (e.g. "I want stylist Maria specifically").

### `book_appointment`

```text
book_appointment(
    service_id: str,
    customer_phone: str,        # E.164 format, validated
    start_time: datetime,
    customer_name: str | None = None,
    resource_id: str | None = None,
    notes: str | None = None,
) -> Appointment
```

Creates the customer record on first booking (keyed by phone). Performs
conflict and working-hour checks. Returns the created appointment.

### `cancel_appointment`

```text
cancel_appointment(
    appointment_id: str,
    customer_phone: str,        # must match the appointment's customer
) -> Appointment
```

Customer-scoped. The MCP layer verifies the phone matches the
appointment's customer record before applying the cancel. No customer
can cancel another customer's booking.

### `list_my_appointments`

```text
list_my_appointments(
    customer_phone: str,
) -> list[Appointment]
```

Returns the caller's upcoming appointments. Past appointments are
filtered out by default; LLM can add a flag later if needed.

## What MCP will NOT expose

These stay REST-only and require admin JWT:

- Creating, updating, or deleting services.
- Creating, updating, or deleting resources.
- Setting working hours or blackouts.
- Listing all customers / all appointments across customers.
- Hard delete of any record.
- User management.

The reason is the trust boundary. The LLM is **not** a privileged
caller; it's a public-facing surface that should only ever do things
on behalf of the specific customer it's talking to.

## Authentication questions

Open. Two reasonable models:

1. **Service token between MCP and backend** — the MCP server holds a
   static signed token (set via env) and uses it on every backend call.
   Authorization happens *inside* the MCP layer based on tool argument
   validation (e.g. phone number check). Simple, fits self-hosted.
2. **Per-customer ephemeral tokens** — issue a customer JWT keyed by
   phone after some out-of-band verification (an SMS/WhatsApp OTP).
   More secure, more moving parts. Only worth it if abuse becomes a
   problem.

Default to (1) for v1. Re-evaluate when WhatsApp lands.

## Tool annotation style

FastMCP reads docstrings and Pydantic types to populate the tool
schema. Keep tool docstrings short, action-oriented, and written *for
the LLM* — i.e. explain when to call the tool and what each argument
means in plain language, not just the type.

```python
@mcp.tool()
def book_appointment(
    service_id: str,
    customer_phone: str,
    start_time: datetime,
) -> Appointment:
    """Book a slot for the customer.

    Call after the customer has confirmed a specific time from
    `check_availability`. The phone is required — it's how the customer
    will be identified for any later cancel/list calls.
    """
```
