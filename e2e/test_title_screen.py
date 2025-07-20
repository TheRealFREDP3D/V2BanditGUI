import time

from playwright.sync_api import sync_playwright

BANDIT_MARKER = "BANDIT TITLE SCREEN LOADED"

def test_bandit_title_screen():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://localhost:8000")
        # Wait for the terminal to appear
        page.wait_for_selector("#terminal")
        # Wait for the WebSocket and some output to appear
        time.sleep(3)  # Wait for animation and output
        # Get the terminal's visible text
        terminal_text = page.inner_text("#terminal")
        assert BANDIT_MARKER in terminal_text, "Bandit title screen not found in terminal output!"
        browser.close() 