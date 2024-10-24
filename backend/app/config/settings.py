from pydantic_settings import BaseSettings
import os 

class Settings(BaseSettings):
    # La chiave segreta viene utilizzata per codificare e decodificare i JWT. 
    # Dovresti generarla in modo casuale e mantenerla sicura. Puoi generare una chiave eseguendo `openssl rand -hex 32` nel terminale.
    SECRET_KEY : str = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"

    # L'algoritmo utilizzato per codificare e decodificare i JWT
    ALGORITHM : str = "HS256"
    
    # Il tempo di scadenza del token di accesso in minuti
    ACCESS_TOKEN_EXPIRE_MINUTES:int = 100

    # Ottieni MONGO_HOST e MONGO_PORT dalla variabile d'ambiente o usa un valore di default
    MONGO_HOST: str = os.environ.get("MONGODB_HOST", "172.31.41.88")
    MONGO_PORT: str = os.environ.get("MONGODB_PORT", "27017")

    # Ottieni PWNDOC_HOST e PWNDOC_PORT dalla variabile d'ambiente o usa un valore di default (db di mongo)
    PWNDOC_HOST: str = os.environ.get("PWNDOC_HOST", "172.31.41.88")
    PWNDOC_PORT: str = os.environ.get("PWNDOC_PORT", "27017")


