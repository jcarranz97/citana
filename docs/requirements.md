# Software Requirements Specification

## 1. Introduction

### 1.1 Purpose

This document specifies the functional and non-functional requirements
for Citana, a self-hostable booking assistant for
small/medium businesses. End customers book appointments through a
conversational interface (an MCP-enabled chat client today; WhatsApp
later) instead of filling out forms.

### 1.2 Scope

The system will provide:

- A REST API for appointment, service, resource, and customer management.
- An MCP server exposing a curated subset of the API as tools, callable
  by any MCP-compatible LLM client.
- Admin authentication for the business owner managing the catalog.
- Identification of end customers by phone number — no account required.

### 1.3 Out of Scope (Initial Releases)

- Payment processing.
- Multi-tenant SaaS (the system is single-tenant per deployment).
- Mobile native apps.

## 2. Overall Description

### 2.1 Product Perspective

Citana is a self-hosted application made of:

- A FastAPI backend with a PostgreSQL database.
- An MCP server (FastMCP) that connects to the backend.
- A chat client of the operator's choice (LibreChat, opencode, …) and,
  later, a WhatsApp gateway.

### 2.2 User Classes

- **Admin** — the business owner. Manages services, resources, working
  hours; views all appointments.
- **Customer** — the end user. Books / cancels their own appointments
  via the chatbot. Identified by phone number.
- **System** — automated behavior triggered by user actions (conflict
  checks, reminders).

## 3. Functional Requirements

### 3.1 Admin Authentication

- **FR-001**: An admin must be able to log in with username + password.
- **FR-002**: All admin endpoints must require a valid JWT bearer token.
- **FR-003**: A default admin user is created on first deploy from
  environment variables.

### 3.2 Service Catalog (Phase 2)

- **FR-010**: Admin must be able to create services with: name,
  description, duration (minutes), price, active status.
- **FR-011**: Admin must be able to update or deactivate services.
- **FR-012**: A service may optionally require a specific resource type.

### 3.3 Resources (Phase 2)

- **FR-020**: Admin must be able to register resources (staff member,
  room, table) with: name, type, active status.
- **FR-021**: Admin must be able to set working hours per resource.
- **FR-022**: Admin must be able to add blackouts (vacation, sick day).

### 3.4 Customers (Phase 2)

- **FR-030**: Customers are identified by phone number; no password.
- **FR-031**: Optional name and notes per customer.
- **FR-032**: Looking up a customer by phone returns their full
  appointment history.

### 3.5 Appointments

- **FR-040**: Admin must be able to list, view, create, modify, and
  cancel appointments.
- **FR-041**: Each appointment has: customer, service, resource (if
  applicable), start time, duration, status (pending / confirmed /
  cancelled / completed), notes.
- **FR-042**: The system must reject overlapping appointments for the
  same resource.
- **FR-043**: The system must reject appointments outside the resource's
  working hours.

### 3.6 MCP Tools (Phase 3)

The MCP server exposes a subset of the above as tools:

- **FR-050**: `list_services` — public, returns active services.
- **FR-051**: `check_availability(service_id, date_range)` — returns
  available slots.
- **FR-052**: `book_appointment(service_id, customer_phone, start_time,
  customer_name?)` — creates the appointment, creates the customer
  record if it doesn't exist.
- **FR-053**: `cancel_appointment(appointment_id, customer_phone)` —
  customer-scoped: phone must match.
- **FR-054**: `list_my_appointments(customer_phone)` — returns the
  caller's upcoming appointments.

Admin-only operations (creating services, modifying working hours,
deleting customers) are intentionally **not** exposed through MCP.

## 4. Non-Functional Requirements

### 4.1 Performance

- **NFR-001**: Availability checks must return within 500 ms for typical
  loads (single-business, dozens of resources).
- **NFR-002**: Booking creation must return within 1 s including
  conflict checks.

### 4.2 Security

- **NFR-010**: All admin endpoints must require JWT.
- **NFR-011**: Passwords must be hashed with Argon2ID.
- **NFR-012**: Customer phone numbers are PII — must not appear in logs
  beyond the last 4 digits.
- **NFR-013**: MCP customer-scoped tools must verify the caller's phone
  matches the appointment's customer.

### 4.3 Reliability

- **NFR-020**: The system must recover gracefully from a database
  restart (connection pool with `pool_pre_ping`).
- **NFR-021**: Soft-delete only — no hard deletes (set
  `active = False`).

### 4.4 Operability

- **NFR-030**: Must run from a single `docker compose up`.
- **NFR-031**: Must be deployable on a single VPS (no managed services
  required for the MVP).
- **NFR-032**: Logs must be JSON-structured for easy ingestion.

## 5. Technical Constraints

- Backend: FastAPI on Python 3.13+, PostgreSQL 15+.
- MCP: FastMCP (Python). Must be packaged as a separate process so it
  can run on a different host if needed.
- All open source, MIT/Apache/BSD compatible.
