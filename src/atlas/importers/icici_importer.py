import hashlib
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from uuid import UUID

import pandas as pd

from atlas.database.models.transaction import Transaction, TransactionType


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
            withdrawal = Decimal(str(row["Withdrawal Amount(INR)"]))
            deposit = Decimal(str(row["Deposit Amount(INR)"]))

            if withdrawal > 0:
                amount = withdrawal
                tx_type = TransactionType.DEBIT
            else:
                amount = deposit
                tx_type = TransactionType.CREDIT

            import_hash = hashlib.sha256(
                (
                    f"{row['Transaction Date']}|"
                    f"{row['Transaction Remarks']}|"
                    f"{amount}|"
                    f"{tx_type.value}"
                ).encode("utf-8")
            ).hexdigest()

            transactions.append(
                Transaction(
                    account_id=account_id,
                    transaction_date=datetime.strptime(
                        row["Transaction Date"],
                        "%d/%m/%Y",
                    ),
                    amount=amount,
                    transaction_type=tx_type,
                    description=row["Transaction Remarks"],
                    import_hash=import_hash,
                )
            )

        return transactions
