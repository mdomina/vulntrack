from app.utility.password import HashPassword
from app.database.database import MyDB

def create_admin_if_not_exists():
    """controlla se esiste la collection users, se non esiste crea un utente admin"""
    
    my_db = MyDB()
    
    password = 'admin'

    users = my_db.get_users_collection()
    if users.count_documents({}) == 0:  # Nessun documento in users
        hash_password = HashPassword()
        password = hash_password.hash_password(password)
        admin_user = {
            "username": "admin",
            "password": password,  
            "role": "admin",
            "email":"admin@admin.it"
        }
        users.insert_one(admin_user)