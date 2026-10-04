# Automated test

`account-deletion.spec.ts` is a black-box safety test for the final confirmation step.

It does **not** delete the account. It intercepts same-origin non-GET requests and aborts them after recording that the application attempted a state-changing operation.

A healthy implementation should attempt such an operation after the correct email is supplied. The reported failure is detected when no such request is initiated after the final click.
