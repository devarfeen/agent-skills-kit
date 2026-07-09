# Repo eval

Kit-wide health. Skills can each score 5/5 and the kit still be broken — this
sheet catches what per-skill scoring cannot see.

## Automated gate

```bash
bash tools/validate.sh
```

Nine checks: frontmatter (name matches folder, kebab-case, description present,
≤1024 chars, parses as **strict YAML**), duplicated-by-design copies
byte-identical, manifest↔folder agreement in both directions, README table rows,
relative links and cross-file anchors resolve, zero-attribution tripwire on files
and branch commits, `agents-md` version markers in sync, manifest phases valid,
trigger-eval sets parse.

Green is a gate, not a score. It proves nothing about whether the skills are good.

> A description containing `: ` (colon-space) must be double-quoted or check 1
> fails. An unquoted one installs nowhere — the skills CLI's YAML parser rejects
> it with "mapping values are not allowed here".

## Manual checks

| # | Check | How | Pass |
| :--- | :--- | :--- | :--- |
| 1 | **No trigger collisions** | Every skill's eval set includes near-miss negatives routing to a *named* sibling | Latest run recorded in each `evals.json` `last_run` |
| 2 | **Gradient coverage** | Each phase (startup → discover → sharpen → plan → slice → implement → verify → ship) has at least one skill | No phase orphaned |
| 3 | **No sprawl** | No skill half-covers a sibling's job | Each pair of adjacent skills has a stated boundary sentence |
| 4 | **Sync map honored** | See CONTRIBUTING's edit→sync map | Skill add/rename touched manifest + README + GUIDE |
| 5 | **Runtime facts fresh** | `tool-calling.md`, `*-tools.md`, `memory-global-defaults.md`, `tdd-loop/references/test-commands.md` | Each carries a "Last verified" stamp against an installed CLI version |
| 6 | **`main` is releasable** | Consumers install from `main` | Validator green, no half-migrated skill |

## Kit score

Average the per-skill averages from each `skills/<name>/evals/quality.md`.
Record the date, the rubric version, and how many readers scored each skill —
a single-reader pass and a panel are not the same evidence.

| Date | Kit average | Method | Lowest skill |
| :--- | :--- | :--- | :--- |
| | | | |

## What a blocker looks like

A skill that cannot reach 5/5 is not a failure of the pass — it is a finding.
Record it as: the skill, the exact remaining defect, the gate that prevents the
fix, and what would clear the gate. Do not lower the rubric to make the number
green.
