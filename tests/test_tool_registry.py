from __future__ import annotations

from collections.abc import Mapping

import pytest

from universal_analytical_agent.domain.contracts import ToolInvocation
from universal_analytical_agent.errors import ToolError
from universal_analytical_agent.tools.registry import ToolDefinition, ToolRegistry


class DummyTool:
    def invoke(self, invocation: ToolInvocation) -> Mapping[str, object]:
        return {"tool": invocation.tool_name}


def _definition(name: str = "example_tool") -> ToolDefinition:
    return ToolDefinition(
        name=name,
        description="A deterministic test tool.",
        input_schema={"type": "object"},
        output_schema={"type": "object"},
    )


def test_tool_registration_supports_lookup_and_discovery() -> None:
    registry = ToolRegistry()
    definition = _definition()

    registry.register(definition, DummyTool())

    assert registry.get("example_tool").definition == definition
    assert registry.definitions() == (definition,)


def test_duplicate_tool_registration_is_rejected() -> None:
    registry = ToolRegistry()
    registry.register(_definition(), DummyTool())

    with pytest.raises(ToolError, match="already registered"):
        registry.register(_definition(), DummyTool())


def test_invalid_tool_registration_is_rejected() -> None:
    registry = ToolRegistry()

    with pytest.raises(ToolError, match="lowercase"):
        registry.register(_definition("Invalid-name"), DummyTool())
