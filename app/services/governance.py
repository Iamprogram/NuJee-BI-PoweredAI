import json
from dataclasses import asdict
from pathlib import Path

from app.models.schemas import AuditEvent

AUDIT_LOG_PATH = Path("data/audit_log.jsonl")


def log_event(event: AuditEvent) -> None:
    AUDIT_LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = asdict(event)
    payload["created_at"] = payload["created_at"].isoformat()
    with AUDIT_LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(payload) + "\n")
