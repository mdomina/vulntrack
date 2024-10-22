from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from app.database.database import MyDB
from app.model.user_model import DeleteUser, UserDataResponseModel, UserInDB
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
    

@router.delete("/users/delete", response_description="Eliminazione dell'utente")
async def delete_user(delete_user: DeleteUser, current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """
    Elimina un utente in base all'email passata nel body della richiesta.
    """
    if current_user.email == delete_user.email:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="you can't eliminate yourself")
    try:
        mydb = MyDB()
        # Chiama il metodo per eliminare l'utente
        success = mydb.delete_user(delete_user.email)

        if not success:
            return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
        return {"msg": "User successfully deleted"}
    
    except Exception as e:
        # Log dell'errore e solleva un'eccezione HTTP
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to delete user")