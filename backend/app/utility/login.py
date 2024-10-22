from app.model.user_model import UserInDB
from app.utility.password import HashPassword
from app.database.database import MyDB


def get_user(username: str):
    """Questa funzione cerca l'utente nel database con lo username specificato"""
    my_db = MyDB()
    users_collection = my_db.get_users_collection()
    user_dict = users_collection.find_one({"username": username})
    if user_dict:
        return UserInDB(**user_dict)# Crea un oggetto UserInDB da questo dizionario
    else:
        return None
    
def authenticate_user(username: str, password: str):
    """Questa funzione autentica l'utente verificando il suo username e la password"""
    hash_password = HashPassword()
    user:UserInDB = get_user(username)
    if not user:
        return False
    # Verifica se la password fornita in chiaro corrisponde alla password crittografata dell'utente
    if not hash_password.verify_password(password, user.password):
        return False
    return user
