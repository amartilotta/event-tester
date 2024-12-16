from playwright.sync_api import sync_playwright


def test_56676925_6e55_4072_98db_ca544bd3dff5():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.locator(".h-4").click()
        browser.close()
