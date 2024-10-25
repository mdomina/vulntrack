from pydantic import BaseModel

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

class InputCompanyName(BaseModel):
    company_name:str