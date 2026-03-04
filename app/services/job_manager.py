import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, Literal, Optional

Status = Literal["queued", "running", "done", "failed"]


@dataclass
class Job:
    job_id: str
    status: Status
    target: str
    action: str
    payload: Dict[str, Any] = field(default_factory=dict)
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class JobManager:
    """
    Minimal in-memory job manager that simulates task execution.
    For a portfolio demo: shows queueing, status transitions, results.
    """

    def __init__(self) -> None:
        self._jobs: Dict[str, Job] = {}

    def create_job(self, target: str, action: str, payload: Dict[str, Any]) -> Job:
        job_id = str(uuid.uuid4())
        job = Job(job_id=job_id, status="queued", target=target, action=action, payload=payload)
        self._jobs[job_id] = job
        return job

    def get_job(self, job_id: str) -> Optional[Job]:
        return self._jobs.get(job_id)

    def run_job(self, job_id: str) -> None:
        job = self._jobs.get(job_id)
        if not job:
            return

        job.status = "running"
        try:
            time.sleep(0.15)
            job.result = {
                "ok": True,
                "action": job.action,
                "payload_echo": job.payload,
                "timestamp": time.time(),
            }
            job.status = "done"
        except Exception as e:
            job.status = "failed"
            job.error = str(e)
