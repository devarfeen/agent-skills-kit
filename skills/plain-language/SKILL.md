---
name: plain-language
description: "Chat style and prose cleanup for every session: plain English, ASD-STE100, no AI tells, mandated text kept. Load at session start; cleans supplied prose. Not code, comments, ADRs, or specs."
metadata:
  version: "0.2.0"
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

## Chat style

Chat only; written artifacts keep their own templates and the Scope above.

- Lead with the conclusion. Be concise, but use a full sentence where clipping would confuse.
- Write ASD-STE100 Simplified Technical English: active voice, present tense, short sentences, one idea per sentence, one meaning per word. Split a sentence that carries more than three identifiers.
- Use `GLOSSARY.md` terms exactly, and everyday words over heavy ones. Keep code, DB, API, route, screen, and file names verbatim; state the plain effect first, identifiers after; explain each technical term once.
- No unexplained shorthand and no arrow-only flows. Brevity skills are user-invoked only.
- Learner depth ("explain like I'm new"), on request only: [`references/learner-depth.md`](references/learner-depth.md).

## Protected text

Rewrite only prose you wrote or edited for the current task; leave unrelated prose alone. Never change meaning, evidence, qualifications, or numbers. Keep exact: templates, markers, headings, field labels, canonical lines, issue-title formats, code, commands, paths, quotations, and anything another skill mandates verbatim. A required line that reads like a tell stays as written.

## Patterns to remove

Numbers are stable ids; a removed rule leaves a gap.

### Content

3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.

### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Say "is" or "has".
9. **"Not just X, but Y."** State the point directly instead.
10. **Rule of three.** Don't force ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash substitutes). If a thought needs separation, end the sentence or use a comma.
14. **Colon overuse.** Colons are fine before a list or example, not as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Rewrite to let the point stand on its own without comparison framing. "Describing when the scheduler should fire works best as plain English." Same meaning, no crutch punctuation.
15. **Boldface overuse.** Don't bold every proper noun or acronym.
16. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove from headings and bullets.
19. **Curly quotes.** Use straight quotes.

### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
22. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.

### Filler

23. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". Delete "It is important to note that".
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
25. **Generic conclusions.** "The future looks bright." State specific plans or facts.

### Jargon

26. **Abstract metaphor nouns.** Substrate (base), wedge, wedge in (add), vector (way, method), locus, vantage, nexus, primitive as a noun, harness as a metaphor, surface as in "API surface", bedrock, scaffolding as a metaphor, modality, paradigm, gold-plating (more than the job needs), ratchet as a metaphor (the mechanism's real name, or a limit that only tightens), evacuate for moving code (move out), endgame (the last phase), north star, flywheel. These read as technical but usually have a plainer concrete word. Pick the concrete word.

### Plain speech

27. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", "types that follow your schema" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.
28. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.
29. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Passive is fine only when the actor is unknown or genuinely doesn't matter.
30. **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number, and "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong.
31. **Prefer the plain word.** "utilize" and "leverage" become "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is rarely clearer.
32. **Mannered prose.** Metaphor or flourish where a literal phrase exists: aphorisms ("wire it or delete it"), rhetorical fragments for effect, personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"), stock framing phrases. "A dial worth turning" becomes "a parameter worth varying". Say what you mean. Rule 26 covers the metaphor nouns.
33. **Over-compression.** Dropped articles, verbless fragments, symbol-speak, and abbreviations that make the reader decode instead of read. "Parser rejects bad date → exit 2, no write" becomes "The parser rejects a bad date, exits with code 2, and writes nothing." Write whole sentences with their articles and verbs, and spell out arrows and abbreviations.

## Rules

- Cleanup grants no workflow authority: never publish, commit, push, ship, or close anything because text is clean.
- Never invent facts to replace a vague claim; use the facts the task supplied or delete the claim.
- Runs inline in the current session; it dispatches no sub-agents and reads no files beyond its own.
- Chat style lives here; the workspace `AGENTS.md` keeps only its short reminder and the understanding-check rule.

## Completion criteria

- [ ] Loaded at session start, or the missing skill was reported once and the workspace style lines were followed
- [ ] Cleaned text keeps every protected span byte-exact and every fact, number, and qualification
- [ ] A cleanup request returned the text plus its `Prose cleanup:` line
- [ ] No code, test, config, comment, ADR, spec, prompt, or glossary text was touched
- [ ] Nothing beyond editing prose was done
