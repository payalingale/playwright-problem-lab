"""
PL-01 — Duplicate 'Save' buttons
Customer: QA engineer at an HR SaaS team ("PeopleDesk").
Goal: the nightly test must save the NOTIFICATIONS section — and prove it.

Run:  pytest tests/test_pl01_duplicate_buttons.py -v
"""


import re
from playwright.sync_api import expect
import pytest

# STEP 1 — Reproduce. EXPECTED to fail with a strict-mode error. Screenshot it.


@pytest.mark.xfail(reason="Reproduction: generic locator matches 2 buttons", strict=True)
def test_step1_reproduce_strict_mode_error(open_lab_page):
    page = open_lab_page("pl01_settings.html")
    page.get_by_label("Email me the weekly digest").check()
    page.get_by_role("button", name="Save").click()


# STEP 2 — The trap. A teammate "fixes" it with .first. The test goes GREEN.
#          Run it, then look at what was actually saved.
def test_step2_the_first_trap_passes_but_is_wrong(open_lab_page):
    page = open_lab_page("pl01_settings.html")
    page.get_by_label("Email me the weekly digest").check()
    page.locator("#notifications-card").get_by_role("button", name="Save")
    expect(page.locator("#toast")).to_have_text(
        "Settings saved")
    save_notifications = (
        # 1. look at all the boxes (divs)
        page.locator("div")
        # 2. keep only the box that has the "Notifications" heading
        .filter(has=page.get_by_role("heading", name="Notifications"))
        # 3. inside that box, find the "Save" button
        .get_by_role("button", name="Save")
    )


# STEP 3 — YOUR SOLUTION. Replace the pytest.fail lines.
#   Rules: no .first / .nth() / .last, no CSS ids (#notifications-card),
#   no weakening the assertion. Prove the RIGHT data was saved.
def test_step3_save_notifications_correctly(open_lab_page):
    page = open_lab_page("pl01_settings.html")
    page.get_by_label("Email me the weekly digest").check()

    save_notifications = (
        page.locator("div")
        .filter(has=page.get_by_role("heading", name="Notifications"))
        .get_by_role("button", name="Save")
    )
    expect(save_notifications).to_have_count(1)
    save_notifications.click()

    expect(page.locator("#saved-state")).to_contain_text("weekly_digest=true")
