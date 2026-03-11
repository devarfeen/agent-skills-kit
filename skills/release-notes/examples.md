# Examples

## Example 1: Date-Based Release Notes

### User Request
Generate release notes for 11 March 2026

### Example Input
- fix: RFID power initialization
- fix: retry RFID reader setup
- fix: prevent scan before reader ready
- feat: verify scanner power before lookup

### Example Output
## Partners App

### RFID Lookup Reliability Improvements

**Summary**
- RFID-enabled workflows now start scans more consistently, reducing retries during daily operations.

**Problem**
- Warehouse teams saw inconsistent scan starts, especially during busy lookup periods.
- Failed first attempts caused repeat actions and slowed task completion.

**Change**
- Standardized how scanning is prepared before each RFID lookup.
- Added readiness checks so the app starts scans only when the scanner is ready.
- Added controlled retry behavior when the scanner is temporarily unavailable.

**Impact**
- Fewer failed first-scan attempts in lookup workflows.
- Less operator rework caused by scanner startup timing.
- More predictable throughput during high-volume tag reads.

**Scope**
- Applies to RFID-enabled stock lookup operations in Partners App.

## Example 2: Single Project on a Date

### User Request
Generate release notes for Partners App on 11 March

### Example Output
## Partners App

### Stock Lookup Stability Improvements

**Summary**
- Stock lookup scans now behave more consistently across shifts.

**Problem**
- Stock teams experienced failed lookups when scans started before setup finished.

**Change**
- Standardized the startup sequence for lookup scanning.
- Added readiness validation before processing lookup scans.

**Impact**
- Fewer interrupted lookup tasks.
- Lower scan failure rates tied to startup timing.
- More predictable operator experience during stock checks.

**Scope**
- Affects stock lookup workflows in Partners App.

## Example 3: Session Summary

### User Request
Summarize today's development session

### Example Output
## Partners App

### RFID Setup and Scan Flow Improvements

**Summary**
- RFID scanning now starts with a consistent setup path across this session's updates.

**Problem**
- Teams faced uneven scan behavior when setup and validation steps varied by flow.

**Change**
- Introduced one shared scanner preparation process before RFID actions.
- Added validation and retry safeguards for scanner readiness.

**Impact**
- More consistent scan starts across updated workflows.
- Fewer repeat attempts due to setup timing issues.
- Higher confidence for teams using RFID-heavy screens.

**Scope**
- Covers RFID-related workflows updated during the development session.

## Example 4: Feature-Based Summary

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

**Impact**
- Fewer startup-related scan failures.
- Reduced operational interruptions in RFID workflows.
- More reliable scan behavior for front-line users.

**Scope**
- Applies to RFID scanning flows covered by this feature.
