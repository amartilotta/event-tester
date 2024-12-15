
from playwright.sync_api import sync_playwright


def test_56676925_6e55_4072_98db_ca544bd3dbb5():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.locator(".flex.items-center.justify-between").click()
        page.locator(".flex.w-full.h-full.items-center.transition-transfo...").click()
        page.locator(".flex.w-full.items-center.rounded-md.border-transpa...").click()
        browser.close()

