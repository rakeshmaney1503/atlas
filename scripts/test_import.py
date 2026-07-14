from uuid import uuid4

from atlas.importers.icici_importer import ICICIImporter

df = ICICIImporter.read(
    "data/samples/icici/OpTransactionHistory14-07-2026.xls"
)

transactions = ICICIImporter.normalize(df, uuid4())

print(f"Imported {len(transactions)} transactions")
print()
print(transactions[0])
