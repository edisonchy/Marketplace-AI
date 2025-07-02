# 🛍️ Carousell AI

Carousell AI is an automated agent designed to interact with the Carousell platform using AI. It can help automate tasks like product listing, replying to messages, and managing customer interactions.

## 🚀 Features

- 🤖 AI-generated replies to customer inquiries  
- 📦 Automated product listing and updates  
- 🌐 Multi-language support with language detection  
- 📊 Intent classification and smart message handling  
- 🔒 Environment-configurable settings  

## 📁 Project Structure

```
carousell_ai/
├── main.py              # Entry point of the bot
├── agent/               # Core logic for Carousell interactions
├── models/              # LLM and intent classification logic
├── utils/               # Helper functions
├── .env                 # Environment variables
├── .gitignore
└── README.md
```

## ⚙️ Setup

1. **Clone the repo**

```bash
git clone https://github.com/your-username/carousell_ai.git
cd carousell_ai
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Create your `.env` file**

```env
CAROUSELL_EMAIL=your_email
CAROUSELL_PASSWORD=your_password
OPENAI_API_KEY=your_key
```

## 🧪 Run the Bot

```bash
python main.py
```

## 🛠️ Tech Stack

- Python 3.10+
- Playwright
- OpenAI / Groq
- dotenv
- Langchain (optional)

## 📄 License

MIT License

---

*Made with ❤️ for automation enthusiasts.*