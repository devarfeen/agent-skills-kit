# Caveman Invocation Reference

To increase the probability of `caveman` mode being active at the start of a session, agents should immediately invoke the skill using their respective internal tool-calling mechanism.

| Agent | Invocation Command / Action |
| :--- | :--- |
| **Gemini CLI** | `activate_skill(name="caveman")` |
| **Claude Code** | `/caveman` |
| **Copilot CLI** | `skill("caveman")` |
| **Codex CLI** | `activate("caveman")` |
| **Opencode CLI** | `load_skill("caveman")` |

**Trigger Condition:** 
- If reading `AGENTS.md` or `CLAUDE.md`/`GEMINI.md` shims, immediately invoke the `caveman` skill.
- In Claude Code, prefer direct `/caveman` invocation. If slash invocation cannot be self-issued from instructions, read the local `caveman` `SKILL.md` and apply its chat-output rules before continuing.
- The 1% Rule: If there is even a 1% chance the task requires efficiency or brevity, invoke `caveman`.
