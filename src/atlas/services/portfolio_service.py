from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Session

from atlas.database.models.holding import Holding
from atlas.schemas.portfolio import (
    PortfolioHoldingRow,
    PortfolioSnapshot,
    PortfolioSummary,
)
from atlas.services.holding_service import HoldingService


class PortfolioService:
    @staticmethod
    def get_portfolio_holdings(
        session: Session,
        account_id,
    ) -> list[Holding]:
        return HoldingService.get_holdings(session, account_id)

    @staticmethod
    def compute_portfolio_summary(
        holdings: list[Holding],
    ) -> PortfolioSummary:
        invested = sum(
            (h.invested_amount for h in holdings),
            Decimal("0.00"),
        )
        current_value = sum(
            (h.current_value for h in holdings),
            Decimal("0.00"),
        )
        pnl = sum(
            (h.pnl for h in holdings),
            Decimal("0.00"),
        )

        return PortfolioSummary(
            invested=invested,
            current_value=current_value,
            pnl=pnl,
        )

    @staticmethod
    def compute_portfolio_rows(
        holdings: list[Holding],
    ) -> list[PortfolioHoldingRow]:
        total_current = sum(
            (h.current_value for h in holdings),
            Decimal("0.00"),
        )

        rows: list[PortfolioHoldingRow] = []

        for holding in holdings:
            allocation_percent = Decimal("0.00")
            if total_current > Decimal("0.00"):
                allocation_percent = (
                    holding.current_value
                    / total_current
                    * Decimal("100.00")
                )

            rows.append(
                PortfolioHoldingRow(
                    instrument=holding.instrument,
                    quantity=holding.quantity,
                    average_cost=holding.average_cost,
                    last_traded_price=holding.last_traded_price,
                    invested_amount=holding.invested_amount,
                    current_value=holding.current_value,
                    pnl=holding.pnl,
                    allocation_percent=allocation_percent,
                )
            )

        return rows

    @staticmethod
    def get_portfolio_snapshot(
        session: Session,
        account_id,
    ) -> PortfolioSnapshot:
        holdings = PortfolioService.get_portfolio_holdings(session, account_id)
        summary = PortfolioService.compute_portfolio_summary(holdings)
        rows = PortfolioService.compute_portfolio_rows(holdings)

        return PortfolioSnapshot(
            summary=summary,
            holdings=rows,
        )
