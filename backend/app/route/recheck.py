from typing import Annotated
from app.database.database import MyDB
from fastapi import APIRouter, Depends, HTTPException, status
from app.model.model import InputFilteredAudit, InputPrint, InputRecheckCompared
from app.utility.format_rechecks import filter_rechecks
from app.utility.mapping_vulnerability import MappingVulnerability
from app.utility.users import get_current_user
from app.model.user_model import UserInDB, UserRole
from app.utility.report_creation.index import GeneralReport
from fastapi.responses import FileResponse
import os


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


@router.post("/printrecheck")
async def recheck_vapt_document(audit_filtered: InputRecheckCompared, current_user: Annotated[UserInDB, Depends(get_current_user)]):
    """Endpoint per stampare il report"""
    mydb = MyDB()
    
    # Ottieni la directory di lavoro corrente (quella da cui è stato avviato FastAPI)
    current_working_directory = os.getcwd()

    # Costruisci il percorso assoluto per la cartella "output"
    output_folder = os.path.join(current_working_directory, 'app', 'utility', 'report_creation', 'output')
    output_file = os.path.join(output_folder, "output_report_recheck.pdf")
    
    # Controlla il ruolo dell'utente
    if current_user.role == UserRole.USER:
        if audit_filtered.company not in current_user.companies:
            raise  HTTPException(status_code=status.HTTP_403_FORBIDDEN)


    audits = mydb.ricerca_filtrata({
            'company': audit_filtered.company,
            'name': audit_filtered.name,
    })
    
    # Genera il report
    general_report = GeneralReport(audits)
    general_report.set_template('recheck.docx', output_file)
    general_report.run_recheck()
    
    # Verifica l'esistenza del file prima di restituirlo
    if not os.path.exists(output_file):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Errore nella generazione del report")
    
    # Restituisci il file come risposta
    return FileResponse(
        path=output_file,
        filename="output_report_recheck.pdf",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
