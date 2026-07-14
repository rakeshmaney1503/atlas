from __future__ import annotations

from decimal import Decimal
from typing import Any

from atlas.database.models.holding import Holding
from atlas.database.models.transaction import Transaction, TransactionType


def format_currency(value: Decimal | None) -> str:
    if value is None:
        return ""
    return f"₹ {value:,.2f}"


def prepare_transaction_rows(transactions: list[Transaction]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for t in transactions:
        rows.append(
            {
                "Date": t.transaction_date.date(),
                "Merchant": t.merchant or "",
                "Category": t.category,
                "Type": t.transaction_type.value,
                "Amount": format_currency(t.amount),
                "Running Balance": format_currency(t.running_balance),
                "Description": t.description,
            }
        )
    return rows


def compute_dashboard_totals(
    transactions: list[Transaction],
    cash_balance: Decimal,
) -> dict[str, Decimal]:
    income = sum(
        (
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.CREDIT
        ),
        Decimal("0.00"),
    )
    expense = sum(
        (
            t.amount
            for t in transactions
            if t.transaction_type == TransactionType.DEBIT
        ),
        Decimal("0.00"),
    )
    return {
        "cash_balance": cash_balance,
        "income": income,
        "expense": expense,
        "net_cash_flow": income - expense,
    }


def compute_net_worth(cash_balance: Decimal, holdings: list[Holding]) -> dict[str, Decimal]:
    investment_value = sum(
        (h.current_value for h in holdings),
        Decimal("0.00"),
    )
    return {
        "cash_balance": cash_balance,
        "investment_value": investment_value,
        "net_worth": cash_balance + investment_value,
    }
