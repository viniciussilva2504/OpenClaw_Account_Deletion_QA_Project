# Bug Report – Account Deletion Confirmation Does Not Complete

## Metadata

| Field | Value |
|---|---|
| Bug type | Functional defect / account lifecycle |
| Proposed severity | High |
| Priority rationale | The user cannot complete a deliberate account-deletion request through the available UI flow. |
| Affected product surface | Account settings / Danger Zone |
| Observed URL | `https://clawbro.ai/pt/dashboard` |
| Browser visible in evidence | Google Chrome |
| OS visible in evidence | Windows |
| Responsive inspection | iPhone SE / `375 x 667` emulation visible in DevTools |
| Evidence recording | `evidence/account-deletion-reproduction-redacted.mp4` |

## Preconditions

- User is authenticated.
- User can access Account settings.
- Account has a known email address.

## Steps to reproduce

1. Open the Account settings page.
2. Locate the **Danger Zone** section.
3. Click **Delete Account**.
4. In the confirmation dialog, enter the authenticated account email in **TYPE YOUR EMAIL TO CONFIRM**.
5. Click the red **Delete Account** button in the modal.

## Expected result

The valid confirmation should initiate the account deletion workflow and provide an explicit completion state, such as successful deletion, sign-out, redirect, or an actionable error explaining why deletion could not proceed.

## Actual result

In the recorded session, the final confirmation click produces no visible completion state. The deletion dialog remains present and the user is not taken through a successful deletion flow.

## Impact

- Blocks a core account lifecycle action.
- Prevents the user from completing an intentional deletion request through the UI.
- Creates uncertainty around account/data-control state.
- Should be treated as a high-impact user-facing workflow defect even though no exploit has been demonstrated.

## Technical observation from captured DevTools state

The recording includes an Elements inspection of the final button. The captured DOM shows a native `<button>` element containing the text **Delete Account** and Tailwind-style `disabled:` utility classes in its class list. A literal HTML `disabled` attribute was not visible in the captured snippet.

This is an observation, not a root-cause conclusion. The failure may involve client-side state, event handling, validation, routing, a blocked request, or another layer of the deletion workflow. Additional network and application logs would be required to establish root cause.

## Evidence map

- `frame-01.png`: Account page with Danger Zone and Delete Account entry point.
- `frame-03.png`: Confirmation dialog with email confirmation field and Delete Account action.
- `frame-07.png`: Account email populated; final Delete Account action is clicked.
- `frame-09.png`: DevTools DOM inspection of the final button.
- `account-deletion-reproduction-redacted.mp4`: full recording with personal email blurred.

## Suggested investigation areas

1. Confirm that the valid email state enables the intended deletion action.
2. Inspect the click handler and the condition that guards submission.
3. Inspect whether the UI sends a state-changing request after the final click.
4. Validate server-side deletion response handling and error propagation.
5. Add automated coverage for the account-deletion happy path and invalid confirmation path.
6. Add a regression test preventing the control from becoming permanently non-functional after valid input.
