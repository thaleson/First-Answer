from app.application.extract_brands_use_case import ExtractBrandsUseCase
from app.domain.interfaces import BrandExtractor
from app.infrastructure.groq_brand_extractor import GroqBrandExtractor


def build_extract_brands_use_case(extractor: BrandExtractor) -> ExtractBrandsUseCase:
    return ExtractBrandsUseCase(extractor=extractor)


def build_extract_brands_use_case_with_groq() -> ExtractBrandsUseCase:
    return build_extract_brands_use_case(extractor=GroqBrandExtractor())
