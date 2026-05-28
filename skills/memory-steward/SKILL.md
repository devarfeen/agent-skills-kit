---
name: memory-steward
description: >-
  Maintain repo-root MEMORY.md (≤300 lines), sync CLI private memories into git,
  compact stale bullets, and promote ADR-tagged items to workspace docs/adr when
  PRDs close. Use at session start after reading MEMORY.md (light pass). Use when
  the user asks to remember, sync memory, compact MEMORY, or promote ADR memory.
  Triggers: session start, MEMORY.md, remember this, sync memory, memory steward.
---

# Memory steward

Keeps **`<repo-root>/MEMORY.md`** healthy. Workspace **`CONTEXT.md`** and **`docs/adr/`** stay at `<artifacts-root>`; this skill does not move domain terms into MEMORY.

## Resolve paths

1. **Active repo root** — git root for cwd, or Project Matrix `Path` for the project being edited. Never use the meta-workspace folder (`path: "."`) for `MEMORY.md`.
2. **`<artifacts-root>`** — directory with `*.code-workspace`, else `CONTEXT-MAP` context root, else single repo root. ADRs: `<artifacts-root>/docs/adr/`.

If `MEMORY.md` is missing at active repo root and recall would help, scaffold using [agents-md MEMORY scaffold](../agents-md/SKILL.md#memorymd-scaffold).

## Session start (light pass)

Run automatically at session start after reading repo `MEMORY.md` (mandated in `AGENTS.md`). Keep output short.

1. Count lines in active repo `MEMORY.md` (0 if missing).
2. Scan `## Promotion queue` and `## Decisions (short)` for `ADR-NNNN:` tags.
3. If lines **> ~300** OR promotion queue non-empty OR user’s last message implies memory work → note that full pass is advised; run full pass only if queue is non-empty or lines > 300.
4. Otherwise: one-line status only (e.g. `Memory: api-service/MEMORY.md, 42 lines, queue empty`). No file writes.

Do not block the user’s actual request on a light pass.

## Full pass (user request or `/memory-steward`)

Run when the user asks to remember/sync/compact/promote, on explicit `/memory-steward`, or when light pass triggers compaction/promotion.

1. Read active repo `MEMORY.md`, `<artifacts-root>/CONTEXT.md` (if present), relevant `docs/adr/`, and open PRD issues (`gh issue view` when PRD numbers are known).
2. **Terminology:** If MEMORY conflicts with `CONTEXT.md`, `CONTEXT.md` wins — fix MEMORY wording, do not edit CONTEXT without user approval.
3. **Promote:** For each `ADR-NNNN:` bullet tied to a **closed** PRD (or accepted ADR):
   - Ensure `<artifacts-root>/docs/adr/NNNN-*.md` contains the decision.
   - Remove promoted detail from MEMORY; leave `- See ADR-NNNN for <topic>.` index lines.
4. **Compact:** If **> ~300 lines**, dedupe, drop stale WIP, move long prose into ADR (not MEMORY). Target ≤ ~300 lines, index-only. Do not copy UA graph prose into MEMORY — index pointers only (e.g. `See ADR-NNNN` or `See .understand-anything graph for <area>`).
5. **Sync private stores (best effort):**
   - Claude: `~/.claude/projects/<project>/memory/MEMORY.md` — merge new durable facts into repo MEMORY; trim duplicate private bullets.
   - Codex: note `~/.codex/memories/` is personal; team facts belong in repo MEMORY / ADRs only.
   - Copilot: do not duplicate GitHub repo memory into MEMORY without user approval; prefer repo MEMORY for team facts.
6. **Write** repo `MEMORY.md` only when changed. Never store secrets.

## MEMORY.md sections (expected)

- `## Stable preferences`
- `## Decisions (short)` — use `ADR-NNNN:` prefix when tied to an ADR
- `## Promotion queue` — bullets awaiting ADR write or PRD close
- `## Gotchas`
- `## Where things are`
- `## Active ADR pointers` — index links after promotion

## Output

**Light pass:**

```markdown
Memory steward (light): <repo>/MEMORY.md — <n> lines; promotion queue <empty|N items>.
```

**Full pass:**

```markdown
Memory steward (full):
- Repo: <path>/MEMORY.md (<before> → <after> lines)
- Promoted: ADR-0042 → docs/adr/0042-*.md
- Synced: <Claude private|none>
- Skipped: <reason>
```

End with `Suggested next skills (optional)` when non-trivial (e.g. `/grill-with-docs` if terminology drifted, `/release-notes` after shipped PRD). After ADR promotion, suggest `/understand` on matrix `Path` roots touched by that ADR when UA is installed (advisory only). After ADR promotion, suggest `/understand` on matrix `Path` roots touched by that ADR when UA is installed (advisory only).

## Do not

- Auto-invoke `caveman` or other optional skills.
- Store secrets, tokens, or credentials in MEMORY.
- Put full glossaries in MEMORY (use `CONTEXT.md`).
- Scaffold MEMORY at `<artifacts-root>` / meta-workspace.
