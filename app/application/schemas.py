from pydantic import BaseModel, ConfigDict, Field, field_validator


class BrandExtractionInput(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    text: str = Field(..., min_length=1)
    monitored_brand: str = Field(..., min_length=1)

    @field_validator("text", "monitored_brand")
    @classmethod
    def validate_non_empty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Field cannot be empty.")
        return value


class BrandExtractionOutput(BaseModel):
    monitored_brand_found: bool
    other_brands: list[str] = Field(default_factory=list)
