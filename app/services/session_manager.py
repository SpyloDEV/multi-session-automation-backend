from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal


Mode = Literal["solo", "group"]


@dataclass
class Session:
    session_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    online: bool = True


class SessionManager:
    """
    Manages multiple sessions (e.g., accounts/agents) and supports
    switchable solo vs group mode (group means broadcast actions).
    """

    def __init__(self) -> None:
        self._sessions: Dict[str, Session] = {}
        self._mode: Mode = "solo"

    def set_mode(self, mode: Mode) -> None:
        self._mode = mode

    def get_mode(self) -> Mode:
        return self._mode

    def add_session(self, session_id: str, metadata: Dict[str, Any]) -> Session:
        s = Session(session_id=session_id, metadata=metadata, online=True)
        self._sessions[session_id] = s
        return s

    def remove_session(self, session_id: str) -> None:
        self._sessions.pop(session_id, None)

    def list_sessions(self) -> List[Session]:
        return list(self._sessions.values())

    def exists(self, session_id: str) -> bool:
        return session_id in self._sessions

    def resolve_targets(self, target: str) -> List[str]:
        """
        target can be:
          - a specific session_id (e.g. 'acc_01')
          - 'group' meaning broadcast to all sessions
        If mode == 'group', any target may be treated as broadcast (optional behavior).
        """
        if target == "group" or self._mode == "group":
            return list(self._sessions.keys())
        return [target] if target in self._sessions else []
