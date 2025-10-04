# Project Aegis

Monorepo for API (Flask) and client (React + Vite).

## Quickstart (local without Docker)

- Backend
  - Create `.env` from `api/.env.example`
  - `python -m venv .venv && source .venv/bin/activate`
  - `pip install -r api/requirements.txt`
  - `python api/run.py`
- Frontend
  - `cd client && pnpm install && pnpm dev`

## Docker Compose

```bash
docker compose up --build
```

Services: API on `http://localhost:8000`, Client on `http://localhost:5173`.
