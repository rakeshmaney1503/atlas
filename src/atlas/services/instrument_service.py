from uuid import UUID

from sqlmodel import Session, select

from atlas.database.models.instrument import Instrument


class InstrumentService:
    @staticmethod
    def create_instrument(session: Session, instrument: Instrument) -> Instrument:
        session.add(instrument)
        session.commit()
        session.refresh(instrument)
        return instrument

    @staticmethod
    def get_instrument_by_id(session: Session, instrument_id: UUID) -> Instrument | None:
        return session.get(Instrument, instrument_id)

    @staticmethod
    def get_instrument_by_symbol(session: Session, symbol: str) -> Instrument | None:
        statement = select(Instrument).where(Instrument.symbol == symbol)
        return session.exec(statement).first()

    @staticmethod
    def list_instruments(session: Session) -> list[Instrument]:
        statement = select(Instrument).order_by(Instrument.symbol)
        return session.exec(statement).all()

    @staticmethod
    def search_instruments(session: Session, query: str) -> list[Instrument]:
        statement = select(Instrument).where(
            (Instrument.symbol.contains(query))
            | (Instrument.name.contains(query))
            | (Instrument.sector.contains(query))
            | (Instrument.industry.contains(query))
        )
        return session.exec(statement).all()

    @staticmethod
    def update_instrument(session: Session, instrument: Instrument) -> Instrument:
        session.add(instrument)
        session.commit()
        session.refresh(instrument)
        return instrument

    @staticmethod
    def delete_instrument(session: Session, instrument: Instrument) -> None:
        session.delete(instrument)
        session.commit()
