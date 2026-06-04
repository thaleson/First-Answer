from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class BrandExtractionResult:
    monitored_brand_found: bool
    other_brands: tuple[str, ...]
