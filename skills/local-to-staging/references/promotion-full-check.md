# Promotion full check

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Read when a repo's project rules declare `Full-check point: promotion`. Its builders shipped into `<source>` on an area check, with `Full check: deferred to promotion`; this step is where that repo's canonical full check runs. Repos with no declaration, or `ship`, skip this file.

## Run

- **Once per repo, on the promoted head.** The checked SHA is `origin/<source>` as fetched in step 1, the PR head this skill will merge. Run in a checkout the project's rules name for this check, with a clean tree and `HEAD` equal to that SHA; read both back first. No such checkout → that repo is `blocked: no checkout at <sha>`. Never commit, push, rebase or move a branch to make one.
- **Project command, project runtime.** Use the canonical full-check command and runtime from the project's verification rules, unchanged: every subcheck, assertion and coverage threshold. Never narrow it to save time.
- **One repo at a time.** Follow the project's heavy-run rule; never start a repo's full check while another heavy run is active. Other repos' read-only steps may continue.
- **Proof.** Keep the producer exit status, pass/fail counts, duration and log path, bound to the checked SHA. A reader's exit status, a partial run or a missing status is not a pass.

## Result

- **Pass** → write into the PR body (new PR) or apply with `gh pr edit --body-file` (reused PR):

  ```md
  Full check: <command> — <passed/failed counts or exit status> — <duration> — <full checked SHA>
  ```

  Merge only while the PR's `headRefOid` equals that SHA; step 4's `--match-head-commit` pins it. A moved head reruns the full check once on the new head.
- **Fail** → that repo stops before PR create or merge; other green repos continue. Report the failing tests or stages from the producer output, the commits merged since the last promotion (`git log --oneline origin/<target>..<checked-sha>`), and a suggested fix branch off `<source>` through the project's normal build and ship path. Open no PR and post nothing for it. After the fix lands on `<source>`, the next `/local-to-staging` run checks that repo once more.
- **Environment failure** (runtime, container, missing dependency) → report it as `blocked`, not as a product failure, with the repair owner. The repo does not promote until a real pass.

## Checklist

- [ ] Each `promotion` repo has exactly one full-check result bound to the head it would merge, or a stated block
- [ ] Every merged `promotion` repo's PR body carries a passing `Full check:` line for its merged head
