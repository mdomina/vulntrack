from datetime import datetime
from fastapi import HTTPException, status
from app.utility.logger import logger

def estrai_mese(dati):  
    try:
        # Itera su ogni dizionario nella lista
        for data in dati:
            # Tenta di formattare la data nel formato '%Y/%m/%d'
            data_formattata = datetime.strptime(data['ultimo aggiornamento'], '%Y-%m-%d')
            
            # Crea un dizionario per mappare i numeri dei mesi ai loro nomi in italiano
            mesi = {1: 'Gennaio', 2: 'Febbraio', 3: 'Marzo', 4: 'Aprile', 5: 'Maggio', 6: 'Giugno',
                7: 'Luglio', 8: 'Agosto', 9: 'Settembre', 10: 'Ottobre', 11: 'Novembre', 12: 'Dicembre'}
        
            # Estrai il mese
            return mesi[data_formattata.month].title()
    except Exception as e:
        logger.error(f"estrazione mese: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Errore estrazione mese"
        )
