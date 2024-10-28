from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.utility.reportCreation.index import GeneralReport

import os
 
router = APIRouter()
 
# Percorso ai template, da configurare se necessario

TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'template')
 
# Endpoint per generare e scaricare il report VAPT

@router.get("/download-vapt-report", response_class=FileResponse)

async def download_vapt_report():

    # Dati di esempio per mongo_data

    mongo_data = []  # Inserisci i dati di MongoDB reali o mock per test

    report_generator = GeneralReport(mongo_data)
 
    # Imposta il template e il percorso del file di output

    report_generator.set_template('dashboard.docx', 'output_report_dashboard.docx')

    # Esegui la generazione del report

    report_generator.run_vapt()

    # Percorso del file generato

    file_path = report_generator.output_path

    if not os.path.isfile(file_path):

        raise HTTPException(status_code=404, detail="File non trovato")

    return FileResponse(path=file_path, filename="output_report_dashboard.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
 
# Endpoint per generare e scaricare il report Recheck

@router.get("/download-recheck-report", response_class=FileResponse)

async def download_recheck_report():

    # Dati di esempio per mongo_data

    mongo_data = []  # Inserisci i dati di MongoDB reali o mock per test

    report_generator = GeneralReport(mongo_data)
 
    # Imposta il template e il percorso del file di output

    report_generator.set_template('recheck.docx', 'output_report_recheck.docx')

    # Esegui la generazione del report

    report_generator.run_recheck()

    # Percorso del file generato

    file_path = report_generator.output_path

    if not os.path.isfile(file_path):

        raise HTTPException(status_code=404, detail="File non trovato")

    return FileResponse(path=file_path, filename="output_report_recheck.docx", media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

 