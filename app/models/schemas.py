from dataclasses import dataclass, field
from datetime import datetime
from typing import Any


@dataclass
class UserContext:
    user_id: str
    role: str
    region: str | None = None


@dataclass
class QueryResult:
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    sources: list[str]
    metrics_used: list[str]
    confidence: float


@dataclass
class InsightItem:
    type: str
    title: str
    description: str
    confidence: float


@dataclass
class AuditEvent:
    event_type: str
    user_id: str
    role: str
    prompt: str | None = None
    sql: str | None = None
    output: str | None = None
    confidence: float | None = None
    created_at: datetime = field(default_factory=datetime.utcnow)
