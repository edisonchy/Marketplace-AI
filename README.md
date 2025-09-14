# Marketplace AI  
*AI agent that automates customer support, payments, and order fulfillment for online marketplaces.*

Marketplace AI is an automation agent designed to **streamline the entire sales process** on online marketplaces.  
It interacts directly with customers, classifies their intent, verifies payments, and handles delivery — all without human intervention.  

## Demo  

<a href="https://youtu.be/ATgwAl5gphQ">
  <img src="https://github.com/user-attachments/assets/f0c6789a-83ea-4525-b9b2-bfd7ba27a931" alt="Video thumbnail" width="400">
</a>  
<br>  
*(Click the image to watch the demo video)* 

## Target Problems  

- **Lack of 24/7 availability** → Customers drop off when no support is available round the clock.  
- **Inconsistent customer experience** → Untrained staff give unprofessional or unfriendly responses.  
- **Manual payment verification** → Checking emails and webhooks manually causes errors and delays.  
- **Slow order fulfillment** → Manual delivery steps prevent instant product access or fast shipping.  
- **Scalability issues** → Growing sales require more staff, driving up costs and limiting growth.  

## Features  

- Handles all marketplace navigation and interactions automatically using **Puppeteer**.  
- Performs **intent classification** with an open-source LLM via **Groq** (`BUY`, `ASK`, `PAID`, `OTHER`).  
- Monitors payments through **webhook integration** and **email parsing**.  
- Includes self-validity checks and safeguards to reduce hallucinations.  
- Generates tailored, AI-driven responses to customer inquiries.  
- Supports **multiple languages** with automatic detection.  

## Requirements  

- Python 3.9+  
- Puppeteer (installed automatically via dependencies)  
- A valid **Groq API key**  
- Marketplace account cookies (`cookies.json`)  

## Quick Start  

1. **Clone the repo**
   ```bash
   git clone https://github.com/edisonchy/Marketplace-AI
   cd Marketplace-AI
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   Create a `.env` file:
   ```env
   GROQ_API_KEY=your-groq-api-key
   WEBHOOK_USER=your-username
   WEBHOOK_PASS=your-password
   WEBSITE=marketplace-website
   ```

### Getting Cookies  

1. Log in to your marketplace account using a web browser (Chrome recommended).  
2. Install a browser extension such as **EditThisCookie** or **Cookie-Editor**.  
3. Export your cookies from the logged-in session.  
4. Copy the exported string and paste it into `cookies.json`:  

```json
{
  "cookies": "your_cookie_string_here"
}
```

*Keep your cookies private — anyone with access can use your marketplace session.*  

4. **Run the bot**
   ```bash
   python main.py
   ```

## Disclaimer  

*This project was developed solely for educational purposes.  
It is intended to demonstrate concepts in AI, automation, and web automation, and is not designed for production or commercial use.*  
