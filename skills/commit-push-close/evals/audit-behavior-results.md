# Shipping simulation results

Zero attribution: omit co-author, AI, and tool attribution from all output.

Date: 2026-09-09. Method: independent document review and simulated execution of `audit-behavior-cases.md`. No GitHub commands, commits, pushes, environment reads, or issue mutations were performed. Returned URLs below are explicit simulation placeholders. Baseline was read from the pre-edit audit snapshot, not reconstructed from memory. These are two prompt simulations, not a statistical reliability estimate.

## Close-1

Revised draft:

```markdown
Implemented in abc1234 on `fix/418-email-error`.

## QA handoff
Change: abc1234 on `fix/418-email-error`.

### What changed
Settings > Profile now shows an error when an Editor submits an invalid email.

### Where changed
- Settings > Profile: `src/settings/ProfileForm.tsx` displays the email validation error.
- `src/settings/ProfileForm.test.tsx` covers invalid and valid email submissions.

### Setup
Run revision abc1234 locally with `pnpm dev` and open http://localhost:3000.
Sign in with an existing Editor test account. Record that account's original email before testing.

### How to test
1. Open Settings > Profile, enter `invalid-email` in the email field, and save. Expect a visible validation error and no successful save.
2. Enter a valid synthetic test email, such as `qa@example.test`, and save. Expect a successful save without the invalid-email error.
3. Run `pnpm test src/settings/ProfileForm.test.tsx`. Expect the invalid and valid cases to pass.
4. Restore the test account's original email. Expect a successful save.

### Verification
The automated command passed 4 tests on this content. Manual UI checks are pending. Deployment has not been verified.
```

Simulated ordered actions: check the recorded content/test match; reuse direct-close and combined approval already supplied; inspect the complete index and commit only the two intended files with the actual issue title and `Issue: #418`; push to the permitted upstream; compare remote SHA with abc1234; fill and post this comment; read back its body and `<simulated-close-comment-url>`; close #418; read `CLOSED`.

Final simulated response: `abc1234 pushed to fix/418-email-error; issue #418 closed (state CLOSED verified); QA: <simulated-close-comment-url>` plus the advisory footer.

Result: all 5 fixture assertions satisfied. Credentials and exact issue title were not invented. The fixture grants existing approved drafts; their issue-title field remains supplied by the recorded issue, outside the QA-comment test.

Baseline draft dictated by the old format:

```markdown
Closed by abc1234 on `fix/418-email-error`.

**What changed**
Editors now see an error when they enter an invalid email in their profile.

**How to confirm it's fixed**
1. Open your profile settings and submit an invalid email.
2. Expect a visible validation error.
3. Submit a valid email and expect it to save.
```

Baseline result: the old format expressly excludes paths and commands, lacks setup and revision instructions, and makes the comment claim closure before closure happens. Its workflow posts without comment read-back and only runs the failing-test gate after push. The new QA-location/setup/verification/read-back assertions therefore do not all pass on the original instructions. The baseline still gives a useful invalid/valid behavior pair; that existing strength was retained.

## Close-2

Revised simulated actions: stop shipping at the required `pnpm test checkout` failure, preserve the unrelated staged `notes/private.md`, and report the ownership conflict before any future commit. Record the permitted `.env.example` key change and request owner parity verification for restricted environments. Do not open production or unapproved staging files.

Simulated response: `Shipping #419 is blocked: pnpm test checkout exited 1, and notes/private.md is already staged outside this change. No commit, push, comment, or closure was performed. The owner must verify CHECKOUT_TIMEOUT_MS in restricted environments; no restricted values were inspected.`

Result: all 4 fixture assertions satisfied. Required validation failure remains a blocker despite draft approval.

Baseline result: its test gate occurs after push; its pre-commit section never checks existing index ownership; its env-parity instructions demand editing even ignored production/staging files. Workspace restrictions still outrank the skill, so the correct baseline execution stops at that instruction conflict. The old skill cannot provide an unambiguous, complete execution of this case on its own. The revised instructions make each stop explicit and move validation ahead of shipment.
