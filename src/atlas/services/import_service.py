from pathlib import Path

from sqlmodel import Session, select

from atlas.database.models.account import Account
from atlas.database.models.transaction import Transaction
from atlas.importers.icici_importer import ICICIImporter
from atlas.services.categorization_service import CategorizationService
from decimal import Decimal
import hashlib


class ImportService:
    @staticmethod
    def import_transactions(
        session: Session,
        transactions: list[Transaction],
    ) -> tuple[int, int]:
        account_ids = {t.account_id for t in transactions}

        # Build a set of existing normalized keys to deduplicate robustly.
        existing_rows = session.exec(
            select(
                Transaction.account_id,
                Transaction.transaction_date,
                Transaction.amount,
                Transaction.description,
            ).where(Transaction.account_id.in_(list(account_ids)))
        ).all()

        def normalize_row_key(account_id, tx_date, amount, description):
            try:
                date_key = tx_date.isoformat()
            except Exception:
                date_key = str(tx_date)

            if isinstance(amount, Decimal):
                amt = amount.quantize(Decimal("0.01"))
            else:
                try:
                    amt = Decimal(str(amount)).quantize(Decimal("0.01"))
                except Exception:
                    amt = Decimal("0.00")

            amount_key = format(amt, 'f')
            desc_key = (description or "").strip()

            return (str(account_id), date_key, amount_key, desc_key)

        existing_keys = {normalize_row_key(*r) for r in existing_rows}

        new_transactions = []
        for t in transactions:
            key = normalize_row_key(t.account_id, t.transaction_date, t.amount, t.description)
            if key not in existing_keys:
                new_transactions.append(t)
                existing_keys.add(key)

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
                transaction.description,
                transaction.merchant,
            )

        return ImportService.import_transactions(
            session,
            transactions,
        )
