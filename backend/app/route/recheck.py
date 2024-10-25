from typing import Annotated
from app.database.database import MyDB
from fastapi import APIRouter, Depends, HTTPException, status

from app.model.model import InputNomeApp
from app.utility.format_rechecks import filter_rechecks
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.users import get_current_user
from app.model.user_model import UserInDB, UserRole

router = APIRouter(prefix="/recheck")
mydb = MyDB()

@router.get("/list")
async def list_recheck(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista delle app e se per la stessa app è presente il recheck"""
    try:
        if current_user.role ==  UserRole.ADMIN:
            audits = mydb.ricerca_filtrata({
                'auditType': {'$ne': 'Recheck'}, 
                })
        else:
            audits = mydb.ricerca_filtrata({
                'auditType': {'$ne': 'Recheck'}, 
                'company': {'$in': current_user.companies}
                })
        audits_format = []
        for audit in audits:
            value = {
                "anno": audit.get('date', '')[:4],  # Anno estratto dalla data
                "mese": audit.get('date', '')[5:7],  # Mese estratto dalla data
                "nome": audit.get('name', ''),
                "type": audit.get('auditType', ''),
                "codice_elettra": ('-'),  # Default '-' se non presente
                "cliente": audit.get('company', '')
            }
            audits_format.append(value)
        return filter_rechecks(audits_format)
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

