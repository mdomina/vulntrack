from passlib.context import CryptContext

# Creiamo un contesto di crittografia che utilizza l'algoritmo bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    # Verifica se la password in chiaro corrisponde alla password crittografata
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str):
    return pwd_context.hash(password)