---
status: someday
kind: idea
captured_at: 2026-06-26T12:00:00+07:00
triaged_at: 2026-07-17T15:45:00+07:00
tags: []
needs_review: false
---

# Android lockout-gate app — JP daily output practice (MVP)

## Idea
An Android app that **locks the phone to a restricted state** and only restores normal behavior after I've completed my daily Japanese **output** practice. Could be a launcher OR just a gate-app (not necessarily a launcher — open design decision).

Merged from two earlier Inbox fragments (`Japanese writing app idea.md` + `Just start app idea.md`) — these were always two faces of one idea.

## The routine that unlocks (MVP scope = writing only)
- Produce 1 JP sentence per day in **2 categories**:
  1. **Something I want to say** — never repeat a sentence (the no-repeat constraint is the real value; it forces me to keep mining fresh patterns, AJATT/MIA-style).
  2. **Something with ≥1 new word or grammar structure**.
- MVP = **writing output only**. Speaking/ASR is explicitly OUT of MVP.

## Bypass / emergency unlock
- Bypass **allowed** (real emergencies — maps, etc.) but each bypass must be **harder than the last** — escalating friction so I don't get used to skipping practice.

## Future scope (declared, NOT MVP — for later iteration)
- Link to my **preferred reader + Anki** so gate can accept input-practice as qualifying output too.
- Allow **emergency apps** (e.g. podcast player) for immersion learning even when locked.
- Per-app **success-criteria rules** that connect to other apps → generalizes beyond JP routine.

## Build intent
Quick first build, **dogfood myself, iterate**. Keep MVP scope small.

## Why
Hold myself accountable to daily JP **output** specifically — current routine is input-heavy (Anki/podcasts), output is the missing half.

## Open design questions (for distill / build)
- Launcher vs non-launcher gate-app — TBD.
- Writing input method: handwriting or typing — TBD.

## Status
Aspirational — fun idea but current phone usage patterns don't naturally fit this kind of routine app. Keeping as a learning project (building it would teach a lot about app development).
