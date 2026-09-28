"""Typed, environment-based application configuration."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from os import environ

from universal_analytical_agent.errors import ConfigurationError

_VALID_ENVIRONMENTS = frozenset({"development", "test", "production"})
_VALID_LOG_LEVELS = frozenset({"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"})


@dataclass(frozen=True, slots=True)
class Settings:
    """Non-secret settings needed by the foundation layer.

    ``deployment_id`` is required only in production so operational events can
    identify their originating deployment. Ollama values are optional until an
    ``OllamaProvider`` is selected; that adapter validates their completeness.
    """

    environment: str
    log_level: str
    deployment_id: str | None
    ollama_base_url: str | None = None
    ollama_model: str | None = None
    ollama_timeout_seconds: float | None = None
    agent_max_steps: int = 4


def load_settings(environment: Mapping[str, str] | None = None) -> Settings:
    """Load and validate settings from a supplied mapping or process environment."""
    values = environ if environment is None else environment
    app_environment = values.get("UAA_ENVIRONMENT", "development").lower()
    log_level = values.get("UAA_LOG_LEVEL", "INFO").upper()
    deployment_id = values.get("UAA_DEPLOYMENT_ID") or None
    ollama_base_url = values.get("UAA_OLLAMA_BASE_URL") or None
    ollama_model = values.get("UAA_OLLAMA_MODEL") or None
    ollama_timeout_seconds = _optional_positive_float(values, "UAA_OLLAMA_TIMEOUT_SECONDS")
    agent_max_steps = _positive_int(values, "UAA_AGENT_MAX_STEPS", default=4)

    if app_environment not in _VALID_ENVIRONMENTS:
        raise ConfigurationError(
            "UAA_ENVIRONMENT must be one of: " + ", ".join(sorted(_VALID_ENVIRONMENTS))
        )
    if log_level not in _VALID_LOG_LEVELS:
        raise ConfigurationError("UAA_LOG_LEVEL must be a standard Python log level")
    if app_environment == "production" and deployment_id is None:
        raise ConfigurationError("UAA_DEPLOYMENT_ID is required when UAA_ENVIRONMENT=production")

    return Settings(
        environment=app_environment,
        log_level=log_level,
        deployment_id=deployment_id,
        ollama_base_url=ollama_base_url,
        ollama_model=ollama_model,
        ollama_timeout_seconds=ollama_timeout_seconds,
        agent_max_steps=agent_max_steps,
    )


def _optional_positive_float(values: Mapping[str, str], name: str) -> float | None:
    raw_value = values.get(name)
    if raw_value is None or not raw_value.strip():
        return None
    try:
        value = float(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} must be a number") from error
    if value <= 0:
        raise ConfigurationError(f"{name} must be greater than zero")
    return value


def _positive_int(values: Mapping[str, str], name: str, *, default: int) -> int:
    raw_value = values.get(name)
    if raw_value is None or not raw_value.strip():
        return default
    try:
        value = int(raw_value)
    except ValueError as error:
        raise ConfigurationError(f"{name} must be an integer") from error
    if value <= 0:
        raise ConfigurationError(f"{name} must be greater than zero")
    return value
