from pydantic import BaseModel

# creazione del modello di dati per gli utenti
class User(BaseModel):
    # valori obbligatori
    username: str
    level: str 

# La classe UserInDB eredita tutti i campi dalla classe User (ovvero username, email, full_name, disabled), e aggiunge un campo addizionale hashed_password.
class UserInDB(User):
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginData(BaseModel):
    username: str
    password: str

class InputNomeApp(BaseModel):
    nome: str
    type: str