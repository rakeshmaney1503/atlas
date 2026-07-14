import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction
from atlas.database.session import engine
from atlas.ui.ui_helpers import prepare_transaction_rows

st.title("💳 Transactions")

with Session(engine) as session:
    transactions = session.exec(
        select(Transaction).order_by(Transaction.transaction_date.desc())
    ).all()

if not transactions:
    st.info("No transactions found.")
    st.stop()

rows = prepare_transaction_rows(transactions)

df = pd.DataFrame(rows)

st.metric("Transactions", len(df))

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
)
