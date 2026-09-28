"""Dependency-free validation for the deliberately small supported schema subset."""

from __future__ import annotations

from collections.abc import Mapping

from universal_analytical_agent.errors import ValidationError


def validate_tool_input(schema: Mapping[str, object], arguments: Mapping[str, object]) -> None:
    """Validate object input using ``type``, ``properties``, ``required``, and extra keys.

    Property schemas support the JSON-schema primitive names ``string``, ``integer``,
    ``number``, ``boolean``, ``object``, and ``array``. This narrow subset is enough
    for explicit test tools while avoiding a runtime schema-library dependency.
    """
    if schema.get("type") != "object":
        raise ValidationError("Tool input schema must declare type=object")
    properties = schema.get("properties", {})
    if not isinstance(properties, Mapping):
        raise ValidationError("Tool input schema properties must be an object")
    required = schema.get("required", ())
    if not isinstance(required, list | tuple) or not all(
        isinstance(name, str) for name in required
    ):
        raise ValidationError("Tool input schema required must be a list of property names")
    for name in required:
        if name not in arguments:
            raise ValidationError(f"Missing required tool argument: {name}")
    if schema.get("additionalProperties") is False:
        unknown = set(arguments).difference(properties)
        if unknown:
            raise ValidationError(f"Unexpected tool argument: {sorted(unknown)[0]}")
    for name, value in arguments.items():
        property_schema = properties.get(name)
        if property_schema is None:
            continue
        if not isinstance(property_schema, Mapping):
            raise ValidationError(f"Tool schema for {name} must be an object")
        expected_type = property_schema.get("type")
        if isinstance(expected_type, str) and not _matches_type(value, expected_type):
            raise ValidationError(f"Tool argument {name} must be of type {expected_type}")


def _matches_type(value: object, expected_type: str) -> bool:
    if expected_type == "string":
        return isinstance(value, str)
    if expected_type == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if expected_type == "number":
        return isinstance(value, int | float) and not isinstance(value, bool)
    if expected_type == "boolean":
        return isinstance(value, bool)
    if expected_type == "object":
        return isinstance(value, Mapping)
    if expected_type == "array":
        return isinstance(value, list | tuple)
    raise ValidationError(f"Unsupported tool schema type: {expected_type}")
