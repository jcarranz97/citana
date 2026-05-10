# Chat Client Options

A survey of open-source MCP-aware chat clients we can use to test the
bot before WhatsApp is ready. All are self-hostable and permissively
licensed.

## Comparison table

| Client | License | MCP support | Best for | Notes |
|---|---|---|---|---|
| **opencode** | MIT | Native | Dev iteration in the terminal | The original choice the project was scoped against. CLI-first. |
| **LibreChat** | MIT | Native | Polished web UI, multi-provider | The strongest pick for a long-term web UI. Docker / Helm available. |
| **LobeChat** | MIT | Native | Slick UI, fast iteration | Lighter than LibreChat; good UX. |
| **AnythingLLM** | MIT | Via agents | RAG-heavy use cases | MCP support added in 2026; good if we'd combine docs with the bot. |
| **Open WebUI** | BSD-3 | Via `mcpo` proxy | Existing Ollama users | Extra moving part: MCP needs the `mcpo` adapter sidecar. |
| **Dive** | MIT | Native | Desktop debugging | Purpose-built MCP host desktop app — good for inspecting tool calls. |
| **mcp-chat** (Flux159) | MIT | Native | Quick CLI test harness | Smallest possible MCP client — great for dev sanity. |

## Recommendation

For each phase:

- **While building the MCP server:** `mcp-chat` or **opencode** locally.
  Fast feedback, no UI to manage.
- **For dogfooding by the operator:** **LibreChat**, deployed alongside
  the backend in docker-compose. Logs every tool call, multi-provider,
  has user accounts.
- **For end customers:** WhatsApp gateway (see
  [WhatsApp Integration](whatsapp-integration.md)). The web chat UIs
  above are not the customer surface long-term — they're the operator's
  testbed.

## Things that don't matter (yet)

- "Best UI" is moot until customers actually use this surface — for
  now the chat UI is just our own tool. Pick the one with the best
  developer experience.
- Multi-model support is a bonus for testing (compare Claude vs Llama
  on the same bookings) but not required.
