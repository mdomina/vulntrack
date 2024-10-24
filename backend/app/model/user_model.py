from enum import Enum
import re
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator
from app.utility.password import HashPassword

class UserRole(Enum):
    """
    Enum per i ruoli utente.
    
    Ruoli disponibili:
        - ADMIN: Amministratore del sistema.
        - USER: Utente normale.
        - HONEYPOT_MANAGER: Gestore della honeypot.
    """
    ADMIN = "admin"
    USER = "user"

class UserDataResponseModel(BaseModel):
    """Dati utente in uscita"""
    name: str
    username: str
    email: EmailStr
    role: UserRole 

class UserInDB(BaseModel):
    """La classe UserInDB eredita tutti i campi dalla classe User (ovvero username, email, full_name, disabled), e aggiunge un campo addizionale hashed_password."""
    name: str
    surname:str
    username: str
    email: EmailStr
    password: str
    role: UserRole 
    companies: list[str]

    class Config:
        # Ignora i campi extra come `_id` senza sollevare errori
        extra = "ignore"

class NewUserModel(BaseModel):
    """
    Modello di input per creare un nuovo utente nel sistema.

    Attributi:
        email (EmailStr): L'indirizzo email dell'utente.
        name (str): Il nome dell'utente.
        surname (str): Il cognome dell'utente.
        password (str): La password dell'utente.
        role (UserRole): Il ruolo dell'utente (admin o user).
        username (str): Lo username generato automaticamente (prima lettera del nome + cognome).
    """
    email: EmailStr
    name: str
    surname: str
    password: str
    role: UserRole
    username: Optional[str] = None  # Lo username verrà generato
    companies: list[str]

    @field_validator('email')
    def normalize_email(cls, v: str) -> str:
        """Normalizza l'email."""
        return v.strip().lower()

    @field_validator('name')
    def normalize_name(cls, v: str) -> str:
        """Normalizza il nome."""
        return v.strip().lower()

    @field_validator('surname')
    def normalize_surname(cls, v: str) -> str:
        """Normalizza il cognome."""
        return v.strip().lower()

    @field_validator('password')
    def validate_new_password(cls, v: str) -> str:
        """Validatore che controlla la complessità della password e la cifra."""
        if len(v) < 12:
            raise ValueError('La password deve contenere almeno 12 caratteri')
        
        if not re.search(r'\d', v):
            raise ValueError('La password deve contenere almeno un numero')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('La password deve contenere almeno un carattere speciale')
        
        if not re.search(r'[A-Z]', v):
            raise ValueError('La password deve contenere almeno una lettera maiuscola')
        
        hash_password = HashPassword()
        return hash_password.hash_password(v)

    def model_post_init(self, __context):
        """Genera lo username automaticamente dopo la validazione."""
        self.username = f"{self.name[0].lower()}.{self.surname.lower().replace(' ', '')}"


class DeleteUser(BaseModel):
    """Modello per la cancellazione di un utente."""
    email: EmailStr