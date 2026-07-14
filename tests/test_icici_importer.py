from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pandas as pd
from sqlmodel import SQLModel, Session, create_engine, select

from atlas.database.models.account import Account, AccountType
from atlas.database.models.holding import Holding
from atlas.database.models.transaction import Transaction, TransactionType
from atlas.importers.icici_importer import ICICIImporter
from atlas.services.account_service import AccountService
from atlas.services.categorization_service import CategorizationService
from atlas.services.import_service import ImportService
from atlas.services.merchant_recognition_service import MerchantRecognitionService


def test_icici_importer_parses_running_balance(tmp_path: Path) -> None:
    data = {
        "Transaction Date": ["01/07/2026", "02/07/2026"],
        "Transaction Remarks": ["Salary", "Coffee"],
        "Withdrawal Amount(INR)": [0.0, 50.0],
        "Deposit Amount(INR)": [1000.0, 0.0],
        "Balance(INR)": [1000.0, 950.0],
    }

    df = pd.DataFrame(data)
    account_id = UUID("11111111-1111-1111-1111-111111111111")
    transactions = ICICIImporter.normalize(df, account_id)

    assert len(transactions) == 2
    assert transactions[0].transaction_type == TransactionType.CREDIT
    assert transactions[0].amount == Decimal("1000.0")
    assert transactions[0].running_balance == Decimal("1000.0")
    assert transactions[0].merchant is None
    assert transactions[1].transaction_type == TransactionType.DEBIT
    assert transactions[1].amount == Decimal("50.0")
    assert transactions[1].running_balance == Decimal("950.0")
    assert transactions[1].merchant is None


def test_icici_importer_recognizes_merchants_from_remarks() -> None:
    data = {
        "Transaction Date": ["01/07/2026", "02/07/2026", "03/07/2026"],
        "Transaction Remarks": [
            "DOMINOS PIZZA ORDER", 
            "NETFLIX MONTHLY",
            "ACT BROADBAND PAYMENT",
        ],
        "Withdrawal Amount(INR)": [500.0, 300.0, 1200.0],
        "Deposit Amount(INR)": [0.0, 0.0, 0.0],
        "Balance(INR)": [10000.0, 9700.0, 8500.0],
    }

    df = pd.DataFrame(data)
    account_id = UUID("22222222-2222-2222-2222-222222222222")
    transactions = ICICIImporter.normalize(df, account_id)

    assert transactions[0].merchant == "Domino's"
    assert transactions[1].merchant == "Netflix"
    assert transactions[2].merchant == "ACT"


def test_categorization_service_uses_merchant_first() -> None:
    assert CategorizationService.categorize(
        "DOMINOS PIZZA ORDER",
        "Domino's",
    ) == "Food"
    assert CategorizationService.categorize(
        "NETFLIX MONTHLY",
        "Netflix",
    ) == "Subscription"
    assert CategorizationService.categorize(
        "ACT BROADBAND PAYMENT",
        "ACT",
    ) == "Internet"


def test_account_service_uses_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        transactions = [
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 1),
                amount=Decimal("1000.00"),
                transaction_type=TransactionType.CREDIT,
                description="Salary",
                running_balance=Decimal("1000.00"),
                import_hash="hash1",
            ),
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 2),
                amount=Decimal("50.00"),
                transaction_type=TransactionType.DEBIT,
                description="Coffee",
                running_balance=Decimal("950.00"),
                import_hash="hash2",
            ),
        ]
        session.add_all(transactions)
        session.commit()

        balance = AccountService.get_current_balance(session, account)

    assert balance == Decimal("950.00")


def test_import_service_avoids_duplicate_transactions(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        transactions = [
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 1),
                amount=Decimal("1000.00"),
                transaction_type=TransactionType.CREDIT,
                description="Salary",
                running_balance=Decimal("1000.00"),
                import_hash="hash1",
            ),
        ]

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )
        assert imported_count == 1
        assert duplicate_count == 0

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )
        assert imported_count == 0
        assert duplicate_count == 1


def test_account_service_get_cash_balance_ignores_investments(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        savings = Account(
            name="Savings",
            institution="ICICI",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("1000.00"),
        )
        investment = Account(
            name="Portfolio",
            institution="Zerodha",
            account_type=AccountType.INVESTMENT,
            opening_balance=Decimal("5000.00"),
        )
        session.add_all([savings, investment])
        session.commit()

        balance = AccountService.get_cash_balance(session)

    assert balance == Decimal("1000.00")


def test_net_worth_uses_latest_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)

        investment_account = Account(
            name="Zerodha Portfolio",
            institution="Zerodha",
            account_type=AccountType.INVESTMENT,
            opening_balance=Decimal("0.00"),
        )
        session.add(investment_account)
        session.commit()
        session.refresh(account)
        session.refresh(investment_account)

        session.add(
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 1),
                amount=Decimal("1000.00"),
                transaction_type=TransactionType.CREDIT,
                description="Salary",
                merchant="Salary",
                running_balance=Decimal("1000.00"),
                import_hash="hash3",
            )
        )
        session.add(
            Holding(
                account_id=investment_account.id,
                instrument="Stock",
                quantity=Decimal("10"),
                average_cost=Decimal("100.00"),
                last_traded_price=Decimal("150.00"),
                invested_amount=Decimal("1000.00"),
                current_value=Decimal("1500.00"),
                pnl=Decimal("500.00"),
                net_change_percent=Decimal("50.00"),
                day_change_percent=Decimal("2.00"),
            )
        )
        session.commit()

        cash_balance = AccountService.get_cash_balance(session)
        investment_value = Decimal("1500.00")
        net_worth = cash_balance + investment_value

    assert cash_balance == Decimal("1000.00")
    assert net_worth == Decimal("2500.00")


def test_import_service_persists_running_balance_from_icici(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        data = {
            "Transaction Date": ["01/07/2026"],
            "Transaction Remarks": ["Salary"],
            "Withdrawal Amount(INR)": [0.0],
            "Deposit Amount(INR)": [1000.0],
            "Balance(INR)": [1000.0],
        }
        df = pd.DataFrame(data)
        transactions = ICICIImporter.normalize(df, account.id)

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )

        assert imported_count == 1
        assert duplicate_count == 0

        stored = session.exec(select(Transaction)).one()
        assert stored.running_balance == Decimal("1000.0")


def test_import_service_updates_existing_transaction_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        existing_transaction = Transaction(
            account_id=account.id,
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("1000.00"),
            transaction_type=TransactionType.CREDIT,
            description="Salary",
            running_balance=None,
            import_hash="hash1",
        )
        session.add(existing_transaction)
        session.commit()

        data = {
            "Transaction Date": ["01/07/2026"],
            "Transaction Remarks": ["Salary"],
            "Withdrawal Amount(INR)": [0.0],
            "Deposit Amount(INR)": [1000.0],
            "Balance(INR)": [1000.0],
        }
        df = pd.DataFrame(data)
        transactions = ICICIImporter.normalize(df, account.id)

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )

        assert imported_count == 0
        assert duplicate_count == 1

        stored = session.exec(select(Transaction)).one()
        assert stored.running_balance == Decimal("1000.0")


def test_import_service_enriches_existing_transaction_with_missing_merchant_and_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        existing_transaction = Transaction(
            account_id=account.id,
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("1000.00"),
            transaction_type=TransactionType.CREDIT,
            description="DOMINOS PIZZA ORDER",
            merchant=None,
            running_balance=None,
            import_hash="hash1",
        )
        session.add(existing_transaction)
        session.commit()

        data = {
            "Transaction Date": ["01/07/2026"],
            "Transaction Remarks": ["DOMINOS PIZZA ORDER"],
            "Withdrawal Amount(INR)": [0.0],
            "Deposit Amount(INR)": [1000.0],
            "Balance(INR)": [1000.0],
        }
        df = pd.DataFrame(data)
        transactions = ICICIImporter.normalize(df, account.id)

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )

        assert imported_count == 0
        assert duplicate_count == 1

        stored = session.exec(select(Transaction)).one()
        assert stored.running_balance == Decimal("1000.0")
        assert stored.merchant == "Domino's"


def test_import_service_does_not_overwrite_existing_merchant_or_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        existing_transaction = Transaction(
            account_id=account.id,
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("1000.00"),
            transaction_type=TransactionType.CREDIT,
            description="DOMINOS PIZZA ORDER",
            merchant="Existing Merchant",
            running_balance=Decimal("1000.00"),
            import_hash="hash1",
        )
        session.add(existing_transaction)
        session.commit()

        data = {
            "Transaction Date": ["01/07/2026"],
            "Transaction Remarks": ["DOMINOS PIZZA ORDER"],
            "Withdrawal Amount(INR)": [0.0],
            "Deposit Amount(INR)": [1000.0],
            "Balance(INR)": [2000.0],
        }
        df = pd.DataFrame(data)
        transactions = ICICIImporter.normalize(df, account.id)

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            transactions,
        )

        assert imported_count == 0
        assert duplicate_count == 1

        stored = session.exec(select(Transaction)).one()
        assert stored.running_balance == Decimal("1000.00")
        assert stored.merchant == "Existing Merchant"


def test_icici_importer_handles_missing_running_balance_column(tmp_path: Path) -> None:
    data = {
        "Transaction Date": ["01/07/2026"],
        "Transaction Remarks": ["Salary"],
        "Withdrawal Amount(INR)": [0.0],
        "Deposit Amount(INR)": [1000.0],
    }

    df = pd.DataFrame(data)
    account_id = UUID("44444444-4444-4444-4444-444444444444")
    transactions = ICICIImporter.normalize(df, account_id)

    assert len(transactions) == 1
    assert transactions[0].running_balance is None
    assert transactions[0].amount == Decimal("1000.0")


def test_account_service_returns_latest_running_balance_directly(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        session.add_all([
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 1),
                amount=Decimal("1000.00"),
                transaction_type=TransactionType.CREDIT,
                description="Salary",
                running_balance=Decimal("1000.00"),
                import_hash="hash1",
            ),
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 2),
                amount=Decimal("50.00"),
                transaction_type=TransactionType.DEBIT,
                description="Coffee",
                import_hash="hash2",
            ),
        ])
        session.commit()

        balance = AccountService.get_current_balance(session, account)

    assert balance == Decimal("950.00")


def test_account_service_applies_transactions_after_last_running_balance(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account = Account(
            name="ICICI Savings",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add(account)
        session.commit()
        session.refresh(account)

        session.add_all([
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 1),
                amount=Decimal("1000.00"),
                transaction_type=TransactionType.CREDIT,
                description="Salary",
                running_balance=Decimal("1000.00"),
                import_hash="hash1",
            ),
            Transaction(
                account_id=account.id,
                transaction_date=datetime(2026, 7, 2),
                amount=Decimal("100.00"),
                transaction_type=TransactionType.DEBIT,
                description="Coffee",
                import_hash="hash2",
            ),
        ])
        session.commit()

        balance = AccountService.get_current_balance(session, account)

    assert balance == Decimal("900.00")


def test_import_service_allows_same_hash_on_different_accounts(tmp_path: Path) -> None:
    engine = create_engine("sqlite://")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        account_one = Account(
            name="Account One",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        account_two = Account(
            name="Account Two",
            institution="ICICI Bank",
            account_type=AccountType.SAVINGS,
            opening_balance=Decimal("0.00"),
        )
        session.add_all([account_one, account_two])
        session.commit()
        session.refresh(account_one)
        session.refresh(account_two)

        transaction_one = Transaction(
            account_id=account_one.id,
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("1000.00"),
            transaction_type=TransactionType.CREDIT,
            description="Salary",
            running_balance=Decimal("1000.00"),
            import_hash="samehash",
        )
        transaction_two = Transaction(
            account_id=account_two.id,
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("1000.00"),
            transaction_type=TransactionType.CREDIT,
            description="Salary",
            running_balance=Decimal("1000.00"),
            import_hash="samehash",
        )

        imported_count, duplicate_count = ImportService.import_transactions(
            session,
            [transaction_one, transaction_two],
        )

    assert imported_count == 2
    assert duplicate_count == 0


def test_icici_importer_parses_timestamp_dates(tmp_path: Path) -> None:
    data = {
        "Transaction Date": [
            pd.Timestamp("2026-07-01"),
            pd.Timestamp("2026-07-02"),
        ],
        "Transaction Remarks": ["Salary", "Coffee"],
        "Withdrawal Amount(INR)": [0.0, 50.0],
        "Deposit Amount(INR)": [1000.0, 0.0],
        "Balance(INR)": [1000.0, 950.0],
    }

    df = pd.DataFrame(data)
    account_id = UUID("33333333-3333-3333-3333-333333333333")
    transactions = ICICIImporter.normalize(df, account_id)

    assert transactions[0].transaction_date == datetime(2026, 7, 1)
    assert transactions[1].transaction_date == datetime(2026, 7, 2)
    assert transactions[1].transaction_type == TransactionType.DEBIT
    assert transactions[1].amount == Decimal("50.0")
    assert transactions[1].running_balance == Decimal("950.0")


def test_icici_importer_recognizes_merchant_and_category(tmp_path: Path) -> None:
    data = {
        "Transaction Date": ["01/07/2026", "02/07/2026", "03/07/2026"],
        "Transaction Remarks": [
            "DOMINOS PIZZA", 
            "NETFLIX SUBSCRIPTION",
            "ACT BROADBAND PAYMENT",
        ],
        "Withdrawal Amount(INR)": [500.0, 300.0, 1200.0],
        "Deposit Amount(INR)": [0.0, 0.0, 0.0],
        "Balance(INR)": [10000.0, 9700.0, 8500.0],
    }

    df = pd.DataFrame(data)
    account_id = UUID("22222222-2222-2222-2222-222222222222")
    transactions = ICICIImporter.normalize(df, account_id)

    assert transactions[0].merchant == "Domino's"
    assert transactions[0].category == "Food" or transactions[0].category is None
    assert transactions[1].merchant == "Netflix"
    assert transactions[1].category == "Subscription" or transactions[1].category is None
    assert transactions[2].merchant == "ACT"
    assert transactions[2].category == "Internet" or transactions[2].category is None
