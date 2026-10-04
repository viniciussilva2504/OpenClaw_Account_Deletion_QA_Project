# Test Plan: Account Deletion Flow

## Preconditions

- Automated local checks require Python, `pytest`, `pytest-playwright`, and a Playwright Chromium installation.
- Local browser tests serve only `tests/fixtures/account-delete-flow.html` on loopback.
- All deletion API calls in these tests are intercepted and answered by a local mock.
- No OpenClaw credentials, storage state, or production URL are required.

## Test cases

| ID | Scenario | Expected result | Automated status |
|---|---|---|---|
| AD-01 | Open deletion dialog | Named dialog appears and email field receives focus | Covered locally |
| AD-02 | Empty confirmation | Submit remains disabled, validation is shown, no request occurs | Covered locally |
| AD-03 | Mismatched email | Submit remains disabled, mismatch is shown, no request occurs | Covered locally |
| AD-04 | Valid email and submit | One POST with confirmation payload is fulfilled by the mock; explicit success is shown | Covered locally |
| AD-05 | Cancel | Dialog closes, focus returns to opener, no request occurs | Covered locally |
| AD-06 | API returns service error | Actionable error appears, dialog remains recoverable, retry can succeed | Covered locally |
| AD-07 | Keyboard dismissal | Escape closes the dialog and restores focus | Covered locally |
| AD-08 | Pending submit state | Submit becomes disabled while the mocked request is pending and returns to a terminal state after response | Covered locally |
| AD-09 | Duplicate submission | At most one deletion operation is accepted across repeated user input | Planned; not yet covered |
| AD-10 | Timeout/offline/malformed response | Clear recoverable state and no false success | Planned; not yet covered |
| AD-11 | Product account lifecycle | Session invalidation and resulting account state are verified in a product-owned sandbox | Blocked pending sandbox/API contract |

## Run locally

```bash
python -m pip install -r requirements-test.txt
python -m playwright install chromium
python -m pytest -q tests/test_account_deletion.py
```

The legacy TypeScript browser suite is separate and runs with `npm test`. Its real-product probe is skipped unless explicitly opted in and supplied with authenticated storage state and an account email. Do not share credentials with the test author or commit storage state.

## Evidence and result handling

Pytest reports pass/fail/skip counts in the terminal. Playwright traces/screenshots are not enabled for the Python suite by default; no evidence artifacts are expected on a passing run. For failures, capture a redacted screenshot/trace from the local harness only. Never attach a real account email, auth state, or original unredacted recording to public artifacts.
