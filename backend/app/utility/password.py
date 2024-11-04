from passlib.context import CryptContext

class HashPassword():
    def __init__(self):
        # Creiamo un contesto di crittografia che utilizza l'algoritmo bcrypt
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        # Verifica se la password in chiaro corrisponde alla password crittografata
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password: str):
        return self.pwd_context.hash(password)