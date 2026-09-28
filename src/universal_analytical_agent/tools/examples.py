"""Tiny deterministic infrastructure-test tools; not product capabilities."""

from __future__ import annotations

from collections.abc import Mapping

from universal_analytical_agent.domain.contracts import ToolInvocation
from universal_analytical_agent.tools.registry import ToolDefinition


class AdditionTool:
    """Return the deterministic sum of two integer inputs."""

    definition = ToolDefinition(
        name="addition",
        description="Add two integer values.",
        input_schema={
            "type": "object",
            "properties": {"left": {"type": "integer"}, "right": {"type": "integer"}},
            "required": ["left", "right"],
            "additionalProperties": False,
        },
        output_schema={
            "type": "object",
            "properties": {"sum": {"type": "integer"}},
            "required": ["sum"],
        },
    )

    def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        """Return the validated sum without external effects."""
        left = invocation.arguments["left"]
        right = invocation.arguments["right"]
        assert isinstance(left, int)
        assert isinstance(right, int)
        return {"sum": left + right}
