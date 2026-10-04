import { test, expect } from '@playwright/test';

/**
 * Safe black-box reproduction.
 *
 * The test blocks non-GET requests after the delete dialog is opened so the
 * real account cannot be deleted. It records whether clicking the final
 * confirmation produces a same-origin state-changing request.
 */
test('AD-06 - valid email should initiate the account deletion workflow', async ({ page }) => {
  test.skip(!process.env.AUTH_STATE, 'Set AUTH_STATE to an authenticated Playwright storage state.');
  test.skip(!process.env.TEST_ACCOUNT_EMAIL, 'Set TEST_ACCOUNT_EMAIL to the authenticated test account email.');

  const attemptedWrites: Array<{ method: string; url: string }> = [];

  await page.goto('/pt/dashboard', { waitUntil: 'domcontentloaded' });

  await page.getByRole('button', { name: /^Delete Account$/ }).first().click();

  const dialog = page.getByRole('heading', { name: /^Delete Account$/ }).locator('..');
  await expect(dialog).toBeVisible();

  const inputs = dialog.locator('input');
  await expect(inputs).toHaveCount(1);
  await inputs.fill(process.env.TEST_ACCOUNT_EMAIL!);

  // Only block writes after the form is ready. This makes the test safe to
  // run against a real authenticated account.
  await page.route('**/*', async (route) => {
    const request = route.request();
    const url = request.url();
    const isSameOrigin = url.startsWith(new URL(page.url()).origin);
    const method = request.method().toUpperCase();

    if (isSameOrigin && !['GET', 'HEAD', 'OPTIONS'].includes(method)) {
      attemptedWrites.push({ method, url });
      await route.abort();
      return;
    }

    await route.continue();
  });

  const finalDeleteButton = page.getByRole('button', { name: /^Delete Account$/ }).last();
  await expect(finalDeleteButton).toBeVisible();
  await finalDeleteButton.click();

  await page.waitForTimeout(1500);

  expect(
    attemptedWrites.length,
    `No same-origin state-changing request was observed after clicking Delete Account.\nObserved requests: ${JSON.stringify(attemptedWrites, null, 2)}`,
  ).toBeGreaterThan(0);
});
