from patchright.sync_api import sync_playwright
import os

def run():
    edge_path = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    user_data_dir = os.path.expanduser("~/Library/Application Support/Microsoft Edge")

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir=user_data_dir,
            executable_path=edge_path,
            headless=False,
            no_viewport=True,
            args=[
                "--disable-blink-features=AutomationControlled",  # reduce detection
            ]
        )

        page = browser.pages[0]
        page.goto("https://bot.sannysoft.com", wait_until="networkidle")

        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    run()
