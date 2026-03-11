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

**Problem**
- RFID scans could start before the reader was fully ready, causing inconsistent results.

**Change**
- Added a shared RFID setup flow before scans begin.
- Scanner power is now set and verified before lookup starts.
- Added retry handling when hardware is not yet ready.

**Impact**
- More reliable RFID scan results
- Fewer scan failures
- Better performance in dense tag environments

## Example 2: Single Project on a Date

### User Request
Generate release notes for Partners App on 11 March

### Example Output
## Partners App

### Stock Lookup Stability Improvements

**Problem**
- Some stock lookup flows were failing when scanner setup was incomplete.

**Change**
- Improved the initialization sequence before lookups begin.
- Added checks to ensure scanner readiness before processing.

**Impact**
- More stable stock lookup workflow
- Reduced failed scans
- Improved consistency for users

## Example 3: Session Summary

### User Request
Summarize today's development session

### Example Output
## Partners App

### RFID Setup and Scan Flow Improvements

**Problem**
- RFID scan behavior was inconsistent due to setup timing and missing validation.

**Change**
- Introduced a shared setup process used before scan operations.
- Added validation and retry handling to improve scan readiness.

**Impact**
- More predictable RFID scanning
- Better reliability during lookup flows
- Reduced need for repeated scan attempts

## Example 4: Feature-Based Summary

### User Request
Write release notes for the RFID scanning improvements

### Example Output
## Partners App

### RFID Scanning Improvements

**Problem**
- RFID scanning was unreliable in some cases because initialization steps were not always completed before scanning.

**Change**
- Standardized scanner setup before scans begin.
- Added readiness checks and retry handling.

**Impact**
- More consistent scan performance
- Fewer operational failures
- Improved user confidence in lookup workflows
