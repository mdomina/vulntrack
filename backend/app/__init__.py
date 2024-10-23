from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.utility.create_admin import create_admin_if_not_exists

# se non esiste l'utente admin lo crea 
create_admin_if_not_exists()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROUTES
from app.route.admin import router as admin
from app.route.auth import router as auth
from app.route.users import router as users
from app.route.vatp import router as vapt
from app.route.recheck import router as recheck


app.include_router(admin)
app.include_router(auth)
app.include_router(users)
app.include_router(vapt)
app.include_router(recheck)

from app.utility.insert_mongo import InsertMongo

insert_Mongo = InsertMongo()

insert_Mongo.main()