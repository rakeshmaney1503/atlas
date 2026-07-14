from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction, TransactionType
from atlas.database.session import engine

income = 0
expense = 0

with Session(engine) as session:
    transactions = session.exec(
        select(Transaction).order_by(Transaction.transaction_date)
    ).all()

print(f"Total transactions: {len(transactions)}")
print()

for t in transactions:
    if t.transaction_type == TransactionType.CREDIT:
        income += float(t.amount)
    else:
        expense += float(t.amount)

print(f"Income : ₹{income:,.2f}")
print(f"Expense: ₹{expense:,.2f}")
print(f"Net     : ₹{income-expense:,.2f}")

print("\nCredits\n--------")
for t in transactions:
    if t.transaction_type == TransactionType.CREDIT:
        print(f"{t.transaction_date.date()}  ₹{float(t.amount):10,.2f}  {t.description}")
