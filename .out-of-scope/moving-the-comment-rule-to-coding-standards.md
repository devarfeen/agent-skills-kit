# Moving the comment rule out of the generated AGENTS.md

The comment rule stays among the non-negotiable rules that `/agents-md`
generates.

## Why this is out of scope

Upstream `retro` argues that review-enforceable standards belong in a
`CODING_STANDARDS.md` read by `/code-review`, not in always-loaded context. The
kit adopted the pointer: judgement-call findings from `/retro` go to that file.
It did not move the existing comment rule, because that would remove it from
implementation-time context in every generated workspace, including ones with
no review step and no standards file. Revisit per workspace, not in the
template.
