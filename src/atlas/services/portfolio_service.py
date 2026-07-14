from decimal import Decimal
from typing import TYPE_CHECKING

from sqlmodel import Session

from atlas.database.models.holding import Holding
from atlas.schemas.portfolio import (
    PortfolioAllocationRow,
    PortfolioHoldingRow,
    PortfolioSnapshot,
    PortfolioSummary,
    PortfolioTopHoldingRow,
    PortfolioViewModel,
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
    def compute_portfolio_allocations(
        holdings: list[Holding],
    ) -> list[PortfolioAllocationRow]:
        total_current = sum(
            (h.current_value for h in holdings),
            Decimal("0.00"),
        )

        rows: list[PortfolioAllocationRow] = []
        for holding in holdings:
            allocation_percent = Decimal("0.00")
            if total_current > Decimal("0.00"):
                allocation_percent = (
                    holding.current_value
                    / total_current
                    * Decimal("100.00")
                )

            rows.append(
                PortfolioAllocationRow(
                    instrument=holding.instrument,
                    current_value=holding.current_value,
                    allocation_percent=allocation_percent,
                )
            )

        return rows

    @staticmethod
    def get_top_holdings(
        holdings: list[Holding],
        top_n: int = 5,
    ) -> list[PortfolioTopHoldingRow]:
        sorted_holdings = sorted(
            holdings,
            key=lambda holding: holding.current_value,
            reverse=True,
        )

        total_current = sum(
            (h.current_value for h in holdings),
            Decimal("0.00"),
        )

        rows: list[PortfolioTopHoldingRow] = []
        for holding in sorted_holdings[:top_n]:
            allocation_percent = Decimal("0.00")
            if total_current > Decimal("0.00"):
                allocation_percent = (
                    holding.current_value
                    / total_current
                    * Decimal("100.00")
                )

            rows.append(
                PortfolioTopHoldingRow(
                    instrument=holding.instrument,
                    current_value=holding.current_value,
                    allocation_percent=allocation_percent,
                )
            )

        return rows

    @staticmethod
    def get_portfolio_view_model(
        session: Session,
        account_id,
    ) -> PortfolioViewModel:
        holdings = PortfolioService.get_portfolio_holdings(session, account_id)
        summary = PortfolioService.compute_portfolio_summary(holdings)
        rows = PortfolioService.compute_portfolio_rows(holdings)
        allocations = PortfolioService.compute_portfolio_allocations(holdings)
        top_holdings = PortfolioService.get_top_holdings(holdings)

        return PortfolioViewModel(
            summary=summary,
            holdings=rows,
            allocations=allocations,
            top_holdings=top_holdings,
        )

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
