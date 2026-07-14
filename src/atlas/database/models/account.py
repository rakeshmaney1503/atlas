from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class AccountType(str, Enum):
    SAVINGS = "Savings"
    CURRENT = "Current"
    CREDIT_CARD = "Credit Card"
    CASH = "Cash"
    INVESTMENT = "Investment"
    LOAN = "Loan"
    OTHER = "Other"


class Account(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)

    name: str
    institution: str

    account_type: AccountType

    currency: str = "INR"

    opening_balance: Decimal = Decimal("0.00")

    is_active: bool = True

    created_at: datetime = Field(
            default_factory=lambda: datetime.now(UTC)
            )                             
    updated_at: datetime = Field(
            default_factory=lambda:datetime.now(UTC)
            )
