# multi-session-automation-backend

This project is a small FastAPI backend for managing multiple sessions and dispatching jobs to them.

The current implementation is intentionally simple and uses in-memory storage. It is meant as a clean backend example with a small API surface, straightforward services and a testable structure.

## What it does

- keeps track of registered sessions
- supports `solo` and `group` mode
- creates jobs for one session or broadcasts them to all sessions
- exposes job status and result payloads
- includes tests and a basic Docker setup

## API overview

Current routes:

- `GET /health`
- `GET /mode`
- `POST /mode`
- `POST /sessions`
- `GET /sessions`
- `DELETE /sessions/{session_id}`
- `POST /jobs`
- `GET /jobs/{job_id}`

## Project structure

- `app/api/` route definitions
- `app/core/` application config
- `app/models/` request and response schemas
- `app/services/` session and job management
- `tests/` API tests

## Run locally

```bash
python -m venv .venv
```

Activate the virtual environment:

- Windows: `.venv\Scripts\activate`
- Linux/macOS: `source .venv/bin/activate`

Install dependencies and run the API:

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Swagger UI is available at:

```text
http://localhost:8000/docs
```

## Quick example

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

In `group` mode, job creation is broadcast to all registered sessions.

## Docker

```bash
docker compose up --build
```

## Tests

```bash
pytest -q
```

## Notes

- jobs are simulated in memory
- there is no persistence layer yet
- the codebase is intentionally small and easy to extend
