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
        self.db = self.client['vulntrack_test']
        self.collection_vapt = self.db['vapt']
        self.collection_users = self.db['users']

        
    def get_all_users(self):
        """"recupera tutti gli utenti"""
        try:
            return self.collection_users.find()
        except Exception as e:
            logger.error(f"recupero utenti : {e}")

    def insert_user(self, document) -> bool:
        """inserisce un utente"""
        try:
            result  = self.collection_users.insert_one(document)
            return result.inserted_id is not None
        except Exception as e:
            # Stampa o log dell'eccezione per il debug
            logger.error(f"durante l'inserimento dell'utente: {e}")
            return False

    def get_users_collection(self):
        """
        controlla se esiste la collection users
        """
        return self.db.get_collection('users')

    def insert(self, document):
        """
        Inserisce un nuovo documento nella collezione 'vapt'.
        
        Solleva:
            - HTTPException con status code 400 se il documento è già presente.
            - Logga l'errore in caso di altri problemi durante l'inserimento.
        """
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
                # Rimuove il campo 'findings' per evitare di includere dati non necessari
                # del remediation['findings']
                
                value = {
                    "id": str(remediation['_id']),
                    "anno": remediation.get('date', '')[:4],  # Anno estratto dalla data
                    "mese": remediation.get('date', '')[5:7],  # Mese estratto dalla data
                    "nome": remediation.get('name', ''),
                    "type": remediation.get('auditType', ''),
                    "codice_elettra": ('-'),  # Default '-' se non presente
                    "cliente": remediation.get('company', '')
                }
                remediations.append(value)
            return remediations
        except Exception as e:
            logger.error(f"estrazione remediation list: {e}")
            return None
    
    def audit_list_name_by_company(self, company:str) -> list:
        """estrae i nomi degli audits in base alla company"""
        try:
            list_name = []
            for audit in self.collection_vapt.find({'company': company},{'name':1}):
                list_name.append(audit['name'])
                list_name.sort(key=str.lower)
            return list_name
        except Exception as e:
            logger.error(f"audit list name: {e}")
            return []
        
    def delete_remediation(self, id_documento):
        try:
            self.collection_vapt.delete_one({"_id": id_documento})
            return True
        except Exception as e:
            logger.error(f"eliminazione remediation: {e}")
            return None
    
    def email_exists(self, email: str) -> bool:
        """
        Verifica se un'email esiste già nella collezione 'users' di MongoDB.

        Args:
            email (str): L'email da verificare.

        Returns:
            bool: True se l'email esiste già nella collezione, False altrimenti.
        """

        # Costruisce la query per cercare l'email ignorando maiuscole/minuscole
        query = {"email": email}

        # Cerca se l'email esiste nella collezione 'users'
        result = self.collection_users.find_one(query)

        # Se trova un risultato, ritorna True, altrimenti False
        return result is not None
    
    def delete_user(self, email: str) -> bool:
        """
        Elimina un utente dalla collezione 'users' in base all'indirizzo email.

        Args:
            email (str): L'indirizzo email dell'utente da eliminare.
        
        Returns:
            bool: True se l'utente è stato eliminato con successo, False altrimenti.
        """
        try:
            result = self.collection_users.delete_one({"email": email})
            # Verifica se un documento è stato effettivamente eliminato
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Errore durante l'eliminazione dell'utente: {e}")
            return False
        
    def get_all_companies(self):
        """estrazione di tutti i clienti a cui è stato fatto un vapt"""
        companies = []
        try:
            for company in self.collection_vapt.find({},{'company':1}):
                companies.append(company['company'])
        except Exception as e:
            logger.error(f"estrazione companies: {e}")
        return companies
    
    def get_filtered_companies(self, user_companies: list[str]):
        """estrazione dei i clienti a cui è stato fatto un vapt in base ai permessi degli utenti"""
        companies = []
        try:
            for company in self.collection_vapt.find({'company': {'$in': user_companies}},{'company':1,'_id':0}):
                companies.append(company['company'])
        except Exception as e:
            logger.error(f"estrazione companies: {e}")
        return companies

if __name__=='__main__':
    db = MyDB()
    print(db.aggregazione())
        