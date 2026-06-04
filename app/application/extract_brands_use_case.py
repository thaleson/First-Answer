from app.application.schemas import BrandExtractionInput, BrandExtractionOutput
from app.domain.entities import BrandExtractionResult
from app.domain.interfaces import BrandExtractor


class ExtractBrandsUseCase:
    def __init__(self, extractor: BrandExtractor) -> None:
        self._extractor = extractor

    def execute(self, data: BrandExtractionInput) -> BrandExtractionOutput:
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
        return " ".join(value.casefold().split())
