---
name: orchestrate-herdr
disable-model-invocation: true
description: "Orchestrate herdr worker tabs for a spec (PRD). Reads a spec/issue URL, finds its open sub-issues, launches one herdr-managed worker tab per issue running a chosen coding CLI, then monitors the tabs until every issue is completed with test evidence, blocked, or errored. Use when running inside herdr (HERDR_ENV=1) and the user wants to fan a spec out to per-issue workers."
---

# Orchestrate herdr

> **STATUS: STALE / DEPRECATED (2026-07-23).** Retained for reference only. This skill is removed from all workspace gradients, routing docs, and rules — do not invoke it for new work; its content may be outdated. If explicitly invoked, surface this notice and proceed only on the user's confirmation.

The full procedure — inputs, rules, workflow, worker prompt template, monitoring, and completion criteria — is archived unchanged in [`references/archived-procedure.md`](references/archived-procedure.md). After the user confirms, load that file and follow it as the skill body.
