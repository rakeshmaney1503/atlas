from __future__ import annotations

from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import SQLModel


class FinancialMetrics(SQLModel):
    """
    Canonical financial metrics used by the Atlas Screening Engine.

    Every provider (FMP, Alpha Vantage, etc.) should populate this model.
    The Screening Engine only consumes this model and never talks directly
    to external APIs.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str

    # ------------------------------------------------------------------
    # Profitability
    # ------------------------------------------------------------------

    roe: Decimal = Decimal("0")
    roce: Decimal = Decimal("0")
    roa: Decimal = Decimal("0")

    # ------------------------------------------------------------------
    # Growth
    # ------------------------------------------------------------------

    revenue_growth: Decimal = Decimal("0")
    eps_growth: Decimal = Decimal("0")
    free_cash_flow_growth: Decimal = Decimal("0")

    # ------------------------------------------------------------------
    # Financial Strength
    # ------------------------------------------------------------------

    debt_to_equity: Decimal = Decimal("0")
    current_ratio: Decimal = Decimal("0")
    interest_coverage: Decimal = Decimal("0")

    # ------------------------------------------------------------------
    # Valuation
    # ------------------------------------------------------------------

    pe_ratio: Decimal = Decimal("0")
    pb_ratio: Decimal = Decimal("0")
    peg_ratio: Decimal = Decimal("0")
    ev_ebitda: Decimal = Decimal("0")
    price_to_sales: Decimal = Decimal("0")

    # ------------------------------------------------------------------
    # Cash Flow
    # ------------------------------------------------------------------

    free_cash_flow: Decimal = Decimal("0")
    operating_cash_flow: Decimal = Decimal("0")

    # ------------------------------------------------------------------
    # Margins
    # ------------------------------------------------------------------

    gross_margin: Decimal = Decimal("0")
    operating_margin: Decimal = Decimal("0")
    net_margin: Decimal = Decimal("0")
