from decimal import Decimal

from sqlmodel import Session, select

from atlas.database.models.account import Account, AccountType
from atlas.database.models.transaction import Transaction, TransactionType


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
    def get_current_balance(
        session: Session,
        account: Account,
    ) -> Decimal:
        transactions = session.exec(
            select(Transaction)
            .where(Transaction.account_id == account.id)
            .order_by(
                Transaction.transaction_date,
                Transaction.created_at,
                Transaction.id,
            )
        ).all()

        if not transactions:
            return account.opening_balance

        latest_running_index = None
        for index, transaction in enumerate(transactions):
            if transaction.running_balance is not None:
                latest_running_index = index

        if latest_running_index is None:
            balance = account.opening_balance
            for transaction in transactions:
                if transaction.transaction_type == TransactionType.CREDIT:
                    balance += transaction.amount
                else:
                    balance -= transaction.amount
            return balance

        balance = transactions[latest_running_index].running_balance
        for transaction in transactions[latest_running_index + 1 :]:
            if transaction.transaction_type == TransactionType.CREDIT:
                balance += transaction.amount
            else:
                balance -= transaction.amount
        return balance

    @staticmethod
    def get_cash_balance(session: Session) -> Decimal:
        return sum(
            (
                AccountService.get_current_balance(session, account)
                for account in AccountService.get_all(session)
                if account.account_type != AccountType.INVESTMENT
            ),
            Decimal("0.00"),
        )

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
