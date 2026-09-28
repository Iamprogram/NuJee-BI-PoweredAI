from __future__ import annotations

import asyncio

from universal_analytical_agent.agent.runtime import AgentRuntime
from universal_analytical_agent.domain.contracts import ExecutionStatus, RunId
from universal_analytical_agent.errors import ProviderError
from universal_analytical_agent.llm.fake import FakeLLMProvider
from universal_analytical_agent.observability.events import EventType
from universal_analytical_agent.tools.examples import AdditionTool
from universal_analytical_agent.tools.executor import ToolEventSink, ToolExecutor
from universal_analytical_agent.tools.policy import ToolExecutionContext, ToolPolicyDecision
from universal_analytical_agent.tools.registry import ToolDefinition, ToolRegistry


class DenyPolicy:
    def evaluate(
        self,
        definition: ToolDefinition,
        invocation: object,
        context: ToolExecutionContext,
    ) -> ToolPolicyDecision:
        del definition, invocation, context
        return ToolPolicyDecision(allowed=False, reason="Approval required")


class BrokenTool:
    definition = ToolDefinition(
        name="broken",
        description="Always fails for runtime testing.",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )

    def invoke(self, invocation: object) -> dict[str, object]:
        del invocation
        raise RuntimeError("handler details must not leak")


def _runtime(
    responses: tuple[str, ...],
    *,
    max_steps: int = 4,
    policy: DenyPolicy | None = None,
    include_broken_tool: bool = False,
) -> tuple[AgentRuntime, ToolEventSink]:
    registry = ToolRegistry()
    registry.register(AdditionTool.definition, AdditionTool())
    if include_broken_tool:
        registry.register(BrokenTool.definition, BrokenTool())
    sink = ToolEventSink()
    executor = ToolExecutor(registry, policy=policy, event_sink=sink)
    runtime = AgentRuntime(
        FakeLLMProvider(scripted_responses=responses),
        executor,
        max_steps=max_steps,
    )
    return runtime, sink


def test_runtime_returns_final_response_without_tool() -> None:
    runtime, sink = _runtime(('{"action":"final","content":"Hello"}',))

    state = asyncio.run(runtime.run("Greet me"))

    assert state.status is ExecutionStatus.COMPLETED
    assert state.final_response == "Hello"
    assert state.current_step == 1
    assert state.tool_results == ()
    assert [event.event_type for event in sink.events] == [
        EventType.RUN_STARTED,
        EventType.LLM_REQUESTED,
        EventType.AGENT_ACTION_RECEIVED,
        EventType.FINAL_RESPONSE_PRODUCED,
    ]


def test_runtime_executes_tool_through_executor_then_returns_final_response() -> None:
    runtime, sink = _runtime(
        (
            '{"action":"tool_call","tool_name":"addition","arguments":{"left":2,"right":3}}',
            '{"action":"final","content":"The total is 5."}',
        )
    )
    run_id = RunId.new()

    state = asyncio.run(runtime.run("What is 2 plus 3?", run_id=run_id))

    assert state.status is ExecutionStatus.COMPLETED
    assert state.final_response == "The total is 5."
    assert state.current_step == 2
    assert state.tool_results[0].output == {"sum": 5}
    assert state.tool_invocations[0].run_id == run_id
    assert all(event.run_id == run_id for event in sink.events)
    assert EventType.TOOL_EXECUTION_STARTED in [event.event_type for event in sink.events]
    assert EventType.TOOL_COMPLETED in [event.event_type for event in sink.events]


def test_runtime_supports_multiple_sequential_tool_calls() -> None:
    runtime, _ = _runtime(
        (
            '{"action":"tool_call","tool_name":"addition","arguments":{"left":1,"right":2}}',
            '{"action":"tool_call","tool_name":"addition","arguments":{"left":3,"right":4}}',
            '{"action":"final","content":"Completed both sums."}',
        )
    )

    state = asyncio.run(runtime.run("Perform two additions"))

    assert state.status is ExecutionStatus.COMPLETED
    assert [result.output for result in state.tool_results] == [{"sum": 3}, {"sum": 7}]
    assert state.current_step == 3


def test_runtime_fails_for_unknown_tool() -> None:
    runtime, _ = _runtime(('{"action":"tool_call","tool_name":"unknown","arguments":{}}',))

    state = asyncio.run(runtime.run("Use an unknown tool"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "tool_unknown"


def test_runtime_fails_for_invalid_tool_arguments_without_executing_tool() -> None:
    invalid_action = '{"action":"tool_call","tool_name":"addition","arguments":{"left":"x"}}'
    runtime, _ = _runtime((invalid_action,))

    state = asyncio.run(runtime.run("Call addition incorrectly"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "tool_validation"


def test_runtime_fails_for_policy_denial() -> None:
    runtime, _ = _runtime(
        ('{"action":"tool_call","tool_name":"addition","arguments":{"left":1,"right":2}}',),
        policy=DenyPolicy(),
    )

    state = asyncio.run(runtime.run("Call a denied tool"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "tool_policy_denied"


def test_runtime_fails_for_tool_exception_without_leaking_exception_text() -> None:
    runtime, _ = _runtime(
        ('{"action":"tool_call","tool_name":"broken","arguments":{}}',),
        include_broken_tool=True,
    )

    state = asyncio.run(runtime.run("Call broken"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "tool_internal"
    assert "handler details" not in state.errors[-1].message


def test_runtime_rejects_malformed_model_action() -> None:
    runtime, _ = _runtime(("not JSON",))

    state = asyncio.run(runtime.run("Malformed output"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "agent_invalid_action"


def test_runtime_preserves_provider_failure() -> None:
    registry = ToolRegistry()
    sink = ToolEventSink()
    provider = FakeLLMProvider(
        failure=ProviderError("provider_timeout", "Timed out", retryable=True)
    )
    runtime = AgentRuntime(provider, ToolExecutor(registry, event_sink=sink))

    state = asyncio.run(runtime.run("Provider fails"))

    assert state.status is ExecutionStatus.FAILED
    assert state.errors[-1].code == "provider_timeout"
    assert state.errors[-1].category == "provider"


def test_runtime_stops_at_maximum_step_limit() -> None:
    repeated_tool_action = (
        '{"action":"tool_call","tool_name":"addition","arguments":{"left":1,"right":1}}'
    )
    runtime, sink = _runtime(
        (repeated_tool_action, repeated_tool_action, repeated_tool_action),
        max_steps=2,
    )

    state = asyncio.run(runtime.run("Repeat forever"))

    assert state.status is ExecutionStatus.FAILED
    assert state.current_step == 2
    assert state.errors[-1].code == "agent_step_limit"
    assert EventType.STEP_LIMIT_REACHED in [event.event_type for event in sink.events]
    assert sink.events[-1].event_type is EventType.RUN_FAILED
