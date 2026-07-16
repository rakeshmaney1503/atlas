from __future__ import annotations

from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import SQLModel


class ScreeningResult(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    rule: str
    passed: bool

    value: Decimal
    threshold: Decimal

    message: str
