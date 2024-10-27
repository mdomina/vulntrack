from typing import Annotated
from app.database.database import MyDB
from fastapi import APIRouter, Depends, HTTPException, status
from app.model.model import InputFilteredAudit, InputRecheckCompared
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
            audits = mydb.ricerca_filtrata({})
        else:
            audits = mydb.ricerca_filtrata({
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
async def recheck_data(app_info: InputRecheckCompared, current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per la dashboard di comparazione tra vapt e recheck per la singola app dello stesso ente"""
    if current_user.role != UserRole.ADMIN:
        if app_info.company not in current_user.companies:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        audits = mydb.ricerca_filtrata({
            'name': app_info.name, 
            'company':app_info.company
            })
        result = {}
        for audit in audits:
            if audit.get('auditType') == 'Recheck':
                result['recheck'] = audit
            else:
                result['vapt'] = audit
        return result
        # mapping = MappingVulnerability()
        
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista vapt/recheck",
        )

