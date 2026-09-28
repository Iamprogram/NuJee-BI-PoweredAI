"""Bounded single-agent runtime with strict action parsing and tool boundaries."""

from __future__ import annotations

import json
from dataclasses import replace

from universal_analytical_agent.agent.action import (
    FinalResponseAction,
    ToolCallAction,
    parse_agent_action,
)
from universal_analytical_agent.agent.state import AgentRunState
from universal_analytical_agent.domain.contracts import (
    ExecutionStatus,
    RunId,
    StructuredError,
    ToolInvocation,
    ToolResult,
)
from universal_analytical_agent.errors import ProviderError, ValidationError
from universal_analytical_agent.llm.provider import LLMMessage, LLMProvider, LLMRequest, MessageRole
from universal_analytical_agent.observability.events import EventType, RunEvent
from universal_analytical_agent.tools.executor import ToolExecutor


class AgentRuntime:
    """Run one inspectable, bounded LLM-to-tool-to-final-response interaction."""

    def __init__(
        self,
        provider: LLMProvider,
        tool_executor: ToolExecutor,
        *,
        max_steps: int = 4,
    ) -> None:
        if max_steps <= 0:
            raise ValueError("max_steps must be greater than zero")
        self._provider = provider
        self._tool_executor = tool_executor
        self._max_steps = max_steps

    async def run(self, user_request: str, *, run_id: RunId | None = None) -> AgentRunState:
        """Execute until a final action, safe failure, or configured step limit."""
        state = self._initial_state(user_request, run_id or RunId.new())
        self._emit(EventType.RUN_STARTED, state)
        for _ in range(self._max_steps):
            state = replace(
                state,
                status=ExecutionStatus.RUNNING,
                current_step=state.current_step + 1,
            )
            self._emit(EventType.LLM_REQUESTED, state)
            try:
                completion = await self._provider.complete(
                    LLMRequest(messages=state.messages, run_id=state.run_id)
                )
            except ProviderError as error:
                return self._fail(state, error.to_structured_error())
            except Exception:
                return self._fail(
                    state,
                    StructuredError(
                        code="agent_provider_failure",
                        message="LLM provider failed unexpectedly",
                        category="agent",
                    ),
                )

            state = replace(
                state,
                messages=(*state.messages, LLMMessage(MessageRole.ASSISTANT, completion.text)),
            )
            try:
                action = parse_agent_action(completion.text)
            except ValidationError as error:
                return self._fail(
                    state,
                    StructuredError(
                        code="agent_invalid_action",
                        message=str(error),
                        category="agent",
                    ),
                )
            self._emit(EventType.AGENT_ACTION_RECEIVED, state, action=action.action_type.value)

            if isinstance(action, FinalResponseAction):
                state = replace(
                    state,
                    status=ExecutionStatus.COMPLETED,
                    final_response=action.content,
                )
                self._emit(EventType.FINAL_RESPONSE_PRODUCED, state)
                return state

            if isinstance(action, ToolCallAction):
                invocation = ToolInvocation(
                    run_id=state.run_id,
                    tool_name=action.tool_name,
                    arguments=action.arguments,
                )
                result = await self._tool_executor.execute(invocation)
                state = replace(
                    state,
                    tool_invocations=(*state.tool_invocations, invocation),
                    tool_results=(*state.tool_results, result),
                    messages=(*state.messages, self._tool_result_message(result)),
                )
                if result.status is not ExecutionStatus.COMPLETED:
                    assert result.error is not None
                    return self._fail(state, result.error)
                continue

        self._emit(EventType.STEP_LIMIT_REACHED, state)
        return self._fail(
            state,
            StructuredError(
                code="agent_step_limit",
                message=f"Agent exceeded the maximum of {self._max_steps} steps",
                category="agent",
            ),
        )

    def _initial_state(self, user_request: str, run_id: RunId) -> AgentRunState:
        definitions = self._tool_executor.available_definitions()
        tools = "; ".join(f"{tool.name}: {tool.description}" for tool in definitions) or "none"
        instructions = (
            "Return exactly one JSON object. Choose either final response "
            '{"action":"final","content":"..."} or a tool call '
            '{"action":"tool_call","tool_name":"...","arguments":{...}}. '
            f"Available tools: {tools}. Do not invent tools. Use a tool only when needed; "
            "return a final response when sufficient information is available."
        )
        return AgentRunState(
            run_id=run_id,
            user_request=user_request,
            messages=(
                LLMMessage(MessageRole.SYSTEM, instructions),
                LLMMessage(MessageRole.USER, user_request),
            ),
        )

    @staticmethod
    def _tool_result_message(result: ToolResult) -> LLMMessage:
        payload = {
            "tool_name": result.invocation.tool_name,
            "status": result.status.value,
            "output": result.output,
            "error": result.error.code if result.error is not None else None,
        }
        return LLMMessage(
            MessageRole.USER,
            f"Tool result: {json.dumps(payload, sort_keys=True, default=str)}",
        )

    def _fail(self, state: AgentRunState, error: StructuredError) -> AgentRunState:
        failed_state = state.with_error(error)
        self._emit(EventType.RUN_FAILED, failed_state, code=error.code)
        return failed_state

    def _emit(self, event_type: EventType, state: AgentRunState, **payload: object) -> None:
        self._tool_executor.event_sink.emit(
            RunEvent(run_id=state.run_id, event_type=event_type, payload=payload)
        )
