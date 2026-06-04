import os
from dataclasses import dataclass

from app.shared.exceptions import InputValidationError


@dataclass(frozen=True, slots=True)
class GroqSettings:
    api_key: str
    model: str = "llama-3.3-70b-versatile"
    log_level: str = "INFO"
    api_url: str = "https://api.groq.com/openai/v1/chat/completions"
    timeout_seconds: float = 30.0
    temperature: float = 0.0

    @classmethod
    def from_env(cls) -> "GroqSettings":
        api_key = os.getenv("GROQ_API_KEY", "").strip()
        model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()
        log_level = os.getenv("LOG_LEVEL", "INFO").strip()

        if not api_key:
            raise InputValidationError("Environment variable GROQ_API_KEY is required.")

        if not model:
            raise InputValidationError(
                "Environment variable GROQ_MODEL cannot be empty."
            )

        if not log_level:
            raise InputValidationError(
                "Environment variable LOG_LEVEL cannot be empty."
            )

        return cls(
            api_key=api_key,
            model=model,
            log_level=log_level.upper(),
        )
