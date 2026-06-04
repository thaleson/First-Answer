from app.application.extract_brands_use_case import ExtractBrandsUseCase
from app.application.schemas import BrandExtractionInput
from app.domain.entities import BrandExtractionResult
from tests.fakes.fake_brand_extractor import FakeBrandExtractor


def test_use_case_returns_true_when_monitored_brand_is_found() -> None:
    extractor = FakeBrandExtractor(
        result=BrandExtractionResult(
            monitored_brand_found=True,
            other_brands=("Banco Inter", "C6 Bank"),
        )
    )
    use_case = ExtractBrandsUseCase(extractor=extractor)

    result = use_case.execute(
        BrandExtractionInput(
            text="Texto qualquer com Nubank, Banco Inter e C6 Bank.",
            monitored_brand="Nubank",
        )
    )

    assert result.monitored_brand_found is True
    assert result.other_brands == ["Banco Inter", "C6 Bank"]
    assert extractor.calls == [
        ("Texto qualquer com Nubank, Banco Inter e C6 Bank.", "Nubank")
    ]


def test_use_case_returns_false_when_monitored_brand_is_not_found() -> None:
    extractor = FakeBrandExtractor(
        result=BrandExtractionResult(
            monitored_brand_found=False,
            other_brands=("Banco Inter",),
        )
    )
    use_case = ExtractBrandsUseCase(extractor=extractor)

    result = use_case.execute(
        BrandExtractionInput(
            text="Texto sem a marca monitorada.",
            monitored_brand="Nubank",
        )
    )

    assert result.monitored_brand_found is False
    assert result.other_brands == ["Banco Inter"]


def test_use_case_removes_monitored_brand_from_other_brands() -> None:
    extractor = FakeBrandExtractor(
        result=BrandExtractionResult(
            monitored_brand_found=True,
            other_brands=("Nubank", "Banco Inter", " nubank "),
        )
    )
    use_case = ExtractBrandsUseCase(extractor=extractor)

    result = use_case.execute(
        BrandExtractionInput(
            text="Texto com Nubank e Banco Inter.",
            monitored_brand="Nubank",
        )
    )

    assert result.other_brands == ["Banco Inter"]


def test_use_case_deduplicates_other_brands() -> None:
    extractor = FakeBrandExtractor(
        result=BrandExtractionResult(
            monitored_brand_found=True,
            other_brands=("Banco Inter", "Banco Inter", " banco inter ", "C6 Bank"),
        )
    )
    use_case = ExtractBrandsUseCase(extractor=extractor)

    result = use_case.execute(
        BrandExtractionInput(
            text="Texto com várias marcas.",
            monitored_brand="Nubank",
        )
    )

    assert result.other_brands == ["Banco Inter", "C6 Bank"]


def test_use_case_discards_empty_other_brand_entries() -> None:
    extractor = FakeBrandExtractor(
        result=BrandExtractionResult(
            monitored_brand_found=True,
            other_brands=("Banco Inter", "", "   ", "C6 Bank"),
        )
    )
    use_case = ExtractBrandsUseCase(extractor=extractor)

    result = use_case.execute(
        BrandExtractionInput(
            text="Texto com marcas e ruído.",
            monitored_brand="Nubank",
        )
    )

    assert result.other_brands == ["Banco Inter", "C6 Bank"]
