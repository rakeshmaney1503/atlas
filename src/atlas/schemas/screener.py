from __future__ import annotations

from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import SQLModel


class ScreeningResult(SQLModel):
    """
    Result of evaluating a company against a single screening rule.
    """

    model_config = ConfigDict(from_attributes=True)

    rule: str
    passed: bool
    value: Decimal | str | None = None
    threshold: Decimal | str | None = None
    message: str


class CompanyScore(SQLModel):
    """
    Overall score assigned to a company.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str

    quality_score: Decimal = Decimal("0")
    financial_strength_score: Decimal = Decimal("0")
    valuation_score: Decimal = Decimal("0")
    growth_score: Decimal = Decimal("0")
    risk_score: Decimal = Decimal("0")

    total_score: Decimal = Decimal("0")

    recommendation: str = ""
    confidence: str = ""

    screening_results: list[ScreeningResult] = []
