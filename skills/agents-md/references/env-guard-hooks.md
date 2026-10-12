# Environment guard hooks (optional)

The generated rules forbid production access and require staging approval. This optional hook blocks literal production-host matches and asks on staging-host matches; it is a best-effort check, not enforcement of every access path. This file is a template to suggest, never to install. Writing settings or scripts needs the user's explicit approval, and the user fills in host lists. An empty list disables that check, never the underlying environment policy.

Zero attribution: omit co-author, AI, and tool attribution from all output, including the hook script and settings.

## When to suggest it

In the run's close, when the workspace or a project names production or staging hosts (deploy config, `.env.example`, compose files, runbooks), suggest this template once. Not named → don't suggest it.

## Claude CLI form

Verified 2026-10-03 against https://code.claude.com/docs/en/hooks-guide.md: `PreToolUse` with matcher `Bash`, `$CLAUDE_PROJECT_DIR`, stdin `.tool_input.command`, and `permissionDecision` `deny` (cancels the call) or `ask`. Other runtimes: use their own permission or sandbox settings; this kit ships no tested form for them.

Owner-applied workspace `.claude/settings.json` patch (merge; never overwrite other keys). Agent-written settings require an explicit zero-attribution rule in a schema-supported field; if none exists, leave this strict JSON patch for the owner rather than inserting unsupported keys or comments:

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
# Zero attribution: never add or leave co-author, AI, or tool attribution in output.
# Deny commands that name a production host; ask before commands that name a staging host.
PROD_HOSTS='prod\.example\.com|203\.0\.113\.10'   # user fills in (extended regex)
STAGING_HOSTS='staging\.example\.com'              # user fills in (extended regex)

cmd=$(jq -r '.tool_input.command // empty')
decide() {
  jq -n --arg d "$1" --arg r "$2" \
    '{hookSpecificOutput: {hookEventName: "PreToolUse", permissionDecision: $d, permissionDecisionReason: $r}}'
  exit 0
}
# An empty list skips its check; an empty pattern would match every command.
[[ -n "$PROD_HOSTS" ]] && grep -Eq "$PROD_HOSTS" <<<"$cmd" && decide deny "Production access is forbidden by AGENTS.md."
[[ -n "$STAGING_HOSTS" ]] && grep -Eq "$STAGING_HOSTS" <<<"$cmd" && decide ask "This command names a staging host. Approve this step?"
exit 0
```

## Limits

Literal text matching has false positives and false negatives: a harmless mention can match, while SSH aliases, variables, wrappers, or encoded hosts can hide access. It sees only Bash commands; MCP and other tools need separate permission rules. The hook does not establish user-provided SSH access or per-mutation staging approval. Use runtime tool and network restrictions for a hard boundary. It complements the git-guardrails companion, which covers git commands only.
