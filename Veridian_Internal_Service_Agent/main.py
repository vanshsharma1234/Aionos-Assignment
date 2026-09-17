
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from pathlib import Path
import json, re

BASE = Path(__file__).parent
KB = json.loads((BASE/"data/kb.json").read_text())
REQUESTS = json.loads((BASE/"data/requests.json").read_text())
TICKETS = json.loads((BASE/"data/tickets.json").read_text())

app = FastAPI(title="Veridian Internal Service Agent", version="1.0")

class ChatIn(BaseModel):
    message: str
    history: list[dict] = []

def result(text, source, action="Resolve / route"):
    return {"response": text, "source": source, "action": action}

def answer(msg: str, history=None):
    m = msg.lower().strip()
    history = history or []
    previous = " ".join(
        str(x.get("content", "")) for x in history[-6:]
        if isinstance(x, dict)
    ).lower()

    # Conversational greeting / onboarding
    if m in {"hi", "hello", "hey", "hii", "helo", "good morning", "good afternoon", "good evening"}:
        return result(
            "Hi! I’m your Veridian IT support agent. Tell me what’s going wrong or what you need help with — you can describe it in your own words.\n\n"
            "I can help with:\n"
            "• Password & account lockouts\n"
            "• VPN access or expired credentials\n"
            "• Laptop / hardware issues\n"
            "• Software installation\n"
            "• Printer problems\n"
            "• Mailbox quota\n"
            "• Guest Wi-Fi\n"
            "• Expense-tool login issues\n"
            "• Security / phishing incidents\n"
            "• Work-from-home equipment",
            "KB-01 to KB-10",
            "Start a support conversation"
        )

    if m in {"help", "what can you do", "what can you help with", "options", "services"}:
        return result(
            "Sure — describe your issue naturally and I’ll guide you. For example: “My VPN stopped working”, “my laptop screen is flickering”, or “I got a suspicious email”.\n\n"
            "I can handle password/account, VPN, laptop, software, printer, mailbox, guest Wi-Fi, expense-tool, security and WFH-equipment requests.",
            "KB-01 to KB-10",
            "Describe your issue"
        )

    # Context-aware follow-up phrases
    if any(p in m for p in ["what should i do", "what do i do", "now what", "how do i fix it", "what next", "help me with this"]):
        if "vpn" in previous:
            return result(
                "For the VPN issue we were discussing: VPN credentials expire every 90 days and must be renewed by the employee. If the problem continues after renewal, the technical issue should go to IT.",
                "KB-02", "Renew credentials / IT if still failing"
            )
        if any(x in previous for x in ["laptop", "screen", "flicker", "computer"]):
            return result(
                "For the laptop issue we were discussing: the next step is IT diagnosis/verification. Replacement is eligible after 3 years or earlier for verified hardware failure, while early replacement outside the 4-year refresh cycle also requires Finance sign-off.",
                "KB-03 + Asset Management Policy", "IT diagnosis / verification"
            )
        if "printer" in previous:
            return result(
                "For the printer issue: first check the printer queue and restart the print spooler. If it still fails, log a ticket with the printer’s asset tag.",
                "KB-05", "Troubleshoot / ticket if unresolved"
            )
        if any(x in previous for x in ["mailbox", "quota", "email full"]):
            return result(
                "For the mailbox issue: archive old mail if you’re nearing the 25GB default quota. A quota increase beyond 25GB needs manager approval and is capped at 50GB.",
                "KB-06", "Archive / approval if increase needed"
            )
        return result(
            "I can help, but I need a little more detail about the issue. Tell me what you’re trying to do and what went wrong.",
            "No matching source", "Clarify request"
        )

    # Security incident: highest-priority routing
    if any(x in m for x in ["phishing", "malware", "unauthorized access", "suspicious email", "suspicious mail"]):
        return result(
            "This is a security incident. Please report suspected phishing, malware, or unauthorized access immediately to security@veridian-corp.example. Do not forward the message to other employees.\n\n"
            "If you have already forwarded it, stop forwarding it further and report it to Security immediately.",
            "KB-09", "Escalate to Security"
        )

    if any(x in m for x in ["guest wifi", "guest wi-fi", "visitor wifi", "visitor wi-fi"]):
        return result(
            "Yes — guest Wi-Fi is handled without an IT ticket. You can generate 24-hour guest credentials from the front-desk kiosk.",
            "KB-07", "Self-service at front-desk kiosk"
        )

    if any(x in m for x in ["password", "locked out", "account locked", "login locked", "forgot password", "reset password"]):
        if any(x in m for x in ["6", "six", "5 failed", "five failed", "too many attempts"]):
            return result(
                "Your account has crossed the 5-failed-attempt threshold. IT needs to unlock the account manually, and no approval is required.",
                "KB-01", "Route to IT"
            )
        return result(
            "You can reset your password yourself through the self-service portal at any time. If you become locked out after 5 failed attempts, IT can manually unlock the account.",
            "KB-01", "Self-service / IT if locked"
        )

    if "vpn" in m:
        if "contractor" in m:
            return result(
                "For a contractor, VPN access requires manager approval submitted through the access request form. VPN credentials expire every 90 days and must be renewed by the employee.",
                "KB-02", "Manager approval"
            )
        if any(x in m for x in ["expired", "90 days", "renew", "stopped working"]):
            return result(
                "It sounds like a VPN credential issue. VPN credentials expire every 90 days and must be renewed by the employee. If access still fails after renewal, the technical issue should go to IT.",
                "KB-02", "Renew credentials / IT if still failing"
            )
        return result(
            "VPN access is automatic for full-time employees. Contractors need manager approval through the access request form. Credentials expire every 90 days and must be renewed by the employee.",
            "KB-02", "Policy lookup"
        )

    if any(x in m for x in ["laptop", "screen flicker", "laptop replacement", "computer", "flicker", "flickering", "won't turn", "wont turn", "dead laptop"]):
        if any(x in m for x in ["dead", "won't turn", "wont turn", "hardware failure", "flicker", "flickering"]):
            return result(
                "I can help with that. First, this should go through IT diagnosis/verification. The policy allows replacement after 3 years or earlier for verified hardware failure. The Asset Management Policy also says company hardware follows a 4-year refresh cycle and early replacement outside that cycle requires Finance sign-off in addition to IT approval.",
                "KB-03 + Asset Management Policy", "IT diagnosis / verification"
            )
        return result(
            "Laptops are eligible for replacement after 3 years, or earlier for verified hardware failure. Requests should be raised at least 2 weeks before the intended replacement.",
            "KB-03", "Request assessment"
        )

    if any(x in m for x in ["software", "install", "browser extension", "extension", "application"]):
        return result(
            "If the software is in the approved catalog, it can be self-installed. If it is not in the catalog, IT Security review is required and takes 3–5 business days.",
            "KB-04", "Self-install if catalog / Security review if non-catalog"
        )

    if "printer" in m or "paper jam" in m or "spooler" in m:
        return result(
            "Let’s troubleshoot it first: check the printer queue and restart the print spooler. If the issue persists after the restart, log a ticket with the printer’s asset tag.",
            "KB-05", "Troubleshoot / ticket if unresolved"
        )

    if any(x in m for x in ["mailbox", "mail full", "email full", "quota", "can't send emails", "cannot send emails"]):
        return result(
            "The default mailbox quota is 25GB. If you’re nearing the limit, archive old mail. A quota increase beyond 25GB needs manager approval and is capped at 50GB.",
            "KB-06", "Archive / approval if increase needed"
        )

    if any(x in m for x in ["expense", "finance tool", "expense tool", "expense management"]):
        return result(
            "For the expense tool, Finance—not IT—grants access. IT can help with login or technical issues once an account already exists.",
            "KB-08", "Finance for access / IT for technical login"
        )

    if any(x in m for x in ["work from home", "wfh", "monitor", "home office", "chair", "remote work"]):
        return result(
            "If you work remotely more than 3 days per week, you’re eligible for a one-time home-office equipment allowance covering a chair or monitor. Manager sign-off and Finance processing are required; IT handles shipping after approval.",
            "KB-10", "Manager + Finance approval, then IT shipping"
        )

    if any(x in m for x in ["admin access", "server access", "administrator", "finance reporting server"]):
        return result(
            "I can route this, but I won’t invent an approval policy. The supplied data pack does not define a general admin-access rule. A previous ticket was rejected for lacking business justification, but that is historical context rather than a general policy.",
            "TK-1050 (precedent only)", "Human review"
        )

    # Generic conversational fallback
    return result(
        "I’m here to help with your IT request. Tell me what you’re trying to do, what happened, and any useful detail such as an error message. I’ll use the Veridian support policies to guide you.",
        "No matching source", "Clarify request"
    )

@app.get("/api/health")
def health():
    return {"status":"ok"}

@app.get("/api/summary")
def summary():
    active = [t for t in TICKETS if not any(x in t[3].lower() for x in ["resolved", "rejected", "approved at"])]
    return {
        "knowledge_policies": len(KB),
        "employee_requests": len(REQUESTS),
        "tickets": len(TICKETS),
        "active_tickets": len(active),
        "closed_tickets": len(TICKETS)-len(active)
    }

@app.get("/api/requests")
def get_requests():
    return [{"id":r[0],"employee":r[1],"email":r[2],"date":r[3],"request":r[4],"status":r[5]} for r in REQUESTS]

@app.get("/api/tickets")
def get_tickets():
    return [{"id":t[0],"employee":t[1],"issue":t[2],"status":t[3]} for t in TICKETS]

@app.post("/api/chat")
def chat(body: ChatIn):
    return answer(body.message, body.history)

@app.get("/", response_class=HTMLResponse)
def home():
    return (BASE/"static/index.html").read_text()

app.mount("/static", StaticFiles(directory=BASE/"static"), name="static")
