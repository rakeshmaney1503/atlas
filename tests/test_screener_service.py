from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.financial_strength import FinancialStrengthRules
from atlas.services.screener.quality import QualityRules
from atlas.services.screener_service import ScreenerService


def build_metrics(
    *,
    roe: Decimal = Decimal("0"),
    roce: Decimal = Decimal("0"),
    roa: Decimal = Decimal("0"),
    debt_to_equity: Decimal = Decimal("0"),
    current_ratio: Decimal = Decimal("0"),
    interest_coverage: Decimal = Decimal("0"),
    free_cash_flow: Decimal = Decimal("0"),
    operating_cash_flow: Decimal = Decimal("0"),
) -> FinancialMetrics:
    return FinancialMetrics(
        symbol="TCS",
        company_name="Tata Consultancy Services",
        roe=roe,
        roce=roce,
        roa=roa,
        debt_to_equity=debt_to_equity,
        current_ratio=current_ratio,
        interest_coverage=interest_coverage,
        free_cash_flow=free_cash_flow,
        operating_cash_flow=operating_cash_flow,
    )


# ----------------------------------------------------------------------
# Quality Rules
# ----------------------------------------------------------------------


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


# ----------------------------------------------------------------------
# Financial Strength Rules
# ----------------------------------------------------------------------


def test_financial_strength_score() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("0.5"),
        current_ratio=Decimal("2"),
        interest_coverage=Decimal("10"),
        free_cash_flow=Decimal("100"),
        operating_cash_flow=Decimal("200"),
    )

    score, results = FinancialStrengthRules.calculate_score(metrics)

    assert score == Decimal("50")
    assert len(results) == 5


# ----------------------------------------------------------------------
# Screener Service
# ----------------------------------------------------------------------


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
    )

    score = ScreenerService.build_company_score(metrics)

    assert score.symbol == "TCS"
    assert score.company_name == "Tata Consultancy Services"

    assert score.quality_score == Decimal("30")
    assert score.financial_strength_score == Decimal("50")

    assert score.total_score == Decimal("80")

    assert score.recommendation == "Buy"
    assert score.confidence == "High"

    assert len(score.screening_results) == 8
