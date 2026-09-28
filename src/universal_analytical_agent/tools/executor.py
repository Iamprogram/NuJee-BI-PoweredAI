"""Safe, deterministic tool execution without planning or tool selection."""

from __future__ import annotations

import inspect
from collections.abc import Mapping

from universal_analytical_agent.domain.contracts import (
    ExecutionStatus,
    StructuredError,
    ToolInvocation,
    ToolResult,
)
from universal_analytical_agent.errors import ToolError, ValidationError
from universal_analytical_agent.observability.events import EventType, RunEvent
from universal_analytical_agent.tools.policy import (
    DefaultToolExecutionPolicy,
    ToolExecutionContext,
    ToolExecutionPolicy,
)
from universal_analytical_agent.tools.registry import ToolDefinition, ToolRegistry
from universal_analytical_agent.tools.validation import validate_tool_input


class ToolEventSink:
    """In-memory event sink suitable for tests and future persistence adapters."""

    def __init__(self) -> None:
        self.events: list[RunEvent] = []

    def emit(self, event: RunEvent) -> None:
        """Record one structured event."""
        self.events.append(event)


class ToolExecutor:
    """Execute a caller-selected registered tool through validation and policy gates.

    This class never chooses a tool, calls an LLM, or grants approval. It is
    asynchronous so sync and async deterministic handlers share one interface.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        policy: ToolExecutionPolicy | None = None,
        event_sink: ToolEventSink | None = None,
    ) -> None:
        self._registry = registry
        self._policy = policy or DefaultToolExecutionPolicy()
        self._event_sink = event_sink or ToolEventSink()

    def available_definitions(self) -> tuple[ToolDefinition, ...]:
        """Return registered metadata for an agent prompt without exposing handlers."""
        return self._registry.definitions()

    @property
    def event_sink(self) -> ToolEventSink:
        """Expose emitted events for observability consumers and tests."""
        return self._event_sink

    async def execute(
        self,
        invocation: ToolInvocation,
        context: ToolExecutionContext | None = None,
    ) -> ToolResult:
        """Validate, authorize, invoke, and normalize one caller-selected tool."""
        execution_context = context or ToolExecutionContext()
        self._emit(EventType.TOOL_REQUESTED, invocation)
        try:
            registered_tool = self._registry.get(invocation.tool_name)
        except ToolError:
            return self._failure(invocation, "tool_unknown", "Requested tool is not registered")

        try:
            validate_tool_input(registered_tool.definition.input_schema, invocation.arguments)
        except ValidationError as error:
            self._emit(EventType.TOOL_VALIDATION_FAILED, invocation, code="tool_validation")
            return self._result_error(
                invocation,
                ExecutionStatus.FAILED,
                "tool_validation",
                str(error),
            )

        try:
            decision = self._policy.evaluate(
                registered_tool.definition,
                invocation,
                execution_context,
            )
        except Exception:
            return self._failure(
                invocation,
                "tool_internal",
                "Tool execution policy failed unexpectedly",
            )
        if not decision.allowed:
            self._emit(EventType.TOOL_EXECUTION_DENIED, invocation, reason=decision.reason)
            return self._result_error(
                invocation,
                ExecutionStatus.DENIED,
                "tool_policy_denied",
                decision.reason or "Tool execution is denied by policy",
            )

        self._emit(EventType.TOOL_EXECUTION_STARTED, invocation)
        try:
            output = registered_tool.handler.invoke(invocation)
            if inspect.isawaitable(output):
                output = await output
            if not isinstance(output, Mapping):
                raise ToolError("Tool handler must return a mapping")
        except ToolError as error:
            return self._failure(invocation, "tool_execution", str(error))
        except Exception:
            return self._failure(
                invocation,
                "tool_internal",
                "Tool execution failed unexpectedly",
            )

        self._emit(EventType.TOOL_COMPLETED, invocation)
        return ToolResult(invocation=invocation, status=ExecutionStatus.COMPLETED, output=output)

    def _failure(self, invocation: ToolInvocation, code: str, message: str) -> ToolResult:
        self._emit(EventType.TOOL_EXECUTION_FAILED, invocation, code=code)
        return self._result_error(invocation, ExecutionStatus.FAILED, code, message)

    @staticmethod
    def _result_error(
        invocation: ToolInvocation,
        status: ExecutionStatus,
        code: str,
        message: str,
    ) -> ToolResult:
        return ToolResult(
            invocation=invocation,
            status=status,
            error=StructuredError(code=code, message=message, category="tool"),
        )

    def _emit(self, event_type: EventType, invocation: ToolInvocation, **payload: object) -> None:
        self._event_sink.emit(
            RunEvent(
                run_id=invocation.run_id,
                event_type=event_type,
                payload={"tool_name": invocation.tool_name, **payload},
            )
        )
