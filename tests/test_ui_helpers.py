from datetime import datetime
from decimal import Decimal
from uuid import UUID

from atlas.database.models.holding import Holding
from atlas.database.models.transaction import Transaction, TransactionType
from atlas.ui.ui_helpers import (
    compute_dashboard_totals,
    compute_net_worth,
    format_currency,
    prepare_transaction_rows,
)


def test_prepare_transaction_rows_includes_running_balance_column() -> None:
    transactions = [
        Transaction(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("100.00"),
            transaction_type=TransactionType.CREDIT,
            description="Salary",
            running_balance=Decimal("1100.00"),
            import_hash="hash1",
        )
    ]

    rows = prepare_transaction_rows(transactions)

    assert rows[0]["Running Balance"] == "₹ 1,100.00"
    assert rows[0]["Amount"] == "₹ 100.00"
    assert rows[0]["Merchant"] == ""
    assert rows[0]["Description"] == "Salary"
    assert list(rows[0].keys()) == [
        "Date",
        "Merchant",
        "Category",
        "Type",
        "Amount",
        "Running Balance",
        "Description",
    ]


def test_compute_dashboard_totals_uses_latest_cash_balance_and_sums_transactions() -> None:
    transactions = [
        Transaction(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            transaction_date=datetime(2026, 7, 1),
            amount=Decimal("100.00"),
            transaction_type=TransactionType.CREDIT,
            description="Salary",
            running_balance=Decimal("1100.00"),
            import_hash="hash1",
        ),
        Transaction(
            account_id=UUID("11111111-1111-1111-1111-111111111111"),
            transaction_date=datetime(2026, 7, 2),
            amount=Decimal("50.00"),
            transaction_type=TransactionType.DEBIT,
            description="Coffee",
            running_balance=Decimal("1050.00"),
            import_hash="hash2",
        ),
    ]

    totals = compute_dashboard_totals(transactions, Decimal("1050.00"))

    assert totals["cash_balance"] == Decimal("1050.00")
    assert totals["income"] == Decimal("100.00")
    assert totals["expense"] == Decimal("50.00")
    assert totals["net_cash_flow"] == Decimal("50.00")


def test_compute_net_worth_adds_cash_and_investments() -> None:
    holdings = [
        Holding(
            account_id=UUID("22222222-2222-2222-2222-222222222222"),
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
    ]

    totals = compute_net_worth(Decimal("1000.00"), holdings)

    assert totals["cash_balance"] == Decimal("1000.00")
    assert totals["investment_value"] == Decimal("1500.00")
    assert totals["net_worth"] == Decimal("2500.00")


def test_format_currency_returns_empty_for_none() -> None:
    assert format_currency(None) == ""
    assert format_currency(Decimal("1234.56")) == "₹ 1,234.56"
