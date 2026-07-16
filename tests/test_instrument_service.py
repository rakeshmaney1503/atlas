from uuid import UUID

from sqlmodel import SQLModel, Session, create_engine

from atlas.database.models.holding import Holding
from atlas.database.models.instrument import Instrument
from atlas.services.instrument_service import InstrumentService


def test_create_and_get_instrument_by_id() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    instrument = Instrument(
        symbol="RELIANCE",
        name="Reliance Industries",
    )

    with Session(engine) as session:
        created = InstrumentService.create_instrument(session, instrument)
        fetched = InstrumentService.get_instrument_by_id(session, created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.symbol == "RELIANCE"
    assert fetched.name == "Reliance Industries"


def test_get_instrument_by_symbol() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    instrument = Instrument(
        symbol="INFY",
        name="Infosys",
    )

    with Session(engine) as session:
        InstrumentService.create_instrument(session, instrument)
        fetched = InstrumentService.get_instrument_by_symbol(session, "INFY")

    assert fetched is not None
    assert fetched.symbol == "INFY"
    assert fetched.name == "Infosys"


def test_list_and_search_instruments() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    instruments = [
        Instrument(symbol="HDFC", name="HDFC Bank", sector="Financials"),
        Instrument(symbol="ICICIBANK", name="ICICI Bank", sector="Financials"),
        Instrument(symbol="TCS", name="Tata Consultancy Services", sector="Information Technology"),
    ]

    with Session(engine) as session:
        for instrument in instruments:
            InstrumentService.create_instrument(session, instrument)

        all_instruments = InstrumentService.list_instruments(session)
        search_results = InstrumentService.search_instruments(session, "Bank")

    assert len(all_instruments) == 3
    assert any(i.symbol == "TCS" for i in all_instruments)
    assert len(search_results) == 2
    assert {i.symbol for i in search_results} == {"HDFC", "ICICIBANK"}


def test_update_and_delete_instrument() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    instrument = Instrument(symbol="SBIN", name="State Bank of India")

    with Session(engine) as session:
        created = InstrumentService.create_instrument(session, instrument)
        created.name = "State Bank of India Updated"
        updated = InstrumentService.update_instrument(session, created)

        fetched = InstrumentService.get_instrument_by_id(session, updated.id)
        assert fetched is not None
        assert fetched.name == "State Bank of India Updated"

        InstrumentService.delete_instrument(session, fetched)
        deleted = InstrumentService.get_instrument_by_id(session, fetched.id)

    assert deleted is None


def test_seed_from_holdings_with_empty_holdings() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        seeded = InstrumentService.seed_from_holdings(session)

    assert seeded == 0
    assert InstrumentService.list_instruments(session) == []


def test_seed_from_holdings_creates_unique_instruments() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    holdings = [
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="TCS",
            quantity=10,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="RELIANCE",
            quantity=10,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
    ]

    with Session(engine) as session:
        session.add_all(holdings)
        session.commit()

        seeded = InstrumentService.seed_from_holdings(session)
        instruments = InstrumentService.list_instruments(session)

    assert seeded == 2
    assert {i.symbol for i in instruments} == {"TCS", "RELIANCE"}


def test_seed_from_holdings_ignores_duplicate_holdings() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    holdings = [
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="TCS",
            quantity=10,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="TCS",
            quantity=5,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
    ]

    with Session(engine) as session:
        session.add_all(holdings)
        session.commit()

        seeded = InstrumentService.seed_from_holdings(session)
        instruments = InstrumentService.list_instruments(session)

    assert seeded == 1
    assert len(instruments) == 1
    assert instruments[0].symbol == "TCS"


def test_seed_from_holdings_preserves_existing_instruments() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    existing = Instrument(symbol="TCS", name="Tata Consultancy Services")
    holdings = [
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="TCS",
            quantity=10,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
        Holding(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            instrument="INFY",
            quantity=5,
            average_cost=0,
            last_traded_price=0,
            invested_amount=0,
            current_value=0,
            pnl=0,
            net_change_percent=0,
            day_change_percent=0,
        ),
    ]

    with Session(engine) as session:
        session.add(existing)
        session.add_all(holdings)
        session.commit()

        seeded = InstrumentService.seed_from_holdings(session)
        instruments = InstrumentService.list_instruments(session)

    assert seeded == 1
    assert {i.symbol for i in instruments} == {"TCS", "INFY"}
