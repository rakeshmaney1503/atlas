from decimal import Decimal
from pathlib import Path

import pandas as pd

from atlas.database.models.holding import Holding


class ZerodhaImporter:
    @staticmethod
    def read(path: str | Path) -> pd.DataFrame:
        df = pd.read_csv(path)

        df = df.drop(columns=["Unnamed: 9"], errors="ignore")
        df.columns = [str(c).strip() for c in df.columns]

        return df

    @staticmethod
    def normalize(
        df: pd.DataFrame,
        account_id,
    ) -> list[Holding]:

        holdings: list[Holding] = []

        for _, row in df.iterrows():

            holdings.append(
                Holding(
                    account_id=account_id,
                    instrument=row["Instrument"],
                    quantity=Decimal(str(row["Qty."])),
                    average_cost=Decimal(str(row["Avg. cost"])),
                    last_traded_price=Decimal(str(row["LTP"])),
                    invested_amount=Decimal(str(row["Invested"])),
                    current_value=Decimal(str(row["Cur. val"])),
                    pnl=Decimal(str(row["P&L"])),
                    net_change_percent=Decimal(str(row["Net chg."])),
                    day_change_percent=Decimal(str(row["Day chg."])),
                )
            )

        return holdings
