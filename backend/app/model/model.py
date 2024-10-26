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
    nome: str
    type: str
    company: str

    @field_validator('nome', 'type', 'company')
    def non_empty_strings(cls, value:str):
        if not value or value.strip() == '':
            raise ValueError('Il campo non può essere vuoto o contenere solo spazi')
        return value

class InputCompanyName(BaseModel):
    company_name:str