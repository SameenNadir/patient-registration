# Patient Registration Voice AI Agent

## What it does
A caller dials a phone number and speaks naturally with an AI voice agent that collects
standard U.S. patient demographic information, confirms it back to them, and saves it
to a persistent database. A companion REST API and dashboard let you view the records.

## Live Demo
- **Phone number:** [YOUR VAPI PHONE NUMBER]
- **API base URL:** https://e38c8f46-cf18-4722-9c7a-ed36ec442b62-00-1kdv481xl1mw6.sisko.replit.dev
- **Dashboard:** https://e38c8f46-cf18-4722-9c7a-ed36ec442b62-00-1kdv481xl1mw6.sisko.replit.dev/dashboard
- **API docs:** https://e38c8f46-cf18-4722-9c7a-ed36ec442b62-00-1kdv481xl1mw6.sisko.replit.dev/docs

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
1. python -m venv venv && venv\Scripts\activate (Windows) or source venv/bin/activate (Mac)
2. pip install -r requirements.txt
3. uvicorn app.main:app --reload --port 8000
4. Visit http://127.0.0.1:8000/docs and /dashboard

## Environment variables
| Variable | Purpose |
|---|---|
| DATABASE_URL | Database connection string (SQLite by default) |

## Known limitations
- SQLite on Replit resets if the container restarts without env var persistence;
  DATABASE_URL is pinned via Replit Secrets to avoid this.
- No authentication on the API — acceptable for this assessment's scope.
- Not HIPAA compliant, per the assessment's explicit scope.

## Bonus features implemented
- Duplicate detection via unique phone number constraint (409 response, agent offers update).
- Live dashboard at /dashboard.

## Next steps
- Appointment scheduling, call transcripts, Postgres migration for production, API auth.