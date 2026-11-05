# Behavioral evaluation

Date: 2026-09-09. Method: independent simulated execution of the three cases in `audit-behavior-cases.md`, with a fresh hypothetical fixture per case. Produced excerpts and action traces describe hypothetical gap maps; they are not proof of an actual product repository trace, preview visit, or disk write by the port workflow. No product files or external applications were changed.

Zero attribution: never add or leave co-author, AI, or tool attribution in any output.

## 1. Current decision conflicts with ADR

Fixture: transfer approval is being ported from LEGACY-WEB to ADMIN-WEB. The current user explicitly requires supervisor-only approval. An older target ADR and the reference implementation allow any manager.

Produced action trace: read the old ADR and reference permission condition; preserve the reference behavior as observed evidence; record the current explicit permission decision as the planned target requirement; write only the simulated gap map and stop.

Produced gap-map excerpts:

> Reference behavior: managers can approve (`legacy/transfers.php:approve`). Target gap: the current user requires supervisor-only approval, superseding the older manager rule (`specs/adr/0007-approval.md`). Tests needed: a supervisor can approve; another manager is denied. Risk: the older ADR still describes the previous rule. Open question: update that ADR during the separately requested planning step.

Result: PASS. The simulation distinguishes observed reference behavior, stale documentation, and the user's current decision without editing the ADR or implementation.

## 2. Missing component preview

Fixture: target source includes `components/ConfirmDialog.tsx`; no preview route or local service is configured.

Produced action trace: inspect component source and imports; inventory ConfirmDialog as a candidate; record the absent preview; do not invent `/ui/preview/all` or start a service; continue the evidence-limited gap map.

Produced excerpt:

> Reusable target component: ConfirmDialog (`components/ConfirmDialog.tsx`) accepts a confirmation action. Its rendered states are unverified because no component preview is available. UI gap: confirm the dialog's layout during an authorized later preview check.

Result: PASS. Source inventory remains usable without pretending that visual verification occurred.

## 3. User-edited gap map

Fixture: the existing map says "Keep manager approval" as a hand-edited decision. New source shows supervisors only; the user is away. No current explicit decision resolves the conflict.

Produced action trace: read the existing map, preserve the hand-edited decision verbatim, append the new evidence and unresolved decision under Open questions, and keep all writes confined to the map.

Produced excerpt:

> Open questions: the existing decision says "Keep manager approval", but `legacy/transfers.php:approve` currently requires a supervisor. The old decision is preserved pending direction. Should this port retain the recorded exception or follow current reference behavior?

Result: PASS. Contradicting source does not silently overwrite a recorded user decision.

## Additional review finding

The initial reviewed path `specs/port/<feature-slug>-gapmap.md` could collide when the same feature is ported to different TARGET PROJECT-CODEs in one workspace. The editor added pair verification and a qualified fallback filename at `SKILL.md:68`.

Additional isolated simulation: an existing `approve-transfer-gapmap.md` belongs to LEGACY-WEB to ADMIN-WEB, while the current request targets MOBILE-APP. Produced action: preserve the existing map, use `approve-transfer-LEGACY-WEB-MOBILE-APP-gapmap.md`, and check the resolved file's nine sections. Result: PASS in simulation; actual file creation was not exercised.

## Limits

Three of three authored simulated cases and one added collision simulation passed. Actual multi-project file collision handling, browser/native preview tooling, filesystem preservation, and runtime invocation were not exercised. Aug 21 routing evidence remains historical and was not rerun.
