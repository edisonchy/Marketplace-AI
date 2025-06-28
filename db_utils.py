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
        "error": "",
        "messages": messages
    }

    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        print(f"Info saved for chat ID {chat_id} to {file_path}")

def update_db(chat_id, updates, file_path="db.json"):
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