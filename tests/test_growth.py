from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.growth import GrowthRules


def build_metrics(**kwargs):

    defaults = dict(
        symbol="TCS",
        company_name="TCS",
        revenue_growth=Decimal("0"),
        eps_growth=Decimal("0"),
        free_cash_flow_growth=Decimal("0"),
    )

    defaults.update(kwargs)

    return FinancialMetrics(**defaults)


def test_growth_full_score():

    card = GrowthRules.evaluate(
        build_metrics(
            revenue_growth=Decimal("15"),
            eps_growth=Decimal("20"),
            free_cash_flow_growth=Decimal("18"),
        )
    )

    assert card.score == Decimal("30")
    assert len(card.results) == 3


def test_growth_partial_score():

    card = GrowthRules.evaluate(
        build_metrics(
            revenue_growth=Decimal("15"),
            eps_growth=Decimal("5"),
            free_cash_flow_growth=Decimal("18"),
        )
    )

    assert card.score == Decimal("20")


def test_growth_zero_score():

    card = GrowthRules.evaluate(
        build_metrics(
            revenue_growth=Decimal("2"),
            eps_growth=Decimal("4"),
            free_cash_flow_growth=Decimal("1"),
        )
    )

    assert card.score == Decimal("0")
