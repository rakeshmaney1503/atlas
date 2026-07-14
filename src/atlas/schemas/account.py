from decimal import Decimal
from uuid import UUID

from pydantic import ConfigDict
from sqlmodel import SQLModel

from atlas.database.models.account import AccountType


class AccountCreate(SQLModel):
    name: str
    institution: str
    account_type: AccountType
    currency: str = "INR"
    opening_balance: Decimal = Decimal("0.00")


class AccountRead(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    institution: str
    account_type: AccountType
    currency: str
    opening_balance: Decimal
    is_active: bool
