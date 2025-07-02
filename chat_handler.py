from groq_utils import interpret_intent, generate_buy_response, generate_ask_response, generate_other_response, generate_paid_response

def handle_chat(chat_id):
    intent = interpret_intent(chat_id)
    print(f"Intent: {intent}")

    if intent == "buy":
        print("Generating buy response...")
        # send_payment_instructions(chat_id)
        response = generate_buy_response(chat_id)

    elif intent == "paid":
        print("Checking email for confirmation...")
        response = generate_paid_response(chat_id)

    elif intent == "ask":
        print("Answering question.")
        response = generate_ask_response(chat_id)

    elif intent == "other":
        print("Sending generic response.")
        response = generate_other_response(chat_id)
        

    else:
        response = "I'm sorry, I don't understand."
    return response



# Placeholder function
def check_payment_received(email, chat_id):
    # Implement your logic to confirm payment
    return False