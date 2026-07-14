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


def test_portfolio_service_computes_allocations_and_top_holdings() -> None:
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
            Holding(
                account_id=UUID("11111111-1111-1111-1111-111111111111"),
                instrument="Stock C",
                quantity=Decimal("2"),
                average_cost=Decimal("500.00"),
                last_traded_price=Decimal("600.00"),
                invested_amount=Decimal("1000.00"),
                current_value=Decimal("1200.00"),
                pnl=Decimal("200.00"),
                net_change_percent=Decimal("20.00"),
                day_change_percent=Decimal("1.00"),
            ),
        ]
        session.add_all(holdings)
        session.commit()

        snapshot = PortfolioService.get_portfolio_view_model(
            session,
            UUID("11111111-1111-1111-1111-111111111111"),
        )

    assert len(snapshot.allocations) == 3
    assert [allocation.instrument for allocation in snapshot.allocations] == [
        "Stock C",
        "Stock A",
        "Stock B",
    ]
    assert snapshot.allocations[0].allocation_percent == Decimal("37.50")
    assert snapshot.allocations[1].allocation_percent == Decimal("34.375")
    assert snapshot.allocations[2].allocation_percent == Decimal("28.125")

    assert len(snapshot.top_holdings) == 3
    assert snapshot.top_holdings[0].instrument == "Stock C"
    assert snapshot.top_holdings[1].instrument == "Stock A"
    assert snapshot.top_holdings[2].instrument == "Stock B"
    assert snapshot.top_holdings[0].allocation_percent == Decimal("37.50")
