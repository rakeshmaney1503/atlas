from decimal import Decimal

from atlas.schemas.financial_metrics import FinancialMetrics
from atlas.services.screener.valuation import ValuationRules


def build_metrics(**kwargs):

    defaults = dict(
        symbol="TCS",
        company_name="TCS",
        pe_ratio=Decimal("20"),
        pb_ratio=Decimal("3"),
        peg_ratio=Decimal("1"),
        ev_ebitda=Decimal("10"),
        price_to_sales=Decimal("3"),
    )

    defaults.update(kwargs)

    return FinancialMetrics(**defaults)


def test_full_score():

    card = ValuationRules.evaluate(
        build_metrics()
    )

    assert card.score == Decimal("50")


def test_partial_score():

    card = ValuationRules.evaluate(
        build_metrics(
            pe_ratio=Decimal("40"),
            pb_ratio=Decimal("8"),
        )
    )

    assert card.score == Decimal("30")


def test_zero_score():

    card = ValuationRules.evaluate(
        build_metrics(
            pe_ratio=Decimal("50"),
            pb_ratio=Decimal("8"),
            peg_ratio=Decimal("4"),
            ev_ebitda=Decimal("30"),
            price_to_sales=Decimal("12"),
        )
    )

    assert card.score == Decimal("0")
