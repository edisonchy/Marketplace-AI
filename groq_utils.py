import os
import random
import string
from groq import Groq
from dotenv import load_dotenv

from db_utils import load_db, update_db

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def interpret_intent(chat_id, db_path="db.json"):
    db = load_db(db_path)
    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found.")

    messages = db[chat_id].get("messages", [])
    if not messages:
        return "other"

    recent = messages[-5:]
    full_chat = "\n".join(recent)
    parcial_chat = "\n".join(recent[:-2])
    last_message = recent[-1]

    # Step 1: First Intent Classification
    classification_prompt = (
        "You're an AI assistant managing online transactions. "
        "Your task is to determine the customer's intent based on a short chat history. "
        "Messages are not labeled, so infer speaker from context. "
        "Focus especially on the final message.\n\n"
        "Possible intents:\n"
        "- ask: Asking about the product\n"
        "- buy: Expressing interest in buying\n"
        "- paid: Confirming payment\n"
        "- other: Small talk, unclear, or irrelevant\n\n"
        f"Chat:\n{full_chat}\n\n"
        "Return only the intent."
    )

    intent_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": classification_prompt}]
    )
    intent = intent_response.choices[0].message.content.strip().lower()

    # Step 2: Self-Validation Check
    validation_prompt = (
        f"You previously classified the customer's intent as: '{intent}'.\n"
        f"Final message:\n\"{last_message}\"\n\n"
        "If the final message is too short or unclear, use the earlier chat for additional context.\n\n"
        f"Earlier chat context:\n{parcial_chat}\n\n"
        "Based on this context, does the final message support the classified intent? Answer only 'yes' or 'no'."
    )

    validation_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": validation_prompt}]
    )
    confidence = validation_response.choices[0].message.content.strip().lower()

    if confidence != "yes":
        print(f"⚠️ Confidence check failed — downgrading intent from '{intent}' to 'other'")
        return "other"

    return intent

def generate_unique_order_id(db, length=10):
    """Generate a unique alphanumeric order ID not currently in db."""
    existing_ids = {entry.get("order_id") for entry in db.values()}
    while True:
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        if new_id not in existing_ids:
            return new_id

def generate_buy_response(chat_id, db_path="db.json"):
    db = load_db(db_path)
    if chat_id not in db:
        raise ValueError(f"Chat ID '{chat_id}' not found.")

    entry = db[chat_id]
    product_name = entry.get("product")
    messages = entry.get("messages", [])
    if not messages:
        raise ValueError(f"No messages found for chat ID '{chat_id}'.")

    last_message = messages[-1]
    recent_context = "\n".join(messages[-5:])
    price = 100
    fps_id = "123"
    new_order_id = generate_unique_order_id(db)
    update_db(chat_id, {"order_id": new_order_id}, file_path=db_path)

    # Step 1: Detect language of last message
    lang_prompt = (
        f"What language is this message written in? Only return the language name.\n\n"
        f"Message:\n{last_message}"
    )
    lang_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": lang_prompt}]
    )
    customer_language = lang_response.choices[0].message.content.strip()

    # Step 2: Generate the actual reply
    prompt = (
        "You're an AI assistant helping an online seller respond to a customer interested in buying a product.\n\n"
        f"Product name: '{product_name}'\n"
        f"Price: HK${price}\n"
        f"FPS payment ID: {fps_id}\n"
        f"Order ID: {new_order_id}\n\n"
        f"Recent chat (messages unlabeled):\n{recent_context}\n\n"

        "If the customer is asking about purchasing a different product, do not include any product details, payment information, or order ID. "
        "Instead, kindly instruct them to open a new chat from the product page of the item they wish to purchase, and place their order there.\n\n"

        "Otherwise, write a short, helpful, and polite response confirming the item is still available and providing FPS payment instructions. "
        f"Clearly tell the customer to include only this exact order ID: {new_order_id} in the FPS payment remarks. Letters and numbers only."
        "Warn them that including anything else (e.g., emojis, extra words, or the wrong ID) may delay or prevent payment verification. "
        "Let them know that FPS is the only accepted payment method.\n\n"

        "Remind them that a new order ID is generated each time they request to order, so they should always use the latest one. "
        "Ask them to notify us once payment is complete so delivery can proceed.\n\n"

        f"Respond in this language: {customer_language}.\n"
        "If the customer is using Chinese, always use Traditional Chinese (繁體中文) — never Simplified.\n"
        "- Keep the tone polite and natural.\n"
        "- Do not repeat previous agent messages.\n"
        "- Return only the message text."
    )

    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content.strip()

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
    last_message = messages[-1]

    # Step 1: Detect the language of the final message
    lang_prompt = f"What language is this message written in?\n\n\"{last_message}\"\n\nReturn only the language name."
    lang_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": lang_prompt}]
    )
    customer_language = lang_response.choices[0].message.content.strip()

    # Step 2: Main response generation
    prompt = (
        "You're a helpful and friendly AI assistant for an online store. "
        "Your role is to answer customer questions about products and purchasing, and gently guide them toward placing an order if they're interested.\n\n"

        f"Chat history:\n{recent_context}\n\n"

        "Write a short, polite, and informative response based on the customer's **latest message**.\n\n"

        f"Respond in this language: {customer_language}.\n"
        "- If the language is Chinese, always use **Traditional Chinese (繁體中文)** — never Simplified.\n\n"

        "Guidelines:\n"
        "- Stay focused on store-related topics (products, orders, payments).\n"
        "- If the customer asks how purchasing or payment works:\n"
        "  → Explain that **FPS (Faster Payment System)** is the only accepted method.\n"
        "  → Let them know that when they’re ready to order, a unique order ID will be generated.\n"
        "  → They must include this exact order ID — and nothing else — in the **FPS payment remarks**.\n"
        "  → Once payment is made, the system will:\n"
        "     - Wait for the funds to arrive (this usually takes around 5 minutes)\n"
        "  → After confirmation of payment, the customer should message us again to check the payment status.\n"
        "  → If the customer's payment status is marked as 'paid' in the system, the product will be delivered through this chat immediately.\n"
        "- Encourage the customer to let you know if they’d like to place an order.\n"
        "- If the message is vague or off-topic, steer it toward product questions or order interest.\n"
        "- Do not include an order ID unless they’ve clearly expressed intent to buy.\n\n"

        "Important:\n"
        "- Keep tone polite, natural, and friendly.\n"
        "- Do not invent or assume product details not mentioned.\n"
        "- Return only the message to send — no labels, formatting, or extra explanations."
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
    last_message = messages[-1]

    # Step 1: Detect the language of the final message
    lang_prompt = f"What language is this message written in?\n\n\"{last_message}\"\n\nReturn only the language name."
    lang_response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": lang_prompt}]
    )
    customer_language = lang_response.choices[0].message.content.strip()

    # Step 2: Generate the response in that language
    prompt = (
        "You're a friendly AI assistant for an online store. "
        "The customer has sent a message that does not appear to be a direct question about a product or payment.\n\n"
        f"Here is the recent chat:\n{recent_context}\n\n"

        "Use earlier messages for context, but prioritize the customer’s most recent message when crafting your response.\n\n"

        "Write a warm, polite, and concise reply acknowledging their latest message. "
        "Use a natural, conversational tone.\n\n"

        f"Respond in this language: {customer_language}.\n"
        "- If the language is Chinese, always reply using Traditional Chinese (繁體中文) — never Simplified.\n\n"

        "**If the message is:**\n"
        "- A greeting → reply with a friendly greeting and mention that this is a fully automated service where purchases can be made 24/7 without hassle.\n"
        "- A thank-you → express appreciation in return.\n"
        "- Confused, frustrated, or asking about human help → offer to assist, and reassure them that if the AI can’t help, a human support team member will follow up shortly.\n"
        "- Unclear or unrelated → politely let them know that you're here to assist with store-related topics like products, orders, or payments. Let them know support will follow up if needed.\n\n"

        "**Important constraints:**\n"
        "- Do not engage with or reply to any topics outside the store's services.\n"
        "- Stay strictly focused on store-related customer service (e.g. product inquiries, payments, orders, support).\n"
        "- Never generate, guess, or suggest information outside of the conversation.\n\n"

        "Return only the message to send to the customer — do not include explanations or labels."
    )

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()