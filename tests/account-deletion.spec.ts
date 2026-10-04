import { test, expect } from '@playwright/test';

/**
 * Safe black-box reproduction.
 *
 * Opt-in black-box probe. After the valid confirmation is ready, it aborts
 * every HTTP request (all methods and origins) before it can reach a server.
 * This observes request intent only; it cannot establish successful deletion.
 */
test('AD-06 - valid email should initiate the account deletion workflow', async ({ page }) => {
  test.skip(process.env.RUN_LIVE_PROBE !== 'true', 'Set RUN_LIVE_PROBE=true to opt in to the guarded live probe.');
  test.skip(!process.env.AUTH_STATE, 'Set AUTH_STATE to an authenticated Playwright storage state.');
  test.skip(!process.env.TEST_ACCOUNT_EMAIL, 'Set TEST_ACCOUNT_EMAIL to the authenticated test account email.');

  const attemptedRequests: Array<{ method: string; url: string }> = [];

  await page.goto('/pt/dashboard', { waitUntil: 'domcontentloaded' });

  await page.getByRole('button', { name: /^Delete Account$/ }).first().click();

  const dialog = page.getByRole('heading', { name: /^Delete Account$/ }).locator('..');
  await expect(dialog).toBeVisible();

  const inputs = dialog.locator('input');
  await expect(inputs).toHaveCount(1);
  await inputs.fill(process.env.TEST_ACCOUNT_EMAIL!);

  // Fail closed after the confirmation value is entered. Blocking every
  // HTTP method and destination also catches APIs that use GET or another
  // origin. The config blocks service workers so page routing can observe
  // requests initiated by the page.
  await page.route('**/*', async (route) => {
    const request = route.request();
    attemptedRequests.push({ method: request.method(), url: request.url() });
    await route.abort();
  });

  const finalDeleteButton = page.getByRole('button', { name: /^Delete Account$/ }).last();
  await expect(finalDeleteButton).toBeVisible();
  await finalDeleteButton.click();

  await page.waitForTimeout(1500);

  expect(
    attemptedRequests.length,
    `No HTTP request was observed after clicking Delete Account.\nObserved requests: ${JSON.stringify(attemptedRequests, null, 2)}`,
  ).toBeGreaterThan(0);
});
