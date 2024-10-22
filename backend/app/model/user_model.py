from enum import Enum
import re
from pydantic import BaseModel, EmailStr, field_validator
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
    HONEYPOT_MANAGER = "honeypot_manager"

class UserDataResponseModel(BaseModel):
    """Dati utente in uscita"""
    name: str
    username: str
    email: EmailStr
    password: str
    role: UserRole 

class UserInDB(BaseModel):
    """La classe UserInDB eredita tutti i campi dalla classe User (ovvero username, email, full_name, disabled), e aggiunge un campo addizionale hashed_password."""
    name: str
    surname:str
    username: str
    email: EmailStr
    password: str
    role: UserRole 

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
    """
    email: EmailStr
    name: str
    surname: str
    password: str
    role: UserRole
    
    @field_validator('email')
    def normalize_email(cls, v: str) -> str:
        """
        Validatore che normalizza l'email.

        Questo validatore:
        - Rimuove eventuali spazi bianchi prima e dopo l'email con `strip()`.
        - Converte l'email in minuscolo con `lower()`.
        """
        return v.strip().lower()
    
    @field_validator('name')
    def normalize_name(cls, v: str) -> str:
        """
        Validatore che normalizza il nome.

        Questo validatore:
        - Rimuove eventuali spazi bianchi prima e dopo l'email con `strip()`.
        - Converte l'email in minuscolo con `lower()`.
        """
        return v.strip().lower()
    
    @field_validator('surname')
    def normalize_surname(cls, v: str) -> str:
        """
        Validatore che normalizza il cognome.

        Questo validatore:
        - Rimuove eventuali spazi bianchi prima e dopo l'email con `strip()`.
        - Converte l'email in minuscolo con `lower()`.
        """
        return v.strip().lower()

    @field_validator('password')
    def validate_new_password(cls, v: str) -> str:
        """
        Validatore che controlla la complessità della password. Ritorna la password cifrata

        Questo validatore:
        - Verifica che la password contenga almeno 12 caratteri.
        - Controlla che la password contenga almeno un numero.
        - Verifica che la password abbia almeno un carattere speciale.
        - Assicura che ci sia almeno una lettera maiuscola.
        """
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
