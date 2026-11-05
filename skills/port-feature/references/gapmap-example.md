# Filled gap-map bullets — the expected granularity

One example bullet per load-bearing section, at the evidence level the gap map
must have. Placeholders never ship; every claim names its evidence.

## 1. Reference behaviour / workflow

- Approving a transfer moves it `pending → approved` and locks line edits —
  evidence: `application/controllers/Transfers.php:approve()`, route
  `POST /transfers/approve/{id}`, `tests/TransferApprovalTest.php:test_locks_lines`.
- Navigation: lives under Inventory › Transfers (left nav, third group); the
  port implies a new "Approvals" tab on the target's existing Transfers screen.

## 4. Reusable target code & DS components

- `App\Services\StockMovementService` already owns quantity mutations — extend
  it rather than adding a parallel approval writer
  (`app/Services/StockMovementService.php`).
- DS `ConfirmDialog` (component preview § dialogs) fits the approve/reject
  confirmation.

## 6. UI / design gaps vs reference (and forced DS deviations)

- Reference approve control is a green row-inline icon → target DS uses
  `PrimaryButton` in the row-actions slot.
- Forced deviation: reference used a blocking full-page confirm; target DS
  does `ConfirmDialog` modals — chose DS per the target's design-system doc
  (Dialogs § confirmation).

## 8. First slice

- Approve a single pending transfer end-to-end (list → approve → status +
  line-lock verified) behind the existing permission — demoable on its own;
  rejection, bulk actions, and notifications stay later slices.
