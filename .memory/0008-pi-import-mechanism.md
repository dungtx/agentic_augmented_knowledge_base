# 0008 — pi `@`-import / AGENTS.md include mechanism (T9 resolved, 2026-07-01)

> **Task:** T9 from `.memory/0003-…-pickup-tasks.md`. Verify whether pi supports an `@path/to/file.md` import in `AGENTS.md` so always-on context can pull `.ai/*` files instead of inlining them. Unblocks T1 (full AGENTS.md) and T7 (`.ai/` design).
> **Method:** read pi 0.79.1 docs (`docs/usage.md`, `docs/quickstart.md`, `docs/extensions.md`, `docs/sdk.md`, `docs/settings.md`, `README.md`).

## Finding

**There is no `@import` / `@include` directive inside `AGENTS.md`.** The "pi `@`-import mechanism" referenced in `.memory/0001`/`0003` does not exist as such. `@file` is a **CLI / editor prompt-time attachment**, not an always-on context include:

```
pi @README.md "Summarize this"     # attaches README.md to THIS prompt only
```

It does not pull the file into the system prompt for every turn.

## Always-on context mechanisms pi actually offers

| Mechanism | Scope | Useful for this vault? |
|-----------|-------|------------------------|
| `AGENTS.md` / `CLAUDE.md` discovery (global `~/.pi/agent/AGENTS.md` + parent-dir walk + cwd; **all concatenated**) | Always-on, system prompt | **Yes — primary.** But limited to those filenames in those locations; no arbitrary `.ai/*.md`. |
| `SYSTEM.md` (replace default) / `APPEND_SYSTEM.md` (append) | Always-on, system prompt | No — we want `AGENTS.md`'s structure, not a prompt replacement. |
| Model-invoked skill `description` | Always-on (description only; body on invocation) | Already used for the 5 skills. |
| `@file` CLI / in-editor | One prompt, not always-on | **No** for always-on; useful for one-shot research. |
| Extension `before_agent_start` — inject message or rewrite `systemPrompt` (`docs/extensions.md`) | Always-on, programmatic | **Can** read `.ai/*` and inject — but requires a TypeScript extension to write and maintain. |
| SDK `DefaultResourceLoader.agentsFilesOverride` (`docs/sdk.md` §Context Files) | Always-on, programmatic (SDK only) | No — we run the TUI, not a custom SDK runtime. |
| `settings.json` | No knob for extra context-file paths | No. |

## Decision for this vault

**Do not build an extension for context inclusion.** Use `AGENTS.md` as the thin always-on brain with **context pointers** to `.ai/*`, and rely on the agent's `read` tool for on-demand loading. This matches the `mp-writing-great-skills` progressive-disclosure / context-pointer pattern the project already follows, and costs zero runtime.

- **Always-on bits** (vault conventions, skill dispatch map) → **inline tight summaries directly into `AGENTS.md`**. No import.
- **On-demand bits** (`zettelkasten-cheatsheet.md`, `retrieval-index.md`, etc.) → live in `.ai/`, reached by a one-line pointer in `AGENTS.md` ("read `.ai/zettelkasten-cheatsheet.md` when running distill-permanent"). The agent `read`s the file when the pointer fires.

## Consequences for downstream tasks

- **T1 (full AGENTS.md):** inline the always-on bits (vault vision, dispatch rules for all skills, `.memory/` + `.ai/` policy blocks as short pointers). Do **not** attempt `@import`. Keep it tight — it pays context load every turn.
- **T7 (`.ai/`):** `.ai/` holds only **on-demand reference**, not always-on context. `vault-conventions.md` and `skill-dispatch-map.md` (previously candidate for `@`-import) instead get **inlined into `AGENTS.md`**; the `.ai/` files become the longer-form on-demand siblings (cheatsheet, retrieval index, lessons). Re-scope T7 accordingly.
- **No code/extension work required** to land T1/T7. Pure markdown.
- **If always-on injection of `.ai/` ever becomes necessary** (e.g. a lesson that must be enforced every turn), the extension route is `before_agent_start` reading the file and returning `{ message: { content: … } }` or `{ systemPrompt: event.systemPrompt + … }`. Documented here so a future agent doesn't re-research.

## Bad-practice warnings

- **W16 (new):** mistaking `@file` for an always-on import. It attaches to one prompt only. Verified against `docs/usage.md` §File Arguments and `docs/quickstart.md` §Reference files.
- Don't build an extension just to inline text — that's runtime cost for a markdown problem. Inline or point, per the ladder in `writing-great-skills`.

---

*T9 resolved. Next: T1 (full AGENTS.md), now unblocked. Re-scoped T7 to on-demand-only `.ai/`.*
