from abc import ABC, abstractmethod

from app.domain.entities import BrandExtractionResult


class BrandExtractor(ABC):
    @abstractmethod
    def extract(self, text: str, monitored_brand: str) -> BrandExtractionResult:
        raise NotImplementedError
