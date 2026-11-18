# NexaSpace: AI Real Estate Assistant

A containerized AI chatbot built as a technical assignment for the **Junior AI Engineer – Applied AI** role at DarGlobal. **NexaSpace** scrapes dynamic public data from DarGlobal and Wasalt, processes it into a knowledge base, and serves a FastAPI backend connected to an LLM via OpenRouter.

### Live Demo
Test the live deployed application here: **[https://nexaspace-3nih.onrender.com](https://nexaspace-3nih.onrender.com)**

---

## Key Features
- **Dynamic Web Scraping:** Utilizes Playwright and BeautifulSoup to bypass anti-bot protections and extract JavaScript-rendered data from modern real estate platforms.
- **Context-Aware AI:** Integrates with OpenRouter (using free-tier LLMs like Meta Llama 3/Nemotron) to generate accurate responses strictly constrained to the scraped knowledge base.
- **Modern Backend:** Built with FastAPI for high performance, asynchronous request handling, and easy API scalability.
- **Fully Containerized:** Packaged with Docker for seamless, platform-agnostic deployment.
- **Cloud Deployment:** Hosted live on Render as a continuous web service.

---

## Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI, Uvicorn
- **AI/LLM:** OpenRouter API (OpenAI Python SDK)
- **Scraping:** Playwright, BeautifulSoup4
- **Frontend:** Vanilla HTML, CSS, JavaScript
- **DevOps:** Docker, Render
