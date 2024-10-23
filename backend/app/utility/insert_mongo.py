import asyncio
from pymongo import MongoClient
from app.database.database import MyDB
from app.config.settings import Settings
from app.utility.logger import logger
import hashlib
import sys

class InsertMongo:

    def __init__(self):
        # Initialize first MongoDB connection (the one you're already using)
        self.settings = Settings()
        self.client_pwndoc = MongoClient(self.settings.PWNDOC_HOST, int(self.settings.PWNDOC_PORT))
        self.database_pwndoc = self.client_pwndoc['pwndoc']
        self.collection_audit_pwndoc = self.database_pwndoc['audits']
        self.collection_companies_pwndoc = self.database_pwndoc['companies']
        self.vulntrack_db = MyDB()  # Another database

        # Initialize second MongoDB connection (the new one)
        self.client_vuln = MongoClient(self.settings.MONGO_HOST, int(self.settings.MONGO_PORT))
        self.database_vuln = self.client_new_mongo['vulntrack']
        self.collection_vapt = self.database_new_mongo['vapt']
        self.collection_companies_vuln = self.database_new_mongo['company']

    @staticmethod
    def hash(documento):
        try:
            hash_string = f"{documento.get('name', '')}{documento.get('auditType', '')}{documento.get('company', '')}{documento.get('date', '')}"
            return hashlib.md5(hash_string.encode()).hexdigest()
        except Exception as e:
            logger.error(f"Errore durante la generazione dell'hash: {e}")
            return None

    def createList(self, collection_audit, collection_companies):
        try:
            check = collection_audit.find({
                "findings.status": 0  # Filter for documents with status == 0
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
                findings_validi = [
                    {**find, "score": self.convertCVSS(find["cvssv3"])[0], "severity": self.convertCVSS(find["cvssv3"])[1]}
                    for find in documento["findings"] if find["status"] == 0
                ]
                if not findings_validi:
                    continue
                documento["findings"] = findings_validi
                company_id = documento.get("company")
                documento["company"] = self.companyFind(company_id, collection_companies)
                documento["id"] = self.hash(documento)
                documenti.append(documento)

            return documenti
        except Exception as e:
            logger.error(f"Errore durante la creazione della lista di documenti: {e}")
            return []

    def companyFind(self, company_ID, collection_companies):
        try:
            if company_ID:
                company_data = collection_companies.find_one({'_id': company_ID}, {"name": 1})
                return company_data.get("name") if company_data else "Non trovata"
            return "Non trovata"
        except Exception as e:
            logger.error(f"Errore durante la ricerca dell'azienda con ID {company_ID}: {e}")
            return "Errore"

    def convertCVSS(self, vector: str):
        try:
            from cvss import CVSS3
            x = CVSS3(vector)
            return x.scores()[0], x.severities()[0]
        except Exception as e:
            logger.error(f"Errore durante la conversione del vettore CVSS: {e}")
            return 0, "Unknown"

    def sync_databases(self):
        try:
            lista_pwndoc = self.createList(self.collection_audit_pwndoc, self.collection_companies_pwndoc)
            lista_vuln = self.createList(self.collection_vapt, self.collection_companies_vuln)

            missing_in_new_mongo, extra_in_new_mongo = self.setsDiff(lista_pwndoc, lista_vuln)

            if missing_in_new_mongo or extra_in_new_mongo:
                logger.info("Discrepanze trovate:")

                if extra_in_new_mongo:
                    logger.info("Elementi presenti nel nuovo MongoDB ma mancanti in pwndoc (saranno eliminati):")
                    for doc in extra_in_new_mongo:
                        original_doc = {k: v for k, v in doc}
                        self.collection_vapt.delete_one({'id': original_doc['id']})
                        logger.info(f"Documento con ID {original_doc['id']} eliminato dal nuovo MongoDB.")

                if missing_in_new_mongo:
                    logger.info("Elementi presenti in pwndoc ma mancanti nel nuovo MongoDB:")
                    for doc in missing_in_new_mongo:
                        original_doc = {k: v for k, v in doc}
                        for documento in lista_pwndoc:
                            if documento["id"] == original_doc["id"]:
                                documento["TAGS"] = documento["company"]
                                self.collection_audit_new.insert_one(documento)
                                logger.info(f"Documento con ID {documento['id']} inserito nel nuovo MongoDB.")

        except Exception as e:
            logger.error(f"Errore durante la sincronizzazione: {str(e)}")
            sys.exit()

    def setsDiff(self, lista1, lista2):
        set1 = {self.make_hashable(d) for d in lista1}
        set2 = {self.make_hashable(d) for d in lista2}

        missing_in_set2 = set1 - set2
        extra_in_set2 = set2 - set1

        return missing_in_set2, extra_in_set2

    def make_hashable(self, item):
        if isinstance(item, dict):
            return tuple(sorted((k, self.make_hashable(v)) for k, v in item.items()))
        elif isinstance(item, list):
            return tuple(self.make_hashable(i) for i in item)
        else:
            return item

if __name__ == "__main__":
    InsertMongo().sync_databases()
