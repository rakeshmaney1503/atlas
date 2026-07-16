from __future__ import annotations

from decimal import Decimal

from pydantic import ConfigDict, Field
from sqlmodel import SQLModel

from atlas.schemas.screening_result import ScreeningResult


class ScoreCard(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    category: str

    score: Decimal
    max_score: Decimal

    percentage: Decimal

    results: list[ScreeningResult] = Field(default_factory=list)
