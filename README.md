# Multi-Tenant AI Voice SaaS Platform

Production-oriented full-stack platform for AI voice calls with tenant isolation, role-based auth, CDR, billing, dashboards, and LiveKit/Sarvam/OpenAI integration points.

## 1) Folder Structure

```text
voicebot/
├─ backend/
│  ├─ app/
│  │  ├─ core/                 # config, db, security, dependencies
│  │  ├─ middleware/           # request logging
│  │  ├─ models/               # SQLAlchemy models
│  │  ├─ routers/              # auth, clients, agents, calls, billing, dashboard, reports
│  │  ├─ schemas/              # Pydantic request/response schemas
│  │  ├─ services/             # LiveKit, queue, storage, OpenAI extraction, audit
│  │  └─ main.py
│  ├─ voice_agent/agent.py     # Dynamic call agent runtime integration
│  ├─ requirements.txt
│  └─ Dockerfile
├─ frontend/
│  ├─ src/
│  │  ├─ api/client.js
│  │  ├─ components/Layout.jsx
│  │  ├─ pages/                # admin/client screens
│  │  ├─ App.jsx
│  │  ├─ main.jsx
│  │  └─ styles.css
│  ├─ package.json
│  └─ Dockerfile
├─ docker-compose.yml
└─ .env.example
```

## 2) Backend (FastAPI)

- JWT auth with `admin` and `client` roles
- Multi-tenant checks enforced in every domain router
- Redis queue hook for call jobs
- LiveKit room metadata generated per call
- Call finalization endpoint to persist transcript, recording URL, extracted data
- Request logging middleware + global error handler

Core endpoints:

- `POST /auth/login`
- `POST /clients`
- `GET /clients`
- `POST /agents`
- `GET /agents`
- `PUT /agents/{id}`
- `POST /calls/start`
- `GET /calls`
- `GET /calls/{id}`
- `GET /dashboard/stats`
- `GET /billing`

Additional:

- `POST /auth/bootstrap-admin`
- `POST /calls/{call_id}/transfer`
- `GET /calls/{call_id}/recording`
- `GET /reports?from_date=...&to_date=...`
- `POST /calls/events/finalize/{call_id}` (voice worker callback)

## 3) Database Models (MySQL + SQLAlchemy)

Tables implemented:

- `users`
- `clients`
- `agents`
- `calls`
- `transcripts`
- `billing`
- `audit_logs`

Every table includes a `client_id` tenant key for partitioned data access.

## 4) Frontend (React + Tailwind + Axios)

Implemented pages:

- Admin login
- Client management (admin)
- Dashboard
- Agents
- Call logs (CDR)
- Recordings
- Reports
- Billing

UI includes:

- Sidebar navigation
- Cards for KPI metrics
- Data tables with filter flows
- Basic chart visualization with Recharts

## 5) Integration Points with `agent.py`

`backend/voice_agent/agent.py` handles:

- Dynamic metadata from LiveKit (`prompt`, `voice`, `client_id`, `agent_id`)
- Dynamic assistant generation per call
- Transcript assembly
- Callback to backend finalization API for transcript + recording + status

Wire this into your LiveKit worker loop by calling:

- `run_livekit_session(metadata: dict)`

## 6) Setup Instructions

### Local with Docker (recommended)

1. Copy env:
   - `cp .env.example .env`
2. Start stack:
   - `docker compose up --build`
3. Seed initial admin:
   - `POST http://localhost:8000/auth/bootstrap-admin`
4. Login:
   - `admin@voicebot.local` / `Admin@123`

### Backend local

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend local

```bash
cd frontend
npm install
npm run dev
```

## Production Notes

- Add Alembic migrations before production rollout.
- Replace bootstrap endpoint with secure one-time provisioning.
- Restrict CORS to trusted domains.
- Integrate full LiveKit server SDK token creation flow.
- Add background workers for async call processing and billing aggregation.
