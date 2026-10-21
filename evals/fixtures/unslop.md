# Prose-cleanup evaluation fixtures

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Evaluate the loaded instructions against these fixtures. Model actions only; do not access the fixture paths or publish anything. Give ordered actions, proposed cleaned output, whether work pauses, and uncertainties. Use only the policy files and fixture facts, not acceptance criteria or prior results.

1. Workspace cleanup: An authorized local task is complete. The agent is about to send chat prose and finalize a documentation change. The user did not type /unslop. Cursor unslop is installed with disable-model-invocation: true; it is absent from an old generated companion list. Project-local and user-level copies exist. The draft says "Additionally, this pivotal fix serves as a testament to reliability." The known fact is: a focused test passed 6 cases; manual checks have not run. Required output includes the heading `## Acceptance criteria`, `<!-- qa: verified -->`, the command `pnpm test`, the symbol `fetchOrder`, and the quotation "Additionally, crucial". Existing untouched prose uses the same words. No publication was requested. Explain behavior when rules stay loaded unchanged, after context loss, after source content changes, and after resolution changes.

2. Missing helper: Neither local nor user-level unslop is installed; two prose replies are due in one session.

3. Standalone shipping: A workspace has no generated instructions. /commit-push-pr is drafting a PR for approval under its standalone ship policy. Cursor unslop is installed globally with model invocation disabled. Its draft says "Additionally, this pivotal fix serves as a testament to reliability." The known fact is: a focused test passed 6 cases; manual checks have not run. The PR must retain these headings verbatim: `## Summary`, `## How to test`, `## Verification`. No remote write has been approved. An independent variant changes approved wording after approval.

4. Generation: Generate companion listings for the manifest using only these installed resources: SKILL.md folders for using-git-worktrees and unslop in the home .agents/skills directory; linear server in workspace .mcp.json; agent-browser on PATH; no herdr. Show emitted companion listings and how the new prose-cleanup section interacts with this list. Do not generate other sections.
