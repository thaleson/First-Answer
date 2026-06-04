"""Domain entities used by the brand extraction flow."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrandExtractionResult:
    """Represent the raw extraction result returned by a provider.

    This entity is intentionally simple and framework-agnostic so it can move across
    the application boundary without depending on external libraries.
    """

    monitored_brand_found: bool
    other_brands: tuple[str, ...]
