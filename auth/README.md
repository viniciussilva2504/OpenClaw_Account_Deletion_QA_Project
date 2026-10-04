# Local authentication state

Place a Playwright storage state file here for local reproduction only.

```bash
npx playwright codegen --save-storage=auth/session.json https://clawbro.ai/pt/dashboard
```

Sign in during the Codegen session and then close it. `auth/session.json` is ignored by Git because it may contain active authentication material.
