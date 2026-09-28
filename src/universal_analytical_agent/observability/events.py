"""Minimal structured events for future run observability."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from universal_analytical_agent.domain.contracts import RunId


class EventType(StrEnum):
    """Events anticipated by the explicit agent runtime state machine."""

    RUN_STARTED = "run_started"
    LLM_REQUESTED = "llm_requested"
    AGENT_ACTION_RECEIVED = "agent_action_received"
    FINAL_RESPONSE_PRODUCED = "final_response_produced"
    STEP_LIMIT_REACHED = "step_limit_reached"
    PLANNING = "planning"
    TOOL_REQUESTED = "tool_requested"
    TOOL_VALIDATION_FAILED = "tool_validation_failed"
    TOOL_EXECUTION_STARTED = "tool_execution_started"
    TOOL_COMPLETED = "tool_completed"
    TOOL_EXECUTION_FAILED = "tool_execution_failed"
    TOOL_EXECUTION_DENIED = "tool_execution_denied"
    VALIDATION = "validation"
    RUN_COMPLETED = "run_completed"
    RUN_FAILED = "run_failed"


@dataclass(frozen=True, slots=True)
class RunEvent:
    """A structured, timestamped event suitable for later persistence."""

    run_id: RunId
    event_type: EventType
    payload: Mapping[str, object] = field(default_factory=dict)
    event_id: UUID = field(default_factory=uuid4)
    occurred_at: datetime = field(default_factory=lambda: datetime.now(UTC))
