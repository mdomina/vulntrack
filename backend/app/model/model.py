from pydantic import BaseModel, constr, field_validator

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str | None = None

class LoginData(BaseModel):
    username: str
    password: str

class InputFilteredAudit(BaseModel):
    nome: str # nome app
    type: str
    company: str

    @field_validator('nome', 'type', 'company')
    def non_empty_strings(cls, value:str):
        if not value or value.strip() == '':
            raise ValueError('Il campo non può essere vuoto o contenere solo spazi')
        return value

class InputRecheckCompared(BaseModel):
    """Modello di input per ricevere i dati necessari a confrontare i 
    risultati del test iniziale e del recheck per la stessa applicazione e lo stesso ente."""

    name: str # nome app
    company: str

    @field_validator('name', 'company')
    def non_empty_strings(cls, value:str):
        if not value or value.strip() == '':
            raise ValueError('Il campo non può essere vuoto o contenere solo spazi')
        return value

class InputPrint(BaseModel):
    name: str # nome app
    type: str # tipologia vatp/recheck
    company: str 

    @field_validator('name', 'type', 'company')
    def strip_strings(cls, value:str):
        return value.strip()

class InputCompanyName(BaseModel):
    company_name:str