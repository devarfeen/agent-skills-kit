# Finding judgment

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

Judge evidence on the pinned revision, not the number or confidence of reviewers.
Use a fresh session with conversation inheritance disabled and no builder or
discovery role. Supply requirements, applicable instructions, authorization,
revision identity, candidate locations/scenarios/evidence, relevant replies
and missing checks. Withhold producing reviewers' verdicts and confidence.
The PR workflow alone permits its labelled `sequential challenge` fallback;
local review requires independent judgment.

For every candidate, read the cited code and relevant guards/callers. Check
the failure's preconditions and the stated requirement. Run a permitted local
reproduction when useful and feasible; a proposed test is not an executed
failure. Record the command and observed result for executed checks, or the
decisive code/requirement proof and execution limitation for static analysis.

| Disposition | Required basis |
| :--- | :--- |
| Confirmed | A concrete scenario violates a cited requirement or invariant, supported by executed reproduction or decisive code evidence. |
| Rejected | A passing assertion or cited code/requirement disproves the candidate's premise; record the reason. |
| Unresolved | Material evidence, a requirement or a required check is missing; name what would settle it. |
| Advisory | A supported improvement without a demonstrated defect; keep it separate from blocking findings. |

Do not reject a finding merely because the builder disagrees, tests are green
or it is inconvenient to fix. Do not convert uncertainty into a confirmed
defect. An out-of-scope defect remains visible with its evidence and scope
disposition; it grants no permission to expand the implementation. Unsupported
preferences are omitted with a reason, not promoted into advisory requirements.

For duplicates, judge one root cause and retain all contributing IDs. Resolve
conflicting claims against evidence rather than voting. A judge-discovered
defect needs the same scenario and proof as a reviewer finding.

The caller's report records each candidate's disposition, reason, evidence
and materiality. Include failed/missing review axes separately. A judge cannot
waive the PR risk rubric, human approval, acceptance criteria or review caps.
Recheck revision identity before returning; changed inputs invalidate the verdict.
