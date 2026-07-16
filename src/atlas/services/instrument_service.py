from __future__ import annotations

from sqlmodel import Session, select

from atlas.database.models.holding import Holding
from atlas.database.models.instrument import Instrument
from atlas.services.providers.fmp_provider import FMPProvider


class InstrumentService:
    @staticmethod
    def create_instrument(
        session: Session,
        instrument: Instrument,
    ) -> Instrument:
        session.add(instrument)
        session.commit()
        session.refresh(instrument)
        return instrument

    @staticmethod
    def get_instrument_by_id(
        session: Session,
        instrument_id,
    ) -> Instrument | None:
        return session.get(Instrument, instrument_id)

    @staticmethod
    def get_instrument_by_symbol(
        session: Session,
        symbol: str,
    ) -> Instrument | None:
        statement = select(Instrument).where(
            Instrument.symbol == symbol,
        )
        return session.exec(statement).first()

    @staticmethod
    def list_instruments(
        session: Session,
    ) -> list[Instrument]:
        return list(session.exec(select(Instrument)).all())

    @staticmethod
    def search_instruments(
        session: Session,
        query: str,
    ) -> list[Instrument]:
        statement = select(Instrument).where(
            Instrument.symbol.contains(query)
            | Instrument.name.contains(query)
        )
        return list(session.exec(statement).all())

    @staticmethod
    def update_instrument(
        session: Session,
        instrument: Instrument,
    ) -> Instrument:
        session.add(instrument)
        session.commit()
        session.refresh(instrument)
        return instrument

    @staticmethod
    def delete_instrument(
        session: Session,
        instrument: Instrument,
    ) -> None:
        session.delete(instrument)
        session.commit()

    @staticmethod
    def seed_from_holdings(
        session: Session,
    ) -> int:
        """
        Create Instrument rows for every unique holding.
        Existing instruments are preserved.
        """

        symbols = {
            h.instrument.strip()
            for h in session.exec(select(Holding)).all()
            if h.instrument and h.instrument.strip()
        }

        existing = {
            i.symbol
            for i in session.exec(select(Instrument)).all()
        }

        created = 0

        for symbol in sorted(symbols):
            if symbol in existing:
                continue

            session.add(
                Instrument(
                    symbol=symbol,
                    name=symbol,
                )
            )
            created += 1

        session.commit()

        return created

    @staticmethod
    def is_metadata_complete(
        instrument: Instrument,
    ) -> bool:
        """
        Determine whether an Instrument already has sufficient metadata.

        This prevents unnecessary provider calls and will later support
        scheduled refresh policies.
        """

        required_fields = (
            instrument.name,
            instrument.exchange,
            instrument.sector,
            instrument.industry,
        )

        return all(
            value is not None and str(value).strip() != ""
            for value in required_fields
        )

    @staticmethod
    def enrich_instrument(
        session: Session,
        instrument: Instrument,
    ) -> Instrument:
        """
        Populate missing metadata from the configured provider.

        Existing values are never overwritten.
        """

        if InstrumentService.is_metadata_complete(instrument):
            return instrument

        provider = FMPProvider()

        profile = provider.get_company_profile(
            instrument.symbol,
        )

        if profile is None:
            return instrument

        if not instrument.name:
            instrument.name = profile.company_name

        if not instrument.exchange:
            instrument.exchange = profile.exchange

        if not instrument.isin:
            instrument.isin = profile.isin

        if not instrument.sector:
            instrument.sector = profile.sector

        if not instrument.industry:
            instrument.industry = profile.industry

        session.add(instrument)
        session.commit()
        session.refresh(instrument)

        return instrument

    @staticmethod
    def enrich_missing_instruments(
        session: Session,
    ) -> int:
        """
        Enrich every instrument that is missing metadata.

        Returns the number of instruments updated.
        """

        updated = 0

        instruments = InstrumentService.list_instruments(session)

        for instrument in instruments:
            if InstrumentService.is_metadata_complete(instrument):
                continue

            InstrumentService.enrich_instrument(
                session,
                instrument,
            )
            updated += 1

        return updated
