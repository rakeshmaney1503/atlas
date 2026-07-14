from decimal import Decimal

import streamlit as st
from sqlmodel import Session, select

from atlas.database.models.holding import Holding
from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.ui.ui_helpers import compute_net_worth

st.set_page_config(
    page_title="Net Worth",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Net Worth")

with Session(engine) as session:
    holdings = session.exec(select(Holding)).all()
    cash_balance = AccountService.get_cash_balance(session)

totals = compute_net_worth(cash_balance, holdings)

c1, c2, c3 = st.columns(3)

c1.metric(
    "Cash",
    f"₹ {totals['cash_balance']:,.2f}",
)

c2.metric(
    "Investments",
    f"₹ {totals['investment_value']:,.2f}",
)

c3.metric(
    "Net Worth",
    f"₹ {totals['net_worth']:,.2f}",
)

st.divider()

st.subheader("Investments")

st.dataframe(
    [
        {
            "Instrument": h.instrument,
            "Current Value": f"₹ {h.current_value:,.2f}",
            "P&L": f"₹ {h.pnl:,.2f}",
        }
        for h in holdings
    ],
    width="stretch",
    hide_index=True,
)
