import os
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

client = AsyncOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY")
)

KNOWLEDGE_FILE = "knowledge_base.json"
try:
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        knowledge = json.load(f)
except FileNotFoundError:
    knowledge = {"error": "No data found. Did you run the scraper?"}

system_prompt = f"""You are a professional real estate assistant for DarGlobal and Wasalt. 
Base your answers STRICTLY on this scraped knowledge: {json.dumps(knowledge)}
If the user asks something not in the knowledge base, politely inform them that you only have information regarding DarGlobal and Wasalt's scraped listings and data."""

class ChatRequest(BaseModel):
    message: str

@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Real Estate AI Chatbot</title></head>
    <body style="font-family: sans-serif; max-width: 700px; margin: 40px auto; background: #f4f4f9;">
        <div style="background: white; padding: 20px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
            <h2>DarGlobal & Wasalt Assistant</h2>
            <div id="chat" style="height: 400px; border: 1px solid #eee; background: #fafafa; overflow-y: auto; padding: 15px; margin-bottom: 15px; border-radius: 4px;"></div>
            <div style="display: flex; gap: 10px;">
                <input type="text" id="msg" style="flex: 1; padding: 10px; border: 1px solid #ccc; border-radius: 4px;" placeholder="Ask about the real estate data..." onkeypress="if(event.key === 'Enter') send()">
                <button onclick="send()" style="padding: 10px 20px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer;">Send</button>
            </div>
        </div>
        <script>
            async function send() {
                const msgInput = document.getElementById('msg');
                const msg = msgInput.value;
                if (!msg) return;
                
                const chat = document.getElementById('chat');
                chat.innerHTML += `<div style="margin-bottom: 10px;"><b>You:</b> ${msg}</div>`;
                msgInput.value = '';
                chat.scrollTop = chat.scrollHeight; // Auto-scroll down
                
                try {
                    const res = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: msg})
                    });
                    const data = await res.json();
                    
                    if (res.ok) {
                        chat.innerHTML += `<div style="margin-bottom: 10px; color: #333;"><b>AI:</b> ${data.reply}</div>`;
                    } else {
                        chat.innerHTML += `<div style="margin-bottom: 10px; color: red;"><b>Error:</b> ${data.detail}</div>`;
                    }
                    chat.scrollTop = chat.scrollHeight;
                } catch (e) {
                    chat.innerHTML += `<div style="margin-bottom: 10px; color: red;"><b>Error:</b> Connection failed.</div>`;
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    if not os.getenv("OPENROUTER_API_KEY") or os.getenv("OPENROUTER_API_KEY") == "sk-or-v1-your-actual-key-here":
        raise HTTPException(status_code=500, detail="Invalid or missing OpenRouter API Key in .env file.")
        
    try:
        response = await client.chat.completions.create(
            model="openrouter/free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message}
            ]
        )
        return {"reply": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))