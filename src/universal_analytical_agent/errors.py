"""Explicit errors raised at application boundaries."""

from __future__ import annotations

from universal_analytical_agent.domain.contracts import StructuredError


class FoundationError(Exception):
    """Base error for the foundation layer."""


class ConfigurationError(FoundationError):
    """Raised when environment-based settings are invalid or incomplete."""


class ProviderError(FoundationError):
    """Provider failure translated into a project-owned structured error."""

    def __init__(self, code: str, message: str, *, retryable: bool = False) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.retryable = retryable

    def to_structured_error(self) -> StructuredError:
        """Return safe error data for future responses and run events."""
        return StructuredError(
            code=self.code,
            message=self.message,
            category="provider",
            retryable=self.retryable,
        )


class ToolError(FoundationError):
    """Raised when a tool contract or invocation fails."""


class ValidationError(FoundationError):
    """Raised when a boundary value violates an explicit contract."""


class RuntimeError(FoundationError):
    """Raised when a future agent runtime cannot progress safely."""
