from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    CREDIT = "Credit"
    DEBIT = "Debit"


class Transaction(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    account_id: UUID

    transaction_date: datetime

    amount: Decimal

    transaction_type: TransactionType

    description: str

    import_hash: str = Field(index=True, unique=True)

    category: str | None = None

    reference: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
