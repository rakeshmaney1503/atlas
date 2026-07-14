import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.account import Account, AccountType
from atlas.database.models.holding import Holding
from atlas.database.models.transaction import Transaction
from atlas.database.session import engine

st.set_page_config(
    page_title="Net Worth",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Net Worth")

with Session(engine) as session:

    accounts = session.exec(select(Account)).all()

    holdings = session.exec(select(Holding)).all()

    transactions = session.exec(select(Transaction)).all()

cash_balance = 0.0

for account in accounts:
    if account.account_type != AccountType.INVESTMENT:

        account_transactions = [
            t
            for t in transactions
            if t.account_id == account.id
        ]

        if account_transactions:
            latest = max(
                account_transactions,
                key=lambda t: t.transaction_date,
            )
            cash_balance += float(latest.amount if False else 0)

investment_value = sum(
    float(h.current_value)
    for h in holdings
)

net_worth = cash_balance + investment_value

c1, c2, c3 = st.columns(3)

c1.metric(
    "Cash",
    f"₹ {cash_balance:,.2f}",
)

c2.metric(
    "Investments",
    f"₹ {investment_value:,.2f}",
)

c3.metric(
    "Net Worth",
    f"₹ {net_worth:,.2f}",
)

st.divider()

st.subheader("Investments")

st.dataframe(
    [
        {
            "Instrument": h.instrument,
            "Current Value": f"₹ {float(h.current_value):,.2f}",
            "P&L": f"₹ {float(h.pnl):,.2f}",
        }
        for h in holdings
    ],
    width="stretch",
    hide_index=True,
)
