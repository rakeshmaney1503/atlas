from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Instrument(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    symbol: str = Field(index=True)
    name: str
    isin: str | None = None
    exchange: str | None = None
    asset_type: str | None = None
    sector: str | None = None
    industry: str | None = None
    market_cap_category: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
