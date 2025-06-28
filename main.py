import threading
import uvicorn
from bot_runner import run  # your Carousell run() function
from webhook import app     # your FastAPI app

def start_webhook():
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    # threading.Thread(target=start_webhook, daemon=True).start()

    run()