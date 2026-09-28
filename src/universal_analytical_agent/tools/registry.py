"""Tool metadata and a minimal in-memory registry."""

from __future__ import annotations

import re
from collections.abc import Awaitable, Mapping
from dataclasses import dataclass
from typing import Protocol, TypeAlias

from universal_analytical_agent.domain.contracts import ToolInvocation
from universal_analytical_agent.errors import ToolError

_TOOL_NAME = re.compile(r"^[a-z][a-z0-9_]{0,63}$")
ToolOutput: TypeAlias = Mapping[str, object]


@dataclass(frozen=True, slots=True)
class ToolDefinition:
    """Discoverable metadata and schemas for one explicitly registered tool."""

    name: str
    description: str
    input_schema: Mapping[str, object]
    output_schema: Mapping[str, object]
    is_read_only: bool = True
    requires_approval: bool = False


class ToolHandler(Protocol):
    """A deterministic handler independent of the LLM and agent runtime."""

    def invoke(self, invocation: ToolInvocation) -> ToolOutput | Awaitable[ToolOutput]:
        """Return normalized output for one already validated invocation."""


@dataclass(frozen=True, slots=True)
class RegisteredTool:
    """Associates public tool metadata with its private handler."""

    definition: ToolDefinition
    handler: ToolHandler


class ToolRegistry:
    """Registry that makes tool discovery explicit and validates registrations."""

    def __init__(self) -> None:
        self._tools: dict[str, RegisteredTool] = {}

    def register(self, definition: ToolDefinition, handler: ToolHandler) -> None:
        """Register a uniquely named tool with non-empty metadata and schemas."""
        if not _TOOL_NAME.fullmatch(definition.name):
            raise ToolError("Tool names must use lowercase letters, digits, and underscores")
        if not definition.description.strip():
            raise ToolError("Tool descriptions must not be empty")
        if not definition.input_schema or not definition.output_schema:
            raise ToolError("Tool input and output schemas must be specified")
        if definition.name in self._tools:
            raise ToolError(f"Tool is already registered: {definition.name}")
        self._tools[definition.name] = RegisteredTool(definition=definition, handler=handler)

    def get(self, name: str) -> RegisteredTool:
        """Return a registered tool or raise an explicit error."""
        try:
            return self._tools[name]
        except KeyError as error:
            raise ToolError(f"Tool is not registered: {name}") from error

    def definitions(self) -> tuple[ToolDefinition, ...]:
        """Return definitions in registration order for future discovery."""
        return tuple(tool.definition for tool in self._tools.values())
