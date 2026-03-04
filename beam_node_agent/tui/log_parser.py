"""Regex-based parser that turns raw agent log lines into structured events."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional


class EventKind(Enum):
    PAIRING_CODE = auto()
    PAIRING_EXPIRED = auto()
    CONNECTED = auto()
    DISCONNECTED = auto()
    ASSIGNMENT = auto()
    JOB_START = auto()
    JOB_DONE = auto()
    PETALS_READY = auto()
    PETALS_EXIT = auto()
    IDENTITY_LOADED = auto()
    FATAL = auto()
    OTHER = auto()


@dataclass
class LogEvent:
    kind: EventKind
    raw: str
    pairing_code: Optional[str] = None
    pairing_expires: Optional[str] = None
    assignment_model: Optional[str] = None
    assignment_blocks: Optional[str] = None
    job_id: Optional[str] = None
    tokens_sent: Optional[int] = None
    petals_exit_code: Optional[int] = None


# ---------------------------------------------------------------------------
# Compiled patterns
# ---------------------------------------------------------------------------
_PAIRING_CODE = re.compile(r"Pairing code:\s+(\S+)\s+\(expires\s+(.+?)\)")
_PAIRING_EXPIRED = re.compile(r"Pairing session expired")
_CONNECTED = re.compile(r"Connected to gateway websocket at")
_DISCONNECTED = re.compile(r"Gateway websocket error:")
_ASSIGNMENT = re.compile(
    r"New assignment received:\s+(\S+)\s+blocks\s+(\[[^\]]+\])"
)
_JOB_START = re.compile(r"Starting inference:.*?job_id=(\S+)")
_JOB_DONE = re.compile(r"Inference done:.*?job_id=(\S+).*?tokens_sent=(\d+)")
_PETALS_READY = re.compile(r"Inference worker subprocess ready")
_PETALS_EXIT = re.compile(r"Petals process exited with code\s+(\d+)")
_IDENTITY_LOADED = re.compile(
    r"(?:Loaded node identity|Using existing identity|Persisted node identity)"
)
_FATAL = re.compile(r"Fatal error in agent:")


def parse(line: str) -> LogEvent:
    """Return a LogEvent for the given raw log line."""
    m = _PAIRING_CODE.search(line)
    if m:
        return LogEvent(
            kind=EventKind.PAIRING_CODE,
            raw=line,
            pairing_code=m.group(1),
            pairing_expires=m.group(2).strip(),
        )

    if _PAIRING_EXPIRED.search(line):
        return LogEvent(kind=EventKind.PAIRING_EXPIRED, raw=line)

    if _CONNECTED.search(line):
        return LogEvent(kind=EventKind.CONNECTED, raw=line)

    if _DISCONNECTED.search(line):
        return LogEvent(kind=EventKind.DISCONNECTED, raw=line)

    m = _ASSIGNMENT.search(line)
    if m:
        return LogEvent(
            kind=EventKind.ASSIGNMENT,
            raw=line,
            assignment_model=m.group(1),
            assignment_blocks=m.group(2),
        )

    m = _JOB_DONE.search(line)
    if m:
        return LogEvent(
            kind=EventKind.JOB_DONE,
            raw=line,
            job_id=m.group(1),
            tokens_sent=int(m.group(2)),
        )

    m = _JOB_START.search(line)
    if m:
        return LogEvent(kind=EventKind.JOB_START, raw=line, job_id=m.group(1))

    if _PETALS_READY.search(line):
        return LogEvent(kind=EventKind.PETALS_READY, raw=line)

    m = _PETALS_EXIT.search(line)
    if m:
        return LogEvent(
            kind=EventKind.PETALS_EXIT, raw=line, petals_exit_code=int(m.group(1))
        )

    if _IDENTITY_LOADED.search(line):
        return LogEvent(kind=EventKind.IDENTITY_LOADED, raw=line)

    if _FATAL.search(line):
        return LogEvent(kind=EventKind.FATAL, raw=line)

    return LogEvent(kind=EventKind.OTHER, raw=line)
