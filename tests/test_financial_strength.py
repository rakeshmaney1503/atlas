from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.financial_strength import (
    FinancialStrengthRules,
)


def build_metrics(
    *,
    debt_to_equity: Decimal = Decimal("0"),
    current_ratio: Decimal = Decimal("0"),
    interest_coverage: Decimal = Decimal("0"),
    free_cash_flow: Decimal = Decimal("0"),
    operating_cash_flow: Decimal = Decimal("0"),
) -> FinancialMetrics:
    return FinancialMetrics(
        symbol="TCS",
        company_name="Tata Consultancy Services",
        debt_to_equity=debt_to_equity,
        current_ratio=current_ratio,
        interest_coverage=interest_coverage,
        free_cash_flow=free_cash_flow,
        operating_cash_flow=operating_cash_flow,
    )


def test_debt_to_equity_passes() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("0.40"),
    )

    result = FinancialStrengthRules.evaluate_debt_to_equity(metrics)

    assert result.passed is True


def test_debt_to_equity_fails() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("2.10"),
    )

    result = FinancialStrengthRules.evaluate_debt_to_equity(metrics)

    assert result.passed is False


def test_current_ratio_passes() -> None:
    metrics = build_metrics(
        current_ratio=Decimal("2.30"),
    )

    result = FinancialStrengthRules.evaluate_current_ratio(metrics)

    assert result.passed is True


def test_interest_coverage_passes() -> None:
    metrics = build_metrics(
        interest_coverage=Decimal("8"),
    )

    result = FinancialStrengthRules.evaluate_interest_coverage(metrics)

    assert result.passed is True


def test_positive_free_cash_flow() -> None:
    metrics = build_metrics(
        free_cash_flow=Decimal("1000000"),
    )

    result = FinancialStrengthRules.evaluate_free_cash_flow(metrics)

    assert result.passed is True


def test_positive_operating_cash_flow() -> None:
    metrics = build_metrics(
        operating_cash_flow=Decimal("2500000"),
    )

    result = FinancialStrengthRules.evaluate_operating_cash_flow(metrics)

    assert result.passed is True


def test_financial_strength_full_score() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("0.50"),
        current_ratio=Decimal("2"),
        interest_coverage=Decimal("10"),
        free_cash_flow=Decimal("100"),
        operating_cash_flow=Decimal("200"),
    )

    score, results = FinancialStrengthRules.calculate_score(metrics)

    assert score == Decimal("50")
    assert len(results) == 5


def test_financial_strength_partial_score() -> None:
    metrics = build_metrics(
        debt_to_equity=Decimal("0.50"),
        current_ratio=Decimal("0.80"),
        interest_coverage=Decimal("10"),
        free_cash_flow=Decimal("-100"),
        operating_cash_flow=Decimal("500"),
    )

    score, _ = FinancialStrengthRules.calculate_score(metrics)

    assert score == Decimal("30")
