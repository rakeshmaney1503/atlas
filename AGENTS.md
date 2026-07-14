# Atlas AI Operating Manual

## Project

Atlas is a Personal Financial Operating System.

It is NOT a budgeting app.

It is NOT a stock screener.

It is NOT a portfolio tracker.

Its purpose is to become a Personal Chief Investment Officer (Personal CIO).

Atlas should eventually help me:

- Understand my complete financial life.
- Protect my existing corpus.
- Grow wealth safely over decades.
- Make better financial decisions.
- Explain every recommendation.
- Reduce unnecessary risk.
- Invest with conviction instead of emotion.

Every feature must move Atlas closer to that vision.

---

# Core Principles

Atlas values:

1. Correctness over speed.
2. Simplicity over cleverness.
3. Maintainability over unnecessary abstraction.
4. Explainability over black-box decisions.
5. Long-term investing over trading.
6. Capital preservation before return maximization.
7. One source of truth for every financial calculation.
8. Small reviewable changes.

---

# Technology

Python 3.13

uv

SQLite

SQLModel

Streamlit

Pandas

Plotly

Never use pip.

---

# Architecture

Importers

↓

Database Models

↓

Business Services

↓

Analytics

↓

Decision Engine

↓

Streamlit UI

Business logic belongs in Services.

UI should never contain financial calculations.

All money uses Decimal.

---

# Financial Rules

The imported financial statement is always the source of truth.

Never overwrite imported financial data.

Never recompute values already supplied by the bank unless explicitly requested.

Running Balance from statements is authoritative.

Net Worth

=

Cash

+

Investments

Every recommendation must be explainable.

Atlas should prefer saying:

"Wait"

or

"Do Nothing"

instead of encouraging unnecessary trading.

---

# AI Rules

Before implementing anything:

1. Read this document.
2. Read the relevant code.
3. Understand the current architecture.
4. Think through the implementation.
5. Explain the implementation plan.
6. Wait for approval.

Only then write code.

---

# Scope Rules

Implement ONE feature at a time.

Never combine multiple features.

Never redesign the architecture unless requested.

Never modify unrelated files.

If another improvement is discovered:

Document it.

Stop.

Wait.

---

# Feature Definition of Done

A feature is complete only when all four layers are finished.

1. Data

Models

Importers

Database

2. Business

Services

Calculations

Rules

3. UI

Visible in Streamlit

Professional presentation

Easy to verify

4. Verification

Tests

Verification commands

UI verification steps

---

# Development Workflow

For every feature:

1. Understand the feature.

2. Present the implementation plan.

3. List every file to be modified.

4. Wait for approval.

5. Implement the feature.

6. Update tests.

7. Explain every change.

8. Provide:

uv run pytest

uv run streamlit run src/atlas/ui/app.py

9. Explain exactly how to verify the feature from the UI.

Then stop.

---

# Coding Standards

Use type hints.

Use Decimal for money.

Reuse existing code.

Avoid duplicate logic.

Keep functions small.

Keep code readable.

Write comments only when they improve understanding.

---

# Roadmap

Phase 1

Financial Foundation

- Accounts
- Transactions
- Cash Balance
- Holdings
- Net Worth
- Merchant Recognition
- Categories
- Rules Engine

Phase 2

Financial Management

- Budgets
- Goals
- Cash Flow
- Subscription Detection
- Analytics

Phase 3

Portfolio Intelligence

- Portfolio Allocation
- Sector Allocation
- Diversification
- Concentration Risk
- Performance
- XIRR
- CAGR

Phase 4

Company Intelligence

- Financial Statements
- Growth
- Profitability
- Valuation
- Quality Score
- Fair Value

Phase 5

Risk Engine

- Concentration Risk
- Sector Risk
- Liquidity Risk
- Downside Analysis
- Goal Protection
- Emergency Fund Analysis

Phase 6

Decision Engine

Recommendations:

Buy

Hold

Sell

Reduce

Accumulate

Wait

Do Nothing

Every recommendation must include:

Evidence

Risk

Confidence

Explanation

Phase 7

Personal CIO

Atlas should eventually answer:

What changed?

What should I do?

What should I not do?

Is my corpus safe?

What is my biggest financial risk?

Where should my next ₹10,000 go?

How do I reach financial independence sooner?

---

# Never Do

Never use pip.

Never delete atlas.db to solve schema problems.

Never silently change financial calculations.

Never modify unrelated files.

Never guess.

Ask instead.

Never sacrifice correctness for speed.

Always leave Atlas in a working state.
Every feature should build a foundation for future features, not just solve today's problem.