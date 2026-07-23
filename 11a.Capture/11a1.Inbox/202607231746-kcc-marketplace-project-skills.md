---
status: fleeting
kind: idea
captured_at: 2026-07-23T17:46:00+07:00
tags: []
needs_review: false
---
# KCC marketplace for project skills

Build a marketplace inside KCC (Knowledge Context Center) that lets users install project-specific skills, hooks, commands, and MCPs — versioned via an internal GitLab repo.

## How it works

- Each project gets a `config.json` that declares only the skills/hooks/commands/MCPs it needs (KCC reframe: bootstrap from config, not blanket install).
- Hosted inside internal GitLab.
- One-line install: `npx <repo>` pulls everything onto the user's machine.

## Reference

https://github.com/davila7/claude-code-templates — similar pattern for Claude Code.

## Why

- Inhouse tooling for the team.
- Doubles as personal reps building tooling infrastructure.
