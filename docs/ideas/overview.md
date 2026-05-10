# Overview

## Vision

People hate filling out booking forms. They love asking a question.
Citana turns appointment booking into a conversation: an
end customer says "can I get a haircut Saturday morning?" in chat, and
the LLM — using tools exposed by our MCP server, backed by our FastAPI
booking system — proposes slots, books one, and confirms. The business
owner manages the catalog through a normal REST API.

The first delivery surface is any open-source MCP-aware client (so the
operator can dogfood the bookings inside opencode or LibreChat). The
medium-term target is **WhatsApp**, where the customer already lives.

## Why this shape

Three deliberately separate components:

- **Backend (FastAPI)** owns the data. Stable, testable, doesn't care
  who calls it.
- **MCP server (FastMCP)** is the *narrow* contract for an LLM. It
  exposes only what a customer should be able to do, with strict
  argument validation and ownership checks. Admin operations stay
  REST-only.
- **Chat client** is whatever the operator wants — and crucially, can
  change. Today it's a CLI; tomorrow it's WhatsApp.

The backend ↔ MCP split is the most important one. It means the LLM
never sees admin endpoints, can't be tricked into deleting things, and
the API surface evolves independently of the tool surface.

## Primary user

A small-business owner — initially a single deployment per business
(salon, dental clinic, restaurant, …). The repo is generic until a real
business shape forces specialization.

## End customer

The person actually booking. Identified by phone number, no account,
no password. Phone number is also the bridge to WhatsApp later.

## Self-hosting + OSS

This is built to be self-hosted on a VPS. Every dependency is
permissively licensed (MIT / Apache / BSD). No proprietary SaaS in the
critical path.
