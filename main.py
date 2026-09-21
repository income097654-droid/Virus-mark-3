import os
from datetime import datetime, timezone
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

APP_NAME = "Virus Mark 3 Backend"
API_KEY = os.getenv("VIRUS_API_KEY", "")

app = FastAPI(title=APP_NAME, version="3.0.0")

# For development this accepts the Mark 3 frontend from any origin.
# In production, set CORS_ORIGINS to the exact frontend URL(s).
origins = [x.strip() for x in os.getenv("CORS_ORIGINS", "*").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins if origins != ["*"] else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommandRequest(BaseModel):
    command: str
    session_id: Optional[str] = None

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

def check_key(x_api_key: Optional[str]):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

def process_command(command: str) -> str:
    text = command.strip()
    low = text.lower()

    if not text:
        return "কমান্ডটি খালি।"

    if any(k in low for k in ["hello", "hi", "hey virus", "হ্যালো", "হাই"]):
        return "হ্যালো Sahadat! আমি Virus Mark 3. কী করতে পারি?"

    if "time" in low or "সময়" in low or "সময়" in low:
        now = datetime.now().astimezone()
        return f"এখন সময় {now.strftime('%I:%M %p')}।"

    if "date" in low or "তারিখ" in low:
        now = datetime.now().astimezone()
        return f"আজ {now.strftime('%d-%m-%Y')}।"

    # Mark 3-এর future integrations এখান থেকে যোগ করা যাবে:
    # Home Assistant, reminders, weather, device control, AI provider, etc.
    return f"তোমার কমান্ড পেয়েছি: {text}"

@app.get("/")
def root():
    return {
        "name": APP_NAME,
        "version": "3.0.0",
        "status": "online",
        "message": "Virus Mark 3 backend is running."
    }

@app.get("/health")
def health():
    return {"status": "ok", "service": "virus-mark-3-backend"}

@app.get("/api/status")
def status():
    return {
        "assistant": "Virus",
        "mark": 3,
        "backend": "online",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.post("/api/command")
def command(req: CommandRequest, x_api_key: Optional[str] = Header(default=None)):
    check_key(x_api_key)
    return {
        "ok": True,
        "type": "command",
        "reply": process_command(req.command),
        "session_id": req.session_id
    }

@app.post("/api/chat")
def chat(req: ChatRequest, x_api_key: Optional[str] = Header(default=None)):
    check_key(x_api_key)
    return {
        "ok": True,
        "type": "chat",
        "reply": process_command(req.message),
        "session_id": req.session_id
    }
