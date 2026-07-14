from sqlmodel import Session, delete, select

from atlas.database.models.holding import Holding


class HoldingService:
    @staticmethod
    def replace_holdings(
        session: Session,
        account_id,
        holdings: list[Holding],
    ) -> int:

        session.exec(
            delete(Holding).where(
                Holding.account_id == account_id
            )
        )

        session.add_all(holdings)

        session.commit()

        return len(holdings)

    @staticmethod
    def get_holdings(
        session: Session,
        account_id,
    ) -> list[Holding]:

        return session.exec(
            select(Holding)
            .where(Holding.account_id == account_id)
            .order_by(Holding.current_value.desc())
        ).all()
