import pandas as pd
import plotly.express as px
import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction, TransactionType
from atlas.database.session import engine

st.title("📊 Dashboard")

with Session(engine) as session:
    transactions = session.exec(select(Transaction)).all()

if not transactions:
    st.info("No transactions available.")
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

income = df[df["type"] == TransactionType.CREDIT.value]["amount"].sum()
expense = df[df["type"] == TransactionType.DEBIT.value]["amount"].sum()

c1, c2, c3 = st.columns(3)

c1.metric("Income", f"₹ {income:,.2f}")
c2.metric("Expense", f"₹ {expense:,.2f}")
c3.metric("Net Cash Flow", f"₹ {(income-expense):,.2f}")

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
