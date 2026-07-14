from sqlmodel import Session

from atlas.database.models.account import AccountType
from atlas.database.session import engine
from atlas.services.account_service import AccountService

with Session(engine) as session:
    AccountService.get_or_create(
        session,
        name="ICICI Salary Account",
        institution="ICICI Bank",
        account_type=AccountType.SAVINGS,
    )

print("Accounts bootstrapped successfully.")
