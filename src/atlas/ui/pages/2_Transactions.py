import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction
from atlas.database.session import engine

st.title("💳 Transactions")

with Session(engine) as session:
    transactions = session.exec(
        select(Transaction).order_by(Transaction.transaction_date.desc())
    ).all()

if not transactions:
    st.info("No transactions found.")
    st.stop()

rows = []

for t in transactions:
    rows.append(
        {
            "Date": t.transaction_date.date(),
            "Category": t.category,
            "Type": t.transaction_type.value,
            "Amount": float(t.amount),
            "Description": t.description,
        }
    )

df = pd.DataFrame(rows)

st.metric("Transactions", len(df))

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
)
