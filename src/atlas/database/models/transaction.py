from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlalchemy import UniqueConstraint
from sqlmodel import Field, SQLModel


class TransactionType(str, Enum):
    CREDIT = "Credit"
    DEBIT = "Debit"


class Transaction(SQLModel, table=True):
    __table_args__ = (
        UniqueConstraint("account_id", "import_hash", name="uq_account_import_hash"),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)

    account_id: UUID

    transaction_date: datetime

    amount: Decimal

    transaction_type: TransactionType

    description: str

    import_hash: str = Field(index=True)

    category: str | None = None

    merchant: str | None = None

    running_balance: Decimal | None = Field(default=None, nullable=True)

    reference: str | None = None

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
