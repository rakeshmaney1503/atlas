from sqlmodel import Session, select

from atlas.database.models.transaction import Transaction
from atlas.database.session import engine
from atlas.services.categorization_service import CategorizationService

with Session(engine) as session:
    transactions = session.exec(select(Transaction)).all()

    for transaction in transactions:
        transaction.category = CategorizationService.categorize(
            transaction.description
        )

    session.commit()

print(f"Updated {len(transactions)} transactions.")
