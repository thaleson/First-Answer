"""Shared application exceptions used across layers."""


class ApplicationError(Exception):
    """Base exception for project-specific application errors."""

    pass


class GroqConnectionError(ApplicationError):
    """Raised when communication with the Groq API fails."""

    pass


class InvalidLLMResponseError(ApplicationError):
    """Raised when the LLM output cannot be parsed or validated."""

    pass


class InputValidationError(ApplicationError):
    """Raised when required runtime configuration is missing or invalid."""

    pass
