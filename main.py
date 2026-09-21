import os
import logging
from datetime import datetime, timezone
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="Virus Mark 3 Final Backend", version="3.1.0")

cors = os.getenv("CORS_ORIGINS", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in cors.split(",")] if cors != "*" else ["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
AI_MODEL = os.getenv("AI_MODEL", "gpt-5.6-luna").strip()
VIRUS_API_KEY = os.getenv("VIRUS_API_KEY", "").strip()
client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None

SYSTEM_PROMPT = """তুমি Virus, Sahadat-এর personal AI companion।
সবসময় স্বাভাবিক, বন্ধুসুলভ Bangladeshi Bangla-তে উত্তর দেবে।
প্রয়োজনে English technical terms ব্যবহার করতে পারো।
উত্তর সরাসরি, পরিষ্কার ও কাজে লাগার মতো হবে।
নিজেকে Virus নামে পরিচয় দেবে।
কোনো secret/API key চাইবে না।
"""

class ChatRequest(BaseModel):
    message: str
    conversation_id: str | None = None

class CommandRequest(BaseModel):
    command: str

def check_key(x_virus_key: str | None):
    if VIRUS_API_KEY and x_virus_key != VIRUS_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid Virus API key")

def demo_reply(message: str) -> str:
    m = message.lower().strip()
    if "hey virus" in m or m in {"hi", "hello", "হাই", "হ্যালো"}:
        return "হ্যালো Sahadat! আমি Virus। কী করতে পারি?"
    if "time" in m or "সময়" in m:
        return "এখন " + datetime.now().strftime("%I:%M %p") + "।"
    if "date" in m or "তারিখ" in m:
        return "আজ " + datetime.now().strftime("%d-%m-%Y") + "।"
    return f"তুমি বলেছো: {message}"

def ask_ai(message: str) -> str:
    if not client:
        return demo_reply(message)
    response = client.responses.create(
        model=AI_MODEL,
        instructions=SYSTEM_PROMPT,
        input=message,
    )
    return response.output_text.strip()

@app.get("/")
def root():
    return {
        "name": "Virus Mark 3 Final Backend",
        "version": "3.1.0",
        "status": "online",
        "ai_enabled": bool(client),
        "model": AI_MODEL if client else None,
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/api/status")
def status():
    return {
        "assistant": "Virus Mark 3",
        "online": True,
        "ai_enabled": bool(client),
        "model": AI_MODEL if client else None,
    }

@app.post("/api/chat")
def chat(req: ChatRequest, x_virus_key: str | None = Header(default=None)):
    check_key(x_virus_key)
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message is empty")
    try:
        return {"reply": ask_ai(req.message)}
    except Exception:
        logging.exception("AI request failed")
        return {"reply": "দুঃখিত Sahadat, এই মুহূর্তে AI সার্ভিসে সমস্যা হচ্ছে। একটু পরে আবার চেষ্টা করো।"}

@app.post("/api/command")
def command(req: CommandRequest, x_virus_key: str | None = Header(default=None)):
    check_key(x_virus_key)
    if not req.command.strip():
        raise HTTPException(status_code=400, detail="Command is empty")
    try:
        return {"reply": ask_ai(req.command)}
    except Exception:
        logging.exception("Command AI request failed")
        return {"reply": "দুঃখিত, কমান্ডটি এখন প্রসেস করা যাচ্ছে না।"}
