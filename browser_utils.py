from patchright.sync_api import sync_playwright
import os

def launch_edge_persistent_context(edge_path=None, user_data_dir=None):
    if not edge_path:
        edge_path = "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"
    if not user_data_dir:
        user_data_dir = os.path.expanduser("~/Library/Application Support/Microsoft Edge")

    playwright = sync_playwright().start()
    browser = playwright.chromium.launch_persistent_context(
        user_data_dir=user_data_dir,
        executable_path=edge_path,
        headless=False,
        no_viewport=True,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--disable-infobars",
        ],
    )
    return browser, playwright