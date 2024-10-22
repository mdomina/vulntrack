from typing import Annotated
from fastapi import APIRouter, Depends

from app.model.user_model import UserInDB, UserDataResponseModel
from app.utility.users import get_current_user


router = APIRouter(prefix="/users")

@router.get("/me", response_model=UserDataResponseModel)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    "Endpoint per ottenere i dettagli dell'utente attualmente autenticato"
    return current_user