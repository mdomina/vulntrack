import pandas as pd
import json
from app.utility.logger import logger
from app.utility.backward_compatibility import b_c
from fastapi import HTTPException, status
import traceback

def normalize_gravity(gravity):
    if gravity.lower() in ['high', 'alta', 'alto']:
        return 'alta'
    elif gravity.lower() in ['medium', 'media', 'medio']:
        return 'media'
    elif gravity.lower() in ['low', 'bassa', 'basso']:
        return 'bassa'
    elif gravity.lower() in ['critical', 'critica', 'critico']:
        return 'critica'
    else:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Errore colonna Gravità')


# Funzione per convertire i valori di data, se esistenti
def convert_if_date(val):
    if isinstance(val, pd.Timestamp):
        return val.strftime('%Y-%m-%d')  # Conversione in stringa nel formato desiderato
    else:
        return val  # Restituisce il valore così com'è se non è un datetime


    
    
def convert_data(file):
    try:
        # Carica il file xlsx in un DataFrame pandas
        df = pd.read_excel(file)

        # Normalizza i nomi delle colonne
        df.columns = df.columns.str.lower().str.strip()
        
        # Normalizza il contenuto delle colonne
        df = df.applymap(lambda x: x.lower().strip() if isinstance(x, str) else x)

        # Retrocompabilità con il vecchio tempalte del report
        df = b_c(df)

        # Normalizza la colonna gravità
        df['gravità'] = df['gravità'].map(normalize_gravity)
             
        # Trova le colonne che sono di tipo datetime
        date_cols = df.select_dtypes(include=['datetime64']).columns
        
        # Converte le colonne date in stringhe
        df[date_cols] = df[date_cols].astype(str)

        # Nella colonna 'data di risoluzione' ci possono essere delle righe con valori stringa '-', questo impedisce la conversione a riga 48 
        try:
            # Sostituisci '-' con 'NaT' (Not a Time, l'equivalente di NaN per i dati datetime)
            df['data di risoluzione'] = df['data di risoluzione'].replace('-', pd.NaT)

            # Successivamente, converti 'NaT' in un formato datetime di stringa o in un altro valore a tua scelta
            df['data di risoluzione'] = df['data di risoluzione'].apply(lambda x: x.strftime('%Y-%m-%d') if pd.notnull(x) else 'Nessuna data disponibile')
        except:
            pass
        
        # Sostituisci i valori NaN (le caselle che sono vuote) con '-'
        df = df.fillna('-')

        # Converti il DataFrame in un dizionario
        dataframe_convertito = df.to_dict(orient='records')
        
        # utilizzando questa funzione controlla possibili errori di formattazione
        json.dumps(dataframe_convertito, indent=4)
        
        return dataframe_convertito
    except Exception as e:
        tb = traceback.format_exc()
        logger.error(f"estrazione data excel: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Errore lettura file")


if __name__=='__main__':
    data = convert_data()
    print(data)