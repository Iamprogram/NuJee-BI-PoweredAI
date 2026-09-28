from __future__ import annotations

import asyncio
import json
from dataclasses import dataclass, field

import pytest

from universal_analytical_agent.config import load_settings
from universal_analytical_agent.errors import ProviderError
from universal_analytical_agent.llm.ollama import HTTPResponse, OllamaProvider, OllamaProviderConfig
from universal_analytical_agent.llm.provider import (
    GenerationOptions,
    LLMMessage,
    LLMRequest,
    MessageRole,
)


@dataclass
class RecordingTransport:
    response: HTTPResponse | Exception
    requests: list[tuple[str, bytes, float]] = field(default_factory=list)

    def post(self, url: str, body: bytes, timeout_seconds: float) -> HTTPResponse:
        self.requests.append((url, body, timeout_seconds))
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


def _config() -> OllamaProviderConfig:
    return OllamaProviderConfig(
        base_url="https://ollama.example.test/",
        model="configured-model",
        timeout_seconds=12.5,
    )


def test_ollama_configuration_loads_from_environment_settings() -> None:
    settings = load_settings(
        {
            "UAA_OLLAMA_BASE_URL": "https://ollama.example.test",
            "UAA_OLLAMA_MODEL": "llama-test",
            "UAA_OLLAMA_TIMEOUT_SECONDS": "15",
        }
    )

    config = OllamaProviderConfig.from_settings(settings)

    assert config.base_url == "https://ollama.example.test"
    assert config.model == "llama-test"
    assert config.timeout_seconds == 15.0


def test_ollama_configuration_requires_all_provider_values() -> None:
    with pytest.raises(ProviderError, match="UAA_OLLAMA_BASE_URL"):
        OllamaProviderConfig.from_settings(load_settings({}))


def test_ollama_translates_request_and_response_without_network() -> None:
    transport = RecordingTransport(
        HTTPResponse(
            status_code=200,
            body=json.dumps(
                {
                    "model": "returned-model",
                    "message": {"role": "assistant", "content": "Hello from Ollama"},
                    "prompt_eval_count": 7,
                    "eval_count": 3,
                    "done_reason": "stop",
                }
            ).encode(),
        )
    )
    provider = OllamaProvider(_config(), transport)
    request = LLMRequest(
        messages=(
            LLMMessage(MessageRole.SYSTEM, "Be helpful."),
            LLMMessage(MessageRole.USER, "Hello"),
        ),
        generation=GenerationOptions(temperature=0.3, max_tokens=25),
    )

    completion = asyncio.run(provider.complete(request))

    url, raw_body, timeout = transport.requests[0]
    assert url == "https://ollama.example.test/api/chat"
    assert timeout == 12.5
    assert json.loads(raw_body) == {
        "model": "configured-model",
        "messages": [
            {"role": "system", "content": "Be helpful."},
            {"role": "user", "content": "Hello"},
        ],
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 25},
    }
    assert completion.text == "Hello from Ollama"
    assert completion.model == "returned-model"
    assert completion.usage is not None
    assert completion.usage.input_tokens == 7
    assert completion.usage.output_tokens == 3


def test_ollama_translates_timeout_to_project_error() -> None:
    provider = OllamaProvider(_config(), RecordingTransport(TimeoutError()))

    with pytest.raises(ProviderError) as error:
        asyncio.run(provider.complete(LLMRequest(messages=())))

    assert error.value.code == "provider_timeout"
    assert error.value.retryable is True


def test_ollama_rejects_malformed_response() -> None:
    provider = OllamaProvider(_config(), RecordingTransport(HTTPResponse(200, b"{not json")))

    with pytest.raises(ProviderError) as error:
        asyncio.run(provider.complete(LLMRequest(messages=())))

    assert error.value.code == "provider_malformed_response"


def test_ollama_translates_http_failure_to_project_error() -> None:
    provider = OllamaProvider(_config(), RecordingTransport(HTTPResponse(503, b"unavailable")))

    with pytest.raises(ProviderError) as error:
        asyncio.run(provider.complete(LLMRequest(messages=())))

    assert error.value.code == "provider_http"
    assert error.value.retryable is True


def test_ollama_translates_connection_failure_to_project_error() -> None:
    provider = OllamaProvider(_config(), RecordingTransport(ConnectionError()))

    with pytest.raises(ProviderError) as error:
        asyncio.run(provider.complete(LLMRequest(messages=())))

    assert error.value.code == "provider_connection"
    assert error.value.to_structured_error().category == "provider"
