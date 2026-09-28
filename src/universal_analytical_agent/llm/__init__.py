"""Vendor-neutral LLM contracts and approved provider adapters."""

from universal_analytical_agent.llm.fake import FakeLLMProvider
from universal_analytical_agent.llm.ollama import OllamaProvider, OllamaProviderConfig
from universal_analytical_agent.llm.provider import (
    GenerationOptions,
    LLMCompletion,
    LLMMessage,
    LLMProvider,
    LLMRequest,
    LLMUsage,
    MessageRole,
)

__all__ = [
    "FakeLLMProvider",
    "GenerationOptions",
    "LLMCompletion",
    "LLMMessage",
    "LLMProvider",
    "LLMRequest",
    "LLMUsage",
    "MessageRole",
    "OllamaProvider",
    "OllamaProviderConfig",
]
