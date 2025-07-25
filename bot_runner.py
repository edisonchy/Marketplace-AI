from patchright._impl._errors import TimeoutError
import re
from dotenv import load_dotenv
import time
import os

from browser_utils import launch_edge_persistent_context
from cookie_utils import sanitize_cookies, load_cookies
from xpath_selectors import unread_badge_xpath, message_xpath, product_xpath, text_area_xpath, send_button_xpath
from db_utils import save_db, update_db, load_db
from chat_handler import handle_chat

load_dotenv()

website = os.getenv("WEBSITE")

def run():
    browser, playwright = launch_edge_persistent_context()
    page = browser.pages[0]
    cookies = sanitize_cookies(load_cookies())
    browser.add_cookies(cookies)

    try:
        while True:
            page.goto(website, wait_until="domcontentloaded")
            if "inbox" not in page.url:
                print("Warning: Inbox page may not have loaded correctly.")
            
            page.screenshot(path="browser_check.png")

            unread_badge_selector = unread_badge_xpath()

            try:
                page.wait_for_selector(unread_badge_selector, timeout=5000)
            except TimeoutError:
                print("No new unread messages, retrying...")
                time.sleep(10)  # Wait before checking again
                continue

            badge = page.locator(unread_badge_selector)

            if badge:
                print("Unread notification found")
                button = badge.evaluate_handle("node => node.closest('[role=\"button\"]')")
                if button:
                    try:
                        button.click()
                    except Exception as e:
                        print(f"Failed to click button: {e}")
                        continue

                    chat_url = page.url
                    match = re.search(r'/inbox/(\d+)', chat_url)
                    if not match:
                        print("Could not extract chat ID.")
                        continue

                    chat_id = match.group(1)

                    try:
                        page.wait_for_selector(product_xpath(), timeout=10000)
                        product = page.locator(product_xpath()).inner_text().strip()
                        page.wait_for_selector(message_xpath(), timeout=10000)
                        messages = [msg.inner_text().strip() for msg in page.locator(message_xpath()).all()]
                    except TimeoutError:
                        print("Timeout retrieving product or messages.")
                        continue

                    db = load_db()

                    if chat_id not in db:
                        save_db(chat_id, product, messages)
                    else:
                        update_db(chat_id, {"messages": messages})
                    response = handle_chat(chat_id)

                    if response:
                        try:
                            page.wait_for_selector(text_area_xpath(), timeout=10000)
                            page.locator(text_area_xpath()).fill(response)
                            page.wait_for_selector(send_button_xpath(), timeout=10000)
                            page.locator(send_button_xpath()).click()
                            print("Response sent.")
                        except TimeoutError:
                            print("Timeout: could not find input/send button.")
                    else:
                        print("No response generated.")
            else:
                print("No unread notifications.")
            
            # Go back to inbox and wait a bit before next poll
            time.sleep(5)

    except KeyboardInterrupt:
        print("Stopping polling loop.")

    finally:
        browser.close()
        playwright.stop()
