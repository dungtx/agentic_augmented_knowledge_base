# Monorepo Structure & DevEx — Lessons

The non-AI counterpart to the three notes in [[11l05.AI/|AI]] (all distilled from the same case study:
kcc-platform, a TypeScript monorepo). These are general software-engineering / project-structure /
developer-experience lessons that have nothing to do with prompting a model.

## One repo, four kinds of things — and the boundary is deployability, not topic

Layout: `apps/{web,api,worker}` (deployable units) · `packages/{ui,shared-types,db,config,ai}` (shared
libraries, nothing runs standalone) · `infra/` (deployment config) · `docs/` (reference material). The
split isn't by feature/topic, it's by **what kind of thing each directory produces** — something you
run, something you import, something you deploy with, something you read. **Lesson:** when structuring a
monorepo, group top-level directories by deployability/role first; feature-based grouping happens one
level down, inside `apps/*`.

## Tailor each package's build target to its actual consumer — don't apply one policy to all

Most workspace packages (`config`, `shared-types`, `ai`, `db`) build to `dist/` as CommonJS with Node16
resolution, because the NestJS runtime needs to `require()` them. The `ui` package instead ships raw TS
source, consumed via Next.js's `transpilePackages` — because its only consumer is a bundler that already
transpiles TS, so a build step would be pure overhead. **Lesson:** in a monorepo, "how does this package
get consumed" should decide its build strategy per-package, not a blanket "everything builds the same
way" rule. Check who actually imports it before deciding how it ships.

## Enforce layering boundaries at every layer the architecture has — code AND data

Two boundaries enforced structurally, not just by convention: (1) in code, CI blocks `modules/* →
core/*|common/*` violations and `core/* ↛ modules/*` (modules can depend on core, never the reverse); (2)
in the database, tables are namespaced into separate Postgres schemas per business module (confirmed:
the `Document` model is `@@schema("acp")`; the platform ships "8 schemas / 41 tables" total). **Lesson:**
if your architecture has a layering rule, enforce it at *every* layer it could be violated — a clean
module boundary in code means little if two modules' tables can still silently join across an
unenforced database boundary. Defense in depth applies to architecture rules, not just security.

## Make traceability a commit-time mechanical check, not a review-time reminder

Every commit must carry a ticket id (`VNX-###`), enforced by `commitlint` — a commit without one simply
fails, it isn't a style-guide suggestion a reviewer has to remember to check for. **Lesson:** whenever a
convention needs to be *always* true across a whole team over years (not just "usually true"), automate
its enforcement at the earliest possible mechanical checkpoint (commit hook > CI > code review > "please
remember" in a wiki page) — each step later in that list is progressively easier to skip.

## Invest in one idempotent, cross-platform bootstrap command

`node scripts/setup.mjs` (or `pnpm setup`) does the *entire* onboarding sequence — toolchain, install,
`.env`, Docker infra, DB migrate + seed, build — in one command, safely re-runnable. **Lesson:** a fresh
machine reaching "fully working" in one idempotent command is worth deliberately engineering as a
first-class deliverable, not an afterthought README checklist. The idempotency matters as much as the
one-command part — a setup script that breaks on re-run trains people to distrust it and fall back to
manual steps, which is where onboarding docs quietly rot.

## Offer two migration paths for two different audiences

`prisma migrate deploy` replays incremental migrations (idempotent — right for an *existing* environment
picking up new changes). Separately, `scripts/db_full_migration.sql` is a single consolidated file with
the entire schema (all 8 schemas / 41 tables) for a *brand-new* database — skipping the replay of
possibly hundreds of historical migration steps. **Lesson:** "upgrade an existing environment" and
"provision a brand-new one" are different jobs with different performance/complexity trade-offs; it's
worth maintaining both a replay-based path and a consolidated-snapshot path rather than forcing every new
environment through the full historical migration sequence.

## Make infra config env-driven, and document the invocation footguns explicitly

Ports are remapped via `.env` (`POSTGRES_PORT`/`REDIS_PORT`) rather than hardcoded in
`docker-compose.yml` — and the docs explicitly flag that `--env-file .env` is *required* on the compose
invocation, because Compose will otherwise silently fall back to defaults instead of erroring. **Lesson:**
env-driven config is necessary but not sufficient — if the tool has a way to silently ignore your env
file (wrong flag, wrong working directory), write that gotcha down explicitly next to the command, don't
assume "it's configurable" means "it'll be used correctly."

## Make the top-level instructions file both the onboarding sequence and the living status board

CLAUDE.md does two jobs at once: it prescribes a **read order** for newcomers ("docs/PLAN_P0.md →
PRD/06_Build_Guide → 02/03/04 → build") instead of leaving discovery order to chance, and it carries a
**live status summary** ("Done & verified: ... In progress: ... Deferred: ... Next: ...") right in the
file every contributor (human or agent) already has to read first. **Lesson:** the file people are
already guaranteed to open is the best place to put both "where do I start" and "what's actually true
right now" — a separate project-status tool that isn't in anyone's default reading path goes stale
because updating it takes a deliberate extra trip.

## Wrap error-prone manual edits to structured artifacts in a small enforcing script

The requirement-tracking spreadsheet (`PRD/05_Requirement_Engineering.xlsx`) isn't hand-edited — status
changes go through `python scripts/update_re_status.py set VNX-005 Done`. **Lesson:** whenever a
structured artifact (spreadsheet, YAML config, generated file) has a "correct shape" that's easy to
violate by hand (wrong column, broken formula, invalid enum value), a five-line CLI wrapper that only
allows valid transitions is cheap insurance against silent corruption — cheaper than the cleanup after
someone free-hand-edits it wrong.

## Seed a known-good demo account — and say the production risk out loud

A fixed seeded super-admin (`admin@aix.local` / password from `.env`) makes every fresh environment
(dev, demo, test) immediately usable with no manual "first register an account" ceremony. **Lesson:**
this is a genuine DevEx win — but it's exactly the kind of convenience that becomes a real vulnerability
if it ever ships to production with a default/weak password. If you adopt this pattern, the
"never let this credential exist in a real production environment" rule needs to be as explicit and
visible as the convenience itself, not an assumed unwritten rule.

## Thread one short-code taxonomy through UI, routes, database schemas, and work-item IDs alike

Each business module has a short code (AKP/ACP/APP/ARP/AFP) that shows up *everywhere* consistently: nav
labels and accent colors, URL routes (`/akp`, `/acp`, `/app`...), Postgres schema names, and it's the
same prefix family as the per-item REQ-id codes (`VNX-###`, `US-####`). **Lesson:** this is the "one
identifier threaded through everything" idea (see the AI notes) applied at the *module* level, not just
the work-item level — pick short, stable codes for your major subsystems early, and reuse the exact same
codes everywhere they'd otherwise need a name: navigation, routing, database namespacing, and docs.
