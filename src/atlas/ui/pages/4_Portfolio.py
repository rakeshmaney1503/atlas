import pandas as pd
import plotly.express as px
import streamlit as st
from sqlmodel import Session

from atlas.database.models.account import AccountType
from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.services.holding_service import HoldingService

st.set_page_config(
    page_title="Portfolio",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Portfolio")

with Session(engine) as session:
    account = next(
        (
            a
            for a in AccountService.get_all(session)
            if a.account_type == AccountType.INVESTMENT
        ),
        None,
    )

    if account is None:
        st.info("No investment account found.")
        st.stop()

    holdings = HoldingService.get_holdings(
        session,
        account.id,
    )

if not holdings:
    st.info("No holdings found.")
    st.stop()

rows = []

invested = 0.0
current = 0.0

for h in holdings:
    invested += float(h.invested_amount)
    current += float(h.current_value)

    rows.append(
        {
            "Instrument": h.instrument,
            "Quantity": float(h.quantity),
            "Avg Cost": float(h.average_cost),
            "LTP": float(h.last_traded_price),
            "Invested": float(h.invested_amount),
            "Current": float(h.current_value),
            "P&L": float(h.pnl),
        }
    )

df = pd.DataFrame(rows)

df["Allocation %"] = (
    df["Current"] / current * 100
).round(2)

summary1, summary2, summary3 = st.columns(3)

summary1.metric(
    "Invested",
    f"₹ {invested:,.2f}",
)

summary2.metric(
    "Current Value",
    f"₹ {current:,.2f}",
)

summary3.metric(
    "Overall P&L",
    f"₹ {current - invested:,.2f}",
)

st.divider()

st.subheader("Portfolio Holdings")

display_df = df.copy()

display_df["Invested"] = display_df["Invested"].map(
    lambda x: f"₹ {x:,.2f}"
)

display_df["Current"] = display_df["Current"].map(
    lambda x: f"₹ {x:,.2f}"
)

display_df["P&L"] = display_df["P&L"].map(
    lambda x: f"₹ {x:,.2f}"
)

display_df["Avg Cost"] = display_df["Avg Cost"].map(
    lambda x: f"₹ {x:,.2f}"
)

display_df["LTP"] = display_df["LTP"].map(
    lambda x: f"₹ {x:,.2f}"
)

display_df["Allocation %"] = display_df["Allocation %"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    display_df[
        [
            "Instrument",
            "Quantity",
            "Avg Cost",
            "LTP",
            "Invested",
            "Current",
            "P&L",
            "Allocation %",
        ]
    ],
    width="stretch",
    hide_index=True,
)

st.divider()

st.subheader("Portfolio Allocation")

fig = px.pie(
    df,
    names="Instrument",
    values="Current",
    hole=0.45,
)

fig.update_layout(
    height=550,
    margin=dict(
        l=20,
        r=180,
        t=40,
        b=20,
    ),
    legend=dict(
        orientation="v",
        y=0.5,
        yanchor="middle",
        x=1.02,
        xanchor="left",
    ),
)

st.plotly_chart(
    fig,
    width="stretch",
)

st.divider()

st.subheader("Top Holdings")

top_df = (
    df.sort_values(
        "Current",
        ascending=False,
    )[
        [
            "Instrument",
            "Current",
            "Allocation %",
        ]
    ]
    .copy()
)

top_df["Current"] = top_df["Current"].map(
    lambda x: f"₹ {x:,.2f}"
)

top_df["Allocation %"] = top_df["Allocation %"].map(
    lambda x: f"{x:.2f}%"
)

st.dataframe(
    top_df,
    width="stretch",
    hide_index=True,
)
