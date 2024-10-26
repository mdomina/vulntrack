from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import MyDB
from app.model.model import InputFilteredAudit, InputCompanyName
from app.model.user_model import UserInDB, UserRole
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.users import get_current_user

router = APIRouter(prefix="/vapt")
mydb = MyDB()

@router.post("/filtered")
async def vapt_list_name(audit_filtered: InputFilteredAudit ,current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista vapt o recheck filtrati per nome"""
    if current_user.role ==  UserRole.USER:
        if audit_filtered.company not in current_user.companies:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Non autorizzato")
    if audit_filtered.type == 'recheck':
        audits = mydb.ricerca_filtrata({
            'auditType': audit_filtered.company, 
            'company':audit_filtered.company,
            'name':audit_filtered.nome
            })
    else:
        audits = mydb.ricerca_filtrata({
            'auditType': {'$ne': 'Recheck'}, 
            'company':audit_filtered.company,
            'name':audit_filtered.nome
            })

    #mapping = MappingVulnerability()
    return audits

@router.post("/names/app")
async def list_names_app(current_user: Annotated[UserInDB, Depends(get_current_user)],  company_input: InputCompanyName):
    """Endpoint per avere i nomi di tutte le app testate"""
    if  current_user.role != UserRole.ADMIN:
        if company_input.company_name not in current_user.companies:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    try:
        return mydb.audit_list_name_by_company(company_input.company_name)
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista nomi app",
        )

@router.get("/data/dashboard")
async def vapt_data(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista vapt da inserire nella dashboard"""
    if current_user.role ==  UserRole.ADMIN:
        audits = mydb.ricerca_filtrata({
            'auditType': {'$ne': 'Recheck'}, 
            })
    else:
        audits = mydb.ricerca_filtrata({
            'auditType': {'$ne': 'Recheck'}, 
            'company': {'$in': current_user.companies}
            })
    mapping = MappingVulnerability()
    return audits
    #return mapping.format_vulerabiliy_name(audits)

@router.get("/companies/list")
async def companies_list(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista delle società in base all'utente"""
    
    mydb = MyDB()
    if current_user.role == UserRole.ADMIN:
        return mydb.get_all_companies()
    else:
        companies = mydb.get_filtered_companies(current_user.companies)
        return companies