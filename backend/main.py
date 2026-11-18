from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="TIWARI AI AGENT API", version="0.1.0")

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: str = "hinglish"

@app.get("/")
async def root():
    return {"agent": "TIWARI AI AGENT", "status": "online", "utc": datetime.now(timezone.utc).isoformat()}

@app.get("/api/health")
async def health():
    return {"ok": True, "service": "tiwari-ai-agent-api"}

@app.post("/api/chat")
async def chat(body: ChatRequest):
    return {"ok": True, "agent": "TIWARI AI AGENT", "received": body.message,
            "reply": "Aapka message mil gaya. AI provider abhi configure hona baaki hai."}
