# Human-facing descriptions for user-invoked skills

The kit does not strip trigger phrasing from the descriptions of its
user-invoked skills.

## Why this is out of scope

Upstream (mattpocock/skills) writes a user-invoked skill's description as a
one-line summary for a person, because the model can never route to it. That
holds only where the runtime honors `disable-model-invocation`. Two of the six
runtimes this kit supports do not:

- Opencode recognizes only `name`, `description`, `license`, `compatibility`,
  and `metadata`; unknown frontmatter fields are ignored
  (<https://opencode.ai/docs/skills/>). Access is controlled in `opencode.json`
  permissions, not in `SKILL.md`.
- Antigravity recognizes only `name` and `description`, and the agent decides
  from the description whether to load a skill
  (<https://antigravity.google/docs/skills>).

Checked 2026-10-05. In those runtimes every kit description is a live router,
so the trigger and boundary sentences, and the trigger evals over all skills,
still do work. Revisit when every supported runtime honors the flag.

Since 2026-10-12 every description is capped at 200 characters. That shortens
the router text; it does not turn it into a human summary. Each description
still names what the skill does, its main trigger, and its nearest sibling,
and the full trigger-eval sweep still runs over all of them.
