from __future__ import annotations

import universal_analytical_agent


def test_package_imports() -> None:
    assert universal_analytical_agent.load_settings({}).environment == "development"
