"""Small immutable contracts shared by future application components."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass, field
from enum import StrEnum
from uuid import UUID, uuid4


class ExecutionStatus(StrEnum):
    """Terminal and non-terminal statuses anticipated for an agent run."""

    CREATED = "created"
    RUNNING = "running"
    AWAITING_APPROVAL = "awaiting_approval"
    COMPLETED = "completed"
    FAILED = "failed"
    DENIED = "denied"
    CANCELLED = "cancelled"


@dataclass(frozen=True, slots=True)
class RunId:
    """Opaque identifier used to correlate a future run and its events."""

    value: UUID

    @classmethod
    def new(cls) -> RunId:
        """Create a new random run identifier."""
        return cls(value=uuid4())


@dataclass(frozen=True, slots=True)
class StructuredError:
    """Safe, serializable error information for a response or event."""

    code: str
    message: str
    category: str
    retryable: bool = False


@dataclass(frozen=True, slots=True)
class AgentRequest:
    """A user's analytical request before orchestration is implemented."""

    run_id: RunId
    prompt: str
    context: Mapping[str, object] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class AgentResponse:
    """A future runtime's response without coupling to a model vendor."""

    run_id: RunId
    status: ExecutionStatus
    summary: str | None = None
    errors: tuple[StructuredError, ...] = ()


@dataclass(frozen=True, slots=True)
class ToolInvocation:
    """A validated request to invoke a named registered tool."""

    run_id: RunId
    tool_name: str
    arguments: Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ToolResult:
    """Normalized result returned by a registered tool."""

    invocation: ToolInvocation
    status: ExecutionStatus
    output: Mapping[str, object] = field(default_factory=dict)
    error: StructuredError | None = None
