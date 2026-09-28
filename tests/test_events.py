from __future__ import annotations

from datetime import UTC

from universal_analytical_agent.domain.contracts import RunId
from universal_analytical_agent.observability.events import EventType, RunEvent


def test_structured_event_can_be_created() -> None:
    event = RunEvent(
        run_id=RunId.new(),
        event_type=EventType.RUN_STARTED,
        payload={"request_source": "test"},
    )

    assert event.event_type is EventType.RUN_STARTED
    assert event.occurred_at.tzinfo is UTC
    assert event.payload["request_source"] == "test"
