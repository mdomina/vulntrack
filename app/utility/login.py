from datetime import datetime, timedelta
from app.model.model import UserInDB
from app.utility.password import verify_password
from app.utility.password import hash_password
from app.database.database import MyDB

my_db = MyDB()

def create_admin_if_not_exists():
    """controlla se esiste la collection users, se non esiste crea un utente admin"""
    users = my_db.get_users_collection()
    if users.count_documents({}) == 0:  # Nessun documento in users
        password = hash_password('admin')
        admin_user = {
            "username": "admin",
            "hashed_password": password,  
            "level": "admin",
        }
        users.insert_one(admin_user)

def get_user(username: str):
    """Questa funzione cerca l'utente nel database con lo username specificato"""
    users_collection = my_db.get_users_collection()
    user_dict = users_collection.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)# Crea un oggetto UserInDB da questo dizionario
    else:
        return None
    
def authenticate_user(username: str, password: str):
    """Questa funzione autentica l'utente verificando il suo username e la password"""
    create_admin_if_not_exists()
    user = get_user(username)
    if not user:
        return False
    # Verifica se la password fornita in chiaro corrisponde alla password crittografata dell'utente
    if not verify_password(password, user.hashed_password):
        return False
    return user
