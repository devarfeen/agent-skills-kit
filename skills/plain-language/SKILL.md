---
name: plain-language
description: "Chat and prose cleanup at session start: fifth-grade English with bold glossary terms. Clean supplied prose; preserve mandated text. Not code, comments, ADRs, or specs."
metadata:
  version: "0.3.0"
---

# plain-language

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Own the free prose an agent sends. Load once at session start and keep it loaded; reload after context loss or a content change.

## Scope

In scope, free prose only: chat replies; the prose of commit messages, PR bodies and comments, issue bodies and comments, and release notes; human-facing guide or README text the task asked you to write; and text a user hands you to clean.

Out of scope, never edited by this skill even when asked to "clean the file": source code, tests, configuration, scripts, migrations, generated files, code comments and docstrings; ADRs, specs (PRDs), prompts, and glossary entries, which follow their own skills' templates; quoted output, logs, commands, and paths. When a cleanup request points at one of these, say so and stop. Inside an in-scope text, every code span, identifier, and quoted line is protected text.

## When it runs

- **Session start.** After the first reporting-gate update, call the Skill tool with `plain-language` where the runtime has one; otherwise read the installed `SKILL.md`, project-local `.agents/skills/` or `.claude/skills/` first, then the user-level copy. Every later reply applies it from context; no further read is needed while it stays loaded.
- **Before each substantive reply and before finalizing written content.** Apply the rules below to the prose you wrote for the current task. Clean drafts before asking for approval; a change to approved wording needs that approval again.
- **On request.** "Clean this", "remove the AI tells", "make this plain": return the cleaned text, then one line: `Prose cleanup: <n> edits; protected spans kept: <m>`.
- Missing skill → say so once per session and follow the style lines in the workspace `AGENTS.md`.

## Chat and prose style

Apply to all in-scope prose. Written artifacts keep their required templates and formats.

- Lead with the conclusion. Be concise, but use a full sentence where clipping would confuse.
- Default to fifth-grade-level English: familiar words, natural sentences, and brief explanations of technical ideas on first use. Connect related ideas when that makes the cause, condition, or sequence easier to follow. Split dense sentences without forcing every idea into a separate sentence.
- Simplify the explanation, not the subject: keep technical depth, facts, conditions, uncertainty, failure behavior, and exact identifiers. Address an adult reader; do not adopt a child persona or replace precise mechanisms with loose analogies. Use the tense the facts require.
- State the plain effect before implementation details. Explain unfamiliar technical terms once per standalone output; use the glossary rules below for domain terms. Keep code, DB, API, route, screen, and file names verbatim.
- No unexplained shorthand and no arrow-only flows. Brevity skills are user-invoked only.
- Extra teaching depth ("explain like I'm new"), on request only: [`references/learner-depth.md`](references/learner-depth.md). Simple English and first-use explanations are already the default.

## Glossary integration

- Before using project terms, read the applicable `GLOSSARY.md` conventions and relevant entries, following workspace glossary maps and project scope. Search terms and aliases first; do not load the whole archive. Reuse loaded definitions until the scope or source changes.
- Use exact canonical terms with their defined meanings, including project qualifiers for ambiguous terms. Explain each unfamiliar term in simple words on first use, then use it consistently. Do not replace it with an easier synonym or invent a definition. Follow the workspace's source precedence when definitions conflict; report unresolved meaning instead of guessing.
- Bold every occurrence of a glossary term used in its domain meaning in editable prose where Markdown is supported, including repeated mentions. Keep punctuation and possessive endings outside the bold span, such as `**Producer**'s`. In plain-text-only fields, keep the exact term without markup. Protected text and required formatting take precedence: never add bold inside code spans, commands, paths, quotations, identifiers, or mandated headings and labels.
- If no applicable glossary exists, continue in simple English with exact technical names. Do not invent glossary entries or block the task. Reading the glossary grants no permission to edit it.

Example with supplied glossary definitions, Producer = service submitting events; Outbox = temporary event table:

The **Producer** is the service that puts an event in the **Outbox**, a database table where events wait to be sent. The event stays in the **Outbox** until it can be sent.

## Protected text

Rewrite only prose you wrote or edited for the current task; leave unrelated prose alone. Never change meaning, evidence, qualifications, or numbers. Keep exact: templates, markers, headings, field labels, canonical lines, issue-title formats, code, commands, paths, quotations, and anything another skill mandates verbatim. A required line that reads like a tell stays as written.

## Prose cleanup

At session start, also load [`references/prose-patterns.md`](references/prose-patterns.md). Apply its patterns to all in-scope prose before sending or finalizing it. Reuse it from context; reload after context loss or a content change.

## Rules

- Cleanup grants no workflow authority: never publish, commit, push, ship, or close anything because text is clean.
- Never invent facts to replace a vague claim; use the facts the task supplied or delete the claim.
- Runs inline in the current session; it dispatches no sub-agents. Read only its own files, task-supplied prose, and applicable glossary conventions, maps, and relevant entries for cleanup.
- Chat style lives here; the workspace `AGENTS.md` keeps only its short reminder and the understanding-check rule.

## Completion criteria

- [ ] Loaded at session start, or the missing skill was reported once and the workspace style lines were followed
- [ ] Cleaned text keeps every protected span byte-exact and every fact, number, and qualification
- [ ] In-scope prose uses simple explanations without losing technical depth; applicable glossary terms keep their meanings and appear in bold wherever formatting allows
- [ ] A cleanup request returned the text plus its `Prose cleanup:` line
- [ ] No code, test, config, comment, ADR, spec, prompt, or glossary text was touched
- [ ] Nothing beyond editing prose was done
