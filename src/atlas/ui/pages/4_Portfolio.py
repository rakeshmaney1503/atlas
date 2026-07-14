import pandas as pd
import plotly.express as px
import streamlit as st
from sqlmodel import Session

from atlas.database.models.account import AccountType
from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.ui.ui_helpers import prepare_portfolio_view_model, format_currency

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

    view_model = prepare_portfolio_view_model(session, account.id)

if not view_model.holdings:
    st.info("No holdings found.")
    st.stop()

st.subheader("Portfolio Performance Summary")
summary_cols = st.columns(4)
summary_cols[0].metric(
    "Total Invested Value",
    format_currency(view_model.summary.invested),
)
summary_cols[1].metric(
    "Total Current Value",
    format_currency(view_model.summary.current_value),
)
summary_cols[2].metric(
    "Absolute P&L",
    format_currency(view_model.summary.pnl),
)
summary_cols[3].metric(
    "ROI",
    f"{view_model.summary.percentage_return:.2f}%",
)

st.subheader("Portfolio Health")
health_cols = st.columns(6)
health_cols[0].metric(
    "Diversification Score",
    f"{view_model.summary.diversification_score:.2f}%",
)
health_cols[1].metric(
    "Concentration Risk",
    view_model.summary.concentration_risk,
)
health_cols[2].metric(
    "Largest Holding %",
    f"{view_model.summary.largest_holding_percent:.2f}%",
)
health_cols[3].metric(
    "Top 5 Holdings %",
    f"{view_model.summary.top_5_concentration:.2f}%",
)
health_cols[4].metric(
    "Effective Holdings",
    f"{view_model.summary.effective_holdings:.2f}",
)
health_cols[5].metric(
    "HHI",
    f"{view_model.summary.hhi:.4f}",
)

rows = []

invested = float(view_model.summary.invested)
current = float(view_model.summary.current_value)

for holding in view_model.holdings:
    rows.append(
        {
            "Instrument": holding.instrument,
            "Quantity": float(holding.quantity),
            "Avg Cost": float(holding.average_cost),
            "LTP": float(holding.last_traded_price),
            "Invested": float(holding.invested_amount),
            "Current": float(holding.current_value),
            "P&L": float(holding.pnl),
            "Allocation %": float(holding.allocation_percent),
        }
    )

df = pd.DataFrame(rows)

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

top_df = pd.DataFrame(
    [
        {
            "Instrument": holding.instrument,
            "Current": float(holding.current_value),
            "Allocation %": float(holding.allocation_percent),
        }
        for holding in view_model.top_holdings
    ]
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
