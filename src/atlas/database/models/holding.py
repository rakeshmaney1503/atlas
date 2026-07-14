from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class Holding(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    account_id: UUID = Field(index=True)

    instrument: str = Field(index=True)

    quantity: Decimal

    average_cost: Decimal

    last_traded_price: Decimal

    invested_amount: Decimal

    current_value: Decimal

    pnl: Decimal

    net_change_percent: Decimal

    day_change_percent: Decimal

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
