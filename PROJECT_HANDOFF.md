# OpenClaw QA Bug Report – Complete Handoff

**Created:** 2026-10-04  
**Purpose:** Provide a GitHub-ready QA portfolio artifact documenting a reproducible account-deletion defect, a safe automation strategy, evidence, and professional outreach context.

---

## 1. Background

While evaluating OpenClaw / the ClawBro web interface, the reporter exercised a broad range of functionality, including agent-related workflows and API-facing interactions. During a later attempt to cancel the account, a defect was identified in the account-deletion flow.

The important QA point is that the issue was discovered during exploratory use rather than through a pre-existing report, then reproduced, recorded, and inspected with browser developer tools.

---

## 2. Reported defect

### Title

**Account deletion action does not complete after valid email confirmation**

### Category

Functional defect / Account lifecycle / Account management

### Proposed severity

**High** – the user-requested account deletion workflow is blocked.

### Observed surface

`https://clawbro.ai/pt/dashboard`

### Preconditions

- Authenticated user account.
- Access to Account settings.
- Known account email address.

### Steps to reproduce

1. Open Account settings.
2. Locate the **Danger Zone** section.
3. Click **Delete Account**.
4. Enter the account email in **TYPE YOUR EMAIL TO CONFIRM**.
5. Click the final **Delete Account** button.

### Expected result

The valid confirmation should initiate the account-deletion workflow and produce an explicit completion state such as successful deletion, sign-out, redirect, or a clear actionable error.

### Actual result

In the recorded session, the final confirmation click did not produce a visible completion state. The dialog remained open and the account was not taken through a successful deletion flow.

### User impact

- Blocks an important account lifecycle operation.
- Prevents the user from completing a deliberate account deletion request.
- Creates uncertainty around account/data-control state.

No exploit or server-side data exposure was established by the evidence. The issue should therefore be presented as a high-impact functional/account-management defect rather than an unverified security vulnerability.

---

## 3. Evidence reviewed

The original recording is approximately 90 seconds and was provided as:

`Open_Claw_Accont_Delete_Bug.mp4`

For public GitHub use, a redacted copy was created because the original recording visibly contains the account email.

### Public-safe evidence included

- `evidence/account-deletion-reproduction-redacted.mp4`
- `evidence/screenshots/frame-01.png` – Account page and Danger Zone.
- `evidence/screenshots/frame-03.png` – Delete Account confirmation modal.
- `evidence/screenshots/frame-07.png` – Correct email populated and final Delete Account interaction.
- `evidence/screenshots/frame-09.png` – DevTools Elements inspection of the final button.

### Technical observation

The captured DevTools DOM shows a native `<button>` containing `Delete Account`. Tailwind-style `disabled:` utility classes are visible in the class list, but a literal HTML `disabled` attribute was not visible in the captured snippet.

This is an observation only. The root cause is not established. Further investigation would require network traces, runtime logs, and/or source-level analysis.

---

## 4. Recommended technical investigation

1. Verify client-side confirmation state after the correct email is supplied.
2. Inspect the click handler and the validation condition guarding deletion.
3. Confirm whether a same-origin state-changing request is initiated after the final click.
4. If a request is sent, inspect its status and response handling.
5. Validate authorization and server-side deletion logic.
6. Add automated regression coverage for the positive and negative confirmation paths.
7. Add explicit UI feedback for both success and failure.

---

## 5. Automated QA approach

The repository contains a Playwright test that is intentionally safe for a real authenticated account.

The strategy is:

- navigate to the account page;
- open the deletion dialog;
- enter the valid account email;
- intercept same-origin non-GET requests immediately before the destructive action;
- click Delete Account;
- record any state-changing request attempt;
- abort the request so the real account cannot be deleted.

A healthy implementation should attempt a state-changing operation. The reported failure is detected when no such request is initiated after the final click.

A deterministic local fixture is also included so the testing logic can be demonstrated without touching production.

---

## 6. QA test coverage recommended

- Open Danger Zone.
- Open deletion modal.
- Empty confirmation input.
- Incorrect email.
- Correct email.
- Correct email + final click.
- Cancel modal.
- Network/server failure.
- Double-click / duplicate submission.
- Refresh or interruption during deletion.
- Responsive/mobile layout.
- Keyboard accessibility and focus management.

---

## 7. Professional profile used for outreach

The reporter is positioning this artifact as evidence of an early-career QA profile:

- Full-Stack Python developer.
- QA Engineering graduate from TripleTen.
- Currently studying Systems Analysis and Development at FIAP.
- Based in Portugal.
- Practical QA experience with manual testing, test case design/execution, functional/regression/exploratory testing, Cypress E2E, Postman REST API testing, SQL/data validation, defect reporting, Python, Git/GitHub and CI/CD.
- Additional operational experience with data validation, ticket/incident handling, anomaly detection, technical documentation and quality control.

The intended professional areas are:

**QA / QA Analyst / Software Testing / AI Validation / AI Data Quality / related entry-level technical roles.**

---

## 8. Outreach message

**Subject: Reproducible Account Deletion Defect – OpenClaw / ClawBro**

Hello OpenClaw Team,

I am writing to report a reproducible issue I encountered in the account cancellation/deletion flow.

While testing OpenClaw, I exercised a broad range of the platform's functionality, including agent-related workflows and API-facing interactions. During that process, I identified several behavioural issues related to the agents, and while attempting to cancel my own account after deciding not to continue using the platform, I identified another reproducible defect in the account management flow.

### Issue: Account cancellation action does not complete after email confirmation

The issue occurs during the account cancellation/deletion process. After entering the account email in the confirmation dialog, the final Delete Account action does not complete the deletion flow.

I recorded the complete interaction and attached a redacted reproduction video so your team can review the behaviour directly.

From a QA perspective, this appears to be a functional defect in the account lifecycle flow because the expected user journey cannot be completed. I have documented the expected and actual behaviour, impact, environment, and suggested investigation areas in the accompanying bug report.

I am reporting this because reproducible defects are much more useful when they are documented clearly and routed to the appropriate engineering team rather than treated only as a support complaint.

### A little about me

I am based in Portugal and am building my career in Quality Assurance and software testing. I am a Full-Stack Python developer, a graduate of the TripleTen QA Engineering program, and I am currently studying Systems Analysis and Development at FIAP.

My practical QA experience includes manual testing, test case design and execution, functional and exploratory testing, E2E automation with Cypress, REST API testing with Postman, SQL/data validation, defect reporting, Python, Git/GitHub, and CI/CD.

What particularly interests me about OpenClaw is the intersection between software quality, AI agents, automation, and complex user-facing systems. I naturally tend to test beyond the happy path, investigate unexpected behaviour, and document reproducible failures, which is how I identified this issue in the first place.

I would also like to take this opportunity to say that I would be genuinely interested in contributing to OpenClaw professionally. If your team has opportunities in QA, QA Analysis, Software Testing, AI Validation, AI/Data Quality, or related entry-level technical roles, I would be very interested in being considered.

I believe the way I approached this issue—identifying it while independently testing the product, reproducing the behaviour, inspecting the affected UI, and documenting the failure—is representative of the kind of contribution I would like to bring to a technical team.

Thank you for taking the time to review the report and recording.

Kind regards,
Vinicius Jesus da Silva
Portugal
Full-Stack Python Developer | QA Analyst
LinkedIn: linkedin.com/in/vjsilva2504
GitHub: github.com/viniciussilva2504
Portfolio: portfolio-ebon-nine-95.vercel.app

---

## 9. Official reporting context consulted

OpenClaw's current documentation says security reports should be directed to the repository where the issue lives, and that `security@openclaw.ai` can route reports when the correct destination is unclear. The ClawHub security policy also covers issues affecting its website, API, authentication, authorization and other platform components.

Public account-lifecycle issues in ClawHub also show that account deletion/authentication workflows have previously produced high-priority user-facing bugs. Those reports were reviewed for context only and do not establish the root cause of this specific defect.

Sources:

- https://github.com/openclaw/openclaw/security
- https://github.com/openclaw/openclaw/blob/main/CONTRIBUTING.md
- https://github.com/openclaw/clawhub/blob/main/SECURITY.md
- https://github.com/openclaw/clawhub/issues/1267
- https://github.com/openclaw/clawhub/issues/1452
- https://github.com/openclaw/clawhub/issues/2025

---

## 10. Accuracy and privacy notes

- The repository does not claim to have established the root cause.
- The public evidence copy redacts the reporter's account email.
- The original recording should not be committed to a public GitHub repository.
- The live automated test is designed to abort state-changing requests so it cannot intentionally delete a real account.
