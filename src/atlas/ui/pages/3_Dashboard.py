from decimal import Decimal

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction, TransactionType
from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.ui.ui_helpers import compute_dashboard_totals

st.title("📊 Dashboard")

with Session(engine) as session:
    transactions = session.exec(select(Transaction)).all()
    cash_balance = AccountService.get_cash_balance(session)

if not transactions:
    st.info("No transactions available.")
    st.metric("Cash Balance", f"₹ {cash_balance:,.2f}")
    st.stop()

rows = [
    {
        "date": t.transaction_date,
        "category": t.category,
        "type": t.transaction_type.value,
        "amount": float(t.amount),
    }
    for t in transactions
]

df = pd.DataFrame(rows)

totals = compute_dashboard_totals(transactions, cash_balance)

c1, c2, c3, c4 = st.columns(4)

c1.metric("Current Cash Balance", f"₹ {totals['cash_balance']:,.2f}")
c2.metric("Total Expenses", f"₹ {totals['expense']:,.2f}")
c3.metric("Total Income", f"₹ {totals['income']:,.2f}")
c4.metric("Net Cash Flow", f"₹ {totals['net_cash_flow']:,.2f}")

st.divider()

category_df = (
    df[df["type"] == TransactionType.DEBIT.value]
    .groupby("category")["amount"]
    .sum()
    .reset_index()
)

fig = px.pie(
    category_df,
    names="category",
    values="amount",
    title="Expenses by Category",
)

st.plotly_chart(fig, width="stretch")
