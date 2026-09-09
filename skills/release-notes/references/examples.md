# Examples

Zero attribution: never add or leave co-author, AI, or tool attribution in commits, PRs, issue comments, release notes, generated docs, settings, or code comments.

Some outputs below are excerpts; a real file always opens with the file-level
Stakeholder Summary and carries every per-feature block (Summary through
Commits Included) for each feature. Session summaries follow `assets/session-summary-template.md`; entries read exactly like Example 1.

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

Additional evidence for this example: the diff shows a Ready status and retries
on Stock Lookup; the user confirms these commits were released. Commit subjects
alone would not establish either fact. The listed checks have not been run.

### Example Output

# Stakeholder Summary

Date: 11 March 2026

WAREHOUSE-APP

- The app now checks scanner readiness first, so first-try scans no longer fail
- New Activity Log shows support what a partner did on their device
- Collection Package screen now filters out unrelated assets so the list is cleaner
- Warning shown when a QR code and RFID tag don't match on the same asset
- Fixed crash on Android when opening the app or selecting photos

---

# Detailed Release Notes

## WAREHOUSE-APP

### Scanner Now Checks Readiness Before Scanning

**Summary**
- The app waits for scanner readiness before scanning, so first tries stop failing.

**Problem**
- Scans sometimes failed when the scanner wasn't ready yet, forcing staff to retry.

**Change**
- The app now shows a "Ready" status before allowing scans on the Stock Lookup screen.
- If the scanner isn't responding, the app retries automatically instead of failing.

**Impact**
- Fewer failed scans and retries during busy shifts.

**Scope**
- Stock Lookup screen in WAREHOUSE-APP.

**Manual QA Steps**
Setup: local test build, warehouse tester account, test asset, and test scanner.
Status: proposed checks, not executed.

1. Open Stock Lookup and start a scan -> "Ready" appears before scanning begins.
2. Scan immediately after opening the app -> The app waits for scanner readiness.
3. Disconnect and reconnect the test scanner -> The next scan retries and recovers.

**Commits Included**
- abc1234
- def5678
- ghi9012
- jkl3456

### Support Teams Can View Partner Activity Logs

(Each additional feature under the same project heading repeats the full
feature block — Summary through Commits Included.)

## Example 2: Bad vs Good (Writing Style Reference)

This example shows the same work described in bad (verbose/corporate) style vs good (clear/simple) style.

### Bad Output (DO NOT generate like this)

```
### Auth Hardening Workstreams Prepared

**Summary**
- The next round of login and password-handling improvements for the Admin and Portal platforms was formally prepared so implementation can move with a clear scope and QA target.

**Problem**
- Follow-up work was still needed around username casing, password visibility, and stronger password rules across multiple auth flows.
- Without a written design and task breakdown, this type of security-sensitive work is easier to implement inconsistently across products.

**Change**
- Two implementation workstreams were documented and broken down for execution:
- Admin portal follow-up work covering username lowercasing and consistent password show/hide behavior across login, signup, reset, invite, and user-management screens.
- Portal auth hardening covering username lowercasing, stronger password requirements when setting a password, and password show/hide coverage in staff and gallery user-management flows.
- Concrete touchpoints called out in the workstream docs include the signin page, signup flow, reset and force-change password pages, invite flow, staff password screens, and gallery user forms.

**Impact**
- Engineering now has approved-ready implementation notes for sensitive auth work instead of relying on ad hoc fixes.
- This reduces the risk of one screen being fixed while another screen keeps the same login or password-typing problem.
```

### Good Output (Generate like this)

```
### Login and password plan documented

**Summary**
- Documented proposed username and password fixes for Admin and Portal apps.

**Problem**
- "John" and "john" were treated as different accounts.
- Some password fields had a show/hide toggle, others didn't.

**Change**
- Wrote a plan for lowercase usernames, password visibility, and stronger password rules.
- Named the login, signup, reset, invite, and user-management pages needing changes.

**Impact**
- Reviewers can check the proposed behavior before coding starts; app behavior is unchanged.
```

### What makes the good version better
- Feature name says what changed ("Login and Password Improvements") not how ("Auth Hardening Workstreams")
- Problem describes what the user experienced, not what the code lacked
- Each bullet is one short sentence
- No jargon: no "workstreams", "touchpoints", "ad hoc", "formally prepared"
- A PM can read it in 10 seconds and know exactly what's happening

## Example 3: Feature Summary

### User Request
Write release notes for the RFID scanning improvements

### Example Output
## WAREHOUSE-APP

### RFID Scanning Improvements

**Summary**
- RFID workflows now follow a more consistent scan startup process.

**Problem**
- Scan attempts could fail when startup steps were incomplete in certain flows.

**Change**
- The app now runs the same setup steps before every scan.
- Added readiness checks and controlled retry handling.
- What changed where: RFID scan pages and scan action controls used by front-line teams.
- Simple logic explanation: The app runs the same scanner setup checklist every time.

**Impact**
- Fewer startup-related scan failures.
- More reliable scanning for front-line teams during daily work.

**Scope**
- Applies to RFID scanning flows covered by this feature.
