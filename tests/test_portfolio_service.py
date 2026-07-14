from decimal import Decimal
from uuid import UUID

from sqlmodel import Session, SQLModel, create_engine

from atlas.database.models.holding import Holding
from atlas.schemas.portfolio import PortfolioSnapshot
from atlas.services.portfolio_service import PortfolioService


def test_portfolio_service_returns_empty_snapshot_for_no_holdings() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        snapshot = PortfolioService.get_portfolio_snapshot(
            session,
            UUID("00000000-0000-0000-0000-000000000000"),
        )

    assert isinstance(snapshot, PortfolioSnapshot)
    assert snapshot.summary.invested == Decimal("0.00")
    assert snapshot.summary.current_value == Decimal("0.00")
    assert snapshot.summary.pnl == Decimal("0.00")
    assert snapshot.holdings == []


def test_portfolio_service_computes_summary_and_rows() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        holdings = [
            Holding(
                account_id=UUID("11111111-1111-1111-1111-111111111111"),
                instrument="Stock A",
                quantity=Decimal("10"),
                average_cost=Decimal("100.00"),
                last_traded_price=Decimal("110.00"),
                invested_amount=Decimal("1000.00"),
                current_value=Decimal("1100.00"),
                pnl=Decimal("100.00"),
                net_change_percent=Decimal("10.00"),
                day_change_percent=Decimal("0.50"),
            ),
            Holding(
                account_id=UUID("11111111-1111-1111-1111-111111111111"),
                instrument="Stock B",
                quantity=Decimal("5"),
                average_cost=Decimal("200.00"),
                last_traded_price=Decimal("180.00"),
                invested_amount=Decimal("1000.00"),
                current_value=Decimal("900.00"),
                pnl=Decimal("-100.00"),
                net_change_percent=Decimal("-10.00"),
                day_change_percent=Decimal("-0.25"),
            ),
        ]

        session.add_all(holdings)
        session.commit()

        snapshot = PortfolioService.get_portfolio_snapshot(
            session,
            UUID("11111111-1111-1111-1111-111111111111"),
        )

    assert snapshot.summary.invested == Decimal("2000.00")
    assert snapshot.summary.current_value == Decimal("2000.00")
    assert snapshot.summary.pnl == Decimal("0.00")
    assert len(snapshot.holdings) == 2

    first_row = snapshot.holdings[0]
    second_row = snapshot.holdings[1]

    assert first_row.instrument == "Stock A"
    assert second_row.instrument == "Stock B"
    assert first_row.allocation_percent == Decimal("55.00")
    assert second_row.allocation_percent == Decimal("45.00")
