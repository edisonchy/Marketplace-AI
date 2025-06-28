from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os
from db_utils import load_db, update_db 

load_dotenv()

app = FastAPI()
security = HTTPBasic()

USERNAME = os.getenv("WEBHOOK_USER")
PASSWORD = os.getenv("WEBHOOK_PASS")

def validate_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != USERNAME or credentials.password != PASSWORD:
        raise HTTPException(status_code=401, detail="Unauthorized")

@app.post("/api/webhook", dependencies=[Depends(validate_basic_auth)])
async def receive_email(request: Request):
    data = await request.json()
    html = data.get("html")

    if not html:
        return {"status": "error", "reason": "No HTML content found."}

    soup = BeautifulSoup(html, "html.parser")
    text_blocks = soup.find_all("p")

    order_id = None
    amount = None

    for i, block in enumerate(text_blocks):
        text = block.text.strip()

        if "Message to recipient" in text or "給受款人的訊息" in text:
            if i + 1 < len(text_blocks):
                order_id = text_blocks[i + 1].text.strip()

        elif "Payment amount" in text or "付款金額" in text:
            if i + 1 < len(text_blocks):
                amount = text_blocks[i + 1].text.strip()

    if not order_id or not amount:
        return {"status": "error", "reason": "Missing order ID or amount"}

    db = load_db()

    for chat_id, record in db.items():
        if record.get("order_id") == order_id:
            update_db(chat_id, {"status": "paid"})
            return {
                "status": "success",
                "chat_id": chat_id,
                "order_id": order_id,
                "amount": amount
            }

    return {
        "status": "error",
        "reason": "Order ID not found in any chat record",
        "order_id": order_id
    }