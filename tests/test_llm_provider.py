from __future__ import annotations

import asyncio

import pytest

from universal_analytical_agent.errors import ProviderError
from universal_analytical_agent.llm.fake import FakeLLMProvider
from universal_analytical_agent.llm.provider import (
    GenerationOptions,
    LLMMessage,
    LLMProvider,
    LLMRequest,
    MessageRole,
)


def test_llm_request_represents_messages_options_and_run_correlation() -> None:
    request = LLMRequest(
        model="test-model",
        messages=(
            LLMMessage(MessageRole.SYSTEM, "Be concise."),
            LLMMessage(MessageRole.USER, "Hello"),
        ),
        generation=GenerationOptions(temperature=0.2, max_tokens=32),
    )

    assert request.messages[0].role is MessageRole.SYSTEM
    assert request.generation.max_tokens == 32
    assert request.model == "test-model"


def test_fake_provider_returns_configured_deterministic_response() -> None:
    provider: LLMProvider = FakeLLMProvider(response_text="deterministic", response_model="fake-v1")
    request = LLMRequest(messages=(LLMMessage(MessageRole.USER, "Hello"),))

    completion = asyncio.run(provider.complete(request))

    assert completion.text == "deterministic"
    assert completion.provider == "fake"
    assert completion.model == "fake-v1"


def test_fake_provider_raises_configured_project_error() -> None:
    failure = ProviderError("provider_connection", "Connection unavailable", retryable=True)
    provider = FakeLLMProvider(failure=failure)

    with pytest.raises(ProviderError) as error:
        asyncio.run(provider.complete(LLMRequest(messages=())))

    assert error.value.to_structured_error().code == "provider_connection"
    assert error.value.to_structured_error().retryable is True
