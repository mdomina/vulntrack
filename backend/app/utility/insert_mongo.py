from pymongo import MongoClient
from app.database.database import MyDB
from app.config.settings import Settings
from app.utility.logger import logger
from cvss import CVSS3
from pymongo.errors import PyMongoError
import hashlib  

class Insert_Mongo():


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
                "_id": 0
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

                    # Genera l'hash MD5 dei valori "name", "auditType", "company", "date"
                    documento["id"] = self.hash(documento)
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
        
    def main(self):

        audits= self.createList()  
        for audit in audits:
            self.vulntrack_db.insert(audit)
