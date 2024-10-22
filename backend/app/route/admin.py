import secrets
from io import BytesIO
from typing import Annotated, List
import uuid
import bcrypt
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from datetime import datetime
from app.database.database import MyDB
from app.model.user_model import UserDataResponseModel, UserInDB
# from app.utility.convert_to_json import convert_data
from app.utility.estrazione_mese import estrai_mese
from app.utility.users import get_current_user
from app.model.user_model import NewUserModel

def check_admin(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Funzione che controlla se l'utente è admin"""
    if current_user.role.value != 'admin':
        raise HTTPException(status_code=403, detail="Permesso negato")
    return current_user

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_admin)]
    )


@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Endpoint per eliminare i doc dal DB"""
    try:
        mydb = MyDB()
        return mydb.delete_remediation(item_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore eliminazione documento",
        )

@router.post("/users/add",response_description="Conferma della registrazione dell'utente")
async def register_user(user: NewUserModel):
    """"""
    mydb = MyDB()
    
    # Controlla se l'email è già presente nel database
    if mydb.email_exists(email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
   
    # Converte il modello in dizionario
    dic_user = user.model_dump()
    
    # Converti l'enum UserRole in stringa
    dic_user['role'] = user.role.value  # Converti UserRole.USER o UserRole.ADMIN in 'user' o 'admin'
    
    dic_user['timestamp'] = datetime.now()

    # Inserimento nel database Elasticsearch
    result = mydb.insert_user(dic_user)
    
    # Verifica del risultato e restituzione della conferma o sollevamento di eccezione
    if result:
        return {'user': 'registered successfully'}
    
    # Se qualcosa va storto, restituiamo un errore 500
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")

@router.get("/users/list", response_model=List[UserDataResponseModel])
async def elenco_user():
    """"""
    try:
        mydb = MyDB()
        users = mydb.get_all_users()
        
        # Converte gli utenti in istanze di UserInDB
        users = [UserInDB(**user) for user in users]
    
        return users
    
    except Exception as e:
        # Log dell'eccezione se necessario
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to retrieve users list")