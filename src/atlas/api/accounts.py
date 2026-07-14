from fastapi import APIRouter, Depends
from sqlmodel import Session

from atlas.api.dependencies import get_session
from atlas.schemas.account import AccountCreate, AccountRead
from atlas.services.account_service import AccountService

router = APIRouter(prefix="/accounts", tags=["Accounts"])


@router.post(
    "",
    response_model=AccountRead,
    status_code=201,
)
def create_account(
    account: AccountCreate,
    session: Session = Depends(get_session),
) -> AccountRead:
    return AccountService.create(session, account)
