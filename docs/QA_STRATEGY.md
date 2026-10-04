# QA Strategy: Account Deletion Flow

## Scope and evidence standard

The reported issue is a black-box UI failure in one recorded session: after the account email was entered and the final confirmation button was clicked, the deletion dialog remained visible without an explicit completion state. The recording and redacted frames support that observation. They do not show the HTTP exchange or establish the resulting server-side account state.

Treat this as a functional account-lifecycle defect pending independent reproduction. Keep observed facts, expected behavior, technical hypotheses, and confirmed cause separate. Do not use a real account for destructive regression coverage.

## Prioritized test strategy

| Priority | Area | Strategy | Pass evidence |
|---|---|---|---|
| P0 | Safety boundary | Run browser tests only on a local harness. Intercept and fulfill the deletion API request; never send it to OpenClaw. Keep live probing opt-in and abort all HTTP methods and destinations before the final action. | Request is handled by the local mock; no OpenClaw host receives a request. |
| P1 | Core functional flow / UI state | Test modal open, valid confirmation, pending/disabled submit state, mocked success, explicit completion, and modal close. | Accessible UI state changes and one correctly shaped mocked request. |
| P1 | Negative testing | Check blank and mismatched email values; final submit stays disabled and no deletion request is produced. | Validation text and zero API calls. |
| P1 | Error handling / retry | Return a simulated service error, assert actionable feedback and recoverable state, then return success on retry. | Error remains visible, submit becomes usable, retry succeeds. |
| P1 | Cancel / lifecycle | Cancel or dismiss the dialog and assert focus returns to the opener with no API call. | Dialog closes, focus is restored, no deletion request. |
| P2 | API validation | Validate client request method, route, content type, and confirmation payload against a local mock contract. Add schema/status tests when an authorized API contract or sandbox is available. | Mock sees one expected request; failures and malformed responses are covered locally. |
| P2 | Accessibility | Check semantic dialog/name, labeled input, focus on open, keyboard dismissal, and focus restoration. Add keyboard tab-order/focus-trap and screen-reader review. | Role/label and keyboard assertions pass; manual assistive-technology review recorded separately. |
| P2 | Regression | Preserve the valid, invalid, cancel, failure, and retry paths as deterministic regression checks. Run across desktop and mobile viewport after a product fix. | Same assertions pass against a product build with destructive endpoint mocked. |
| P3 | Account lifecycle | Against a product-owned sandbox only, validate request acceptance, pending state, sign-out/session invalidation, re-authentication denial, and documented retention/deletion outcomes. | Server-side audit or sandbox state proves lifecycle completion; no production account used. |
| P3 | Resilience | Cover duplicate submission, refresh/back during pending state, timeout, offline, and repeated retry behavior. | At most one operation is accepted and every state has explicit user feedback. |

## Current implementation boundary

`tests/test_account_deletion.py` drives a local HTML contract harness with Playwright for Python. The browser's `/api/account/delete` request is fulfilled by the test itself. This proves that the harness behaves as specified and that the browser automation can validate the contract safely; it does not prove current OpenClaw production behavior.

The TypeScript live probe is opt-in (`RUN_LIVE_PROBE=true`) and aborts all HTTP requests after the confirmation is ready. It observes request intent only. Browser routing is not a substitute for a product-owned sandbox and should not be treated as proof of server-side deletion behavior.

## Entry criteria for product-level regression

- Product owner supplies a non-production environment and disposable test account.
- Documented API contract and expected success/error states are available.
- Deletion endpoint and all alternate deletion paths are identified.
- A verified server-side cleanup/reset process exists.
- Network interception, service-worker handling, and evidence redaction are reviewed before execution.
