Veridian Internal Service Agent

AIONOS Recruitment Process — Assignment 2

A policy-grounded conversational IT support agent prototype for Veridian Corp.

The solution lets employees describe IT/support issues in natural language, uses the supplied Assignment 2 data pack as its source of truth, provides relevant guidance and next actions, and routes unsupported or sensitive requests for human review.

Data note: Employee requests and ticket records shown in the dashboard are sample/assignment data. They are not connected to live Veridian production systems.

1. Assignment Objective

The prototype demonstrates an internal IT service agent that can:

Understand natural-language employee requests.

Continue conversations using recent context.

Ground responses in supplied Veridian policies.

Recommend appropriate next actions.

Identify requests requiring human intervention.

Prioritize security-related incidents.

Demonstrate escalation through a ticket queue.

Provide a dashboard for sample requests and tickets.

2. Key Features

Conversational Support

Users can describe issues naturally instead of selecting only predefined questions.

Example:
My VPN stopped working this morning.

Context-Aware Follow-ups

Recent conversation context is used for follow-up questions such as:
What should I do?

Policy-Grounded Responses

The supplied assignment data pack is treated as the source of truth. Unsupported company policies are not intentionally invented.

Human Escalation

When available policy information is insufficient, the agent can recommend human review and create a demonstration escalation ticket.

Security Routing

Security/phishing-related requests are handled using the supplied security guidance.

Dashboard

Displays policy/source counts, sample employee requests, sample tickets, Employee Requests, and Ticket Queue.

3. Architecture and Process Flow

Employee/User
     |
     v
Web Interface (HTML/CSS/JavaScript)
     |
     | HTTP / JSON
     v
FastAPI Backend / Conversational Logic
     |
     +----------------+----------------+
     |                |                |
     v                v                v
Knowledge Base   Conversation     Routing /
kb.json          Context          Escalation
     |                |                |
     +----------------+----------------+
                      |
             +--------+---------+
             |                  |
             v                  v
      Policy Guidance     Human Review
             |                  |
             +--------+---------+
                      v
                 Ticket Queue
                 tickets.json

Process

Employee enters a request.

Frontend sends the request and recent context to FastAPI.

Backend identifies the relevant support area.

Agent checks the supplied knowledge/policy data.

It returns policy-grounded guidance and an action.

Unsupported/sensitive requests can be escalated.

The Ticket Queue updates for the demonstration workflow.

4. Inputs, Sources and Assumptions

Inputs

Natural-language employee requests and recent conversation context.

Examples:

My VPN stopped working this morning.

I received a suspicious email asking for my password.

My laptop screen is flickering.

Data Sources

The supplied Assignment 2 Data Pack, stored locally as:

data/
├── kb.json
├── requests.json
└── tickets.json

These contain the knowledge/policy records, employee-request records, and ticket records supplied for the assignment.

Assumptions

The supplied Assignment 2 data pack is the source of truth.

Unsupported policies are not invented.

Historical tickets are treated as sample/operational records, not automatically as general policy.

Security incidents follow the supplied security guidance.

The prototype is not connected to a live Veridian ITSM, employee directory, email system, or production database.

Escalation is a demonstration workflow.

Dashboard records are clearly labelled assignment sample data.

5. AI Tools Used

ChatGPT

Used for:

Solution and architecture ideation.

Conversational-agent workflow design.

Backend/frontend code assistance.

Debugging and implementation support.

UI/UX refinement.

README and demo documentation.

VS Code / AI-Assisted Development

Used for:

Development and file management.

Running/debugging the FastAPI application.

Iterating on frontend and backend implementation.

AI tools were used to assist development; the prototype was reviewed and tested locally.

6. Technology Stack

Component

Technology

Backend

Python

API

FastAPI

Server

Uvicorn

Data validation

Pydantic

Frontend

HTML, CSS, JavaScript

Data

JSON

Development

VS Code

Version control

Git / GitHub

7. Project Structure

Veridian_Internal_Service_Agent/
├── main.py
├── requirements.txt
├── README.md
├── demo_script.txt
├── .gitignore
├── data/
│   ├── kb.json
│   ├── requests.json
│   └── tickets.json
└── static/
    └── index.html

8. How to Run the Project

Prerequisites

Python 3.9+

Git

VS Code (recommended)

Modern web browser

Check Python:

python3 --version

Step 1 — Clone the repository

git clone <YOUR_GITHUB_REPOSITORY_URL>
cd Veridian_Internal_Service_Agent

Replace <YOUR_GITHUB_REPOSITORY_URL> with your GitHub repository URL.

Step 2 — Open the project in VS Code

code .

The terminal must be at the project root containing main.py and requirements.txt.

Check:

pwd
ls

You should see:

main.py
requirements.txt
README.md
data
static

Step 3 — Create a virtual environment

python3 -m venv .venv

Step 4 — Activate it

macOS / Linux

source .venv/bin/activate

Windows

.venv\Scripts\activate

You should see (.venv) in the terminal.

Step 5 — Install dependencies

pip install -r requirements.txt

Step 6 — Start the server

uvicorn main:app --reload

You should see:

Uvicorn running on http://127.0.0.1:8000

Step 7 — Open the application

Open:

http://127.0.0.1:8000

Step 8 — Test the agent

Try:

Hello

Then:

My VPN stopped working this morning.

Then:

What should I do?

Also test:

I received a suspicious email asking for my password.

and:

I need admin access to the finance reporting server.

The last example demonstrates how the prototype avoids inventing unsupported policy and can route the request for human escalation.

9. Recommended Demo Flow

Open Dashboard
      ↓
Show assignment-sample-data label
      ↓
Type "Hello"
      ↓
Show conversational response
      ↓
Ask a VPN issue
      ↓
Ask a follow-up question
      ↓
Show context-aware response
      ↓
Enter a security/phishing issue
      ↓
Show security routing
      ↓
Enter an unsupported request
      ↓
Create escalation ticket
      ↓
Open Ticket Queue
      ↓
Show the new demo ticket

This demonstrates conversation, context, policy grounding, routing, escalation, and ticket visibility.

10. Limitations

No connection to a production IT Service Management platform.

No live employee data.

Ticket creation is a demonstration workflow.

Knowledge is limited to the supplied Assignment 2 data pack.

External company policies are not assumed when absent from the supplied data.

Authentication and role-based access are outside the prototype scope.

11. Submission Deliverables

As specified in the AIONOS Assignment 2 instructions:

GitHub link — source code and project documentation.

Demo video — uploaded to Google Drive with open/public access.

Working agent / clickable prototype.

10-slide PPT covering:

Architecture and process flow.

Inputs, sources and assumptions.

AI tools used and how they were used.

Architecture of the complete solution.

File naming

Use:

RollNo_Name

for submitted files.

12. Conclusion

The Veridian Internal Service Agent demonstrates:

Natural-language interaction → Policy grounding → Context-aware guidance → Correct routing → Human escalation → Ticket visibility

The prototype is designed to demonstrate the complete support workflow while clearly distinguishing assignment sample data from live enterprise data.
