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

class InputPrint(BaseModel):
    name: str
    type: str
    company: str

    @field_validator('name', 'type', 'company')
    def strip_strings(cls, value:str):
        return value.strip()

class InputCompanyName(BaseModel):
    company_name:str