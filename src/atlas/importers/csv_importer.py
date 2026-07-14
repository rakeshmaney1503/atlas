from pathlib import Path

import pandas as pd


class CSVImporter:
    @staticmethod
    def read(path: str | Path) -> pd.DataFrame:
        return pd.read_csv(path)
