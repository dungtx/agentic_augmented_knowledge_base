# MCP Server Design Critique — Where the Fundamentals Note Overclaims

Counter-argument pass on [[mcp-server-design-fundamentals|MCP Server Design Fundamentals]] — same
docuware-tools case study, but arguing where its advice is unproven, deployment-specific rather than
protocol-general, or (in one case) papering over an actual authorization bug in the source code. Each
section below tracks one section of the companion note; each ends with **Options to consider** for
someone designing a *different* MCP server who shouldn't just copy the original note's conclusions
uncritically.

## Critique 1 — "Tools only" was presented as normal, not as a choice

The fundamentals note mentions Resources and Prompts exist, then moves on because docuware-tools only
uses Tools. That's descriptively true but prescriptively lazy: modeling *everything* as a Tool means
every read — even purely contextual ones like "list of file cabinets" — has to be explicitly invoked by
the model, costs a full round-trip, and adds another schema to the context budget every other tool
already competes in. Resources exist precisely for data a client can attach ambiently without the model
spending a turn deciding to call something.

**Options to consider:**
- Model passive/reference data (lookup lists, schemas, cabinet directories) as **Resources**, and reserve
  **Tools** for parameterized actions that actually need arguments and produce a result the model reasons
  over.
- Consider **Prompts** for canned, frequently-repeated report shapes (e.g., "monthly completion report")
  instead of relying on the model to re-derive the same tool-call sequence every time.
- Check your actual target client's support level first — Resources/Prompts rendering is less uniform
  across MCP clients than Tools; don't design around a primitive your primary client half-supports.

## Critique 2 — "stdio vs HTTP" conflates protocol constraints with deployment-target constraints

The fundamentals note's "stateless per request, no shared in-memory state" constraint is real for
docuware-tools specifically because it's deployed on Azure Functions (serverless, scale-out). That is
**not** an MCP protocol constraint — a long-running HTTP MCP server (a plain Node/Python process behind a
load balancer with sticky sessions, or a single VM) can hold an authenticated client and a real rate
limiter in memory exactly like stdio does. The note also undersells that full Streamable HTTP supports
session IDs and server-initiated SSE notifications — docuware-tools deliberately opts out of that (`GET`
returns 405) rather than that being a documented protocol ceiling.

**Options to consider:**
- Decide your hosting model *before* concluding you need to design stateless: a long-running container
  gets to keep stdio's in-memory simplicity while still being network-reachable.
- If you do need serverless scale-out, treat shared state (rate limits, auth token caches) as a distinct
  design problem — solve it with Redis/DB, don't let it silently shape your whole handler into "rebuild
  everything per request."
- If your tools involve long operations (bulk export, multi-step workflow), evaluate whether you actually
  need session-based Streamable HTTP (progress notifications, resumability) before defaulting to the
  simpler stateless request/response model docuware-tools used.

## Critique 3 — "One tool, one job" is asserted, not measured, and has a live counter-example

The claim that narrow tools beat one parameterized tool is a real, contested tradeoff, not a settled
rule. Every extra registered tool adds a full schema + description to what the model has to hold and
discriminate between on *every* turn, not just the turns that use it. Tool-selection accuracy is known to
degrade as tool count grows. Notably: the very harness this note was written in solves this by *not*
loading full schemas for its long tail of tools up front — deferred tools are discovered on demand via a
search call, precisely because "just register more narrow tools" doesn't scale past some threshold.

**Options to consider:**
- If you're past ~15-20 tools for one integration, consider consolidating related read-only reports into
  fewer tools with a `report_type` enum/discriminated-union argument, trading some selection precision
  for a smaller standing context footprint.
- If your MCP SDK/host supports it, group tools into namespaces or toolsets the host can enable/disable
  per session, rather than always exposing the full set to every conversation.
- Consider a deferred/search-based discovery pattern (expose a small stable core set directly, put the
  long tail behind a "find the right tool" lookup) instead of assuming every tool must be in `tools/list`
  up front.
- Don't take "narrow is better" on faith — if you can, measure your own model's tool-pick accuracy at
  your actual tool count before committing to a granularity policy.

## Critique 4 — "Errors are tool output, not exceptions" trades away observability and can leak internals

Catching every error and returning it as friendly text content is good for conversational recovery, but
docuware-tools' `handleError()` returns `(e as Error).message` more or less verbatim into the model's
context. That message can carry internal detail (backend hostnames, stack fragments, auth-provider error
text) the caller was never meant to see — and because the response is still HTTP 200 with error *content*,
not an HTTP error status, ordinary APM/error-rate dashboards won't flag it as a failure either. The
"friendly for the model" design goal quietly became "invisible to the operator" as a side effect.

**Options to consider:**
- Log the real error server-side (structured, with a correlation ID) even while returning a sanitized,
  friendly message to the model — don't let the conversational-recovery goal be the only place the error
  is recorded.
- Draw a line between *expected/business* errors (safe to echo verbatim — "workflow not found") and
  *unexpected/system* errors (return a generic message + correlation ID, log the real detail internally).
- Put the correlation ID in both the log line and the text returned to the model, so a user report
  ("the tool said X") is traceable back to the exact server-side event.

## Critique 5 — Multi-tenancy via `connection_id` has an actual authorization gap, not just a UX rough edge

The fundamentals note frames `connection_id` as "the client picks which backend by ID; it never handles
the secret" and stops there, treating it as solved. Checking the real code: `validateApiKey()` returns a
`keyRecord` that includes `userId`, but **that value is only ever used for rate limiting** — it never
flows into `resolveClient(connection_id)` or `listConnections()`. Concretely, in
`dashboard/api/src/functions/mcp.ts` / `dashboard/api/src/lib/connection.ts`:
`listConnections()` runs an unfiltered `SELECT c.id, c.name, c.baseUrl, c.username, c.createdBy FROM c`,
and `resolveClient(connection_id)` will happily authenticate against *any* connection ID it's given. Any
valid API key — regardless of which user or tenant it belongs to — can enumerate every configured
connection's base URL and username via `list_connections`, then pull data through any of them via
`resolveClient`. This isn't a hypothetical edge case; it's the literal behavior of the code as written.

**Options to consider:**
- Scope API keys to specific connection(s) at mint time (an API-key ↔ connection mapping table), and
  enforce that scope inside `resolveClient`/`listConnections` — never trust a client-supplied
  `connection_id` alone as an authorization check.
- Alternative: derive the tenant/connection from the authenticated API key itself server-side (1 key → 1
  connection looked up by key, not by client-supplied ID) so there's no ID to guess or enumerate at all.
- If cross-tenant visibility genuinely isn't needed, don't return `baseUrl`/`username` for connections
  outside the caller's scope — filter at the query level, not just the display level.
- Add an audit log (which API key touched which connection, on which call) — the current design has no
  way to answer "who read this data" after the fact.

## Critique 6 — The guardrails section lists mechanisms, not their hardening gaps

The fundamentals note treats "rate limiting / SSRF prevention / secrets encryption exist" as the finish
line. Each one has a concrete gap worth knowing before copying the pattern:

- **Rate limiter** is a plain in-memory `Map`, keyed only by API key — no cost weighting, so a tool that
  fans out N backend calls (e.g., `get_task_execution_times` looping per workflow) costs the same "1
  request" as a cheap `check_connection`.
- **SSRF check** (`validateBaseUrl`) is a one-time regex match against the hostname *string* at save time.
  It doesn't re-resolve DNS at request time (so a hostname that's public at save-time but rebinds to a
  private IP later slips through), and it only covers IPv4 private ranges — no IPv6 loopback/private/link-
  local (`::1`, `fc00::/7`, `fe80::/10`).
- **Secrets encryption** (AES-256-GCM) protects data at rest, but the key itself is a single static
  64-char hex value in app settings — no rotation story, no per-tenant key, no KMS/HSM-backed lifecycle.

**Options to consider:**
- Weight rate-limit cost per tool (cheap lookups = 1 unit, fan-out reports = N units) instead of a flat
  per-request counter, and move the counter to shared storage if you deploy to scale-out infrastructure.
- Re-validate the resolved IP at request time (or pin it after first validation), not just once at save
  time, to close the DNS-rebinding gap; extend the private-range check to IPv6.
- Move the encryption key into a managed KMS (Azure Key Vault, AWS KMS) with rotation support rather than
  a raw env var, especially once more than one tenant's secrets share the same key.

## Critique 7 — The admin/MCP surface split is a good idea partially undermined by Critique 5

The "keep credential/account management out of MCP tools, put it in a normal authenticated CRUD app"
pattern is sound and worth keeping. But the split only delivers its intended security value if the MCP
surface can't be used *as* an admin surface by accident — and per Critique 5, `list_connections` +
`resolveClient` currently let any authenticated MCP caller do exactly that (enumerate and use connections
that were never meant to be theirs). The architectural separation exists in the file layout; it doesn't
yet exist in the authorization logic.

**Options to consider:**
- Treat "does every MCP tool call respect the same tenant boundary the admin app enforces?" as a required
  check before calling the split "done," not just "is credential CRUD in a separate file."
- Add the audit-log/scoping fixes from Critique 5 as the actual enforcement mechanism for this pattern —
  without them, the split is organizational, not a security boundary.
- When reviewing any MCP server that reads from a multi-tenant store, explicitly test: "can a valid
  credential for tenant A read tenant B's data?" — this is the single highest-value adversarial question
  for this architecture shape.

## Where to invest first, if resource-constrained

(1) Fix the connection_id/API-key authorization gap (Critique 5) — it's the only finding here that's an
active vulnerability, not a design tradeoff. (2) Sanitize error messages before they reach the model
(Critique 4) — cheap, high leverage. (3) Re-evaluate tool count/granularity once past ~15-20 tools
(Critique 3). (4) Everything else (Resources/Prompts modeling, transport statefulness, guardrail
hardening depth) is a real tradeoff worth a deliberate choice, not an obvious fix.
