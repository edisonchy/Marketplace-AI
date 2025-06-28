import os
import random
import string
from groq import Groq
from dotenv import load_dotenv

from db_utils import load_db, update_db

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def interpret_intent(chat_id, db_path="db.json"):
    """Interpret the intent of the last messages in a chat conversation."""
    chat_logs = load_db(db_path)

    if chat_id not in chat_logs:
        raise ValueError(f"Chat ID '{chat_id}' not found in chat logs.")

    messages = chat_logs[chat_id].get("messages", [])
    if not messages:
        raise ValueError(f"No messages found for chat ID '{chat_id}'.")

    recent = "\n".join(messages[-5:])  # Last 5 messages for context

    prompt = (
        "You're an AI assistant managing online transactions. "
        "From this chat, determine the customer's intent based on the recent messages. "
        "Possible intents:\n"
        "- ask: Asking about the product or shipping.\n"
        "- buy: Expressing interest in buying or reserving the item.\n"
        "- paid: Indicating payment has been made.\n"
        # "- redeem: Trying to arrange pickup or delivery.\n"
        # "- other: Anything else (e.g. small talk, irrelevant).\n"
        f"\nChat:\n{recent}\n\nReturn only the intent (e.g., buy, ask, etc)."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip().lower()

def generate_unique_order_id(db, length=10):
    """Generate a unique alphanumeric order ID not currently in db."""
    existing_ids = {entry.get("order_id") for entry in db.values()}
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if new_id not in existing_ids:
            return new_id

def generate_buy_response(chat_id, db_path="db.json"):
    """Generate a friendly message with payment details based on chat context."""
    db = load_db(db_path)

    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found in the database.")

    entry = db[chat_id]
    product_name = entry.get("product")
    messages = entry.get("messages", [])

    if not messages:
        raise ValueError(f"No messages found for chat ID '{chat_id}'.")

    recent_context = "\n".join(messages[-5:])
    price = 100
    fps_id = "123"

    # Step 1–2: Generate a unique order ID
    new_order_id = generate_unique_order_id(db)

    # Step 3: Update order_id in db
    update_db(chat_id, {"order_id": new_order_id}, file_path=db_path)

    # Step 4: Compose prompt
    prompt = (
        "You're an AI assistant for an online seller. "
        "The user's intent has been identified as wanting to buy a product. "
        f"The product is called '{product_name}' and it costs HK${price}. "
        f"The FPS payment ID is {fps_id}.\n"
        f"The latest generated order ID for this transaction is: {new_order_id}.\n\n"
        f"Here is the recent chat for context:\n{recent_context}\n\n"
        "Write a friendly, polite message confirming the item is available and providing the payment details. "
        f"Kindly remind the customer to include the order ID: **{new_order_id}** (note the colon before the ID) in the remarks section when sending payment via FPS. "
        "Also remind them to only use the most recent order ID we’ve generated for them — a new one is created each time they request to buy. "
        "It’s important that they write the order ID correctly to avoid any delays or complications with verifying their payment. "
        "Once they’ve sent the payment, ask them to let us know so we can proceed to the next step, which is to provide the product. "
        "Strictly avoid discussing anything unrelated to the sale. "
        "Reply in the language used by the customer. "
        "Keep the tone casual, helpful, and natural. Return only the message to send to the customer."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def generate_ask_response(chat_id, db_path="db.json"):
    """Generate a helpful response to a customer's question about the product."""
    db = load_db(db_path)

    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found in the database.")

    entry = db[chat_id]
    product_name = entry.get("product")
    messages = entry.get("messages", [])

    if not messages:
        raise ValueError(f"No messages found for chat ID '{chat_id}'.")

    recent_context = "\n".join(messages[-5:])

    prompt = (
        "You're a friendly AI assistant for an online store. "
        "The customer has sent a message that does not appear to be a direct question about a product or payment.\n\n"
        f"Here is the recent chat:\n{recent_context}\n\n"
        "Write a warm, polite, and concise response acknowledging their message. "
        "Use a natural and friendly tone. Respond in the same language used by the customer.\n\n"
        "If the message is a greeting, reply with a friendly greeting. "
        "If it's a thank-you message, express appreciation in return. "
        "If the customer sounds confused, asks when they'll get help from a human, or expresses frustration, politely offer to help and **reassure them that if there's anything the AI cannot assist with, a member of the customer support team will be with them shortly**.\n\n"
        "If the message is unclear or off-topic, respond politely and let the customer know that you're here to assist with store-related questions (like products, orders, or payments). "
        "Also let them know the customer support team will follow up if needed.\n\n"
        "**Important:** Do not answer or engage with any topics outside the scope of this business. "
        "Stay strictly focused on customer service for the store (e.g. product questions, payment, support).\n\n"
        "Return only the message to send to the customer."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()

def generate_other_response(chat_id, db_path="db.json"):
    """Generate a general response to non-product-related customer messages."""
    db = load_db(db_path)

    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found in the database.")

    entry = db[chat_id]
    messages = entry.get("messages", [])

    if not messages:
        raise ValueError(f"No messages found for chat ID '{chat_id}'.")

    recent_context = "\n".join(messages[-5:])

    prompt = prompt = (
        "You're a friendly AI assistant for an online store. "
        "The customer has sent a message that does not appear to be a direct question about a product or payment.\n\n"
        f"Here is the recent chat:\n{recent_context}\n\n"
        "Write a warm, polite, and concise response acknowledging their message. "
        "Use a natural and friendly tone. Respond in the same language used by the customer.\n\n"
        "If the message is a greeting, reply with a friendly greeting. "
        "If it's a thank-you message, express appreciation in return. "
        "If the customer sounds confused, asks when they'll get help from a human, or expresses frustration, politely offer to help and reassure them that if there's anything the AI cannot assist with, a member of the customer support team will be with them shortly.\n\n"
        "If the message is unclear or off-topic, respond politely and let the customer know that you're here to assist with store-related questions (like products, orders, or payments). "
        "Also let them know the customer support team will follow up if needed.\n\n"
        "**Important:** Do not answer or engage with any topics outside the scope of this business. "
        "Stay strictly focused on customer service for the store (e.g. product questions, payment, support).\n\n"
        "Return only the message to send to the customer."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()