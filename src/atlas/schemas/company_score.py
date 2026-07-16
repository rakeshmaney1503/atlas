from __future__ import annotations

from decimal import Decimal

from pydantic import ConfigDict, Field
from sqlmodel import SQLModel

from atlas.schemas.scorecard import ScoreCard
from atlas.schemas.screening_result import ScreeningResult


class CompanyScore(SQLModel):
    """
    Final result returned by the Atlas Screening Engine.
    """

    model_config = ConfigDict(from_attributes=True)

    symbol: str
    company_name: str

    # Legacy summary fields (kept for compatibility)
    quality_score: Decimal = Decimal("0")
    financial_strength_score: Decimal = Decimal("0")
    valuation_score: Decimal = Decimal("0")
    growth_score: Decimal = Decimal("0")
    risk_score: Decimal = Decimal("0")

    total_score: Decimal = Decimal("0")

    recommendation: str
    confidence: str

    # New architecture
    scorecards: list[ScoreCard] = Field(default_factory=list)

    screening_results: list[ScreeningResult] = Field(
        default_factory=list
    )
