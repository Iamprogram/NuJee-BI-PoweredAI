from __future__ import annotations

import asyncio
from collections.abc import Mapping
from typing import cast

from universal_analytical_agent.domain.contracts import ExecutionStatus, RunId, ToolInvocation
from universal_analytical_agent.observability.events import EventType
from universal_analytical_agent.tools.examples import AdditionTool
from universal_analytical_agent.tools.executor import ToolEventSink, ToolExecutor
from universal_analytical_agent.tools.policy import ToolExecutionContext, ToolPolicyDecision
from universal_analytical_agent.tools.registry import ToolDefinition, ToolRegistry


class CountingTool:
    def __init__(self) -> None:
        self.calls = 0

    def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        self.calls += 1
        return {"echo": invocation.arguments["value"]}


class FailingTool:
    def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        del invocation
        raise RuntimeError("private handler failure")


class BadOutputTool:
    def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        del invocation
        return cast(Mapping[str, object], "wrong output type")


class AsyncEchoTool:
    async def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        return {"echo": invocation.arguments["value"]}


class DenyPolicy:
    def evaluate(
        self,
        definition: ToolDefinition,
        invocation: ToolInvocation,
        context: ToolExecutionContext,
    ) -> ToolPolicyDecision:
        del definition, invocation, context
        return ToolPolicyDecision(allowed=False, reason="Test policy denied this tool")


def _invocation(name: str, arguments: Mapping[str, object]) -> ToolInvocation:
    return ToolInvocation(run_id=RunId.new(), tool_name=name, arguments=arguments)


def _registry_with_addition() -> ToolRegistry:
    registry = ToolRegistry()
    registry.register(AdditionTool.definition, AdditionTool())
    return registry


def _echo_definition() -> ToolDefinition:
    return ToolDefinition(
        name="echo",
        description="Echo a string.",
        input_schema={
            "type": "object",
            "properties": {"value": {"type": "string"}},
            "required": ["value"],
            "additionalProperties": False,
        },
        output_schema={"type": "object"},
    )


def test_executor_executes_valid_tool_and_preserves_invocation_and_events() -> None:
    sink = ToolEventSink()
    invocation = _invocation("addition", {"left": 2, "right": 3})
    result = asyncio.run(
        ToolExecutor(_registry_with_addition(), event_sink=sink).execute(invocation)
    )

    assert result.status is ExecutionStatus.COMPLETED
    assert result.error is None
    assert result.invocation is invocation
    assert result.output == {"sum": 5}
    assert [event.event_type for event in sink.events] == [
        EventType.TOOL_REQUESTED,
        EventType.TOOL_EXECUTION_STARTED,
        EventType.TOOL_COMPLETED,
    ]
    assert all(event.run_id == invocation.run_id for event in sink.events)


def test_unknown_tool_returns_structured_error() -> None:
    invocation = _invocation("missing_tool", {})
    result = asyncio.run(ToolExecutor(ToolRegistry()).execute(invocation))

    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error.code == "tool_unknown"
    assert result.invocation.run_id == invocation.run_id


def test_invalid_input_prevents_handler_execution_and_emits_validation_event() -> None:
    registry = ToolRegistry()
    tool = CountingTool()
    registry.register(_echo_definition(), tool)
    sink = ToolEventSink()
    result = asyncio.run(
        ToolExecutor(registry, event_sink=sink).execute(_invocation("echo", {"value": 4}))
    )

    assert result.error is not None
    assert result.error.code == "tool_validation"
    assert tool.calls == 0
    assert [event.event_type for event in sink.events] == [
        EventType.TOOL_REQUESTED,
        EventType.TOOL_VALIDATION_FAILED,
    ]


def test_policy_denial_prevents_handler_execution_and_emits_denial_event() -> None:
    registry = ToolRegistry()
    tool = CountingTool()
    registry.register(_echo_definition(), tool)
    sink = ToolEventSink()
    result = asyncio.run(
        ToolExecutor(registry, policy=DenyPolicy(), event_sink=sink).execute(
            _invocation("echo", {"value": "allowed shape"})
        )
    )

    assert result.status is ExecutionStatus.DENIED
    assert result.error is not None
    assert result.error.code == "tool_policy_denied"
    assert tool.calls == 0
    assert sink.events[-1].event_type is EventType.TOOL_EXECUTION_DENIED


def test_handler_failure_returns_safe_structured_error_and_event() -> None:
    registry = ToolRegistry()
    registry.register(_echo_definition(), FailingTool())
    sink = ToolEventSink()
    result = asyncio.run(
        ToolExecutor(registry, event_sink=sink).execute(_invocation("echo", {"value": "value"}))
    )

    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error.code == "tool_internal"
    assert result.error.message == "Tool execution failed unexpectedly"
    assert sink.events[-1].event_type is EventType.TOOL_EXECUTION_FAILED


def test_handler_contract_failure_is_distinguished_from_unexpected_failure() -> None:
    registry = ToolRegistry()
    registry.register(_echo_definition(), BadOutputTool())
    result = asyncio.run(ToolExecutor(registry).execute(_invocation("echo", {"value": "value"})))

    assert result.status is ExecutionStatus.FAILED
    assert result.error is not None
    assert result.error.code == "tool_execution"


def test_executor_supports_async_handlers() -> None:
    registry = ToolRegistry()
    registry.register(_echo_definition(), AsyncEchoTool())

    result = asyncio.run(
        ToolExecutor(registry).execute(_invocation("echo", {"value": "asynchronous"}))
    )

    assert result.status is ExecutionStatus.COMPLETED
    assert result.output == {"echo": "asynchronous"}
