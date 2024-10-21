from io import BytesIO
from typing import Annotated
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from app.database.database import MyDB
from app.model.model import User
from app.utility.convert_to_json import convert_data
from app.utility.estrazione_mese import estrai_mese
from app.utility.users import get_current_user

def check_admin(current_user: Annotated[User, Depends(get_current_user)]):
    """Funzione che controlla se l'utente è admin"""
    if current_user.level != 'admin':
        raise HTTPException(status_code=403, detail="Permesso negato")
    return current_user

router = APIRouter(
    prefix="/admin",
    dependencies=[Depends(check_admin)]
    )
mydb = MyDB()



@router.delete("/items/{item_id}")
async def delete_item(item_id: str):
    """Endpoint per eliminare i doc dal DB"""
    try:
        return mydb.delete_remediation(item_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore eliminazione documento",
        )

# upload file
# admin
@router.post("/uploadfile")
async def create_upload_file(file: Annotated[UploadFile, File()]):
    
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

