from fastapi import APIRouter, HTTPException
from typing import List

from app.models.schemas import (
    JobCreate,
    JobInfo,
    ModeUpdate,
    SessionCreate,
    SessionInfo,
)
from app.services.session_manager import SessionManager
from app.services.job_manager import JobManager

router = APIRouter()

sessions = SessionManager()
jobs = JobManager()


@router.get("/health")
def health():
    return {"status": "ok"}


@router.get("/mode")
def get_mode():
    return {"mode": sessions.get_mode()}


@router.post("/mode")
def set_mode(body: ModeUpdate):
    sessions.set_mode(body.mode)
    return {"mode": sessions.get_mode()}


@router.post("/sessions", response_model=SessionInfo)
def add_session(body: SessionCreate):
    s = sessions.add_session(body.session_id, body.metadata)
    return SessionInfo(session_id=s.session_id, online=s.online, metadata=s.metadata)


@router.get("/sessions", response_model=List[SessionInfo])
def list_sessions():
    out = []
    for s in sessions.list_sessions():
        out.append(SessionInfo(session_id=s.session_id, online=s.online, metadata=s.metadata))
    return out


@router.delete("/sessions/{session_id}")
def remove_session(session_id: str):
    sessions.remove_session(session_id)
    return {"removed": session_id}


@router.post("/jobs", response_model=JobInfo)
def create_job(body: JobCreate):
    resolved = sessions.resolve_targets(body.target)
    if not resolved:
        raise HTTPException(status_code=400, detail="Target session(s) not found. Add sessions first.")

    created = []
    for t in resolved:
        job = jobs.create_job(target=t, action=body.action, payload=body.payload)
        jobs.run_job(job.job_id)
        created.append(job)

    primary = created[0]
    return JobInfo(
        job_id=primary.job_id,
        status=primary.status,
        target=primary.target,
        action=primary.action,
        result={
            "primary": primary.result,
            "broadcast_count": len(created),
            "broadcast_targets": [j.target for j in created],
        },
        error=primary.error,
    )


@router.get("/jobs/{job_id}", response_model=JobInfo)
def get_job(job_id: str):
    job = jobs.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return JobInfo(
        job_id=job.job_id,
        status=job.status,
        target=job.target,
        action=job.action,
        result=job.result,
        error=job.error,
    )
