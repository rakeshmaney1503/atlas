from pathlib import Path

from sqlmodel import Session, select

from atlas.database.models.account import Account
from atlas.database.models.transaction import Transaction
from atlas.importers.icici_importer import ICICIImporter
from atlas.services.categorization_service import CategorizationService


class ImportService:
    @staticmethod
    def import_transactions(
        session: Session,
        transactions: list[Transaction],
    ) -> tuple[int, int]:
        existing_hashes = set(
            session.exec(
                select(Transaction.import_hash)
            ).all()
        )

        new_transactions = [
            t for t in transactions
            if t.import_hash not in existing_hashes
        ]

        if new_transactions:
            session.add_all(new_transactions)
            session.commit()

        return len(new_transactions), len(transactions) - len(new_transactions)

    @staticmethod
    def import_icici_statement(
        session: Session,
        statement_path: str | Path,
        account: Account,
    ) -> tuple[int, int]:

        df = ICICIImporter.read(statement_path)

        transactions = ICICIImporter.normalize(
            df,
            account.id,
        )

        for transaction in transactions:
            transaction.category = CategorizationService.categorize(
                transaction.description
            )

        return ImportService.import_transactions(
            session,
            transactions,
        )
