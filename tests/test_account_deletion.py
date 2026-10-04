"""Browser tests for the local account-deletion contract harness.

All deletion requests are intercepted and fulfilled by the test. This suite
does not navigate to or send requests to OpenClaw/ClawBro.
"""

from __future__ import annotations

import functools
import json
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest
from playwright.sync_api import Page, Route, expect


FIXTURE_DIR = Path(__file__).parent / "fixtures"
MOCK_ENDPOINT = "**/api/account/delete"


class QuietStaticHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        pass


@pytest.fixture
def local_app_url() -> str:
    handler = functools.partial(QuietStaticHandler, directory=str(FIXTURE_DIR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}/account-delete-flow.html"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


@pytest.fixture
def app_page(page: Page, local_app_url: str) -> Page:
    page.goto(local_app_url)
    return page


def open_dialog(page: Page) -> None:
    page.get_by_role("button", name="Delete Account").click()
    expect(page.get_by_role("dialog", name="Delete Account")).to_be_visible()


def test_valid_confirmation_sends_only_mocked_request_and_shows_success(app_page: Page) -> None:
    seen: list[dict[str, object]] = []

    def fulfill_mock(route: Route) -> None:
        request = route.request
        seen.append(
            {
                "method": request.method,
                "url": request.url,
                "content_type": request.headers.get("content-type"),
                "body": json.loads(request.post_data or "{}"),
            }
        )
        route.fulfill(status=200, json={"ok": True})

    app_page.route(MOCK_ENDPOINT, fulfill_mock)
    open_dialog(app_page)
    app_page.get_by_label("Type your email to confirm").fill("qa-test@example.com")
    dialog = app_page.get_by_role("dialog", name="Delete Account")
    confirm = dialog.get_by_role("button", name="Delete Account")
    expect(confirm).to_be_enabled()
    confirm.click()

    expect(app_page.get_by_role("status")).to_contain_text("request completed")
    expect(app_page.get_by_role("dialog")).to_be_hidden()
    assert len(seen) == 1
    assert seen[0]["method"] == "POST"
    assert seen[0]["content_type"] == "application/json"
    assert seen[0]["body"] == {"email": "qa-test@example.com"}
    assert str(seen[0]["url"]).endswith("/api/account/delete")


@pytest.mark.parametrize(
    ("value", "expected_message"),
    [
        ("", "Enter your account email."),
        ("someone-else@example.com", "Email does not match this account."),
    ],
)
def test_empty_or_mismatched_email_is_rejected_without_request(
    app_page: Page, value: str, expected_message: str
) -> None:
    requests: list[str] = []
    app_page.on("request", lambda request: requests.append(request.url))
    open_dialog(app_page)
    email_input = app_page.get_by_label("Type your email to confirm")
    if value == "":
        # Exercise clearing a previously entered value so the UI's input
        # validation handler observes the empty state.
        email_input.fill("previous@example.com")
    email_input.fill(value)

    expect(app_page.get_by_role("dialog").get_by_role("button", name="Delete Account")).to_be_disabled()
    expect(app_page.get_by_role("alert")).to_have_text(expected_message)
    assert not any("/api/account/delete" in url for url in requests)


def test_cancel_closes_dialog_and_restores_focus_without_request(app_page: Page) -> None:
    requests: list[str] = []
    app_page.on("request", lambda request: requests.append(request.url))
    open_dialog(app_page)

    app_page.get_by_role("button", name="Cancel").click()

    expect(app_page.get_by_role("dialog")).to_be_hidden()
    expect(app_page.get_by_role("button", name="Delete Account")).to_be_focused()
    assert not any("/api/account/delete" in url for url in requests)


def test_api_failure_is_visible_and_retry_can_complete(app_page: Page) -> None:
    calls = 0

    def mock_failure_then_success(route: Route) -> None:
        nonlocal calls
        calls += 1
        if calls == 1:
            route.fulfill(status=503, json={"error": "unavailable"})
        else:
            route.fulfill(status=200, json={"ok": True})

    app_page.route(MOCK_ENDPOINT, mock_failure_then_success)
    open_dialog(app_page)
    app_page.get_by_label("Type your email to confirm").fill("qa-test@example.com")
    confirm = app_page.get_by_role("dialog").get_by_role("button", name="Delete Account")
    confirm.click()

    expect(app_page.get_by_role("dialog")).to_be_visible()
    expect(app_page.get_by_role("alert")).to_have_text("Deletion request failed. Please try again.")
    expect(confirm).to_be_enabled()

    confirm.click()
    expect(app_page.get_by_role("status")).to_contain_text("request completed")
    assert calls == 2


def test_pending_state_disables_submit_until_mock_response(app_page: Page) -> None:
    calls = 0

    def fulfill_mock(route: Route) -> None:
        nonlocal calls
        calls += 1
        route.fulfill(status=200, json={"ok": True})

    app_page.route(MOCK_ENDPOINT, fulfill_mock)
    open_dialog(app_page)
    app_page.get_by_label("Type your email to confirm").fill("qa-test@example.com")
    app_page.evaluate(
        """() => {
          window.__qaHoldSubmission = new Promise(resolve => {
            window.__qaReleaseSubmission = resolve;
          });
        }"""
    )
    confirm = app_page.get_by_role("dialog").get_by_role("button", name="Delete Account")
    confirm.click()

    pending_button = app_page.get_by_role("dialog").get_by_role("button", name="Deleting…")
    expect(pending_button).to_be_disabled()
    assert calls == 0
    app_page.evaluate("window.__qaReleaseSubmission()")

    expect(app_page.get_by_role("status")).to_contain_text("request completed")
    assert calls == 1


def test_dialog_has_accessible_name_and_keyboard_dismissal(app_page: Page) -> None:
    opener = app_page.get_by_role("button", name="Delete Account")
    opener.click()
    dialog = app_page.get_by_role("dialog", name="Delete Account")
    expect(dialog).to_be_visible()
    expect(app_page.get_by_label("Type your email to confirm")).to_be_focused()

    app_page.keyboard.press("Escape")

    expect(dialog).to_be_hidden()
    expect(opener).to_be_focused()
