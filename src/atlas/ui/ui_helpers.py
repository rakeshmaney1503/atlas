from __future__ import annotations

from decimal import Decimal
from typing import Any
from uuid import UUID

from atlas.database.models.holding import Holding
from atlas.database.models.transaction import Transaction, TransactionType
from atlas.schemas.portfolio import PortfolioSnapshot, PortfolioViewModel
from atlas.services.portfolio_service import PortfolioService


def format_currency(value: Decimal | None) -> str:
    if value is None:
        return ""
    return f"₹ {value:,.2f}"


def prepare_portfolio_snapshot(session: "Session", account_id) -> PortfolioSnapshot:
    return PortfolioService.get_portfolio_snapshot(session, account_id)


def prepare_portfolio_view_model(session: "Session", account_id) -> PortfolioViewModel:
    return PortfolioService.get_portfolio_view_model(session, account_id)


def _transaction_sort_key(transaction: Transaction) -> tuple:
    return (
        transaction.transaction_date,
        transaction.created_at,
        transaction.id,
    )


def _compute_running_balances(
    transactions: list[Transaction],
    opening_balance: Decimal | None = None,
) -> list[Decimal | None]:
    balances: list[Decimal | None] = [t.running_balance for t in transactions]

    if opening_balance is not None and balances[0] is None:
        first_transaction = transactions[0]
        if first_transaction.transaction_type == TransactionType.CREDIT:
            balances[0] = opening_balance + first_transaction.amount
        else:
            balances[0] = opening_balance - first_transaction.amount

    if all(balance is None for balance in balances):
        return balances

    for index in range(1, len(transactions)):
        if balances[index] is None and balances[index - 1] is not None:
            previous = balances[index - 1]
            transaction = transactions[index]
            if transaction.transaction_type == TransactionType.CREDIT:
                balances[index] = previous + transaction.amount
            else:
                balances[index] = previous - transaction.amount

    for index in range(len(transactions) - 2, -1, -1):
        if balances[index] is None and balances[index + 1] is not None:
            next_balance = balances[index + 1]
            transaction = transactions[index + 1]
            if transaction.transaction_type == TransactionType.CREDIT:
                balances[index] = next_balance - transaction.amount
            else:
                balances[index] = next_balance + transaction.amount

    return balances


def prepare_transaction_rows(
    transactions: list[Transaction],
    opening_balances: dict[UUID, Decimal] | None = None,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    account_groups: dict[UUID, list[Transaction]] = {}

    for transaction in transactions:
        account_groups.setdefault(transaction.account_id, []).append(transaction)

    running_balances: dict[str, Decimal | None] = {}
    for account_id, group in account_groups.items():
        sorted_group = sorted(group, key=_transaction_sort_key)
        opening_balance = None
        if opening_balances is not None:
            opening_balance = opening_balances.get(account_id)
        computed = _compute_running_balances(sorted_group, opening_balance)
        for transaction, balance in zip(sorted_group, computed):
            running_balances[str(transaction.id)] = balance

    for t in transactions:
        rows.append(
            {
                "Date": t.transaction_date.date(),
                "Merchant": t.merchant or "",
                "Category": t.category,
                "Type": t.transaction_type.value,
                "Amount": format_currency(t.amount),
                "Running Balance": format_currency(
                    running_balances.get(str(t.id), t.running_balance)
                ),
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
