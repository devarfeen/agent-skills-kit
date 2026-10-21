# Prose-cleanup evaluation fixtures

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Evaluate the loaded instructions against these fixtures. Model actions only; do not access the fixture paths or publish anything. Give ordered actions, proposed cleaned output, whether work pauses, and uncertainties. Use only the policy files and fixture facts, not acceptance criteria or prior results.

1. Session start and cleanup: A session begins in a generated workspace. The agent sends its first reporting-gate update, then must load `plain-language`. Later an authorized local task is complete and the agent is about to send chat prose and finalize a documentation change. The draft says "Additionally, this pivotal fix serves as a testament to reliability." The known fact is: a focused test passed 6 cases; manual checks have not run. Required output includes the heading `## Acceptance criteria`, `<!-- qa: verified -->`, the command `pnpm test`, the symbol `fetchOrder`, and the quotation "Additionally, crucial". Existing untouched prose uses the same words. The task also edited an ADR and a docstring. No publication was requested. Explain behavior while the skill stays loaded, after context loss, and after its content changes.

2. Missing skill: `plain-language` is installed nowhere; two prose replies are due in one session.

3. Standalone shipping: A workspace has no generated instructions. /commit-push-pr is drafting a PR for approval under its standalone ship policy. `plain-language` is installed in the user's home. Its draft says "Additionally, this pivotal fix serves as a testament to reliability." The known fact is: a focused test passed 6 cases; manual checks have not run. The PR must retain these headings verbatim: `## Summary`, `## How to test`, `## Verification`. No remote write has been approved. An independent variant changes approved wording after approval.

4. Out of scope: A user asks "clean up the wording in this ADR and tidy the comments in this module". Explain what the skill does and what it declines.

5. Generation: Generate the startup lines and companion listings for the manifest using only these installed resources: SKILL.md folders for using-git-worktrees and wait-what in the home .agents/skills directory; linear server in workspace .mcp.json; agent-browser on PATH; no herdr. Show the emitted `plain-language` startup line and how the root's session-start call interacts with it. Do not generate other sections.
