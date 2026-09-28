"""Provider-neutral contracts for non-streaming LLM text generation."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

from universal_analytical_agent.domain.contracts import RunId


class MessageRole(StrEnum):
    """Roles supported by the compact cross-provider message contract."""

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"


@dataclass(frozen=True, slots=True)
class LLMMessage:
    """One provider-neutral instruction or conversation message."""

    role: MessageRole
    content: str


@dataclass(frozen=True, slots=True)
class GenerationOptions:
    """Optional generation controls that adapters may translate when supported."""

    temperature: float | None = None
    max_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class LLMRequest:
    """A non-streaming text request independent of any provider SDK."""

    messages: tuple[LLMMessage, ...]
    model: str | None = None
    generation: GenerationOptions = GenerationOptions()
    run_id: RunId | None = None


@dataclass(frozen=True, slots=True)
class LLMUsage:
    """Token counts when a provider returns them."""

    input_tokens: int | None = None
    output_tokens: int | None = None


@dataclass(frozen=True, slots=True)
class LLMCompletion:
    """Provider-neutral text and metadata returned by one generation request."""

    text: str
    provider: str
    model: str
    usage: LLMUsage | None = None
    finish_reason: str | None = None
    run_id: RunId | None = None


class LLMProvider(Protocol):
    """Contract implemented by local, OpenAI-compatible, or other providers."""

    async def complete(self, request: LLMRequest) -> LLMCompletion:
        """Return one non-streaming completion without exposing SDK types."""
