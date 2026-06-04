"""Domain interfaces for brand extraction providers."""

from abc import ABC, abstractmethod

from app.domain.entities import BrandExtractionResult


class BrandExtractor(ABC):
    """Contract for components that extract brand mentions from text.

    Implementations are responsible for talking to external systems or local strategies
    and returning a provider-agnostic domain entity.
    """

    @abstractmethod
    def extract(self, text: str, monitored_brand: str) -> BrandExtractionResult:
        """Extract brand information from a text payload.

        Args:
            text (str): Source text that will be analyzed for brand mentions.
            monitored_brand (str): Brand that must be checked explicitly in the text.

        Returns:
            BrandExtractionResult: Raw extraction result produced by the implementation.
        """

        raise NotImplementedError
