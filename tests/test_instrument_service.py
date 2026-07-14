from uuid import UUID

from sqlmodel import SQLModel, Session, create_engine

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
