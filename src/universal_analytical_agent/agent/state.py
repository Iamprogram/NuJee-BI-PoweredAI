"""Inspectable per-run state for the bounded single-agent runtime."""

from __future__ import annotations

from dataclasses import dataclass, replace

from universal_analytical_agent.domain.contracts import (
    ExecutionStatus,
    RunId,
    StructuredError,
    ToolInvocation,
    ToolResult,
)
from universal_analytical_agent.llm.provider import LLMMessage


@dataclass(frozen=True, slots=True)
class AgentRunState:
    """All and only the in-memory facts required for one current agent run."""

    run_id: RunId
    user_request: str
    messages: tuple[LLMMessage, ...]
    tool_invocations: tuple[ToolInvocation, ...] = ()
    tool_results: tuple[ToolResult, ...] = ()
    current_step: int = 0
    final_response: str | None = None
    status: ExecutionStatus = ExecutionStatus.CREATED
    errors: tuple[StructuredError, ...] = ()

    def with_error(self, error: StructuredError) -> AgentRunState:
        """Create a failed state while preserving the full run record."""
        return replace(self, status=ExecutionStatus.FAILED, errors=(*self.errors, error))
