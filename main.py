from patchright.sync_api import sync_playwright
import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()  # Load .env

def sanitize_cookies(raw_cookies):
    for cookie in raw_cookies:
        cookie.pop("id", None)
        cookie.pop("storeId", None)
        cookie.pop("hostOnly", None)
        cookie.pop("session", None)
        if cookie.get("sameSite") not in ["Strict", "Lax", "None"]:
            cookie["sameSite"] = "Lax"
    return raw_cookies

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
                "--disable-blink-features=AutomationControlled",
                "--disable-infobars",
            ],
        )

        page = browser.pages[0]

        with open("cookies.json", "r") as f:
            raw_cookies = json.load(f)

        cookies = sanitize_cookies(raw_cookies)
        browser.add_cookies(cookies)

        page.goto("https://www.carousell.com.hk/inbox", wait_until="domcontentloaded")
        if "inbox" not in page.url:
            print("Warning: Inbox page may not have loaded correctly.")
        # page.evaluate("document.body.style.zoom = '0.9'")
        
        required_classes = [
        'D_lm', 'D_ln', 'D_lr', 'D_lu', 'D_lx', 'D_l_', 'D_arx', 'D_lJ'
        ]
        class_condition = " and ".join([f"contains(@class, '{cls}')" for cls in required_classes])
        badge_xpath = f'//span[{class_condition} and string(number(normalize-space(text()))) != "NaN"]'
        
        try:
            page.wait_for_selector(badge_xpath, timeout=10000)
        except TimeoutError:
            print("Timeout: No badge found within the wait period.")
            return
        
        badge = page.locator(badge_xpath)

        if badge:
            print("Unread notification found")
            button = badge.evaluate_handle("node => node.closest('[role=\"button\"]')")
            if button:
                try:
                    button.click()
                except Exception as e:
                    print(f"Failed to click button: {e}")
                    return

                # Wait for real messages
                required_classes = [
                    'D_lm', 'D_ln', 'D_ls', 'D_lq', 'D_lu', 'D_lx', 'D_lz', 'D_ctB', 'D_cts', 'D_lH'
                ]
                class_condition = " and ".join([f"contains(@class, '{cls}')" for cls in required_classes])
                xpath = f'//div[starts-with(@id, "chat-message-")]//p[{class_condition}]'

                try:
                    page.wait_for_selector(xpath, timeout=10000)
                except TimeoutError:
                    print("Timeout: No messages found within the wait period.")
                    return
                
                count = page.locator(xpath).count()
                print(f"Found {count} messages")

                message_blocks = page.locator(xpath).all()

                if message_blocks:
                    for msg in message_blocks:
                        print(msg.inner_text().strip())
                else:
                    print("No message blocks found.")

            else:
                print("Parent button not found")
        else:
            print("No unread notifications")





        # page.screenshot(path="inbox.png")

        # coords = detect_notification_coords("inbox.png")
        # if coords is None:
        #     print("No unread notifications found.")
        # else:
        #     x, y = int(coords["x"]), int(coords["y"])
        #     print(f"Badge found at ({x}, {y})")
        #     page.evaluate(f"""
        #         const marker = document.createElement('div');
        #         marker.style.position = 'absolute';
        #         marker.style.left = '{x}px';
        #         marker.style.top = '{y}px';
        #         marker.style.width = '12px';
        #         marker.style.height = '12px';
        #         marker.style.backgroundColor = 'red';
        #         marker.style.borderRadius = '50%';
        #         marker.style.zIndex = 9999;
        #         marker.style.boxShadow = '0 0 5px black';
        #         marker.style.pointerEvents = 'none';
        #         document.body.appendChild(marker);
        #     """)

        #     page.mouse.click(x, y)
        #     print(f"Badge clicked at ({x}, {y})")

        # if coords is not None:
        #     x, y = int(coords["x"]), int(coords["y"])
        #     page.mouse.click(x, y)
        #     print(f"Badge clicked at ({x}, {y})")
        # else:
        #     print("No unread notifications found.")
        #     browser.close()

        # x, y = int(coords["x"]), int(coords["y"])

        # page.evaluate(f"""
        #     const marker = document.createElement('div');
        #     marker.style.position = 'absolute';
        #     marker.style.left = '{x}px';
        #     marker.style.top = '{y}px';
        #     marker.style.width = '12px';
        #     marker.style.height = '12px';
        #     marker.style.backgroundColor = 'red';
        #     marker.style.borderRadius = '50%';
        #     marker.style.zIndex = 9999;
        #     marker.style.boxShadow = '0 0 5px black';
        #     marker.style.pointerEvents = 'none';
        #     document.body.appendChild(marker);
        # """)

        # # page.mouse.click(x, y)
        # print(f"Badge clicked at ({x}, {y})")

        input("Press Enter to close browser...")
        browser.close()

if __name__ == "__main__":
    run()