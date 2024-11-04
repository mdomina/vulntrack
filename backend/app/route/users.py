from typing import Annotated
import bcrypt
from fastapi import APIRouter, Depends, HTTPException, status
from app.model.user_model import ChangePasswordModel, UserInDB, UserDataResponseModel
from app.utility.users import get_current_user
from app.database.database import MyDB


router = APIRouter(prefix="/users")

@router.get("/me", response_model=UserDataResponseModel)
async def read_users_me(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    "Endpoint per ottenere i dettagli dell'utente attualmente autenticato"
    return current_user



@router.post("/change-password",
    response_description="Conferma del cambio della password",
    responses={
        200: {
            "description": "Cambio della password completato con successo.",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "message": {
                                "type": "string",
                                "description": "Messaggio di conferma del cambio della password."
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Dati della richiesta non validi.",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid password or new password does not meet criteria"}
                }
            }
        },
        500: {
            "description": "Errore interno del server.",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal Server Error"}
                }
            }
        }
    }
)
async def change_password(
    password_data: ChangePasswordModel, 
    current_user: Annotated[UserInDB, Depends(get_current_user)]
):
    """
    Cambia la password di un utente esistente nel sistema.

    **Parametri**:
    - **old_password**: str  # Campo per la password corrente dell'utente
    - **new_password**: str  # Campo per la nuova password proposta dall'utente

    **Risposte**:
    - **200 OK**: Restituisce un messaggio di conferma del cambio della password.
    - **422 Bad Request**: Se lla nuova password non soddisfa i criteri di sicurezza.
    - **400 Bad Request**: Se la password attuale non è corretta.

    **Esempio di richiesta**:
    ```json
    {
        "old_password": "currentpassword123",
        "new_password": "newSecurePassword123!"
    }
    ```

    **Esempio di risposta (successo)**:
    ```json
    {
        "message": "Password changed successfully"
    }
    ```

    **Esempio di risposta (errore)**:
    ```json
    {
        "detail": "Invalid password or new password does not meet criteria"
    }
    """
    
        # Aggiorna la password nel database
    
    mydb = MyDB()

    # Verifica la password corrente
    if not bcrypt.checkpw(password_data.old_password.encode('utf-8'), current_user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password errata")

    # Assuming current_user has an attribute `_id` which is the user's ID
    success = mydb.update_user_password(current_user.email, password_data.new_password)

    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Errore durante l'aggiornamento della password")

    return {"message": "Password changed successfully"}