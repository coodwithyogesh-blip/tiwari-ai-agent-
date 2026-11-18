from datetime import datetime, timezone
from fastapi import FastAPI
from pydantic import BaseModel, Field

from policy import plan_command

app = FastAPI(title="TIWARI AI AGENT API", version="0.2.0")


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    language: str = "hinglish"


@app.get("/")
async def root():
    return {
        "agent": "TIWARI AI AGENT",
        "status": "online",
        "utc": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/api/health")
async def health():
    return {
        "ok": True,
        "service": "tiwari-ai-agent-api",
        "version": "0.2.0",
        "integrations_configured": [],
    }


@app.get("/api/capabilities")
async def capabilities():
    return {
        "control_mode": "phone_and_web",
        "automation_mode": "automatic_for_safe_read_only_tasks",
        "approval_required_for": [
            "payments", "final_bookings", "placing_orders",
            "cancellations", "sending_messages", "account_changes",
        ],
        "planned_services": [
            "rail", "zepto", "shopping", "github", "email",
            "sms", "whatsapp", "chatgpt", "phone",
        ],
        "note": "Listed services are planned; only configured integrations can execute.",
    }


@app.post("/api/plan")
async def plan(body: ChatRequest):
    """Classify a command without executing an external action."""
    return {"ok": True, "agent": "TIWARI AI AGENT", **plan_command(body.message)}


@app.post("/api/chat")
async def chat(body: ChatRequest):
    plan = plan_command(body.message)
    if plan["approval_required"]:
        reply = (
            "Command samajh gaya. Is action ke liye aapki final permission chahiye. "
            "Abhi koi booking, order, payment ya message execute nahi hua."
        )
    else:
        reply = (
            "Command samajh gaya. Yeh read-only task automatic ho sakta hai, "
            "lekin sambandhit service integration abhi configure nahi hai."
        )
    return {
        "ok": True,
        "agent": "TIWARI AI AGENT",
        "reply": reply,
        "plan": plan,
    }
