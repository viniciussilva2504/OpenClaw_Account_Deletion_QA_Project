# Automated tests

## Python local contract tests

`test_account_deletion.py` uses Playwright for Python against `fixtures/account-delete-flow.html`, a local test harness. Every `/api/account/delete` request is intercepted and fulfilled by the test. These tests do not access OpenClaw and do not prove production behavior.

Run with:

```bash
python -m pytest -q tests/test_account_deletion.py
```

## Optional TypeScript live diagnostic

`account-deletion.spec.ts` is explicitly opt-in with `RUN_LIVE_PROBE=true` plus an authenticated Playwright state and account email. It aborts all HTTP requests after confirmation is entered. It only observes request attempts and is not a deletion regression test or proof of successful deletion. Never use real-account execution as a destructive test.

`bug-confirmation.spec.ts` checks the click and persistent modal in an inert local fixture; it is a failure-pattern demonstration, not coverage of the product implementation.
