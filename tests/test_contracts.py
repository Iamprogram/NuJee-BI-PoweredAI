from __future__ import annotations

from universal_analytical_agent.domain.contracts import (
    AgentRequest,
    AgentResponse,
    ExecutionStatus,
    RunId,
    StructuredError,
    ToolInvocation,
    ToolResult,
)


def test_domain_contracts_can_be_instantiated() -> None:
    run_id = RunId.new()
    request = AgentRequest(run_id=run_id, prompt="Summarize the result.")
    invocation = ToolInvocation(run_id=run_id, tool_name="example_tool", arguments={})
    result = ToolResult(invocation=invocation, status=ExecutionStatus.COMPLETED)
    response = AgentResponse(
        run_id=run_id,
        status=ExecutionStatus.FAILED,
        errors=(StructuredError("invalid", "Invalid request", "validation"),),
    )

    assert request.run_id == run_id
    assert result.invocation == invocation
    assert response.errors[0].retryable is False
