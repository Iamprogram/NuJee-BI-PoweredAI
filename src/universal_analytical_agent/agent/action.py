"""Strict, provider-neutral actions interpreted from untrusted model text."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from enum import StrEnum

from universal_analytical_agent.errors import ValidationError


class AgentActionType(StrEnum):
    """The only actions a model may request in the minimal runtime."""

    FINAL = "final"
    TOOL_CALL = "tool_call"


@dataclass(frozen=True, slots=True)
class FinalResponseAction:
    """A completed response supplied by the model."""

    content: str
    action_type: AgentActionType = AgentActionType.FINAL


@dataclass(frozen=True, slots=True)
class ToolCallAction:
    """A request for the already-registered named tool only."""

    tool_name: str
    arguments: Mapping[str, object]
    action_type: AgentActionType = AgentActionType.TOOL_CALL


AgentAction = FinalResponseAction | ToolCallAction


def parse_agent_action(text: str) -> AgentAction:
    """Parse strict JSON without reinterpreting arbitrary text as an action."""
    try:
        raw_action = json.loads(text)
    except json.JSONDecodeError as error:
        raise ValidationError("Model output is not valid action JSON") from error
    if not isinstance(raw_action, Mapping):
        raise ValidationError("Model action must be a JSON object")
    action_type = raw_action.get("action")
    if action_type == AgentActionType.FINAL:
        content = raw_action.get("content")
        if not isinstance(content, str) or not content.strip():
            raise ValidationError("Final action requires non-empty string content")
        if set(raw_action) != {"action", "content"}:
            raise ValidationError("Final action contains unsupported fields")
        return FinalResponseAction(content=content)
    if action_type == AgentActionType.TOOL_CALL:
        tool_name = raw_action.get("tool_name")
        arguments = raw_action.get("arguments")
        if not isinstance(tool_name, str) or not tool_name:
            raise ValidationError("Tool action requires a non-empty tool_name")
        if not isinstance(arguments, Mapping) or not all(isinstance(key, str) for key in arguments):
            raise ValidationError("Tool action requires an object with string argument names")
        if set(raw_action) != {"action", "tool_name", "arguments"}:
            raise ValidationError("Tool action contains unsupported fields")
        return ToolCallAction(tool_name=tool_name, arguments=arguments)
    raise ValidationError("Model action is unsupported")
