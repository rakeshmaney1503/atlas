from decimal import Decimal

from pydantic import ConfigDict
from sqlmodel import SQLModel


class PortfolioHoldingRow(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    instrument: str
    quantity: Decimal
    average_cost: Decimal
    last_traded_price: Decimal
    invested_amount: Decimal
    current_value: Decimal
    pnl: Decimal
    allocation_percent: Decimal


class PortfolioSummary(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    invested: Decimal
    current_value: Decimal
    pnl: Decimal
    percentage_return: Decimal


class PortfolioAllocationRow(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    instrument: str
    current_value: Decimal
    allocation_percent: Decimal


class PortfolioTopHoldingRow(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    instrument: str
    current_value: Decimal
    allocation_percent: Decimal


class PortfolioViewModel(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    summary: PortfolioSummary
    holdings: list[PortfolioHoldingRow]
    allocations: list[PortfolioAllocationRow]
    top_holdings: list[PortfolioTopHoldingRow]


class PortfolioSnapshot(SQLModel):
    model_config = ConfigDict(from_attributes=True)

    summary: PortfolioSummary
    holdings: list[PortfolioHoldingRow]
