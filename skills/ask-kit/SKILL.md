---
name: ask-kit
disable-model-invocation: true
description: "Ask which agent-skills-kit skill fits your situation — a router over this kit's skills from workspace setup through shipping. Names one skill, why it fits, and what it needs; never runs it. Use when the user asks which kit skill to use, what to run next with no spec or PR to point at, or how the kit's skills fit together. A spec, ticket, or PR that already exists routes to /factory; choosing among Matt Pocock's planning and build skills routes to ask-matt."
metadata:
  version: "0.0.2"
---

# ask-kit

A router: it turns a described situation into the one kit skill to run next. It reads nothing but the conversation and never starts the skill it names.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## Rules

- **Route, never run.** Name the skill and stop; the user starts it. Most kit skills are user-invoked.
- **One skill.** Give the single best next step. A second is allowed only as the step after it, labelled `then`.
- **Ask one question when two rows fit.** Lead with the recommended answer so the user can accept it in a word.
- **Missing skill.** A skill the session does not list → name it with `npx skills add devarfeen/agent-skills-kit -g --skill <name>`.
- **Outside the kit.** Planning, slicing, and building a ticket belong to Matt Pocock's skills; name the entry skill below, or `ask-matt` for the route through them.

## The map

| Situation | Skill |
| :--- | :--- |
| New workspace, or the Project Matrix is stale | `/agents-md` |
| A UI project has no tokens or component library | `/design-system` |
| How does this existing feature work, or what uses it | `/feature-discovery` |
| Rebuild a feature from one stack in another | `/port-feature` |
| Rough idea, destination and open decisions already sharp | `/feature-prompt`, then `/grill-with-docs` |
| Rough idea, decisions still gate the scope | `/wayfinder` (Matt) |
| Build one ticket or fix a bug test-first | `/tdd-loop` |
| Fan a spec's sub-issues out to worker tabs, inside herdr | `/orchestrate-herdr` |
| Fan a spec's sub-issues or a list of issues out to T3 Code threads | `/orchestrate-t3` |
| The work must happen in a worktree | `/using-git-worktrees`, then the task skill |
| A page must match Figma or reference screens | `/pixel-audit` |
| Small copy, spacing, or alignment nits from QA | `/polish-batch` |
| A spec spans more than one project | `/integration-contract` |
| Done; close the issue directly | `/commit-push-close` |
| Done; open a PR for review | `/commit-push-pr` |
| Reviewer left comments on an open PR | `/pr-feedback` |
| CI is red on an open PR | `/ci-loop` |
| CI is green and the change can reach a screen | `/agentic-qa` |
| May this PR merge without an engineer | `/risk-review` |
| A PR merged to staging; did the deploy land | `/deploy-watch` |
| Staging is broken | `/staging-fix` |
| Human QA found a bug after the work was called done | `/qa-escape` |
| Promote every project from local to staging | `/local-to-staging` |
| Is staging ready for production | `/staging-to-production` |
| Production incident or outage | `/incident-triage` |
| Notes for PMs and QA on what shipped | `/release-notes` |
| A spec, ticket, or PR exists and its next gate is unclear | `/factory <reference>` |
| Work every issue carrying a label end to end, pausing for review and merge | `/factory run <label>` |
| Editing this kit's own skills | `/writing-kit-skills` |

## Output

```
Run: /<skill> — <one-line reason tied to what the user said>
Needs: <the input that skill will ask for, or "nothing">
Then: /<skill> — <only when the next step is already certain>
```

Nothing after it.

## Completion criteria

- [ ] The reply names exactly one `Run:` skill that appears in the map or is a named Matt entry skill
- [ ] No tool call ran and no file changed during the reply
