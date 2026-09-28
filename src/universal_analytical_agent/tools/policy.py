"""Small, explicit policy boundary for deterministic tool execution."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from universal_analytical_agent.domain.contracts import ToolInvocation
from universal_analytical_agent.tools.registry import ToolDefinition


@dataclass(frozen=True, slots=True)
class ToolExecutionContext:
    """Execution facts available to policy without adding identity or authorization."""

    approval_granted: bool = False


@dataclass(frozen=True, slots=True)
class ToolPolicyDecision:
    """Allow/deny outcome with a safe reason for future events and results."""

    allowed: bool
    reason: str | None = None


class ToolExecutionPolicy(Protocol):
    """Policy contract evaluated before a tool handler is invoked."""

    def evaluate(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
        context: ToolExecutionContext,
    ) -> ToolPolicyDecision:
        """Return whether this specific invocation may execute."""


class DefaultToolExecutionPolicy:
    """Allow deterministic tools unless their declared approval gate is unmet."""

    def evaluate(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
        context: ToolExecutionContext,
    ) -> ToolPolicyDecision:
        del invocation
        if definition.requires_approval and not context.approval_granted:
            return ToolPolicyDecision(allowed=False, reason="Human approval is required")
        return ToolPolicyDecision(allowed=True)
