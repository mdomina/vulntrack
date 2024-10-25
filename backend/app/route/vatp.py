from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from app.database.database import MyDB
from app.model.model import InputNomeApp
from app.model.user_model import UserInDB
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.users import get_current_user

router = APIRouter(prefix="/vapt")
mydb = MyDB()

@router.post("/list/filtered")
async def vapt_list_name(name_input: InputNomeApp ,current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista vapt e recheck filtrati per nome"""
    
    remediation = mydb.ricerca_filtrata({'nome': name_input.nome, 'type': name_input.type})
    mapping = MappingVulnerability()
    return mapping.format_vulerabiliy_name(remediation)

@router.get("/list")
async def vapt_list_name(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista di tutti i remediation (nome, anno, codice elettra, id mongo e type)"""
    try:
        return mydb.remediations_list()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista remediations",
        )

@router.get("/data")
async def remediation_data(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere tutti i remediation"""
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

@router.get("/names/app")
async def list_names_app(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere i nomi di tutte le app testate"""
    try:
        return mydb.remediation_list_name()
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione lista nomi app",
        )

@router.get("/data/dashboard")
async def vapt_data(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista vapt da inserire nella dashboard"""
    remediation = mydb.ricerca_filtrata({'type': 'vapt'})
    mapping = MappingVulnerability()
    return mapping.format_vulerabiliy_name(remediation)

@router.get("/companies/list")
async def companies_list(current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per avere la lista delle società in base all'utente"""
    
    mydb = MyDB()
    companies = mydb.get_filtered_companies(current_user.companies)
    return companies