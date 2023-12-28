from app import app
from fastapi import UploadFile, HTTPException, File, Form, Depends, status
import pandas as pd
from io import BytesIO
from typing import Annotated
from app.database.database import MyDB
from app.utility.login import authenticate_user
from app.model.model import Token, User, LoginData, InputNomeApp
from app.utility.users import get_current_user, get_auth
from app.utility.convert_to_json import convert_data
from app.utility.format_name import format
from app.utility.estrazione_mese import estrai_mese
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.format_rechecks import filter_rechecks
from app.utility.jwt_token import create_access_token
from fastapi.middleware.cors import CORSMiddleware

mydb = MyDB()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# upload file
# admin
@app.post("/uploadfile")
async def create_upload_file(
    file: Annotated[UploadFile, File()],
    current_user: Annotated[User, Depends(get_current_user)]
    ):

    if current_user.level != 'admin':
        raise HTTPException(status_code=401, detail="Permesso negato")
    
    if file.filename.endswith('.xlsx'):
        contents = await file.read()  # read file
        data = BytesIO(contents)  # convert bytes to BytesIO
        df = convert_data(data) # il file viene letto da pandas e ritorna un json
        document = format(file.filename)
        document['mese'] = estrai_mese(df)
        document['data'] = df
        mydb.insert(document)
        return {"filename": file.filename}
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")



# Endpoint per l'autenticazione
@app.post("/token", response_model=Token)
async def login_for_access_token(
    login_data: LoginData
):
    user = authenticate_user(login_data.username, login_data.password)
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


# Endpoint per controllare se l'utente è autenticato
@app.get("/auth/check")
async def auth_check(auth: Annotated[bool, Depends(get_auth)]):
    return auth


# endpoint per avere la lista vapt e recheck filtrati per nome
@app.post("/remediadions/list/filtered")
async def vapt_list_name(name_input: InputNomeApp ,current_user: Annotated[User, Depends(get_current_user)]):
    remediation = mydb.ricerca_filtrata({'nome': name_input.nome, 'type': name_input.type})
    mapping = MappingVulnerability()
    return mapping.format_vulerabiliy_name(remediation)
    

# endpoint per avere la lista di tutti i remediation (nome, anno, codice elettra, id mongo e type)
@app.get("/remediadions/list")
async def vapt_list_name(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return mydb.remediations_list()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista remediations",
        )

# endpoint per avere tutti i remediation
@app.get("/remediadion/data")
async def remediation_data(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        remediation = mydb.ricerca_all()
        mapping = MappingVulnerability()
        data = mapping.format_vulerabiliy_name(remediation)
        return data
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista remediations",
        )


# endpoint per eliminare i doc dal DB
# admin
@app.delete("/items/{item_id}")
async def delete_item(current_user: Annotated[User, Depends(get_current_user)], item_id: str):
    if current_user.level != 'admin':
        raise HTTPException(status_code=401, detail="Permesso negato")
    try:
        return mydb.delete_remediation(item_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore eliminazione documento",
        )

# endpoint per avere i nomi di tutte le app testate
@app.get("/remediadion/names/app")
async def list_names_app(current_user: Annotated[User, Depends(get_current_user)]):
    try:
        return mydb.remediation_list_name()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista nomi app",
        )

# endpoint per avere la lista delle app e se per la stessa app è presente il recheck
@app.get("/recheck/list")
async def list_recheck(currente_user: Annotated[User, Depends(get_current_user)]):
    try:
        rl = mydb.remediations_list()
        return filter_rechecks(rl)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista vapt/recheck",
        )

# endpoint per la dashboard di comparazione tra vapt e recheck per la singola app
@app.post("/recheck/data")
async def recheck_data(currente_user: Annotated[User, Depends(get_current_user)], nome_app: InputNomeApp):
    try:
        vapt = mydb.ricerca_filtrata({'nome': nome_app.nome, 'type': 'vapt'})
        recheck = mydb.ricerca_filtrata({'nome': nome_app.nome, 'type': 'recheck'})
        mapping = MappingVulnerability()
        return {'vapt': mapping.format_vulerabiliy_name(vapt), 'recheck': mapping.format_vulerabiliy_name(recheck)}
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista vapt/recheck",
        )

# endpoint per avere la lista vapt da inserire nella dashboard
@app.get("/remediadion/data/dashboard")
async def vapt_data(current_user: Annotated[User, Depends(get_current_user)]):
    remediation = mydb.ricerca_filtrata({'type': 'vapt'})
    mapping = MappingVulnerability()
    return mapping.format_vulerabiliy_name(remediation)