"""Application use case for brand extraction orchestration."""

from app.application.schemas import BrandExtractionInput, BrandExtractionOutput
from app.domain.entities import BrandExtractionResult
from app.domain.interfaces import BrandExtractor


class ExtractBrandsUseCase:
    """Coordinate brand extraction and normalize the final response.

    This use case delegates extraction to a provider that implements the domain contract
    and applies the final business-level cleanup required by the challenge output.

    Attributes:
        _extractor (BrandExtractor): Extractor implementation used to obtain raw brand matches.
    """

    def __init__(self, extractor: BrandExtractor) -> None:
        self._extractor = extractor

    def execute(self, data: BrandExtractionInput) -> BrandExtractionOutput:
        """Execute the extraction flow for a validated input payload.

        This method delegates raw extraction to the configured extractor and then normalizes
        the output so the monitored brand is excluded from the secondary brand list.

        Args:
            data (BrandExtractionInput): Validated input payload with text and monitored brand.

        Returns:
            BrandExtractionOutput: Normalized extraction result ready for presentation.
        """

        result = self._extractor.extract(
            text=data.text,
            monitored_brand=data.monitored_brand,
        )
        return self._build_output(
            monitored_brand=data.monitored_brand,
            result=result,
        )

    def _build_output(
        self,
        monitored_brand: str,
        result: BrandExtractionResult,
    ) -> BrandExtractionOutput:
        """Build the final output model from the raw extractor result.

        This method removes empty entries, deduplicates equivalent brand names, and ensures
        the monitored brand is not included in the `other_brands` collection.

        Args:
            monitored_brand (str): Brand being monitored for presence in the text.
            result (BrandExtractionResult): Raw extractor result returned by the provider.

        Returns:
            BrandExtractionOutput: Sanitized output model for downstream consumers.
        """

        monitored_brand_key = self._normalize_brand(monitored_brand)
        normalized_brands: list[str] = []
        seen_brands: set[str] = set()

        for brand in result.other_brands:
            cleaned_brand = brand.strip()
            if not cleaned_brand:
                continue

            brand_key = self._normalize_brand(cleaned_brand)
            if brand_key == monitored_brand_key or brand_key in seen_brands:
                continue

            seen_brands.add(brand_key)
            normalized_brands.append(cleaned_brand)

        return BrandExtractionOutput(
            monitored_brand_found=result.monitored_brand_found,
            other_brands=normalized_brands,
        )

    @staticmethod
    def _normalize_brand(value: str) -> str:
        """Normalize a brand name for comparison purposes.

        The normalization is used internally to compare brands in a case-insensitive way
        while collapsing repeated whitespace.

        Args:
            value (str): Raw brand name value.

        Returns:
            str: Normalized brand key used for deduplication and exclusion checks.
        """

        return " ".join(value.casefold().split())
