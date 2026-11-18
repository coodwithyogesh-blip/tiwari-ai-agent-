"""Safe command classification for TIWARI AI AGENT.

This module plans actions only. It never pretends that an external order,
booking, message, or account operation has actually been completed.
"""
from typing import Any

SERVICE_RULES = [
    ("rail", ("train", "railway", "pnr", "ticket", "irctc", "live train")),
    ("zepto", ("zepto", "grocery", "kirana")),
    ("shopping", ("amazon", "flipkart", "order", "cart", "product", "purchase")),
    ("github", ("github", "repository", "repo", "commit", "pull request", "actions build")),
    ("email", ("email", "e-mail", "gmail", "inbox")),
    ("sms", ("sms", "text message", "message bhejo", "message send")),
    ("whatsapp", ("whatsapp", "wa message")),
    ("chatgpt", ("chatgpt", "chat gpt", "openai")),
    ("phone", ("call", "phone", "open app", "launch app")),
]

READ_ONLY_TERMS = (
    "status", "search", "find", "show", "dikhao", "batao", "read",
    "check", "track", "summary", "list", "view", "open",
)
HIGH_IMPACT_TERMS = (
    "book", "booking", "buy", "purchase", "order", "pay", "payment",
    "cancel", "return", "refund", "send", "bhejo", "submit", "confirm",
    "place order", "ticket",
)


def plan_command(message: str) -> dict[str, Any]:
    """Return a conservative plan; integrations are disabled until configured."""
    text = " ".join((message or "").lower().split())
    service = "general"
    for name, terms in SERVICE_RULES:
        if any(term in text for term in terms):
            service = name
            break

    read_only = any(term in text for term in READ_ONLY_TERMS)
    high_impact = any(term in text for term in HIGH_IMPACT_TERMS)

    # A command is auto-eligible only when it clearly reads/opens information
    # and contains no high-impact verb.
    approval_required = high_impact or not read_only
    return {
        "service": service,
        "approval_required": approval_required,
        "execution": "not_configured",
        "message": (
            "Integration abhi configure nahi hai. Koi external action execute nahi hua."
        ),
        "requested_command": message,
    }
