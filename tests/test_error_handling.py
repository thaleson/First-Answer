import pytest

from app.application.extract_brands_use_case import ExtractBrandsUseCase
from app.application.schemas import BrandExtractionInput
from app.shared.exceptions import GroqConnectionError


class FailingBrandExtractor:
    def extract(self, text: str, monitored_brand: str) -> None:
        raise GroqConnectionError("Simulated connection failure.")


def test_use_case_propagates_extractor_errors() -> None:
    use_case = ExtractBrandsUseCase(extractor=FailingBrandExtractor())

    with pytest.raises(GroqConnectionError, match="Simulated connection failure."):
        use_case.execute(
            BrandExtractionInput(
                text="Texto válido",
                monitored_brand="Nubank",
            )
        )
