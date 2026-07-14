from datetime import datetime
from uuid import UUID

from sqlmodel import SQLModel, Session, create_engine

from atlas.database.models.instrument import Instrument


def test_instrument_model_can_be_created_and_retrieved() -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    instrument = Instrument(
        symbol="TCS",
        name="Tata Consultancy Services",
        isin="INE467B01029",
        exchange="NSE",
        asset_type="Equity",
        sector="Information Technology",
        industry="IT Services",
        market_cap_category="Large Cap",
    )

    with Session(engine) as session:
        session.add(instrument)
        session.commit()
        session.refresh(instrument)

        retrieved = session.get(Instrument, instrument.id)

    assert retrieved is not None
    assert retrieved.id == instrument.id
    assert retrieved.symbol == "TCS"
    assert retrieved.name == "Tata Consultancy Services"
    assert retrieved.isin == "INE467B01029"
    assert retrieved.exchange == "NSE"
    assert retrieved.asset_type == "Equity"
    assert retrieved.sector == "Information Technology"
    assert retrieved.industry == "IT Services"
    assert retrieved.market_cap_category == "Large Cap"
    assert isinstance(retrieved.created_at, datetime)
    assert isinstance(retrieved.updated_at, datetime)
