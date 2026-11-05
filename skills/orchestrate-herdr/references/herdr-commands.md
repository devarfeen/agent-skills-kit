# herdr commands

Zero attribution: omit co-author, AI, and tool attribution from all output.

The installed binary is the authority for syntax: print a command group's help by running the group with no subcommand — `herdr agent`, `herdr tab`. Never run bare `herdr`, which launches or attaches the TUI, and never probe a *mutating* nested command by omitting its arguments — `herdr workspace create` is valid with defaults and will execute. Control commands return JSON; read IDs and states from the response, never predict them. Server errors are JSON on stderr with exit 1; syntax errors exit 2.

## Companion

The herdr skill ships inside the binary. Already in context → skip. Otherwise load it:

```bash
herdr --skill
```

If loading fails, stop and report the error. `HERDR_ENV=1` identifies the intended environment; it does not prove the binary or server works.

## Context

Herdr injects the caller's context into every managed pane. Save these at the start; every later step confirms it acts in this workspace:

```bash
printf '%s\n' "$HERDR_WORKSPACE_ID" "$HERDR_TAB_ID" "$HERDR_PANE_ID"
herdr tab list --workspace "$HERDR_WORKSPACE_ID"
herdr agent list
```

`tab list` backs the leftover-tab check; `agent list` shows which worker names are already live.

## Names

Each worker needs two distinct names — they are not interchangeable:

- **Tab label** — human-facing, shown in the herdr UI: `[CLI_NAME] - <TRACKER_TAG> #<n>`, e.g. `codex - G #42`, `codex - L #PRWL-101`. The leftover-tab check matches on this.
- **Agent name** — the handle every `herdr agent` command takes. It must match `[a-z][a-z0-9_-]{0,31}` and be unique among live agents, so the tab label's spaces, `#`, and uppercase are illegal. Slugify: lowercase, every run of non-conforming characters to a single `-`. `codex - G #42` → `codex-g-42`; `codex - L #PRWL-101` → `codex-l-prwl-101`. Over 32 characters → drop the `CLI_NAME` prefix, then truncate; a collision with a live agent name → stop and ask, never reuse.

An agent name follows its pane's occupant and is cleared when that agent exits or is replaced.

## Create tab

```bash
herdr tab create --workspace "$HERDR_WORKSPACE_ID" --cwd "$PWD" \
  --label "<tab label>" --no-focus
```

`--cwd "$PWD"` keeps every worker in the orchestrator's folder. `--no-focus` keeps the user's focus put. Read the tab ID from `.result.tab` and the pane ID from `.result.root_pane` — that fresh pane sits at an interactive shell prompt, which is what `agent start` requires.

## Start agent

```bash
herdr agent start <agent-name> --kind <AGENT_KIND> --pane <root-pane-id> \
  --timeout 120000 -- <CODING_CLI flags...>
```

`--kind` is a closed enum of supported agents. Run `herdr agent start --help` for the current list and check `AGENT_KIND` against it. Cursor's kind is `cursor` although its launch token is `agent`. An absent kind stops that launch. Native launch flags go **after `--`**, never as part of `--kind`.

The command returns only once herdr has detected the agent in that pane and it is ready for input, so no readiness polling is needed. Startup defaults to a 30-second wait (max 300000ms). An agent blocked during startup returns `agent_not_ready` immediately but keeps the name usable for `agent read` — wait for idle before prompting.

## Submit

```bash
herdr agent prompt <agent-name> "<worker prompt>" --wait --timeout 60000
```

`agent prompt` honors bracketed-paste and sends the text plus Enter — the prompt is never a launch argument. It **refuses an agent already sitting at an approval or question dialog**, returning `agent_blocked` before sending any input; that is the mechanical guarantee behind "never paste into a blocked or dead shell". On that error, read the pane and surface the dialog under Needs user — never answer it yourself.

`--wait` alone waits for the first settled `idle`, `done`, or `blocked`; do not restate those with `--until`. A submission from a non-working state that produces no observed state change within 5000ms returns `agent_prompt_stalled`.

A timeout or stalled response does not prove non-delivery. Inspect `agent get` and `agent read` before retrying; never submit the same issue twice blindly. Submit prompts concurrently across independent workers, then continue monitoring accepted submissions after a timeout.

## Watch

```bash
herdr agent wait <agent-name> --timeout 60000
herdr agent get <agent-name>
```

Lifecycle states, and what each means for Monitor:

| State | Meaning | Monitor action |
| :--- | :--- | :--- |
| `working` | turn in progress | leave it |
| `idle` / `done` | ready for input; the turn finished | read the tab for the report |
| `blocked` | herdr recognized an approval or question UI | surface under Needs user — never relaunch, never answer |
| `unknown` | an agent is present but unclassified | inspect current state and output; silence alone proves neither completion nor blockage |

`--until` is only for a state-specific wait; bare `agent wait` uses the same settled-state defaults as `prompt --wait`.

Wait concurrently across running workers. A timeout permits a status update and another wait; it does not make a healthy long test blocked.

## Read

```bash
herdr agent read <agent-name> --source recent-unwrapped --lines 200
```

Use `recent-unwrapped` for transcripts and logs — it joins soft wraps. Other sources: `visible` (viewport), `recent` (wrapped), `detection` (agent-detection snapshot). Use `--format ansi` only when color is the evidence.

**Alternate-screen caveat.** If raising `--lines` reveals no more of a finished response, the CLI is drawing on the terminal's alternate screen and those rows never entered herdr's scrollback — a larger count cannot recover them. This is the one case where test evidence can be unquotable. Only then, ask that worker to write its full report as Markdown to a temp file and reply with the path, and read the file. Never request file output in the initial worker prompt.
