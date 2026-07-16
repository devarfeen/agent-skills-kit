# Quality scorecard — `/release-notes`

**Scored:** 2026-07-17 · **Reader:** fresh scorer agent (post-revamp rescore) · **Rubric:** `evals/skill-quality-rubric.md`

## Trigger eval

Routing baseline: maintainer sweep pending for the 2026-07-16/17 description batch (description gained the `/handoff` negative route in 192b37b; last passing run 22/22 on 2026-07-14 predates it).

## Quality

| Category | Score | Note (only if below 5) |
| :--- | :---: | :--- |
| Purpose clarity | 5 | |
| Trigger clarity | 5 | |
| Scope control | 5 | |
| Instruction quality | 5 | |
| Brevity | 5 | |
| Engineering usefulness | 5 | |
| Agent usability | 4 | Multi-step skill (multi-repo scan, lane dispatch, cluster, write) with no `Stage / Found / Next / Needs user` phase updates; per `evals/agent-usability-eval.md` that caps at 4 — a caller cannot tell a slow multi-repo run from a stuck one. Ten sibling skills carry the canonical line. |
| Verification quality | 4 | One completion criterion is self-assessment ("a QA reader knows what to test"), which the rubric excludes from done-ness; the other five criteria are observable. |
| TDD / testing compat | N/A | |
| Maintainability | 4 | Footer cap drifted from the house source of truth: SKILL.md says 1–6 suggestions where `skills/writing-kit-skills/SKILL.md:52` (and sibling skills) fix the `Suggested next skills (optional)` cap at 1–3. |
| Frontier readiness | 5 | |
| **Average** | **4.70** | |

`N/A` is permitted only on TDD / testing compat, and only with a justification
sentence here:

> The skill produces a PM-facing Markdown document from git history it only reads; it neither ships code nor gates on anyone's test run, so there is no testable surface — `evals/tdd-workflow-eval.md` itself lists `release-notes` under the "None" surface.

## Defects

One row per defect. A defect with no anchor and no exact edit is an opinion —
delete it.

| `file:line` | Category | Problem | Exact fix | Gate |
| :--- | :--- | :--- | :--- | :--- |
| `skills/release-notes/SKILL.md:102` | Agent usability | Long-running multi-step run (per-repo git scans, optional lane dispatch, clustering, file output) emits no phase visibility; lane announcements cover only the sub-agent path, so a lane-less run is silent until the file lands | Append the canonical one-liner byte-exact at the end of the "Agent use" section: `Emit \`Stage / Found / Next / Needs user\` at each phase transition — one line per field.` (validate.sh check 13 then binds it) | `none` |
| `skills/release-notes/SKILL.md:188-190` | Verification quality | Completion criterion "Re-read the saved file as a PM: every entry understandable without code context … a QA reader knows what to test" is self-assessment — it cannot fail observably | Replace the criterion with an observable read-back: `- [ ] Every Manual QA step in the saved file is \`Action -> Expected Result\` and names a screen, button, or field; every Impact bullet states a behavior change, not a risk reduction.` | `none` |
| `skills/release-notes/SKILL.md:192` | Maintainability | Footer cap "1–6 advisory suggestions" contradicts the house output cap of 1–3 (`skills/writing-kit-skills/SKILL.md:52`; `pr-feedback` and `commit-push-pr` both say 1–3) | Change "1–6 advisory suggestions" to "1–3 advisory suggestions" | `none` |

**Gates** mean the fix cannot land as an ordinary edit:

- `dup-pair` — the text is duplicated by design (`ship-policy.md`,
  `context-terms.md`). Edit every copy together or `tools/validate.sh` check 2
  fails.
- `description-locked` — the fix would change frontmatter `description`, which
  invalidates the trigger-eval baseline. Needs a maintainer eval re-run.

## Verdict

- [ ] Averages 5.00 — nothing left to point at
- [x] Below 5.00 — the blocking defects are listed above, each with an owner
      and a gate
