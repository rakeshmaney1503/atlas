from sqlmodel import Session

from atlas.database.models.account import AccountType
from atlas.database.session import engine
from atlas.importers.zerodha_importer import ZerodhaImporter
from atlas.services.account_service import AccountService
from atlas.services.holding_service import HoldingService

with Session(engine) as session:

    account = AccountService.get_or_create(
        session,
        name="Zerodha",
        institution="Zerodha",
        account_type=AccountType.INVESTMENT,
    )

    df = ZerodhaImporter.read(
        "data/samples/zerodha/holdings-2.csv"
    )

    holdings = ZerodhaImporter.normalize(
        df,
        account.id,
    )

    imported = HoldingService.replace_holdings(
        session,
        account.id,
        holdings,
    )

print(f"Imported {imported} holdings.")
