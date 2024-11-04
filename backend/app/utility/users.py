from typing import Annotated
from fastapi import HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.model.user_model import UserInDB
from app.config.settings import Settings
from app.utility.jwt_token import get_user_from_token
from app.database.database import MyDB

my_db = MyDB()

# Crea un'istanza di OAuth2PasswordBearer.
# Questa classe gestisce l'acquisizione di token di accesso dal client,
# la verifica che i token siano presenti in tutte le richieste che richiedono autenticazione,
# e restituisce un errore se il token non è presente.
# "tokenUrl" è l'URL dove il client invierà i dati dell'utente per ottenere un token.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


settings = Settings()

def get_user(username: str) -> UserInDB:
    """Questa funzione cerca l'utente nel database con lo username specificato"""
    users_collection = my_db.get_users_collection()
    user_dict = users_collection.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)# Crea un oggetto UserInDB da questo dizionario
    else:
        return None
    


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserInDB:
    """Recupera i dati utente dal JWT"""
    
    # Creiamo un'eccezione per i casi in cui non possiamo validare le credenziali dell'utente
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Non è possibile validare le credenziali",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Recuperiamo il nome utente dal token
    token_data = get_user_from_token(token)
    if token_data is None:
        raise credentials_exception
    
    # Otteniamo l'utente dal nostro finto database con il nome utente
    user = get_user(username=token_data.username)
    # Se non c'è un utente con quel nome utente, solleviamo l'eccezione delle credenziali
    if user is None:
        raise credentials_exception
    # Se tutto va bene, restituiamo l'utente
    return user

async def get_auth(token: Annotated[str, Depends(oauth2_scheme)]):
    if get_user_from_token(token):
        return  {"authenticated": True }
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=False)