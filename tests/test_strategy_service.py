from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.strategy_service import StrategyService


def test_quality_strategy():

    metrics = FinancialMetrics(
        symbol="TCS",
        company_name="TCS",
        roe=Decimal("25"),
        roce=Decimal("25"),
        roa=Decimal("10"),
        debt_to_equity=Decimal("0.2"),
        current_ratio=Decimal("2"),
        interest_coverage=Decimal("10"),
        free_cash_flow=Decimal("100"),
        operating_cash_flow=Decimal("100"),
        revenue_growth=Decimal("15"),
        eps_growth=Decimal("15"),
        free_cash_flow_growth=Decimal("15"),
    )

    result = StrategyService.evaluate(
        "quality",
        metrics,
    )

    assert result.symbol == "TCS"
    assert result.total_score == Decimal("110")
