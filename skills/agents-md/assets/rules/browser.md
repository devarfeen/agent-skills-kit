<!-- agents-md marker · v57 · re-run /agents-md to regenerate -->
# Browser verification

Zero attribution: never add co-author, AI, or tool attribution to any output.

Read before driving a browser.

Applies to every browser mechanism in every runtime — agent-browser, a browser subagent, a Playwright/CDP MCP.

- One authenticated session per task, one name reused across shells and turns, one command at a time. Health-check a reused session; on failure close and reopen **that session only** — never `close --all`.
- One batched flow per route — open → interact → deterministic assertion — through the project's flow runner or batch mode (agent-browser: `batch --bail`). A simple smoke takes about three calls.
- Timeouts of 3–8 s per command and one outer timeout per flow. Wait on a condition — selector, text, URL — never a bare timeout. Warm a cold build with an HTTP request first.
- Launch options apply only when a session's browser starts; an ignored-flag warning means close that session and reopen it.
- Stable selectors (`data-test`, CSS) and waits taken from the app's source, never guessed strings or framework refs. Assert stable state — URL, DOM, session state — never toast timing or `networkidle`. Snapshot one element, not the page.
- Isolate mutation checks: record originals, change one setting, verify, restore — also when the flow fails.
- One flow plus one evidence check per behavior. On failure, fix waits or selectors and retry in the same session; restart only for an ignored launch flag, a dead session, or an intended auth reset, and say why.
- Pass secrets through stdin or a file, never the command line.
