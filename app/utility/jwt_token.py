from datetime import timedelta, datetime
from app.config.settings import Settings
from jose import jwt, JWTError
from app.model.model import TokenData

settings = Settings()

def create_access_token(data: dict):
    to_encode = data.copy()
    
    # Calcoliamo la data e l'ora di scadenza del token di accesso
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Aggiungiamo la data e l'ora di scadenza del token di accesso ai dati che saranno codificati nel token
    to_encode.update({"exp": expire})
    # Codifichiamo i dati in un JWT
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def get_user_from_token(token):
    # Tentiamo di decodificare il token dell'utente
    try:
        # Decodifichiamo il token utilizzando la chiave segreta e l'algoritmo definito
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        # Estraiamo il nome utente dal payload del token
        username: str = payload.get("sub")
        # Se il nome utente non è presente, solleviamo l'eccezione delle credenziali
        if username is None:
            return None
        # Creiamo un oggetto TokenData con il nome utente
        return TokenData(username=username)
    # Se si verifica un errore durante la decodifica del token, solleviamo l'eccezione delle credenziali
    except JWTError:
        return None