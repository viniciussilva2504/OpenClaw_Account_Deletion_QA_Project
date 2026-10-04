# OpenClaw / ClawBro Account Deletion – QA Reproduction

A small, evidence-driven QA project documenting and reproducing a user-facing defect observed in the account deletion flow shown in the attached recording.

> **Important:** this repository does not claim to identify the server-side root cause. It documents a black-box failure: after entering the correct account email in the deletion confirmation dialog, clicking **Delete Account** produced no observable transition in the recorded session.

## Bug at a glance

**Title:** Account deletion action does not complete after valid email confirmation  
**Category:** Functional / Account lifecycle / Account management  
**Proposed severity:** High – user-requested account deletion is blocked  
**Affected surface observed in evidence:** `https://clawbro.ai/pt/dashboard`  
**Evidence:** `evidence/account-deletion-reproduction-redacted.mp4` and screenshots in `evidence/screenshots/`

### Reproduction flow

1. Sign in to the account.
2. Open the **Account** settings page.
3. Scroll to **Danger Zone**.
4. Click **Delete Account**.
5. Enter the account email into **TYPE YOUR EMAIL TO CONFIRM**.
6. Click **Delete Account** in the confirmation modal.
7. Observe that the deletion flow does not complete and the modal remains visible in the recording.

### Expected

A valid confirmation should submit the deletion request and the UI should transition to the documented success state, such as account deletion confirmation, sign-out, redirect, or another explicit completion state.

### Actual

The confirmation action does not complete in the recorded session. The modal remains open and there is no visible success/redirect state.

## Automated reproduction

The Playwright test in `tests/account-deletion.spec.ts` is designed to be **safe to execute against a real authenticated account**: it blocks non-GET requests after the confirmation dialog is ready, so the account cannot actually be deleted. The test observes whether clicking the final button attempts to initiate a same-origin state-changing request.

A healthy implementation should attempt a state-changing request or navigation. The recorded failure is consistent with the absence of an observable deletion transition after the final click.

### Setup

```bash
npm install
npx playwright install chromium
```

Create a local authenticated Playwright storage state. Do not commit it:

```bash
npx playwright codegen --save-storage=auth/session.json https://clawbro.ai/pt/dashboard
```

Log in during the Codegen session, close the browser, then run:

```bash
TEST_ACCOUNT_EMAIL="your-test-email@example.com" \
BASE_URL="https://clawbro.ai" \
AUTH_STATE="auth/session.json" \
npm test
```

The test intentionally intercepts non-GET requests immediately before the destructive action and aborts them after recording the attempt. This prevents accidental deletion of the test account.

## Evidence

The public-safe evidence copy has the account email blurred. The original recording should not be committed to a public repository because it contains personal information.

- `evidence/account-deletion-reproduction-redacted.mp4`
- `evidence/screenshots/frame-01.png` – Account page / Danger Zone
- `evidence/screenshots/frame-03.png` – Delete Account confirmation modal
- `evidence/screenshots/frame-07.png` – Email entered and final button clicked
- `evidence/screenshots/frame-09.png` – DOM inspection of the final button

## Related OpenClaw reporting guidance

OpenClaw's current security/reporting guidance says that ClawHub issues belong in `openclaw/clawhub`, and that `security@openclaw.ai` can route reports when the correct destination is unclear. The ClawHub security policy also treats website/API/authentication issues as platform-level reports. See the sources listed in `docs/sources.md`.

## QA scope

The repository also contains:

- `docs/bug-report.md` – structured report with expected/actual behavior and impact.
- `docs/test-plan.md` – recommended positive, negative, regression, and failure-path coverage.
- `docs/technical-observations.md` – evidence-based observations from the recording, without claiming an unverified root cause.
- `docs/outreach-email.md` – professional outreach message to the product/engineering team.
- `docs/professional-context.md` – concise profile context for presenting the author as a QA/full-stack candidate.
