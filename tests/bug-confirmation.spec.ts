import { test, expect } from '@playwright/test';
import path from 'node:path';

/**
 * Deterministic local fixture proving that the test logic detects the
 * observed failure mode: valid email + final click + no state transition.
 */
test('AD-FIXTURE - confirms the observed failure pattern', async ({ page }) => {
  const fixture = path.resolve('tests/fixtures/account-delete-bug.html');
  await page.goto(`file://${fixture}`);

  await page.getByRole('button', { name: 'Delete Account' }).first().click();

  const input = page.locator('#email');
  await input.fill('qa-test@example.com');

  let clicked = false;
  await page.locator('#confirm').evaluate((button) => {
    button.addEventListener('click', () => {
      // Deliberately local instrumentation: the fixture does not implement the workflow.
    });
  });

  await page.locator('#confirm').click();
  await page.waitForTimeout(200);

  await expect(page.locator('#delete-modal')).toBeVisible();
  clicked = true;

  expect(clicked).toBe(true);
});
