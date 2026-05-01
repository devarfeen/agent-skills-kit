# Agent Skills Kit

A collection of reusable **skills** for AI coding agents (Claude Code, Cursor,
and any agent runtime that supports the [`skills`](https://www.npmjs.com/package/skills)
package format).

A *skill* is a small, self-contained bundle of instructions, examples, and
templates that teaches an agent how to do one specific job well — for example,
"write PM-friendly release notes from git history". Install a skill into your
agent's workflow and the agent picks it up automatically when a matching
request comes in.

## Repository Layout

```
agent-skills-kit/
├── README.md                 # This file
├── LICENSE                   # MIT
└── skills/
    ├── release-notes/        # The release-notes skill
    │   ├── SKILL.md          # Required: metadata + instructions
    │   ├── README.md         # Human-readable docs for this skill
    │   ├── references/       # Additional docs loaded on demand
    │   │   ├── examples.md   # Worked input → output examples
    │   │   └── triggers.md   # Phrases that activate the skill
    │   └── assets/           # Output templates the skill fills in
    │       ├── release-notes-template.md
    │       └── session-summary-template.md
    ├── feature-discovery/    # The feature-discovery skill
    │   └── SKILL.md          # Required: metadata + instructions
    └── feature-prompt/       # The feature-prompt skill
        └── SKILL.md          # Required: metadata + instructions
```

Each subfolder under `skills/` is a standalone skill that follows the
[Agent Skills spec](https://agentskills.io/specification) — a `SKILL.md` with
`name` + `description` frontmatter plus optional supporting files. Skills can
be installed on their own.

## Installing a Skill

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill <skill-name>
```

Updating to the latest version:

```bash
npx skills update https://github.com/devarfeen/agent-skills-kit --skill <skill-name>
```

The `skills` CLI fetches the named subfolder from this repo and installs it
into your agent's local skills directory. After install, just talk to your
agent normally — it will invoke the skill when your request matches one of
its trigger phrases.

## Available Skills

### `release-notes`

Turns git commits, the current dev session, or finished feature work into
**clear, PM-friendly release notes**. Designed so a non-technical reader can
scan everything in 30 seconds.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill release-notes
```

**What it does**

- Reads git history (locally only — never runs `git fetch` or `git pull`)
- Walks multi-repo workspaces and finds every `.git` root
- Clusters related commits into a single logical change instead of
  commit-by-commit narration
- Produces a single markdown file with two sections:
  1. **Stakeholder Summary** — bullet list grouped by product code, one
     sentence per change
  2. **Detailed Release Notes** — full Problem → Change → Impact → Scope →
     Manual QA Steps → Commits Included blocks per feature

**Generation modes**

| Mode | Example prompt |
| --- | --- |
| Date-based (single date or range) | `Generate release notes for 11 March 2026` |
| Single project on a date | `Generate release notes for Partners App on 11 March` |
| All projects on a date | `Create changelog for all projects on 15 April` |
| Current dev session | `Summarize today's development session` |
| Specific feature | `Write release notes for the QR scanning improvements` |

**Output location**

When you run the skill, generated files land in a `changelog/` folder at
**your** workspace root (the skill creates it if it doesn't exist):

- Date or session: `changelog/DD-Month-YYYY.md` (e.g. `changelog/12-March-2026.md`)
- Feature: `changelog/Feature-Name.md` in Title-Case-Hyphenated form
  (e.g. `changelog/RFID-Scanner-Reliability.md`)

**Manual QA steps**

Each detailed feature entry includes a Manual QA Steps subsection. If a
`specs/5-manual-qa-steps.md` file exists for the feature it is linked and key
steps are inlined; otherwise the skill generates 3–5 practical
Action → Expected Result steps.

**Writing style**

The skill enforces strict plain-language rules — no jargon, max 2 bullets per
section, feature names describe *what changed* not *how*, and a banned-words
list (`workstream`, `touchpoint`, `formally`, etc.) keeps output readable.

See [skills/release-notes/README.md](skills/release-notes/README.md) for the
full feature list and [skills/release-notes/references/examples.md](skills/release-notes/references/examples.md)
for input/output examples (including a side-by-side bad-vs-good comparison).

### `feature-discovery`

Performs a read-only discovery pass for a feature, issue, module, workflow,
API, config, or behavior across one or more codebase projects.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill feature-discovery
```

**What it does**

- Maps project codes to likely repo, app, or package roots
- Searches code, tests, docs, configs, routes, jobs, and feature flags
- Traces definitions to callers and user-facing flows
- Uses recent git history only when code scanning is not enough
- Produces a structured report covering summary, behavior, implementation,
  usage sites, rationale, risks, gaps, and next checks

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| Feature lookup | `Explain how asset lookup works in APP` |
| Issue trace | `Investigate why RFID scans fail in APP` |
| Workflow audit | `Trace the invite-user workflow across Admin and API` |

### `feature-prompt`

Turns a rough feature idea into a **precise feature-development prompt** for
one or more codebase projects. Designed for short, step-by-step clarification
before handing work to an implementation agent.

```bash
npx skills install https://github.com/devarfeen/agent-skills-kit --skill feature-prompt
```

**What it does**

- Interviews the user one section at a time: Projects, Need, Integration,
  Reason, Constraints, and optional Acceptance
- Challenges vague answers before moving on
- Inspects the codebase when local context can answer or sharpen a section
- Produces a short final prompt in the same section order

**Prompt sections**

| Section | Purpose |
| --- | --- |
| Projects | Project codes or repos affected by the change |
| Need | What needs to be built or changed |
| Integration | Where the change connects in code, UI, APIs, DB, jobs, or services |
| Reason | Why the change is needed |
| Constraints | Limits, exclusions, compatibility needs, or `none` |
| Acceptance | Optional done-state; inferred if skipped |

**Example prompts**

| Mode | Example prompt |
| --- | --- |
| New feature | `Help me create a feature prompt for stock transfer approvals` |
| Change request | `Turn this rough request into a dev prompt for APP and API` |
| Multi-project work | `Create a feature prompt for Admin, Mobile, and Backend` |

## Using a Skill (Quick Walkthrough)

1. **Install:** run the `npx skills install …` command for the skill you want.
2. **Ask your agent:** use a natural request that matches the skill — e.g.
   "Generate release notes for today" or "Create a feature prompt for APP".
3. **Review the output:** release notes write markdown files under
   `changelog/`; discovery and prompt skills return structured markdown in the
   conversation.

The skills avoid changing your git state unless their own instructions say
otherwise. Skills that inspect history only read commits already available on
your machine.

## Contributing a New Skill

1. Create a new folder under `skills/your-skill-name/`.
2. Add a `SKILL.md` with frontmatter (`name`, `description`) followed by the
   instructions the agent should follow.
3. Add a `README.md` describing the skill for humans.
4. Optionally add `references/` for on-demand docs (examples, trigger
   phrases) and `assets/` for templates and other static resources, per the
   [spec conventions](https://agentskills.io/specification).
5. Open a PR.

Keep skill instructions deterministic and example-driven — skills work best
when they spell out exactly what to do, what to avoid, and what good output
looks like.

## License

[MIT](LICENSE) © Arfeen Arif
