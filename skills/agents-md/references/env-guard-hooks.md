# Environment guard hooks (optional)

The generated rules forbid production access and gate staging, but prose is advisory: a runtime hook enforces it before the command runs. This file is a template to suggest, never to install. Writing settings or scripts needs the user's explicit approval, and the user fills in the host lists.

Zero attribution: omit co-author, AI, and tool attribution from all output, including the hook script and settings.

## When to suggest it

In the run's close, when the workspace or a project names production or staging hosts (deploy config, `.env.example`, compose files, runbooks), suggest this template once. Not named → don't suggest it.

## Claude CLI form

Verified 2026-10-03 against https://code.claude.com/docs/en/hooks-guide.md: `PreToolUse` with matcher `Bash`, `$CLAUDE_PROJECT_DIR`, stdin `.tool_input.command`, and `permissionDecision` `deny` (cancels the call) or `ask`. Other runtimes: use their own permission or sandbox settings; this kit ships no tested form for them.

Workspace `.claude/settings.json` (merge; never overwrite other keys):

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/.claude/hooks/env-guard.sh" }
        ]
      }
    ]
  }
}
```

`.claude/hooks/env-guard.sh` (make it executable; needs `jq`):

```bash
#!/usr/bin/env bash
# Deny commands that name a production host; ask before commands that name a staging host.
PROD_HOSTS='prod\.example\.com|203\.0\.113\.10'   # user fills in (extended regex)
STAGING_HOSTS='staging\.example\.com'              # user fills in (extended regex)

cmd=$(jq -r '.tool_input.command // empty')
decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}
grep -Eq "$PROD_HOSTS" <<<"$cmd" && decide deny "Production access is forbidden by AGENTS.md."
grep -Eq "$STAGING_HOSTS" <<<"$cmd" && decide ask "Staging access needs explicit approval for this step."
exit 0
```

## Limits

Matching is by text, so it over-blocks (a command that only mentions a host) rather than under-blocks. It sees only Bash commands, so MCP or other tools that reach a host need their own permission rules. It complements the git-guardrails companion, which covers git commands only.
