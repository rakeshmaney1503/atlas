from sqlmodel import Session

from atlas.database.session import engine
from atlas.services.account_service import AccountService
from atlas.services.import_service import ImportService

with Session(engine) as session:

    account = AccountService.get_by_name(
        session,
        "ICICI Salary Account",
    )

    if account is None:
        raise RuntimeError("ICICI Salary Account not found")

    imported, duplicates = ImportService.import_icici_statement(
        session=session,
        statement_path="data/samples/icici/OpTransactionHistory14-07-2026.xls",
        account=account,
    )

print(f"Imported   : {imported}")
print(f"Duplicates : {duplicates}")
