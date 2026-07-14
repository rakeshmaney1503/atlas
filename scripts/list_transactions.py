from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction
from atlas.database.session import engine

with Session(engine) as session:
    transactions = session.exec(select(Transaction)).all()

print(f"Total transactions: {len(transactions)}")
print()

for transaction in transactions[:20]:
    print(
        f"{transaction.transaction_date.date()} | "
        f"{transaction.category:<12} | "
        f"{transaction.amount:10.2f} | "
        f"{transaction.description}"
    )
