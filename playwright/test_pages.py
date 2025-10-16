# Playwright test skeleton - requires Playwright to be installed and browsers to be installed via `playwright install`

try:
    from playwright.sync_api import sync_playwright
except Exception:
    sync_playwright = None


def test_pages_basic():
    if sync_playwright is None:
        import pytest

        pytest.skip("Playwright not installed")

    import os

    pages_url = os.getenv("PAGES_URL")
    if not pages_url:
        import pytest

        pytest.skip("PAGES_URL not set")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(pages_url)
        assert page.status == 200
        # placeholder: check that page has at least one element
        assert page.query_selector("body") is not None
        browser.close()
