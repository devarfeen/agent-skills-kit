# Exception protocol

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

TDD adapts to real work — it never silently disappears. Declare the exception
before proceeding, in one line: `TDD exception: <case> — <reason>.` Then state
how the change WILL be verified, and record a follow-up test plan in the
summary (and in the ship skill's `Notes:` section when shipping).

- **Spike / prototype.** Code written to answer a question. No tests during
  the spike; name the question and timebox it. The keeper version re-enters
  the loop from Red — or use `/prototype` and throw the spike away.
- **Legacy code without tests.** Write a characterization test first: pin
  current behavior at the nearest seam before changing anything. No harness at
  all → build the smallest harness that runs one test at that seam; if that's
  out of scope, verify manually and file the harness as the follow-up.
- **Urgent hotfix.** The fix may ship on manual verification evidence when
  waiting is worse than shipping. The regression test is written immediately
  after — same iteration, before the issue closes — and must be seen failing
  against the pre-fix commit. Implement locally; this
  exception grants no production access or deployment authority.
- **Infrastructure / config.** Unit tests rarely apply. Assert what is
  assertable — a validation command, dry run, plan diff, or smoke check — name
  which, run it, and record the output.
- **Exploratory refactor.** Green tests are the harness: run them before,
  continuously, and after. No tests over the area → that's the legacy case
  first.

An exception without declared verification is just untested code.
