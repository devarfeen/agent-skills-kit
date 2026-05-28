# Memory — global defaults by CLI

Copy-paste snippets for **user-level** config. Merge into existing files; do not overwrite unrelated keys.

**SSOT:** Team-shared recall lives in **`<repo-root>/MEMORY.md`** (git-committed, per Project Matrix row). Built-in CLI memories are personal/supplementary unless synced into repo `MEMORY.md` via `/memory-steward`.

See [`memory-steward`](../../memory-steward/SKILL.md) for compaction, promotion to workspace ADRs, and sync.

---

## Codex CLI

**File:** `~/.codex/config.toml`  
**Docs:** [Memories](https://developers.openai.com/codex/memories), [Config reference](https://developers.openai.com/codex/config-reference)

```toml
[features]
memories = true

[memories]
use_memories = true
generate_memories = true
disable_on_external_context = true
```

- Private store: `~/.codex/memories/` (generated; do not treat as team SSOT).
- Team rules: `AGENTS.md` + repo `MEMORY.md`.
- EEA/UK/CH: native memories may be unavailable; rely on repo `MEMORY.md`.

---

## Claude CLI

**Files:** `~/.claude/settings.json`, optional `~/.claude/CLAUDE.md`  
**Docs:** [Memory](https://code.claude.com/docs/en/memory)

```json
{
  "autoMemoryEnabled": true
}
```

Add to `~/.claude/CLAUDE.md` (global):

```markdown
## Memory SSOT

- Repo-root `MEMORY.md` (git) is the team source of truth for shared recall.
- Claude auto memory at `~/.claude/projects/<project>/memory/MEMORY.md` is supplementary.
- At session end, merge durable facts into the active repo `MEMORY.md`; run `/memory-steward` when they diverge.
```

- `autoMemoryDirectory` is **user/local settings only** (not project `settings.json`).
- Optional advanced: symlink `~/.claude/projects/<hash>/memory/MEMORY.md` → repo `MEMORY.md` (one machine; verify writes land in git).

---

## GitHub Copilot CLI

**Account:** GitHub → profile → **Copilot settings** → **Copilot Memory** → Enabled (Pro/Pro+ default on; org/enterprise may be off).

**File:** `~/.copilot/copilot-instructions.md`

```markdown
## Memory

- Prefer `/memory on` in CLI sessions (`/memory show` to verify).
- Distinguish Copilot Memory (`store_memory` tool, GitHub-stored) from repo `MEMORY.md` (git SSOT).
- Put team-shared repo facts in `<repo-root>/MEMORY.md`; use Copilot Memory for personal prefs only when appropriate.
```

- No `memory` key in `~/.copilot/settings.json`; enablement is account + `/memory` slash commands.

---

## Cursor CLI

**File:** `~/.cursor/cli-config.json` — no built-in memory toggle ([CLI config](https://cursor.com/docs/cli/reference/configuration)).

- **IDE** (optional): Settings → Rules → Generate Memories — separate from repo `MEMORY.md`; do not duplicate team recall there.
- **SSOT:** Generated `AGENTS.md` + repo `MEMORY.md`; session-start `/memory-steward` light pass.
- Optional: MCP memory server in `~/.cursor/mcp.json` — not required for this kit.

---

## Opencode CLI

**File:** `~/.config/opencode/opencode.json`

```json
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": ["MEMORY.md", "CONTEXT.md"]
}
```

- Walk-up `AGENTS.md` / `CLAUDE.md` still apply; `instructions` loads `MEMORY.md` when present in cwd/repo.
- **Workspace** `opencode.json` at `<workspace-root>`: add explicit paths for multi-repo, e.g. `../api-service/MEMORY.md`, `<artifacts-root>/CONTEXT.md`.

---

## Antigravity CLI

**File:** `~/.gemini/antigravity-cli/settings.json` — no native memory file store.

- **SSOT:** `AGENTS.md` + repo `MEMORY.md`.
- Optional MCP: `~/.gemini/config/mcp_config.json` or `~/.gemini/antigravity-cli/mcp_config.json` (Mem0, AutoMem, etc.) — supplementary only.

---

## Quick reference

| Runtime | Enable built-in memory | Team SSOT |
| :--- | :--- | :--- |
| Codex | `[features] memories = true` | `<repo-root>/MEMORY.md` |
| Claude | `autoMemoryEnabled: true` (default) | `<repo-root>/MEMORY.md` |
| Copilot | GitHub settings + `/memory on` | `<repo-root>/MEMORY.md` |
| Cursor | AGENTS + `/memory-steward` | `<repo-root>/MEMORY.md` |
| Opencode | `instructions` + AGENTS.md | `<repo-root>/MEMORY.md` |
| Antigravity | AGENTS + `/memory-steward` | `<repo-root>/MEMORY.md` |
