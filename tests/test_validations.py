import pytest
from pydantic import ValidationError

from app.application.schemas import BrandExtractionInput


def test_input_schema_rejects_empty_text() -> None:
    with pytest.raises(ValidationError):
        BrandExtractionInput(
            text="",
            monitored_brand="Nubank",
        )


def test_input_schema_rejects_empty_monitored_brand() -> None:
    with pytest.raises(ValidationError):
        BrandExtractionInput(
            text="Texto válido",
            monitored_brand="",
        )


def test_input_schema_rejects_whitespace_only_fields() -> None:
    with pytest.raises(ValidationError):
        BrandExtractionInput(
            text="   ",
            monitored_brand="Nubank",
        )

    with pytest.raises(ValidationError):
        BrandExtractionInput(
            text="Texto válido",
            monitored_brand="   ",
        )


def test_input_schema_rejects_null_fields() -> None:
    with pytest.raises(ValidationError):
        BrandExtractionInput.model_validate(
            {
                "text": None,
                "monitored_brand": "Nubank",
            }
        )

    with pytest.raises(ValidationError):
        BrandExtractionInput.model_validate(
            {
                "text": "Texto válido",
                "monitored_brand": None,
            }
        )


def test_input_schema_strips_surrounding_whitespace() -> None:
    payload = BrandExtractionInput(
        text="  Texto válido  ",
        monitored_brand="  Nubank  ",
    )

    assert payload.text == "Texto válido"
    assert payload.monitored_brand == "Nubank"
