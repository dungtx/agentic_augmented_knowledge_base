---
status: permanent
source: "Distilled directly from a live code-reading session of the docuware-tools repo (BJP26110-RIC) — not from a vault seed; no capture/seed provenance chain exists for this note."
tags: [mcp, agent-design, ai]
keywords: [mcp-server, tool-schema, transport, admin-surface, guardrails]
summary: "MCP is JSON-RPC 2.0 plus three conventions (tools/resources/prompts): a client calls tools/list to auto-discover a server's tools and their Zod/JSON-Schema input shape, then tools/call to invoke one — the SDK enforces that schema per-call, but authentication, rate limiting, SSRF protection, and secrets-at-rest are never provided by the protocol and must be hand-built. The docuware-tools repo is a working case study of splitting a deployment into two surfaces: a broadly-reachable, stateless, read-mostly HTTP MCP server for the LLM client, and a separate human-facing admin CRUD app (Entra ID login) that owns credential storage and connection config, plus a narrower local stdio MCP server carrying the write/destructive tools that only runs with operator-held credentials."
parents: ["[[../MOC|Long-term Storage]]"]
siblings: ["[[mcp-server-design-critique|MCP Server Design Critique]]"]
---

# MCP Server Design Fundamentals

Written from a real two-server MCP deployment (docuware-tools: a DocuWare workflow-analytics
integration) as the case study, but the lessons generalize to any "let an LLM call into a backend
system" build. Assumes near-zero prior MCP knowledge. Companion to
[[mcp-server-design-critique|MCP Server Design Critique]], which argues where the advice below is
unproven, deployment-specific rather than protocol-general, or (in one case) papers over an actual
authorization bug found in the source.

## What MCP actually is

MCP (Model Context Protocol) is a thin, standardized contract on top of **JSON-RPC 2.0** so that any
MCP-aware client (Claude Code, Claude Desktop, etc.) can talk to any MCP server without custom
integration code per server. Three primitives exist in the spec:

- **Tools** — model-invoked actions with a name, a human-readable description, and a typed input
  schema. This is what almost everyone means when they say "MCP server" — docuware-tools uses only this.
- **Resources** — contextual data the client can read (files, URIs) without the model "calling" anything.
- **Prompts** — reusable, parameterized prompt templates the server exposes.

The **whole interface a client sees is generated for you** by the SDK (`@modelcontextprotocol/sdk`):
register a tool with `server.tool(name, description, zodSchema, handler)` and the server automatically
answers `tools/list` (schema + description for every registered tool) and `tools/call` (validates
input against the Zod schema before your handler ever runs, rejects malformed calls with a protocol-level
error). You never hand-write the discovery or validation plumbing — you only write `description` strings
and Zod shapes, and those two things *are* the entire contract the model reasons against.

## Transport choice is a real architectural decision, not a config flag

- **stdio** — the client spawns your server as a local child process and talks over stdin/stdout.
  One process per client session, full trust, no network exposure, holds in-memory state naturally
  (an authenticated API client, a token cache) for the life of the process. Cheapest to build, but only
  reachable by whoever can run the binary locally with the right env vars/credentials.
- **Streamable HTTP** — your server is a normal network endpoint (`POST /mcp`, JSON-RPC body). Multiple
  clients, multiple concurrent sessions, and **the MCP spec itself defines no authentication** — you own
  that entirely (docuware-tools bolts on an `x-api-key` header checked against a database).

Constraint that bites people: if the HTTP transport is deployed to something serverless/scale-out
(Azure Functions, Lambda, Cloudflare Workers), **you cannot rely on in-process state surviving between
calls or being shared across instances.** docuware-tools' HTTP handler
(`dashboard/api/src/functions/mcp.ts`) constructs a brand-new `McpServer` + `InMemoryTransport` pair
*per HTTP request* — nothing persists. Its per-API-key rate limiter is a plain in-memory `Map`, which
means the 30 req/min budget is actually "30 req/min per warm function instance," silently multiplied
under scale-out and reset on cold start. If you need a durable limit under a serverless HTTP transport,
it has to live in shared storage (Redis, the same DB backing your auth), not a module-level `Map`.

## Tool design principles

- **The description string is the interface.** The model chooses which tool to call and how to fill its
  arguments based on nothing but the name, description, and field-level `.describe()` text you write.
  Vague or overlapping descriptions across tools (two tools that both sound like "get workflow data")
  cause wrong-tool selection more often than any code bug will.
- **Keep each tool to one clear action.** docuware-tools has ~13-20 narrow tools
  (`get_workflow_errors`, `get_task_decisions`, `list_file_cabinets`...) rather than one parameterized
  "query anything" tool — narrow tools are individually easy for the model to pick correctly; one
  do-everything tool pushes all the disambiguation work into argument-filling, where models are weaker.
- **Errors are tool output, not exceptions.** Every handler in docuware-tools catches its own errors and
  returns `{ content: [{ type: "text", text: "Error: ..." }] }` instead of throwing. This matters because
  a normal tool-result error lands back in the conversation where the model can read it and react (retry
  with different args, tell the user, try another tool); an unhandled throw/HTTP 500 just kills the
  turn. Reserve real protocol/HTTP-level errors (401, 429, malformed JSON) for failures that happen
  *before* a tool handler runs at all — auth and rate-limit checks, not business logic.
- **Multi-tenancy via an optional selector param, resolved server-side.** Tools take an optional
  `connection_id`; the server looks up encrypted credentials for that ID from its own database
  (`dashboard/api/src/lib/connection.ts: resolveClient`) rather than ever accepting raw credentials as a
  tool argument. The client picks *which* backend account by ID; it never handles the secret.

## Guardrails the protocol will never give you — build them yourself

MCP defines the calling convention, nothing about safety. Everything below was hand-rolled in
docuware-tools and has to be hand-rolled in any HTTP-facing MCP server:

- **AuthN for the tool-calling client** — API key header (`x-api-key`/`Bearer`) validated per request
  against a datastore, independent of any human login flow.
- **AuthN/Z for the humans who administer the server** — see the split-surface pattern below; this is
  deliberately a *different* mechanism (Entra ID / OAuth) from the tool-caller's API key.
- **Rate limiting** — per-API-key sliding window; must live in shared state if the transport scales out.
- **SSRF prevention**, if any tool or config lets a human point the server at an arbitrary URL: enforce
  HTTPS-only and reject hostnames resolving to RFC1918/loopback/link-local ranges
  (`10.`, `172.16-31.`, `192.168.`, `127.`, `169.254.`, `localhost`) at the point the URL is *saved*, not
  just at call time.
- **Secrets at rest** — encrypt (AES-256-GCM in this case), never store backend passwords/tokens in
  plaintext in whatever DB backs your connection config.

## Pattern: separate the MCP (LLM-facing) surface from the admin (human-facing) surface

This is the "small companion server for administration" piece. The instinct to avoid: exposing
account/credential/access-key management *as MCP tools* the model can call. If "create an API key" or
"add a new backend connection" is a tool, then any conversation that reaches that tool — including a
successful prompt-injection from untrusted content the model reads elsewhere — can mint new access or
repoint the server at an attacker-controlled backend. Humans configuring *what the MCP server has access
to* is a different trust boundary than an LLM *using* that access, and it deserves a different auth
mechanism and a different interface.

docuware-tools' concrete split:

- **Admin surface** — an ordinary authenticated web app (`dashboard/public/*.html` +
  `dashboard/api/src/functions/{connections,apikeys,users,auth}.ts`). Humans log in with Entra ID,
  register DocuWare connections (URL/username/password), mint or revoke API keys, manage who has
  Owner/Member access. Plain CRUD, plain session/OAuth auth, no LLM in the loop.
- **MCP surface** — `dashboard/api/src/functions/mcp.ts`. Authenticated only by API key (minted by the
  admin surface, not self-service). Its tools only ever *read* what the admin surface wrote
  (`resolveClient`, `listConnections` in `connection.ts`) — there is no `create_connection` or
  `create_api_key` tool anywhere in the HTTP-deployed server.
- **The write/destructive tools live somewhere narrower entirely.** docuware-tools actually ships a
  *second*, separate MCP server (stdio, `src/index.ts`) that does carry `create_user` / `update_user` /
  `delete_user` (irreversible) — but that binary only runs locally, spawned by whoever holds
  Owner-level DocuWare credentials in their own `.env`. It was never wired into the broadly-reachable
  HTTP deployment. The general rule this generalizes to: **if a tool is destructive or privilege-granting,
  ask whether it needs to be reachable by every client of the public MCP endpoint at all — often the
  right answer is to keep it on a narrower, operator-only surface instead of gating it with in-tool
  confirmation logic.**

## First-build checklist

1. Pick stdio if the only caller is you, locally, with your own credentials in env vars. Pick HTTP only
   once you actually need multiple/remote clients — it drags in auth, rate limiting, and statelessness
   constraints stdio never has.
2. Write tool descriptions like you're teaching a new hire what each does and when to reach for it —
   this text is doing more work than any code in the handler.
3. One tool, one job. Split before you're tempted to add a fourth optional param that changes what a
   tool fundamentally does.
4. Catch errors inside every handler and return them as text content; don't let exceptions escape to the
   transport layer.
5. If humans need to configure credentials/access, build that as a normal authenticated CRUD app —
   never as a tool the model can call.
6. Before deploying a write/destructive tool over a network transport, ask whether it should instead live
   on a narrower, operator-only surface (local stdio, admin-only route) rather than the general-purpose
   endpoint.
7. Rate limiting, SSRF checks, and secrets encryption are 100% your responsibility — none of them come
   from `@modelcontextprotocol/sdk`.
