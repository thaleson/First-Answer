from app.domain.entities import BrandExtractionResult
from app.domain.interfaces import BrandExtractor


class FakeBrandExtractor(BrandExtractor):
    def __init__(self, result: BrandExtractionResult) -> None:
        self._result = result
        self.calls: list[tuple[str, str]] = []

    def extract(self, text: str, monitored_brand: str) -> BrandExtractionResult:
        self.calls.append((text, monitored_brand))
        return self._result
