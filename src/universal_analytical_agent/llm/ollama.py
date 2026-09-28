"""Small HTTP-based Ollama adapter kept behind the provider-neutral contract."""

from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from universal_analytical_agent.errors import ProviderError
from universal_analytical_agent.llm.provider import (
    LLMCompletion,
    LLMMessage,
    LLMProvider,
    LLMRequest,
    LLMUsage,
)

if TYPE_CHECKING:
    from universal_analytical_agent.config import Settings


@dataclass(frozen=True, slots=True)
class OllamaProviderConfig:
    """Validated non-secret configuration for one Ollama endpoint."""

    base_url: str
    model: str
    timeout_seconds: float

    @classmethod
    def from_settings(cls, settings: Settings) -> OllamaProviderConfig:
        """Create provider configuration from the optional application settings."""
        if settings.ollama_base_url is None:
            raise ProviderError(
                "provider_configuration", "UAA_OLLAMA_BASE_URL is required for Ollama"
            )
        if settings.ollama_model is None:
            raise ProviderError("provider_configuration", "UAA_OLLAMA_MODEL is required for Ollama")
        if settings.ollama_timeout_seconds is None:
            raise ProviderError(
                "provider_configuration", "UAA_OLLAMA_TIMEOUT_SECONDS is required for Ollama"
            )
        return cls(
            base_url=settings.ollama_base_url,
            model=settings.ollama_model,
            timeout_seconds=settings.ollama_timeout_seconds,
        )

    def __post_init__(self) -> None:
        if not self.base_url.startswith(("http://", "https://")):
            raise ProviderError("provider_configuration", "Ollama base URL must use http or https")
        if not self.model.strip():
            raise ProviderError("provider_configuration", "Ollama model must not be empty")
        if self.timeout_seconds <= 0:
            raise ProviderError(
                "provider_configuration", "Ollama timeout must be greater than zero"
            )


@dataclass(frozen=True, slots=True)
class HTTPResponse:
    """Minimal HTTP response used to isolate the adapter from a client library."""

    status_code: int
    body: bytes


class OllamaHTTPError(Exception):
    """HTTP failure represented without leaking an HTTP client exception."""

    def __init__(self, status_code: int, body: bytes) -> None:
        super().__init__(f"Ollama HTTP request failed with status {status_code}")
        self.status_code = status_code
        self.body = body


class OllamaHTTPTransport(Protocol):
    """Minimal injectable transport for the Ollama adapter."""

    def post(self, url: str, body: bytes, timeout_seconds: float) -> HTTPResponse:
        """Perform a JSON HTTP POST request."""


class UrllibOllamaTransport:
    """Standard-library HTTP transport; no third-party runtime dependency is needed."""

    def post(self, url: str, body: bytes, timeout_seconds: float) -> HTTPResponse:
        request = Request(
            url,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urlopen(request, timeout=timeout_seconds) as response:  # noqa: S310
                return HTTPResponse(status_code=response.status, body=response.read())
        except HTTPError as error:
            raise OllamaHTTPError(error.code, error.read()) from error


class OllamaProvider(LLMProvider):
    """Translate the neutral request/response contract to Ollama's chat endpoint."""

    def __init__(
        self,
        config: OllamaProviderConfig,
        transport: OllamaHTTPTransport | None = None,
    ) -> None:
        self._config = config
        self._transport = transport or UrllibOllamaTransport()

    async def complete(self, request: LLMRequest) -> LLMCompletion:
        """Generate non-streaming text and translate all failures to ``ProviderError``."""
        model = request.model or self._config.model
        payload = {
            "model": model,
            "messages": [self._message_payload(message) for message in request.messages],
            "stream": False,
            "options": self._options_payload(request),
        }
        try:
            response = self._transport.post(
                url=f"{self._config.base_url.rstrip('/')}/api/chat",
                body=json.dumps(payload).encode("utf-8"),
                timeout_seconds=self._config.timeout_seconds,
            )
            return self._parse_response(response, request, model)
        except ProviderError:
            raise
        except OllamaHTTPError as error:
            raise ProviderError(
                "provider_http", f"Ollama returned HTTP status {error.status_code}", retryable=True
            ) from error
        except TimeoutError:
            raise ProviderError(
                "provider_timeout", "Ollama request timed out", retryable=True
            ) from None
        except (ConnectionError, URLError, OSError):
            raise ProviderError(
                "provider_connection", "Unable to connect to Ollama", retryable=True
            ) from None
        except Exception as error:
            raise ProviderError(
                "provider_unexpected", "Unexpected Ollama provider failure"
            ) from error

    @staticmethod
    def _message_payload(message: LLMMessage) -> dict[str, str]:
        return {"role": message.role.value, "content": message.content}

    @staticmethod
    def _options_payload(request: LLMRequest) -> dict[str, float | int]:
        options: dict[str, float | int] = {}
        if request.generation.temperature is not None:
            options["temperature"] = request.generation.temperature
        if request.generation.max_tokens is not None:
            options["num_predict"] = request.generation.max_tokens
        return options

    @staticmethod
    def _parse_response(response: HTTPResponse, request: LLMRequest, model: str) -> LLMCompletion:
        if not 200 <= response.status_code < 300:
            raise ProviderError(
                "provider_http",
                f"Ollama returned HTTP status {response.status_code}",
                retryable=True,
            )
        try:
            parsed = json.loads(response.body.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ProviderError(
                "provider_malformed_response", "Ollama returned invalid JSON"
            ) from error
        if not isinstance(parsed, Mapping):
            raise ProviderError("provider_malformed_response", "Ollama response must be an object")
        message = parsed.get("message")
        if not isinstance(message, Mapping) or not isinstance(message.get("content"), str):
            raise ProviderError(
                "provider_malformed_response", "Ollama response is missing message content"
            )
        return LLMCompletion(
            text=message["content"],
            provider="ollama",
            model=OllamaProvider._string_or_default(parsed.get("model"), model),
            usage=OllamaProvider._usage(parsed),
            finish_reason=OllamaProvider._string_or_none(parsed.get("done_reason")),
            run_id=request.run_id,
        )

    @staticmethod
    def _usage(response: Mapping[str, object]) -> LLMUsage | None:
        input_tokens = OllamaProvider._integer_or_none(response.get("prompt_eval_count"))
        output_tokens = OllamaProvider._integer_or_none(response.get("eval_count"))
        if input_tokens is None and output_tokens is None:
            return None
        return LLMUsage(input_tokens=input_tokens, output_tokens=output_tokens)

    @staticmethod
    def _integer_or_none(value: object) -> int | None:
        return value if isinstance(value, int) and not isinstance(value, bool) else None

    @staticmethod
    def _string_or_none(value: object) -> str | None:
        return value if isinstance(value, str) else None

    @staticmethod
    def _string_or_default(value: object, default: str) -> str:
        return value if isinstance(value, str) else default
