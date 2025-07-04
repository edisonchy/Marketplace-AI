# Carousell AI

Marketplace AI is an automation agent designed to interact with customers on an online marketplace. The goal of this project is to fully automate the sales process on the platform. The agent uses AI to identify customer intent and generate appropriate responses to meet their needs. It tracks payments through email forwarding and webhooks (via FastAPI), and once payment is confirmed, it automatically handles the delivery of the purchased product.

## Features

- Automates navigation and interaction within the online marketplace
- Performs intent classification and self-validity checks
- Handles response types: BUY, ASK, PAID, OTHER
- Implements safeguards to reduce AI hallucinations
- Generates tailored, AI-driven responses to customer inquiries
- Supports multiple languages with automatic language detection
- Monitors payments via webhook integration and email parsing

## Get Up and Running

1. **Clone the repo**

```bash
git clone https://github.com/your-username/carousell_ai.git
cd carousell_ai
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate        # macOS/Linux
# OR
.venv\Scripts\activate           # Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

## Configeration
**Make your `.env` file**

```env
GROQ_API_KEY=your-groq-api-key
WEBHOOK_USER=your-username
WEBHOOK_PASS=your-password
WEBSITE=your-website-url
```

**Import your cookies**

Import your cookies in cookies.json:

```cookies.json
{
  "cookies": "your_cookie_string_here"
}
```

## Run the Bot

```bash
python main.py
```

## 🛠️ Tech Stack

- Python 3.10+
- Patchright
-	Groq
-	FastAPI

---

*This project was developed solely for educational purposes. It is intended to demonstrate concepts in AI, automation, and web automation, and is not designed for production or commercial use.*
