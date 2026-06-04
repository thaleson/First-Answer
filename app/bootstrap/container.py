"""Composition helpers for wiring application dependencies."""

from app.application.extract_brands_use_case import ExtractBrandsUseCase
from app.domain.interfaces import BrandExtractor
from app.infrastructure.groq_brand_extractor import GroqBrandExtractor


def build_extract_brands_use_case(extractor: BrandExtractor) -> ExtractBrandsUseCase:
    """Build the use case with an explicit extractor dependency.

    Args:
        extractor (BrandExtractor): Extractor implementation to inject into the use case.

    Returns:
        ExtractBrandsUseCase: Configured use case instance.
    """

    return ExtractBrandsUseCase(extractor=extractor)


def build_extract_brands_use_case_with_groq() -> ExtractBrandsUseCase:
    """Build the use case using the Groq-backed extractor implementation.

    Returns:
        ExtractBrandsUseCase: Configured use case using the default Groq provider.
    """

    return build_extract_brands_use_case(extractor=GroqBrandExtractor())
