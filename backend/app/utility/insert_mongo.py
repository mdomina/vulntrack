from pymongo import MongoClient
from app.database.database import MyDB
from app.config.settings import Settings
from app.utility.logger import logger
from cvss import CVSS3
from pymongo.errors import PyMongoError

class InsertMongo():
    def __init__(self):
        """
        Inizializza la connessione ai database e le collezioni necessarie.
        Imposta il client MongoDB per 'pwndoc' e una connessione separata a 'vulntrack'.
        """
        self.settings = Settings()
        self.client = MongoClient(self.settings.PWNDOC_HOST, int(self.settings.PWNDOC_PORT))
        self.database = self.client['pwndoc']
        self.collection_audit = self.database['audits']
        self.collection_companies = self.database['companies']
        self.vulntrack_db = MyDB()
        
    def convertCVSS(self, vector: str) -> str:
        """
        Calcola il punteggio e la severità basati sul vettore CVSSv3 fornito.
        
        Args:
            vector (str): Il vettore CVSSv3.
        
        Returns:
            tuple: Punteggio base e severità base.
        """
        x = CVSS3(vector)
        base_score, temporal_score, environmental_score = x.scores()
        base_severity, temporal_severity, enviromental_sevirity = x.severities()
        return base_score, base_severity
        
    def companyFind(self, company_ID):
        """
        Trova il nome dell'azienda associato a un ID specifico nella collezione 'companies'.

        Args:
            company_ID: ID univoco dell'azienda.

        Returns:
            str: Nome dell'azienda o messaggio di errore.
        """
        try:
            if company_ID:
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
        """
        Crea una lista di documenti dalla collezione 'audits' filtrando per findings con status == 0.
        I documenti vengono arricchiti con il punteggio CVSS e la severità, e il nome dell'azienda.

        Returns:
            list: Lista di documenti filtrati e processati.
        """
        try:
            check = self.collection_audit.find({
                "findings.status": 0
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
                    findings_validi = []
                    for find in documento["findings"]:
                        if find["status"] == 0:
                            score, severity = self.convertCVSS(find["cvssv3"])
                            find["score"] = score
                            find["severity"] = severity
                            findings_validi.append(find)

                    if not findings_validi:
                        continue

                    documento["findings"] = findings_validi

                except Exception as e:
                    logger.error(f"Conversione cvssv3: {e}")

                try:
                    company_id = documento.get("company")
                    documento["company"] = self.companyFind(company_id)
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
        """
        Sincronizza i dati tra i database 'pwndoc' e 'vulntrack'.
        Confronta i documenti e allinea le discrepanze inserendo o eliminando i documenti necessari.
        """
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
                        for documento in lista_pwndoc:
                            try:   
                                if documento["_id"] == original_doc["_id"]:      
                                    self.vulntrack_db.collection_vapt.insert_one(documento)
                                    logger.info(f"Documento con ID {str(original_doc['_id'])} inserito nel nuovo MongoDB.")
                            except Exception as e:
                                logger.error(f"Errore durante l'inserimento: {e}")

        except Exception as e:
            logger.error(f"Errore durante la sincronizzazione: {str(e)}")

    def setsDiff(self, lista1, lista2):
        """
        Trova le discrepanze tra due liste di documenti.

        Args:
            lista1: Prima lista di documenti.
            lista2: Seconda lista di documenti.

        Returns:
            tuple: Elementi mancanti e in eccesso.
        """
        set1 = {self.make_hashable(d) for d in lista1}
        set2 = {self.make_hashable(d) for d in lista2}
        missing_vulntrack = set1 - set2
        extra_vulntrack = set2 - set1

        return missing_vulntrack, extra_vulntrack
    
    def make_hashable(self, item):
        """
        Converte ricorsivamente un elemento in una versione hashabile per consentire confronti.

        Args:
            item: Elemento da convertire.

        Returns:
            Elemento hashabile.
        """
        if isinstance(item, dict):
            return tuple(sorted((k, self.make_hashable(v)) for k, v in item.items()))
        elif isinstance(item, list):
            return tuple(self.make_hashable(i) for i in item)
        else:
            return item
        
    def vulnlist(self):
        """
        Ottiene tutti i documenti dalla collezione 'vapt' del database 'vulntrack'.

        Returns:
            list: Lista di documenti presenti nel database.
        """
        try:
            result = []
            lista_vuln = self.vulntrack_db.collection_vapt.find()
            for documento in lista_vuln:
                result.append(documento)
            return result
        except Exception as e:
            logger.error(f"Errore durante l'elaborazione dei documenti: {e}")
