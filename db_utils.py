import os
import json

def load_db(file_path="db.json"):
    """Load existing chat logs from JSON file."""
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_db(chat_id, product, messages, file_path="db.json"):
    """
    Save chat log for a given chat_id including product and messages
    in the format: { chat_id: { "product": ..., "messages": [...] } }
    """
    db = load_db(file_path)
    
    db[chat_id] = {
        "product": product,
        "order_id": "",
        "status": "",
        "purchased_ids": "",
        "error": "",
        "messages": messages
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"Info saved for chat ID {chat_id} to {file_path}")

def update_db(chat_id, updates: dict, file_path="db.json"):
    """
    Update fields for a specific chat_id in the database.
    Only overwrites keys provided in the `updates` dict.
    """
    db = load_db(file_path)

    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found in {file_path}")

    db[chat_id].update(updates)

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"Updated chat ID {chat_id} in {file_path}")

def get_next_redeem_code(file_path="redeem_codes.json"):
    """Retrieve the next available redeem code and update the file."""
    try:
        with open(file_path, "r") as f:
            redeem_data = json.load(f)

        if redeem_data["unused"]:
            redeem_code = redeem_data["unused"].pop(0)
            redeem_data["used"].append(redeem_code)

            with open(file_path, "w") as f:
                json.dump(redeem_data, f, indent=2)

            return redeem_code
        else:
            print("⚠️ No unused redeem codes available.")
            return None
    except (FileNotFoundError, KeyError, json.JSONDecodeError) as e:
        print(f"❌ Error handling redeem codes: {e}")
        return None