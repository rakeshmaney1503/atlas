import pandas as pd
import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.account import Account
from atlas.database.models.transaction import Transaction
from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.ui.ui_helpers import prepare_transaction_rows

st.title("💳 Transactions")

with Session(engine) as session:
    transactions = session.exec(
        select(Transaction).order_by(Transaction.transaction_date.desc())
    ).all()

    accounts = {account.id: account for account in AccountService.get_all(session)}
    opening_balances = {
        account_id: account.opening_balance
        for account_id, account in accounts.items()
    }

if not transactions:
    st.info("No transactions found.")
    st.stop()

rows = prepare_transaction_rows(transactions, opening_balances)

df = pd.DataFrame(rows)

st.metric("Transactions", len(df))

st.dataframe(
    df,
    width="stretch",
    hide_index=True,
)
