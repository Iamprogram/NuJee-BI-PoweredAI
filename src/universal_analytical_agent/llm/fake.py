"""Deterministic provider implementation for offline tests and runtime fixtures."""

from __future__ import annotations

from dataclasses import dataclass, field

from universal_analytical_agent.errors import ProviderError
from universal_analytical_agent.llm.provider import LLMCompletion, LLMProvider, LLMRequest


@dataclass(slots=True)
class FakeLLMProvider(LLMProvider):
    """Return configured responses or a project-level failure without network access."""

    response_text: str = "fake response"
    response_model: str = "fake-model"
    failure: ProviderError | None = None
    scripted_responses: tuple[str, ...] = ()
    requests: list[LLMRequest] = field(default_factory=list)
    _response_index: int = field(default=0, init=False)

    async def complete(self, request: LLMRequest) -> LLMCompletion:
        """Record the request and deterministically return or raise the configured outcome."""
        self.requests.append(request)
        if self.failure is not None:
            raise self.failure
        text = self._next_response()
        return LLMCompletion(
            text=text,
            provider="fake",
            model=request.model or self.response_model,
            run_id=request.run_id,
        )

    def _next_response(self) -> str:
        if not self.scripted_responses:
            return self.response_text
        if self._response_index >= len(self.scripted_responses):
            raise ProviderError(
                "provider_script_exhausted", "Fake provider response script is exhausted"
            )
        response = self.scripted_responses[self._response_index]
        self._response_index += 1
        return response
