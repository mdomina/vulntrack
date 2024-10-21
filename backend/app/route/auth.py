from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.model.model import LoginData, Token
from app.utility.jwt_token import create_access_token
from app.utility.login import authenticate_user
from app.utility.users import get_auth


router = APIRouter(prefix="/auth")


@router.post("/token", response_model=Token)
async def login_for_access_token(login_data: LoginData):
    """Endpoint per l'autenticazione"""
    user = authenticate_user(login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint per controllare se l'utente è autenticato
@router.get("/check")
async def auth_check(auth: Annotated[bool, Depends(get_auth)]):
    return auth
