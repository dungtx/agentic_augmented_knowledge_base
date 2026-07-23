---
status: triaged
kind: idea
captured_at: 2026-07-21T00:00:00+07:00
tags: []
needs_review: false
triaged_to: "[[../../11c.Projects/BGB26195-CDI/README.md]]"
triaged_at: 2026-07-23T09:00:00+07:00
---

# CDI (Cedar) — customer meeting, AI/OCR + UX focus

Customer meeting, AI/OCR-focused features.

The customer focused on **the volumes of bills**. He thinks the power of AI is in the **Claude model** — it can read a bill correctly without any problems — so he doesn't understand **why it takes so long to develop a wrapper around that**.

Project timeline is **too long**, when Claude already works out of the box.

He thinks **4 months** is only for building a **basic OCR app** with mapping data that handles **only 1 supplier**. To him this is too small for an **MVP**, without understanding of the actual **hidden complexity** of a system that can read **all types of bills in the future**.

## UX focus

He wants the user to **not feel like a SaaS platform** — just let the user **upload their bills**. Simplify login/auth flows.

He wants to **think about the UX first** — the background data processing is **not the focus of the client right now**.

He still wants **correct data**, but the **quickest answer to the client's customer** is the main focus.

## The AI gap

The problem right now for AI: we can **read a bill but no way to fill missing information**. The customer is focused on the UX, so this information needs to be **added behind the scene somehow**.
