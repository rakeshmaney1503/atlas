from sqlmodel import Session, select

from atlas.database.models.account import Account, AccountType


class AccountService:
    @staticmethod
    def get_all(session: Session) -> list[Account]:
        return session.exec(
            select(Account).order_by(Account.name)
        ).all()

    @staticmethod
    def get_by_name(
        session: Session,
        name: str,
    ) -> Account | None:
        return session.exec(
            select(Account).where(Account.name == name)
        ).first()

    @staticmethod
    def create(
        session: Session,
        *,
        name: str,
        institution: str,
        account_type: AccountType,
    ) -> Account:
        account = Account(
            name=name,
            institution=institution,
            account_type=account_type,
        )

        session.add(account)
        session.commit()
        session.refresh(account)

        return account

    @staticmethod
    def get_or_create(
        session: Session,
        *,
        name: str,
        institution: str,
        account_type: AccountType,
    ) -> Account:
        account = AccountService.get_by_name(session, name)

        if account:
            return account

        return AccountService.create(
            session,
            name=name,
            institution=institution,
            account_type=account_type,
        )
