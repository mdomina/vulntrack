from app.database.database import MyDB
from fastapi import APIRouter, Depends, HTTPException, status

from app.model.model import InputNomeApp, User
from app.utility.format_rechecks import filter_rechecks
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.users import get_current_user

router = APIRouter(prefix="/recheck", dependencies=[Depends(get_current_user)])
mydb = MyDB()

@router.get("/list")
async def list_recheck():
    """Endpoint per avere la lista delle app e se per la stessa app è presente il recheck"""
    try:
        rl = mydb.remediations_list()
        return filter_rechecks(rl)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista vapt/recheck",
        )

@router.post("/data")
async def recheck_data(nome_app: InputNomeApp):
    """Endpoint per la dashboard di comparazione tra vapt e recheck per la singola app"""
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

