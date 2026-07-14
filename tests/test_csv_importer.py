from pathlib import Path

from atlas.importers.csv_importer import CSVImporter


def test_read_csv(tmp_path: Path) -> None:
    csv = tmp_path / "sample.csv"

    csv.write_text(
        "Date,Description,Amount\n"
        "2026-07-01,Salary,100000\n"
        "2026-07-02,Coffee,-250\n"
    )

    df = CSVImporter.read(csv)

    assert len(df) == 2
    assert list(df.columns) == [
        "Date",
        "Description",
        "Amount",
    ]
