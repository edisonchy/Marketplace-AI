# Carousell AI

Carousell AI is an automation agent built to interact with the Carousell platform. It uses AI and a real browser profile to automate responses and customer interactions.

## Features

- AI-generated responses using Groq and LangChain
- Intent classification and validity checks
- Multi-language support with detection
- Handles response types: BUY, ASK, PAID, OTHER
- Uses Patchright to load Edge browser with real user profile
- Configurable via `.env`

## Setup

### 1. Clone the repo

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

4. **Create your `.env` file**

```env
GROQ_API_KEY=your-groq-api-key
WEBHOOK_USER=your-username
WEBHOOK_PASS=your-password
```

## 🧪 Run the Bot

```bash
python main.py
```

## 🛠️ Tech Stack

- Python 3.10+
- Patchright
- Playwright
-	Groq
-	FastAPI
-	LangChain
-	dotenv

## 📄 License

MIT License

---

*Made with ❤️ for automation enthusiasts.*