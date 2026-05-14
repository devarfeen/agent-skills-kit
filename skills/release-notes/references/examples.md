# Examples

## Example 1: Date-Based Release Notes

### User Request
Generate release notes for 11 March 2026

### Example Input
- fix: RFID power initialization
- fix: retry RFID reader setup
- fix: prevent scan before reader ready
- feat: verify scanner power before lookup
- feat: add activity tracking for field support
- fix: filter component asset list in Collection Package
- feat: verification warnings for QR/RFID data mismatches
- fix: Android app startup crash
- fix: photo selection crash on Android

### Example Output

# Stakeholder Summary

Date: 11 March 2026

PARTNERS-APP

- App now checks the scanner is ready before starting a scan, so first-try scans no longer fail
- New Activity Log in Field Support screen lets support see what a partner did on their device
- Collection Package screen now filters out unrelated assets so the list is cleaner
- Warning shown when a QR code and RFID tag don't match on the same asset
- Fixed crash on Android when opening the app or selecting photos

---

# Detailed Release Notes

## Partners App

### Scanner Now Checks Readiness Before Scanning

**Summary**
- The app waits for the scanner to be ready before starting a scan, so scans don't fail on the first try.

**Problem**
- Scans sometimes failed when the scanner wasn't ready yet, forcing staff to retry.

**Change**
- The app now shows a "Ready" status before allowing scans on the Stock Lookup screen.
- If the scanner isn't responding, the app retries automatically instead of failing.

**Impact**
- Fewer failed scans and retries during busy shifts.

**Scope**
- Stock Lookup screen in Partners App.

**Manual QA Steps**
1. Open Stock Lookup and start a scan → "Ready" status should appear before the scan begins.
2. Start a scan right after opening the app → Scan should wait for the scanner, not fail.
3. Unplug the scanner briefly, then try again → App should retry and recover on its own.

**Commits Included**
- abc1234, def5678, ghi9012, jkl3456

### Support Teams Can View Partner Activity Logs

**Summary**
- Field support can now see a log of what a partner did on their device, making troubleshooting faster.

**Problem**
- Support had no way to see what happened on a partner's device and had to call them to ask.

**Change**
- New Activity Log section in the Field Support screen shows recent partner actions with timestamps.

**Impact**
- Support can troubleshoot without calling the partner.

**Scope**
- Field Support screen in Partners App.

**Manual QA Steps**
1. Log in as field support and open a partner's Activity Log → Recent actions should appear with timestamps.
2. Do a few actions as a partner (scan, lookup, submit), then check the log → All actions should be listed.
3. Filter the log by date → Only matching entries should show.

**Commits Included**
- mno7890

## Example 2: Single Project on a Date

### User Request
Generate release notes for Partners App on 11 March

### Example Output

# Stakeholder Summary

Date: 11 March 2026

PARTNERS-APP

- App now checks the scanner is ready before starting a scan, so first-try scans no longer fail

---

# Detailed Release Notes

## Partners App

### Scanner Now Checks Readiness Before Scanning

**Summary**
- The app waits until the scanner is ready before starting, so scans don't fail on the first try.

**Problem**
- Scans sometimes failed when started before the scanner was ready.

**Change**
- Stock Lookup screen now shows a "Ready" indicator before scans can begin.
- App retries automatically if the scanner is slow to connect.

**Impact**
- Fewer failed scans during stock checks.

**Scope**
- Stock Lookup screen in Partners App.

**Manual QA Steps**
1. Open Stock Lookup and start a scan → "Ready" indicator should appear first.
2. Switch between screens and scan again → Each scan should wait for readiness.
3. Start a scan with a slow connection → App should show "waiting" then proceed.

**Commits Included**
- abc1234, def5678

## Example 3: Session Summary

### User Request
Summarize today's development session

### Example Output

# Stakeholder Summary

PARTNERS-APP

- All scanner screens now use the same setup process, so scanning works reliably everywhere

---

# Detailed Release Notes

## Partners App

### Consistent Scanner Setup Across All Screens

**Summary**
- All screens that use the scanner now prepare it the same way, so scanning works reliably everywhere.

**Problem**
- Some screens prepared the scanner differently, causing scans to sometimes fail on certain pages.

**Change**
- All scanner screens now use the same setup process and show a retry message if the scanner isn't ready.

**Impact**
- Scanning works the same way no matter which screen you're on.

**Scope**
- All scanner-enabled screens in Partners App.

**Manual QA Steps**
1. Open any scanner screen and start a scan → Scanner should finish setup before scan begins.
2. Try scanning on 3 different screens → All should behave the same way.
3. Turn Bluetooth off and on, then scan → App should show a retry message and recover.

## Example 4: Bad vs Good (Writing Style Reference)

This example shows the same work described in bad (verbose/corporate) style vs good (clear/simple) style.

### Bad Output (DO NOT generate like this)

```
### Auth Hardening Workstreams Prepared

**Summary**
- The next round of login and password-handling improvements for the Partners and Portfolio platforms was formally prepared so implementation can move with a clear scope and QA target.

**Problem**
- Follow-up work was still needed around username casing, password visibility, and stronger password rules across multiple auth flows.
- Without a written design and task breakdown, this type of security-sensitive work is easier to implement inconsistently across products.

**Change**
- Two implementation workstreams were documented and broken down for execution:
- Partners portal follow-up work covering username lowercasing and consistent password show/hide behavior across login, signup, reset, invite, and user-management screens.
- Portfolio auth hardening covering username lowercasing, stronger password requirements when setting a password, and password show/hide coverage in staff and gallery user-management flows.
- Concrete touchpoints called out in the workstream docs include the signin page, signup flow, reset and force-change password pages, invite flow, staff password screens, and gallery user forms.

**Impact**
- Engineering now has approved-ready implementation notes for sensitive auth work instead of relying on ad hoc fixes.
- This reduces the risk of one screen being fixed while another screen keeps the same login or password-typing problem.
```

### Good Output (Generate like this)

```
### Login and Password Improvements Planned

**Summary**
- Planned fixes for how usernames and passwords work across Partners and Portfolio apps.

**Problem**
- "John" and "john" were treated as different accounts. Some password fields had a show/hide toggle, others didn't.

**Change**
- Wrote the plan for: making usernames always lowercase, adding show/hide to all password fields, and requiring stronger passwords.
- Covers: Login, Sign Up, Reset Password, Invite, and User Management pages in both apps.

**Impact**
- Once built, all login pages will work the same way across both apps.
```

### What makes the good version better
- Feature name says what changed ("Login and Password Improvements") not how ("Auth Hardening Workstreams")
- Problem describes what the user experienced, not what the code lacked
- Each bullet is one short sentence
- No jargon: no "workstreams", "touchpoints", "ad hoc", "formally prepared"
- A PM can read it in 10 seconds and know exactly what's happening

### User Request
Write release notes for the RFID scanning improvements

### Example Output
## Partners App

### RFID Scanning Improvements

**Summary**
- RFID workflows now follow a more consistent scan startup process.

**Problem**
- Scan attempts could fail when startup steps were incomplete in certain flows.

**Change**
- Standardized scanner setup before scan actions.
- Added readiness checks and controlled retry handling.
- What changed where: RFID scan pages and scan action controls used by front-line teams.
- Simple logic explanation: The app turns the scanner setup steps into the same repeatable checklist every time.

**Impact**
- Fewer startup-related scan failures.
- Reduced operational interruptions in RFID workflows.
- More reliable scan behavior for front-line users.

**Scope**
- Applies to RFID scanning flows covered by this feature.

## Example 5: Omit Unchanged Projects

### User Request
Generate release notes for 12 March 2026 across all projects

### Example Input
- Partners App commits found for 12 March 2026
- Warehouse Admin commits found for 12 March 2026
- No commits found for Customer Portal on 12 March 2026

### Example Output Rule
- Include Partners App and Warehouse Admin sections.
- Do not include Customer Portal because it has no confirmed changes.

### Example Output
Date: 12 March 2026

## Partners App

### RFID Scanner Reliability

**Summary**
- Scanner startup became more consistent in daily operations.

**Problem**
- Teams faced failed first scans in some operational flows.

**Change**
- Standardized scanner startup behavior across updated flows.
- What changed where: scan setup setting and scan status indicator.

**Impact**
- Fewer failed first-scan attempts.

**Scope**
- RFID-enabled operational flows in Partners App.

**Commits Included**
- 148cfb8f, f626e8fa

## Warehouse Admin

### Intake Validation Clarity

**Summary**
- Intake warnings are clearer before submission.

**Problem**
- Users missed required fields during intake.

**Change**
- Added clearer required-field guidance in intake screens.
- What changed where: intake page warning banner and submit-state message.

**Impact**
- Fewer intake retries due to missing fields.

**Scope**
- Intake flow for warehouse supervisors.

**Commits Included**
- a1b2c3d4

## Example 6: Output File Naming

Release notes live in `<artifacts-root>/docs/adr/` alongside ADRs. The `-release-notes` suffix distinguishes them from ADRs (no suffix). Feature prompts (`-prompt`) live in the sibling `<artifacts-root>/docs/prompt/` folder. Numbering is shared globally across both folders — replace `0042` below with the next available number across `<artifacts-root>/docs/adr/` and `<artifacts-root>/docs/prompt/` combined.

`<artifacts-root>` resolves to (1) the directory containing the `*.code-workspace` file when a VS Code workspace is present, (2) the per-context root in a multi-context repo (`CONTEXT-MAP.md` at root), or (3) the repo root for single-repo projects. Workspace mode is preferred — it keeps artifacts out of individual project repos.

### User Request
Generate release notes for 12 March 2026

### Expected Output File
- Workspace mode: `<workspace-dir>/docs/adr/0042-12-march-2026-release-notes.md`
- Single repo: `docs/adr/0042-12-march-2026-release-notes.md`

### User Request
Write release notes for RFID Scanner Reliability

### Expected Output File
- Workspace mode: `<workspace-dir>/docs/adr/0042-rfid-scanner-reliability-release-notes.md`
- Single repo: `docs/adr/0042-rfid-scanner-reliability-release-notes.md`
