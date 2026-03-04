# Multi-Session Automation Backend (Portfolio Demo)

A production-style FastAPI backend that demonstrates:
- Multi-session management (e.g. accounts/agents)
- Switchable solo vs group (broadcast) control mode
- Job creation + status + structured results
- Clean architecture (api/services/models/core), tests, Docker

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open Swagger UI:
- http://localhost:8000/docs

## Quick demo (curl)
```bash
curl -X POST http://localhost:8000/sessions -H "Content-Type: application/json" \
  -d "{\"session_id\":\"acc_01\",\"metadata\":{\"role\":\"leader\"}}"

curl -X POST http://localhost:8000/sessions -H "Content-Type: application/json" \
  -d "{\"session_id\":\"acc_02\",\"metadata\":{\"role\":\"follower\"}}"

curl -X POST http://localhost:8000/mode -H "Content-Type: application/json" \
  -d "{\"mode\":\"group\"}"

curl -X POST http://localhost:8000/jobs -H "Content-Type: application/json" \
  -d "{\"target\":\"acc_01\",\"action\":\"navigate\",\"payload\":{\"to\":\"map_12\"}}"
```

## Docker
```bash
docker compose up --build
```

## Tests
```bash
pytest -q
```
