from typing import Annotated
from fastapi import APIRouter, Depends

from backend.app.model.model import User
from backend.app.utility.users import get_current_user


router = APIRouter(prefix="/users")

@router.get("/me", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    "Endpoint per ottenere i dettagli dell'utente attualmente autenticato"
    return current_user