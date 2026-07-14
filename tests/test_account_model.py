from decimal import Decimal

from sqlmodel import SQLModel, Session, create_engine, select

from atlas.database.models.account import Account, AccountType


def test_create_account() -> None:
    engine = create_engine("sqlite://")

    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="HDFC Salary",
            institution="HDFC Bank",
            account_type=AccountType.SAVINGS,
            currency="INR",
            opening_balance=Decimal("1000.00"),
        )

        session.add(account)
        session.commit()

        saved = session.exec(select(Account)).one()

        assert saved.name == "HDFC Salary"
        assert saved.institution == "HDFC Bank"
        assert saved.account_type == AccountType.SAVINGS
        assert saved.currency == "INR"
        assert saved.opening_balance == Decimal("1000.00")
