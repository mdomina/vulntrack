from pymongo import MongoClient
from app.database.database import MyDB
from app.config.settings import Settings
from app.utility.logger import logger
from cvss import CVSS3
from pymongo.errors import PyMongoError
import hashlib  

class InsertMongo():
    def __init__(self):

        # Inizializzazione del client
        self.settings = Settings()
        self.client = MongoClient(self.settings.PWNDOC_HOST, int(self.settings.PWNDOC_PORT))
        self.database = self.client['pwndoc']
        self.collection_audit = self.database['audits']
        self.collection_companies = self.database['companies']
        self.vulntrack_db = MyDB()

    @staticmethod
    def hash(documento):
        try:
            hash_string = f"{documento.get('name', '')}{documento.get('auditType', '')}{documento.get('company', '')}{documento.get('date', '')}"
            return hashlib.md5(hash_string.encode()).hexdigest()  # Genera l'hash MD5
        except Exception as e:
            logger.error(f"Errore durante la generazione dell'hash: {e}")
            return None
        
    def convertCVSS(self, vector: str) -> str:
        x = CVSS3(vector)
        base_score, temporal_score, environmental_score = x.scores()
        base_severity, temporal_severity, enviromental_sevirity = x.severities()
        return base_score, base_severity
        
    def companyFind(self, company_ID):
        try:
            if company_ID:
                # Trova il nome dell'azienda nella collezione companies
                company_data = self.collection_companies.find_one({'_id': company_ID}, {"name": 1})
                if company_data:
                    return company_data.get("name")
                else:
                    logger.warning(f"Azienda con ID {company_ID} non trovata.")
                    return "Non trovata"
            else:
                return "Non trovata"
        except PyMongoError as e:
            logger.error(f"Errore durante la ricerca dell'azienda con ID {company_ID}: {e}")
            return "Errore"
        except Exception as e:
            logger.error(f"Errore generico durante la ricerca dell'azienda con ID {company_ID}: {e}")
            return "Errore"
        
    def createList(self):
        try:
            # Query per estrarre i campi desiderati e filtrare per findings.status == 0
            check = self.collection_audit.find({
                "findings.status": 0  # Aggiungi la condizione per filtrare i documenti con status == 0
            }, {
                "name": 1,
                "auditType": 1,
                "findings.title": 1,
                "findings.vulnType": 1,
                "findings.category": 1,
                "findings.cvssv3": 1,
                "findings.status": 1,
                "date": 1,
                "company": 1,
                "_id": 1
            })

            documenti = []
            for documento in check:
                try:
                    # Itera tra i findings e aggiorna solo quelli con status == 0
                    findings_validi = []
                    for find in documento["findings"]:
                        if find["status"] == 0:
                            score, severity = self.convertCVSS(find["cvssv3"])
                            find["score"] = score
                            find["severity"] = severity
                            findings_validi.append(find)  # Aggiungi solo i findings con status == 0

                    if not findings_validi:
                        continue  # Salta il documento se non ci sono findings con status == 0
                    
                    documento["findings"] = findings_validi

                except Exception as e:
                    logger.error(f"Conversione cvssv3: {e}")

                try:
                    company_id = documento.get("company")
                    documento["company"] =  self.companyFind(company_id)

                    documenti.append(documento)


                except Exception as e:
                    logger.error(f"Errore durante l'elaborazione del documento: {e}")

            return documenti
        except PyMongoError as e:
            logger.error(f"Errore durante la creazione della lista di documenti: {e}")
            return []
        except Exception as e:
            logger.error(f"Errore generico durante la creazione della lista di documenti: {e}")
            return []
        
    def sync_databases(self):
        
        try:
            lista_pwndoc = self.createList()
            lista_vuln = self.vulnlist()

            missing_vulntrack, extra_vulntrack = self.setsDiff(lista_pwndoc, lista_vuln)

            if missing_vulntrack or extra_vulntrack:
                logger.info("Discrepanze trovate:")

                if extra_vulntrack:
                    logger.info("Elementi presenti nel vulntrack db ma mancanti in pwndoc (saranno eliminati):")
                    for doc in extra_vulntrack:
                        original_doc = {k: v for k, v in doc}
                        self.vulntrack_db.collection_vapt.delete_one({'_id': original_doc['_id']})
                        logger.info(f"Documento con ID {str(original_doc['_id'])} eliminato dal nuovo MongoDB.")

                if missing_vulntrack:
                    logger.info("Elementi presenti in pwndoc ma mancanti nel vulntrack db:")
                    for doc in missing_vulntrack:
                        original_doc = {k: v for k, v in doc}  
                        try:         
                            self.vulntrack_db.collection_vapt.insert_one(original_doc)
                            logger.info(f"Documento con ID {str(original_doc['_id'])} inserito nel nuovo MongoDB.")
                        except Exception as e:
                            logger.error(f"Errore durante l'inserimento: {e}")

        except Exception as e:
            logger.error(f"Errore durante la sincronizzazione: {str(e)}")

    def setsDiff(self, lista1, lista2):

        set1 = {self.make_hashable(d) for d in lista1}
        set2 = {self.make_hashable(d) for d in lista2}
        missing_vulntrack = set1 - set2
        extra_vulntrack = set2 - set1

        return missing_vulntrack, extra_vulntrack
    
    def make_hashable(self, item):
        """
        Converte ricorsivamente un elemento in una versione hashabile.
        Se l'elemento è un dizionario, lo converte in una tupla ordinata.
        Se l'elemento è una lista, la converte in una tupla. Altri tipi di dati rimangono invariati.
        Questo è utile per comparare strutture dati non hashabili come dizionari e liste.
        """

        if isinstance(item, dict):
            return tuple(sorted((k, self.make_hashable(v)) for k, v in item.items()))
        elif isinstance(item, list):
            return tuple(self.make_hashable(i) for i in item)
        else:
            return item
        
    def vulnlist(self):
        try:
            # Fetch all documents from the collection_vapt
            result = []
            lista_vuln = self.vulntrack_db.collection_vapt.find()

            # Iterate through each document and remove the '_id' field
            for documento in lista_vuln:
                result.append(documento)
            return result
        except Exception as e:
            logger.error(f"Errore durante l'elaborazione dei documenti: {e}")

