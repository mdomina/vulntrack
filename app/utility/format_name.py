import re
from fastapi import HTTPException, status

import hashlib

def generate_md5(string):
    # Creazione dell'oggetto hash MD5
    md5_hash = hashlib.md5()

    # Aggiunta della stringa da hashare all'oggetto hash
    md5_hash.update(string.encode('utf-8'))

    # Generazione dell'hash MD5
    md5_digest = md5_hash.hexdigest()

    return md5_digest

def extract_year(s):
    match = re.search(r'\b(\d{4})\b', s)
    return match.group(1) if match else None

def format(filename):
    try:
        filename_split = filename.lower().split('-')
        info_app = {}
        info_app['anno'] = extract_year(filename_split[0])
        info_app['cliente'] = filename_split[1].strip().title()
        
        # il codice elettra è sono nei test Aria
        if 'aria' in filename.lower():
            info_app['codice_elettra'] = filename_split[2].strip().upper()
        else:
            info_app['codice_elettra'] = '-'

        if len(filename_split) >= 5:# qundi contiene anche il nome dell'app
            info_app['nome'] = filename_split[3].strip().title()
        else:
            info_app['nome'] = filename_split[2].strip().title()

        info_app['_id'] = generate_md5(filename.lower())

        if "recheck" in filename.lower():
            info_app['type'] = "recheck"
        else:
            info_app['type'] = "vapt"
            
        return info_app
    except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='nome file errato')

