# Veridian Internal Service Agent — Assignment 2

A lightweight, policy-grounded internal IT support agent for the Veridian Corp data pack.

## What it demonstrates
- Chat-based IT support agent
- Source/policy citation for every answer
- Safe escalation when the data pack does not contain enough information
- Security-incident routing
- Employee request dashboard
- Ticket queue / history view
- No external policy assumptions

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open: http://127.0.0.1:8000

Windows activation:
`.venv\Scripts\activate`

## Demo queries
1. `My VPN credentials expired`
2. `I got a phishing email`
3. `My laptop is dead`
4. `Guest Wi-Fi for tomorrow`
5. `My mailbox is full`
6. `I need a monitor because I work from home 4 days a week`
7. `I need admin access to the finance server`

The final query intentionally demonstrates human routing because the supplied data pack does not define a general admin-access policy.

## Architecture

Browser → FastAPI → Policy/intent router → Veridian data pack → grounded response + source + action

The frontend is static HTML/CSS/JS, so the prototype is easy for a reviewer to open and run.

## Data boundary
The supplied data pack explicitly says to use only its material as source data and not invent unsupported policies. The application follows this constraint.

## Conversational behavior
The UI is designed as a support conversation rather than a fixed question-answer game:
- A greeting such as “hello” introduces the service and shows supported areas.
- Users can describe problems in their own words.
- Follow-ups such as “what should I do?” use recent conversation context when a clear policy topic was established.
- Each response still shows its policy source and recommended action.
- Unsupported policy questions are routed to human review rather than guessed.

## Demo data
The dashboard's employee requests and ticket queue use the sample records supplied in Assignment 2. They are intentionally labelled as assignment sample data and are not presented as live Veridian production data.

## Dynamic escalation
When the conversational agent determines that a request needs human handling, the UI can create a demo escalation ticket and refresh the Ticket Queue. This demonstrates the intended workflow without pretending to connect to a live ITSM system.
