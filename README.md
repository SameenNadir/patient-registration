# Patient Registration Voice AI Agent

## What it does
A caller dials a phone number and speaks naturally with an AI voice agent that collects
standard U.S. patient demographic information, confirms it back to them, and saves it
to a persistent database. A companion REST API and dashboard let you view the records.

## Demo
The live demo (Vapi phone line + Replit hosting) is no longer active.
To see it working, follow the Setup steps below and open the dashboard locally.

## Architecture
Caller → Vapi (telephony + STT/TTS) → GPT-4o-mini (conversation) → create_patient tool
→ FastAPI backend → SQLite database → REST API + Dashboard

Backend layers: routers (HTTP) → services (business logic, duplicate detection) →
schemas (validation) → models (database).

## Tech stack and why
- FastAPI: automatic validation, interactive docs, fast to build correctly.
- SQLite: zero-setup persistence, sufficient for this scope.
- Vapi: handles telephony/STT/TTS so effort goes into conversation design and integration.
- GPT-4o-mini: fast, inexpensive, capable of structured tool-calling conversations.

## Setup (local)
1. `python -m venv venv && venv\Scripts\activate` (Windows) or `source venv/bin/activate` (Mac)
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in your values
4. `uvicorn app.main:app --reload --port 8000`
5. Visit http://127.0.0.1:8000/docs and http://127.0.0.1:8000/dashboard

To let Vapi reach your local server, run `python start_tunnel.py`
(requires ngrok and the `NGROK_AUTHTOKEN` environment variable).

## Environment variables
| Variable | Purpose |
|---|---|
| DATABASE_URL | Database connection string (SQLite by default) |
| NGROK_AUTHTOKEN | Only needed for `start_tunnel.py` to expose the API publicly |

## Known limitations
- No authentication on the API (acceptable for a prototype).
- Not HIPAA compliant (out of scope for this project).

## Features
- Duplicate detection via unique phone number constraint (409 response, agent offers update).
- Live dashboard at /dashboard.

## Next steps
- Appointment scheduling, call transcripts, Postgres migration for production, API auth.
