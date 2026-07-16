from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.financial_strength import FinancialStrengthRules
from atlas.services.screener.growth import GrowthRules
from atlas.services.screener.quality import QualityRules
from atlas.services.screener_service import ScreenerService


def build_metrics(**kwargs) -> FinancialMetrics:
    defaults = dict(
        symbol="TCS",
        company_name="Tata Consultancy Services",
        roe=Decimal("0"),
        roce=Decimal("0"),
        roa=Decimal("0"),
        debt_to_equity=Decimal("2"),
        current_ratio=Decimal("1"),
        interest_coverage=Decimal("1"),
        free_cash_flow=Decimal("-1"),
        operating_cash_flow=Decimal("-1"),
        revenue_growth=Decimal("15"),
        eps_growth=Decimal("15"),
        free_cash_flow_growth=Decimal("15"),
    )

    defaults.update(kwargs)

    return FinancialMetrics(**defaults)


def test_roe_passes() -> None:
    metrics = build_metrics(roe=Decimal("18"))

    result = QualityRules.evaluate_roe(metrics)

    assert result.passed is True


def test_roe_fails() -> None:
    metrics = build_metrics(roe=Decimal("12"))

    result = QualityRules.evaluate_roe(metrics)

    assert result.passed is False


def test_roce_passes() -> None:
    metrics = build_metrics(roce=Decimal("22"))

    result = QualityRules.evaluate_roce(metrics)

    assert result.passed is True


def test_roa_passes() -> None:
    metrics = build_metrics(roa=Decimal("10"))

    result = QualityRules.evaluate_roa(metrics)

    assert result.passed is True


def test_quality_score_full_marks() -> None:
    metrics = build_metrics(
        roe=Decimal("20"),
        roce=Decimal("20"),
        roa=Decimal("10"),
    )

    score, results = QualityRules.calculate_score(metrics)

    assert score == Decimal("30")
    assert len(results) == 3


def test_financial_strength_full_marks() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("0.40"),
        current_ratio=Decimal("2.50"),
        interest_coverage=Decimal("12"),
        free_cash_flow=Decimal("1000"),
        operating_cash_flow=Decimal("2000"),
    )

    score, results = FinancialStrengthRules.calculate_score(metrics)

    assert score == Decimal("50")
    assert len(results) == 5


def test_growth_full_marks() -> None:
    metrics = build_metrics(
        revenue_growth=Decimal("15"),
        eps_growth=Decimal("18"),
        free_cash_flow_growth=Decimal("20"),
    )

    card = GrowthRules.evaluate(metrics)

    assert card.score == Decimal("30")


def test_company_score() -> None:
    metrics = build_metrics(
        roe=Decimal("30"),
        roce=Decimal("32"),
        roa=Decimal("12"),
        debt_to_equity=Decimal("0.40"),
        current_ratio=Decimal("2.50"),
        interest_coverage=Decimal("12"),
        free_cash_flow=Decimal("1000"),
        operating_cash_flow=Decimal("2000"),
        revenue_growth=Decimal("20"),
        eps_growth=Decimal("20"),
        free_cash_flow_growth=Decimal("20"),
    )

    score = ScreenerService.build_company_score(metrics)

    assert score.symbol == "TCS"
    assert score.company_name == "Tata Consultancy Services"

    assert score.quality_score == Decimal("30")
    assert score.financial_strength_score == Decimal("50")
    assert score.growth_score == Decimal("30")

    assert score.total_score == Decimal("110")

    assert score.recommendation == "Strong Buy"
    assert score.confidence == "High"
