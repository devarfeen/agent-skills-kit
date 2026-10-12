<!-- agents-md marker · v52 · re-run /agents-md to regenerate -->
# Skills and companions

Zero attribution: never add co-author, AI, or tool attribution to any output.

Load before choosing a skill or companion. At later phase boundaries, reuse this file while it remains loaded and unchanged; reload after context loss or a change in available skills.

- **Context window:** choose at a phase boundary, never mid-phase: continue while the next phase needs this context and the window has room; `/clear` when nothing here matters next; `/handoff` only to change harness, directory, or person; a sub-agent for a scoped unattended task; otherwise `/compact`, naming the next phase.

## Skills by phase

[GRADIENT TABLE — columns `Phase | Skills`. Apply the manifest's note exclusions first. One row per gradient phase in manifest order (discover, sharpen, plan, slice, implement, verify, ship). In each row list every eligible `kit` and `external` skill whose manifest `phase` matches, in the manifest's gradient-cell format. Omit phases with no eligible skills.]

Each skill's own description says when to use it.

[STARTUP NOTE — apply the manifest's note exclusions first, then one line per eligible skill with `phase: startup`, in the manifest's startup-line format.]

## Companion skills and MCPs

[COMPANIONS — apply the manifest's note exclusions and install check first, then emit the manifest's companion format: one line naming the installed companion skills, and a `Companion | Use when` table for installed MCPs, CLIs, and plugins only.]

Only companions installed when this file was generated are listed; re-run `/agents-md` after installing another.

## Matt skill routing

Use `/ask-matt` to choose a Matt skill flow — it routes, never executes; do not auto-run its suggestion.

- `/grill-with-docs`: ask once, up front, whether archived context exists; quote pastes in the ADR as a blockquote with `Source: "<doc title>" · pasted <date>`; offer revealed names as `GLOSSARY.md` aliases; flag ADR contradictions, never drop them.
- A requested worktree is set up per `orchestration.md` before any Matt skill does task work; pass it the verified checkout. Do not rewrite installed third-party skills.
- One fresh agent session per ticket. `/implement` says to use `/tdd` and to commit after `/code-review`; this workspace overrides both: drive `/tdd-loop` at each seam, with `/tdd` as reference only, and stop after `/code-review` (`shipping.md`).
- `/implement-spec` (user-invoked): implementers are local sub-agents under `orchestration.md`, each in its own worktree and driving `/tdd-loop`; commits and merges stay local; it opens no PR and resolves no ticket — after `/code-review`, report the integration branch and stop.
- `/pr`: a ship skill's body and the repo's PR template win — mandated sections, their order, and `Closes #N` stay; `/pr` shapes only the summary visual and wording.

[RUNTIME TOOL-CALLING — emit the `## Runtime tool-calling` section here, per the Working with skills rules in SKILL.md]
