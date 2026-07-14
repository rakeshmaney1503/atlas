import hashlib
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pandas as pd

from atlas.database.models.transaction import Transaction, TransactionType
from atlas.services.merchant_recognition_service import MerchantRecognitionService


class ICICIImporter:
    HEADER_ROW = 12

    @staticmethod
    def read(path: str | Path) -> pd.DataFrame:
        df = pd.read_excel(path, header=ICICIImporter.HEADER_ROW)

        df = df.drop(columns=["Unnamed: 0"], errors="ignore")
        df.columns = [str(c).strip() for c in df.columns]

        df = df[df["Transaction Date"].notna()].copy()
        df.reset_index(drop=True, inplace=True)

        return df

    @staticmethod
    def normalize(
        df: pd.DataFrame,
        account_id: UUID,
    ) -> list[Transaction]:
        transactions: list[Transaction] = []

        for _, row in df.iterrows():
            withdrawal = Decimal(str(row.get("Withdrawal Amount(INR)", 0) or 0))
            deposit = Decimal(str(row.get("Deposit Amount(INR)", 0) or 0))

            if withdrawal > 0:
                amount = withdrawal
                tx_type = TransactionType.DEBIT
            else:
                amount = deposit
                tx_type = TransactionType.CREDIT

            description_value = row.get("Transaction Remarks", "")
            description = (
                str(description_value).strip()
                if pd.notna(description_value)
                else ""
            )

            if isinstance(row["Transaction Date"], str):
                transaction_date = datetime.strptime(
                    row["Transaction Date"],
                    "%d/%m/%Y",
                )
            else:
                transaction_date = pd.to_datetime(
                    row["Transaction Date"],
                    dayfirst=True,
                ).to_pydatetime()

            # Normalize values used for deduplication so the hash is deterministic
            # across runs and across pandas/python datetime representations.
            # Use ISO format for date and quantize amount to 2 decimals.
            try:
                date_key = transaction_date.isoformat()
            except Exception:
                date_key = str(transaction_date)

            amount = amount.quantize(Decimal("0.01"))
            amount_key = format(amount, 'f')

            desc_key = description.strip()

            import_hash = hashlib.sha256(
                (f"{date_key}|{desc_key}|{amount_key}|{tx_type.value}").encode("utf-8")
            ).hexdigest()

            running_balance = None
            if pd.notna(row.get("Balance(INR)")):
                value = row["Balance(INR)"]
                if hasattr(value, "item"):
                    value = value.item()
                running_balance = Decimal(str(value))

            merchant = MerchantRecognitionService.recognize(description)

            transactions.append(
                Transaction(
                    account_id=account_id,
                    transaction_date=transaction_date,
                    amount=amount,
                    transaction_type=tx_type,
                    description=description,
                    merchant=merchant,
                    running_balance=running_balance,
                    import_hash=import_hash,
                )
            )

        return transactions
