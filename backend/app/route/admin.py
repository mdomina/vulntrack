import secrets
from io import BytesIO
from typing import Annotated
import uuid
import bcrypt
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from datetime import datetime
from app.database.database import MyDB
from app.model.user_model import UserInDB
# from app.utility.convert_to_json import convert_data
from app.utility.estrazione_mese import estrai_mese
from app.utility.users import get_current_user
from app.model.user_model import NewUserModel

def check_admin(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Funzione che controlla se l'utente è admin"""
    if current_user.role != 'admin':
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

# @router.post("/uploadfile")
# async def create_upload_file(file: Annotated[UploadFile, File()]):
    
#     if file.filename.endswith('.xlsx'):
#         contents = await file.read()  # read file
#         data = BytesIO(contents)  # convert bytes to BytesIO
#         df = convert_data(data) # il file viene letto da pandas e ritorna un json
#         document = format(file.filename)
#         document['mese'] = estrai_mese(df)
#         document['data'] = df
#         mydb.insert(document)
#         return {"filename": file.filename}
#     else:
#         raise HTTPException(status_code=400, detail="Invalid file type")

@router.post("/user/register",response_description="Conferma della registrazione dell'utente")
async def register_user(user: NewUserModel):
    """
    Registra un nuovo utente nel database.

    **Parametri**:
    - **user** (NewUserModel): Oggetto contenente le informazioni dell'utente da registrare.

    **Risposte**:
    - **200 OK**: Restituisce un messaggio di conferma della registrazione dell'utente.
    - **403 Forbidden**: Se l'utente non ha i permessi per creare nuovi utenti.
    - **500 Internal Server Error**: Se si verifica un errore durante la registrazione dell'utente.
    """
    mydb = MyDB()
    
    # Controlla se l'email è già presente nel database
    mydb
    if mydb.email_exists(index="netpot-user", email=user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already in use")
    
    # Generazione username
    username = f"{user.name.lower().replace(' ', '')}.{user.surname.lower().replace(' ', '')}"
    
    # Dizionario dell'utente da inserire in Elasticsearch
    dic_user = {
        "timestamp": datetime.now(),
        "email": user.email,
        "name": user.name,
        "surname": user.surname,
        "username": username,
        "password": user.password,
        "role": user.role.value
    }

    # Inserimento nel database Elasticsearch
    result = mydb.insert(dic_user)
    
    # Verifica del risultato e restituzione della conferma o sollevamento di eccezione
    if result:
        return {'user': 'registered successfully'}
    
    # Se qualcosa va storto, restituiamo un errore 500
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")
