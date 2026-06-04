"""Pydantic schemas for application inputs and outputs."""

from pydantic import BaseModel, ConfigDict, Field, field_validator


class BrandExtractionInput(BaseModel):
    """Validated input payload for the brand extraction flow.

    This model normalizes string fields by trimming surrounding whitespace and rejects
    empty values before the use case is executed.
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(..., min_length=1)
    monitored_brand: str = Field(..., min_length=1)

    @field_validator("text", "monitored_brand")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        """Reject empty strings after normalization.

        Args:
            value (str): Candidate string value for the validated field.

        Returns:
            str: The original value when it remains non-empty after stripping.

        Raises:
            ValueError: If the normalized field value is empty.
        """

        if not value.strip():
            raise ValueError("Field cannot be empty.")
        return value


class BrandExtractionOutput(BaseModel):
    """Structured output returned by the application layer.

    This model represents the final response exposed by the CLI and Streamlit interfaces.
    """

    monitored_brand_found: bool
    other_brands: list[str] = Field(default_factory=list)
