from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from fastapi import HTTPException, status
from bson.objectid import ObjectId
from app.utility.logger import logger
from app.config.settings import Settings

settings = Settings()

class MyDB():
    def __init__(self) -> None:
        mongo_host = settings.MONGO_HOST
        mongo_port = int(settings.MONGO_PORT)
        self.client = MongoClient(mongo_host, mongo_port)
        self.db = self.client.vulntrack
        self.collection_vapt = self.db.vapt
    
    def get_users_collection(self):
        """
        controlla se esiste la collection users
        """
        return self.db.get_collection('users')

    def insert(self, document):
        try:
            # Inserisci un documento nella tua collezione
            self.collection_vapt.insert_one(document)
        except DuplicateKeyError as e:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File esistente")
        except Exception as e:
            logger.error(f"inserimento database: {e}")
    
    def ping(self):
        try:
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            logger.error(f"ping database: {e}")

    def ricerca_filtrata(self, filtro):
        try:
            results = []
            # In questo caso, cerchiamo tutti i documenti dove il campo 'type' è uguale al valore passato.
            for result in self.collection_vapt.find(filtro):
                results.append(result)
            return results
        except Exception as e:
            logger.error(f"ricerca filtrata: {e}")
            return None
    
    def ricerca_all(self):
        try:
            remediations = []
            for value in self.collection_vapt.find():
                del value['_id']
                remediations.append(value)
            return remediations
        except Exception as e:
            logger.error(f"ricerca totale: {e}")
            return None
    
    def remediations_list(self):
        try:
            remediations = []
            for remediation in self.collection_vapt.find():
               del remediation['data']
               value = {
                   "id": str(remediation['_id']),
                   "anno": remediation['anno'],
                   "mese": remediation['mese'],
                   "nome": remediation['nome'],
                   "type": remediation['type'],
                   "codice_elettra": remediation['codice_elettra'],
                   "cliente": remediation['cliente']
               }
               remediations.append(value)
            return remediations
        except Exception as e:
            logger.error(f"estrazione remediation list: {e}")
            return None
    
    def remediation_list_name(self):
        try:
            list_name = []
            for remediation in self.collection_vapt.find():
                list_name.append(remediation['nome'])
                list_name.sort(key=str.lower)
            return list_name
        except Exception as e:
            logger.error(f"remediation list name: {e}")
            return None
        
    def delete_remediation(self, id_documento):
        try:
            self.collection_vapt.delete_one({"_id": id_documento})
            return True
        except Exception as e:
            logger.error(f"eliminazione remediation: {e}")
            return None
    
if __name__=='__main__':
    db = MyDB()
    print(db.aggregazione())
        