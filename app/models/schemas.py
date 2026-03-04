from pydantic import BaseModel, Field
from typing import Any, Dict, Literal, Optional

Mode = Literal["solo", "group"]


class SessionCreate(BaseModel):
    session_id: str = Field(..., examples=["acc_01"])
    metadata: Dict[str, Any] = Field(default_factory=dict)


class SessionInfo(BaseModel):
    session_id: str
    online: bool
    metadata: Dict[str, Any]


class ModeUpdate(BaseModel):
    mode: Mode


class JobCreate(BaseModel):
    target: str = Field(..., examples=["acc_01", "group"])
    action: str = Field(..., examples=["navigate", "gather", "fight_rotation"])
    payload: Dict[str, Any] = Field(default_factory=dict)


class JobInfo(BaseModel):
    job_id: str
    status: Literal["queued", "running", "done", "failed"]
    target: str
    action: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
