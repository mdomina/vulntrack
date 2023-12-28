from fastapi import FastAPI, UploadFile, HTTPException, File, Form, Depends, status
import pandas as pd
from io import BytesIO
from typing import Annotated
from database.database import MyDB
from database.fake_db import fake_users_db
from utility.login import authenticate_user, create_access_token
from model.model import Token, User, LoginData
from utility.users import get_current_user
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

mydb = MyDB()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# upload file
@app.post("/uploadfile")
async def create_upload_file(
    file: Annotated[UploadFile, File()], 
    anno: Annotated[str, Form()], 
    nome: Annotated[str, Form()]
    ):
    if file.filename.endswith('.xlsx'):
        contents = await file.read()  # read file
        data = BytesIO(contents)  # convert bytes to BytesIO
        df = pd.read_excel(data)

        document = {"name": nome, "anno": anno, "data": df.to_dict()}
        mydb.insert(document)
        return {"filename": file.filename}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")



# Endpoint per l'autenticazione
@app.post("/token", response_model=Token)
async def login_for_access_token(
    login_data: LoginData
):
    user = authenticate_user(fake_users_db, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Endpoint per ottenere i dettagli dell'utente attualmente autenticato
@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user
