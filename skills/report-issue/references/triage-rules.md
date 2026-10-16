# Triage rules

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Load at step 4. Workspace issue, routing and label policy replaces any default here; quote the workspace rule you applied in the triage note.

## Template

| Classification | Template | Classification label |
| --- | --- | --- |
| bug | Bug | `bug` |
| improvement | Improvement | `improvement` (kit default `enhancement`) |
| feature | Feature | `feature` (kit default `enhancement`) |
| maintenance | Maintenance | the label the live template applies |

Read the live template with the tracker's template tool. Its `labelIds` are the template's default classification and workflow labels; resolve their names. No matching template → use the generic skeleton in [issue-body.md](issue-body.md) and say so in the draft.

## Title

Use the workspace title format. Default: `<PROJECT-CODE>: <short imperative heading>`, at most 70 characters. The heading names the outcome the fix delivers, not the symptom: `Keep filters after saving a stock transfer`, not `Filters broken`. Never add `HITL:`, `AFK:`, `BLOCKER:` or priority words.

## Labels

Exactly one classification label. The workflow label is the template's default only when every agent-ready check passes; otherwise `needs-triage`:

1. Bug: expected and actual are observations. Other classes: the desired outcome is observable.
2. Steps to reproduce or an entry route or screen exists.
3. Numbered acceptance criteria restate the reported outcomes without new scope.
4. The primary project is known from code evidence, not guessed.
5. No product, design, permission or data decision is open, including any edge case marked `decision needed`.
6. Dependencies and blocking issues are named, or none exist.

Name each failed check in the triage note. Never set `needs-info`, `ready-for-human` or `wontfix`: those are triage decisions. Never add `qa-escape`; `/qa-escape` owns it. Add another label only when workspace policy defines its meaning. A required label missing from the tracker → leave it off and report the mismatch; never create or rename a label.

## Priority

Use the tracker's scale; never leave the issue at "No priority". State the reason in one line.

| Priority | When |
| --- | --- |
| Urgent | Security exposure, data loss or corruption, wrong money amounts, or a core flow down for every user with no workaround |
| High | A core flow broken for a role, tenant or many users with no reasonable workaround; or it blocks a release's QA |
| Medium | Wrong behaviour with a workaround, or a non-core flow broken. Default for features and improvements |
| Low | Cosmetic, copy, layout or minor polish. Default for maintenance, except a security advisory or failing check (High) |

The environment changes impact, not severity: a production report with users affected moves one level up; a local-only report does not move down.

## Cycle and due date

Compute dates in the team's time zone. A cycle's `endsAt` is exclusive; its last day is the day before. **Active** cycle: `startsAt` ≤ now < `endsAt`. **Upcoming**: the next by `startsAt`. In the cooldown gap there is no active cycle.

| Priority | Cycle | Due date |
| --- | --- | --- |
| Urgent | Active, else upcoming | 2 working days from today, no later than the cycle's last working day |
| High | Active, else upcoming | The cycle's last working day |
| Medium | The cycle after the active one, else upcoming | The cycle's last working day |
| Low | None | None |

The needed cycle does not exist yet → leave cycle and due date unset and say so. Team without cycles → Urgent 2 working days, High 10 working days, Medium and Low none. Working days are Monday to Friday unless the workspace states otherwise.

## Other fields

- **Team and project:** the primary PROJECT-CODE's team and baseline project from the workspace routing map; never a team that only shares the project.
- **State:** the team default. Never set started or completed states.
- **Assignee:** none, unless workspace policy names an intake owner.
- **Relations:** related and duplicate issues as tracker relations when the tool supports them; otherwise list them in the triage note.
