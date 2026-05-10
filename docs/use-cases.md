# Use Case Specification

This document describes the use cases for Citana — the
specific goals each actor can accomplish through the system. Use cases
complement the [Software Requirements Specification](requirements.md):
they describe the *how*, not just the *what*.

Each use case references the functional requirements it satisfies
(FR-###). Many use cases are forward-looking — see the
[roadmap](roadmap.md) for which phase implements them.

---

## Actors

| Actor | Description |
|---|---|
| **Admin** | The business owner. Manages services, resources, schedules. |
| **Customer** | The end user. Books appointments via chat. Identified by phone number. |
| **Chat Client** | An MCP-aware client (LibreChat / opencode / WhatsApp gateway) acting on behalf of a customer. |
| **System** | Automated behavior triggered by user actions or schedules. |

---

## Use Case Index

| ID | Name | Actor | Phase |
|---|---|---|---|
| [UC-01](#uc-01-admin-log-in) | Admin Log In | Admin | 1 |
| [UC-02](#uc-02-admin-list-appointments) | Admin List Appointments | Admin | 1 |
| [UC-03](#uc-03-admin-create-appointment) | Admin Create Appointment | Admin | 1 |
| [UC-04](#uc-04-admin-cancel-appointment) | Admin Cancel Appointment | Admin | 1 |
| [UC-05](#uc-05-admin-create-service) | Admin Create Service | Admin | 2 |
| [UC-06](#uc-06-admin-create-resource) | Admin Create Resource | Admin | 2 |
| [UC-07](#uc-07-admin-set-working-hours) | Admin Set Working Hours | Admin | 2 |
| [UC-08](#uc-08-customer-list-services) | Customer List Services | Chat Client | 3 |
| [UC-09](#uc-09-customer-check-availability) | Customer Check Availability | Chat Client | 3 |
| [UC-10](#uc-10-customer-book-appointment) | Customer Book Appointment | Chat Client | 3 |
| [UC-11](#uc-11-customer-list-own-appointments) | Customer List Own Appointments | Chat Client | 3 |
| [UC-12](#uc-12-customer-cancel-own-appointment) | Customer Cancel Own Appointment | Chat Client | 3 |

---

## Phase 1 — Admin Auth + Appointment Stub

### UC-01: Admin Log In

**Actor:** Admin

**Related Requirements:** FR-001, FR-002

**Preconditions:** Default admin exists (created at first deploy).

**Main Flow:**

1. Admin POSTs `username` and `password` to `/api/v1/auth/login`.
2. System verifies credentials.
3. System issues a JWT access token.
4. Admin uses the token in the `Authorization: Bearer <token>` header.

**Alternative Flows:**

- **A1 — Bad credentials:** 401 returned.

---

### UC-02: Admin List Appointments

**Actor:** Admin

**Related Requirements:** FR-040

**Preconditions:** Admin holds a valid JWT.

**Main Flow:**

1. Admin GETs `/api/v1/appointments/`.
2. System returns all appointments ordered by start time.

---

### UC-03: Admin Create Appointment

**Actor:** Admin

**Related Requirements:** FR-040, FR-041

**Preconditions:** Admin holds a valid JWT.

**Main Flow:**

1. Admin POSTs an appointment (customer name, phone, start time,
   duration).
2. System creates the appointment with status `pending`.
3. System returns the created appointment.

**Alternative Flows:**

- **A1 — Past start time:** System returns 422.

In Phase 1 the appointment domain is a stub: no resource conflict
detection, no service catalog. Those land in Phase 2.

---

### UC-04: Admin Cancel Appointment

**Actor:** Admin

**Related Requirements:** FR-040

**Main Flow:**

1. Admin DELETEs `/api/v1/appointments/{id}`.
2. System sets status to `cancelled` (soft cancel).

---

## Phase 2 — Catalog & Resources

### UC-05: Admin Create Service

**Actor:** Admin

**Related Requirements:** FR-010

**Main Flow:**

1. Admin POSTs `/api/v1/services/` with name, description, duration,
   price.
2. System creates the service.

---

### UC-06: Admin Create Resource

**Actor:** Admin

**Related Requirements:** FR-020

**Main Flow:**

1. Admin POSTs `/api/v1/resources/` with name and type.
2. System creates the resource.

---

### UC-07: Admin Set Working Hours

**Actor:** Admin

**Related Requirements:** FR-021

**Main Flow:**

1. Admin POSTs `/api/v1/resources/{id}/working-hours/` with day-of-week
   and time range entries.
2. System replaces the existing schedule for that resource.

---

## Phase 3 — Customer-Facing MCP Tools

### UC-08: Customer List Services

**Actor:** Chat Client (on behalf of Customer)

**Related Requirements:** FR-050

**Main Flow:**

1. Chat client invokes the `list_services` MCP tool.
2. MCP server queries the backend for active services.
3. Chat client receives the list and presents it to the customer.

---

### UC-09: Customer Check Availability

**Actor:** Chat Client

**Related Requirements:** FR-051

**Main Flow:**

1. Chat client invokes `check_availability(service_id, date_range)`.
2. MCP server fetches working hours, existing appointments, blackouts,
   computes free slots, and returns them.

---

### UC-10: Customer Book Appointment

**Actor:** Chat Client

**Related Requirements:** FR-052, FR-042, FR-043

**Main Flow:**

1. Chat client invokes `book_appointment(service_id, customer_phone,
   start_time, customer_name?)`.
2. MCP server checks for resource conflicts and working-hour violations.
3. MCP server creates the customer record if it doesn't exist (keyed by
   phone number).
4. MCP server creates the appointment with status `pending`.
5. MCP server returns confirmation including a human-readable
   appointment id.

**Alternative Flows:**

- **A1 — Conflict:** MCP server returns an `appointment_conflict`
  error so the LLM can ask for another time.

---

### UC-11: Customer List Own Appointments

**Actor:** Chat Client

**Related Requirements:** FR-054

**Main Flow:**

1. Chat client invokes `list_my_appointments(customer_phone)`.
2. MCP server returns the customer's upcoming appointments — never
   another customer's data.

---

### UC-12: Customer Cancel Own Appointment

**Actor:** Chat Client

**Related Requirements:** FR-053

**Main Flow:**

1. Chat client invokes `cancel_appointment(appointment_id,
   customer_phone)`.
2. MCP server verifies the phone matches the appointment's customer.
3. MCP server sets the status to `cancelled`.

**Alternative Flows:**

- **A1 — Phone does not match:** MCP server returns
  `unauthorized_for_appointment`.
