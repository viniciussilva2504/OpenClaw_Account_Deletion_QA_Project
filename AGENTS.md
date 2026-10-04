# OpenClaw Account Deletion QA Project

## Project Context

This repository documents and tests a reproducible account-deletion/cancellation defect observed in the OpenClaw product.

The project was created by Vinicius Jesus da Silva, a Portugal-based Full-Stack Python developer transitioning into professional QA.

### Professional profile

- Full-Stack Python developer
- QA Engineering graduate: TripleTen
- Systems Analysis and Development student: FIAP
- Practical QA experience with:
  - Manual testing
  - Test case design and execution
  - Functional testing
  - Regression testing
  - Exploratory testing
  - E2E testing
  - Cypress
  - Postman
  - REST API testing
  - SQL / PostgreSQL
  - Python
  - Git / GitHub
  - GitHub Actions / CI/CD
  - Robot Framework / BDD
  - Defect reporting
  - Data validation

## Main Objective

Produce a technically credible QA case study documenting the OpenClaw account cancellation/deletion defect and provide safe, reproducible automated coverage for the failure pattern.

## Confirmed Bug

During an attempt to cancel/delete the user's OpenClaw account, the account cancellation flow failed after the user entered the required email information.

The attached screen recording is the primary evidence.

Do not invent a backend root cause unless it is demonstrated by evidence.

## Evidence

Relevant files may include:

- `PROJECT_HANDOFF.md`
- `README.md`
- `evidence/`
- `evidence/account-deletion-reproduction-original.mp4`
- `evidence/account-deletion-reproduction-redacted.mp4`
- screenshots and extracted video frames

The original video contains the user's personal email address.

Treat the original recording as private evidence.

Never publish or upload the original video to a public repository unless the user explicitly asks for that.

## Safety Rules

This project must NEVER perform destructive operations against a real OpenClaw account.

Do not:

- delete an account
- modify account data
- submit irreversible account actions
- send emails automatically
- create GitHub repositories
- configure GitHub remotes
- commit changes
- push changes

unless the user explicitly requests the specific action.

Automated tests must use mocks, local fixtures, request interception, or another non-destructive mechanism.

## QA Methodology

When analyzing the defect, distinguish clearly between:

1. Observed behaviour
2. Expected behaviour
3. Reproduction steps
4. Evidence
5. Impact
6. Technical hypotheses
7. Confirmed root cause

Never present a hypothesis as a confirmed root cause.

Use standard QA terminology where appropriate:

- Severity
- Priority
- Preconditions
- Test scenario
- Test case
- Expected result
- Actual result
- Test evidence
- Defect report
- Retest
- Regression
- Functional testing
- Exploratory testing
- API validation
- Data validation
- Account lifecycle

## Engineering Guidelines

Prefer Python and Playwright where appropriate.

Keep automated tests deterministic and safe.

When possible:

- isolate external dependencies
- intercept destructive network requests
- use fixtures
- document expected versus actual behaviour
- produce reproducible test results
- preserve evidence
- avoid unnecessary dependencies

## Source of Truth

Before making significant changes, inspect the relevant project files.

Use:

- `README.md` for project overview
- `PROJECT_HANDOFF.md` for the detailed investigation context
- `evidence/` for screenshots and recordings
- automated tests as the executable representation of the documented behaviour

Do not require every context file to be read for every small change. Read the files relevant to the current task.

## Communication

When reporting findings, be concise and technical.

Separate:

- confirmed facts
- observations
- hypotheses
- recommendations

The project is intended to demonstrate professional QA reasoning rather than merely reproduce a UI failure.
