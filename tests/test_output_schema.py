from app.application.schemas import BrandExtractionOutput


def test_output_schema_accepts_expected_payload() -> None:
    output = BrandExtractionOutput.model_validate(
        {
            "monitored_brand_found": True,
            "other_brands": ["Banco Inter", "C6 Bank"],
        }
    )

    assert output.monitored_brand_found is True
    assert output.other_brands == ["Banco Inter", "C6 Bank"]


def test_output_schema_defaults_other_brands_to_empty_list() -> None:
    output = BrandExtractionOutput.model_validate(
        {
            "monitored_brand_found": False,
        }
    )

    assert output.monitored_brand_found is False
    assert output.other_brands == []
