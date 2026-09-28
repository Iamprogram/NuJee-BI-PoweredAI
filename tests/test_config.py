from __future__ import annotations

import pytest

from universal_analytical_agent.config import load_settings
from universal_analytical_agent.errors import ConfigurationError


def test_load_settings_uses_safe_defaults() -> None:
    settings = load_settings({})

    assert settings.environment == "development"
    assert settings.log_level == "INFO"
    assert settings.deployment_id is None
    assert settings.agent_max_steps == 4


def test_production_requires_deployment_id() -> None:
    with pytest.raises(ConfigurationError, match="UAA_DEPLOYMENT_ID"):
        load_settings({"UAA_ENVIRONMENT": "production"})


def test_load_settings_normalizes_valid_values() -> None:
    settings = load_settings(
        {
            "UAA_ENVIRONMENT": "TEST",
            "UAA_LOG_LEVEL": "warning",
            "UAA_DEPLOYMENT_ID": "test-runner",
        }
    )

    assert settings.environment == "test"
    assert settings.log_level == "WARNING"
    assert settings.deployment_id == "test-runner"


def test_load_settings_validates_agent_max_steps() -> None:
    with pytest.raises(ConfigurationError, match="UAA_AGENT_MAX_STEPS"):
        load_settings({"UAA_AGENT_MAX_STEPS": "0"})
