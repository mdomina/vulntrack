from collections import defaultdict
from datetime import datetime
from collections import Counter

def get_vuln_data_by_month(mongo_data):
    """
    Aggrega i dati delle vulnerabilità per mese, raggruppandoli per livello di gravità.

    Questa funzione elabora i dati delle vulnerabilità provenienti da un database MongoDB,
    calcolando il numero di vulnerabilità per ciascun livello di gravità (Critica, Alta, Media, Bassa)
    per ogni mese. I mesi sono restituiti in ordine cronologico.

    :param mongo_data: Lista di dizionari contenenti dati delle vulnerabilità. Ogni dizionario rappresenta
                       un documento con i campi 'date' (in formato 'YYYY-MM-DD') e 'findings', che è una
                       lista di dizionari con il campo 'severity' che indica la gravità della vulnerabilità.
    :return: Tuple con cinque liste:
             - months: lista dei nomi dei mesi in ordine cronologico
             - critical_counts: lista dei conteggi di vulnerabilità critiche per ogni mese
             - high_counts: lista dei conteggi di vulnerabilità alte per ogni mese
             - medium_counts: lista dei conteggi di vulnerabilità medie per ogni mese
             - low_counts: lista dei conteggi di vulnerabilità basse per ogni mese
    """
    
    # Inizializza il dizionario per contare le vulnerabilità per ogni mese e livello di gravità
    severity_counts_by_month = defaultdict(lambda: {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0})
    
    # Mappa le gravità in inglese a quelle in italiano
    severity_map = {'Critical': 'Critica', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Bassa'}

    # Itera su ogni elemento nei dati MongoDB
    for item in mongo_data:
        findings = item.get('findings', [])  # Ottieni la lista delle vulnerabilità (findings)
        date_str = item.get('date', '')      # Ottieni la data come stringa
        
        # Procedi solo se la data è disponibile
        if date_str:
            # Estrai il numero del mese dalla data
            month_number = int(date_str.split('-')[1])  
            
            # Converte il numero del mese nel nome del mese (es. "01" -> "January")
            month_name = datetime.strptime(str(month_number), "%m").strftime("%B")  
            
            # Itera su ogni vulnerabilità per determinare il livello di gravità
            for finding in findings:
                severity = finding.get('severity', 'Unknown')    # Ottieni il livello di gravità
                severity_name = severity_map.get(severity, 'Unknown')  # Converte la gravità in italiano
                
                # Incrementa il conteggio della gravità solo se è un livello valido
                if severity_name in severity_counts_by_month[month_name]:
                    severity_counts_by_month[month_name][severity_name] += 1

    # Ordina i mesi in ordine cronologico
    ordered_months = sorted(severity_counts_by_month.keys(), key=lambda x: datetime.strptime(x, "%B").month)
    
    # Crea liste ordinate per i mesi e i conteggi di ciascun livello di gravità
    months = ordered_months  
    critical_counts = [severity_counts_by_month[month]['Critica'] for month in ordered_months]
    high_counts = [severity_counts_by_month[month]['Alta'] for month in ordered_months]
    medium_counts = [severity_counts_by_month[month]['Media'] for month in ordered_months]
    low_counts = [severity_counts_by_month[month]['Bassa'] for month in ordered_months]

    # Restituisce le liste dei mesi e dei conteggi di gravità per ciascun mese
    return months, critical_counts, high_counts, medium_counts, low_counts

def get_vuln_data_from_mongo(mongo_data):
    """
    Estrae e aggrega i dati delle vulnerabilità da una fonte MongoDB.

    Questa funzione elabora i dati di vulnerabilità contenuti in `mongo_data`, un insieme di documenti MongoDB.
    Per ogni vulnerabilità, raccoglie i titoli, i tipi e i livelli di gravità. Restituisce il conteggio
    di ogni titolo, tipo di vulnerabilità e livello di gravità.

    :param mongo_data: Lista di dizionari contenenti i dati delle vulnerabilità. Ogni dizionario rappresenta
                       un documento con un campo 'findings', che è una lista di vulnerabilità. Ogni vulnerabilità
                       contiene i campi 'title' (titolo), 'vulnType' (tipo di vulnerabilità) e 'severity' (gravità).
    :return: Tuple con sei liste:
             - name_vapt: lista dei titoli unici delle vulnerabilità
             - sizes_vapt: lista dei conteggi per ciascun titolo di vulnerabilità
             - vuln_type_names: lista dei nomi dei tipi di vulnerabilità unici
             - vuln_type_sizes: lista dei conteggi per ciascun tipo di vulnerabilità
             - severity_names: lista dei nomi dei livelli di gravità (Critical, High, Medium, Low)
             - severity_sizes: lista dei conteggi per ciascun livello di gravità
    """
    
    findings_titles = []  # Lista per raccogliere tutti i titoli delle vulnerabilità
    vuln_types = []       # Lista per raccogliere tutti i tipi di vulnerabilità
    severities = []       # Lista per raccogliere tutti i livelli di gravità

    # Itera su ciascun documento in mongo_data
    for item in mongo_data:
        # Estende findings_titles con tutti i titoli presenti in 'findings' del documento corrente
        findings_titles.extend([finding['title'] for finding in item['findings']])
        # Estende vuln_types con tutti i tipi di vulnerabilità presenti in 'findings' del documento corrente
        vuln_types.extend([finding['vulnType'] for finding in item['findings']])
        # Estende severities con tutti i livelli di gravità presenti in 'findings' del documento corrente
        severities.extend([finding['severity'] for finding in item['findings']])

    # Conta le occorrenze di ciascun titolo di vulnerabilità
    title_counts = Counter(findings_titles)
    # Conta le occorrenze di ciascun tipo di vulnerabilità
    vuln_type_counts = Counter(vuln_types)
    # Conta le occorrenze di ciascun livello di gravità
    severity_counts = Counter(severities)

    # Inizializza un dizionario con tutti i livelli di gravità a zero per garantire che tutte le categorie siano presenti
    all_severities = {'Critical': 0, 'High': 0, 'Medium': 0, 'Low': 0}  
    # Aggiorna all_severities con i conteggi effettivi trovati in severity_counts
    all_severities.update(severity_counts) 

    # Crea liste ordinate per i titoli delle vulnerabilità e i loro conteggi
    name_vapt = list(title_counts.keys())           # Lista dei titoli unici delle vulnerabilità
    sizes_vapt = list(title_counts.values())        # Lista dei conteggi per ciascun titolo di vulnerabilità
    
    # Crea liste ordinate per i tipi di vulnerabilità e i loro conteggi
    vuln_type_names = list(vuln_type_counts.keys()) # Lista dei tipi unici di vulnerabilità
    vuln_type_sizes = list(vuln_type_counts.values()) # Lista dei conteggi per ciascun tipo di vulnerabilità
    
    # Crea liste ordinate per i livelli di gravità e i loro conteggi
    severity_names = list(all_severities.keys())    # Lista dei nomi dei livelli di gravità
    severity_sizes = list(all_severities.values())  # Lista dei conteggi per ciascun livello di gravità
    
    # Restituisce le liste con i titoli, tipi e livelli di gravità, insieme ai loro conteggi
    return name_vapt, sizes_vapt, vuln_type_names, vuln_type_sizes, severity_names, severity_sizes

def get_vuln_data_for_vapt_and_recheck(mongo_data):
    """
    Aggrega i dati delle vulnerabilità separandoli per tipo di audit: VAPT e Recheck.

    Questa funzione esamina i dati delle vulnerabilità provenienti da un database MongoDB,
    suddividendo le vulnerabilità per livello di gravità (Critica, Alta, Media, Bassa) e
    per tipo di audit ("VAPT" o "Recheck"). Restituisce due dizionari con i conteggi delle
    vulnerabilità per ciascun livello di gravità, uno per VAPT e uno per Recheck.

    :param mongo_data: Lista di dizionari contenente documenti di vulnerabilità, dove ogni documento
                       ha un campo 'auditType' che indica il tipo di audit ("VAPT" o "Recheck")
                       e una lista di "findings" con il campo 'severity' che indica la gravità della vulnerabilità.
    :return: Tuple contenente due dizionari:
             - vapt_data: Dizionario con i conteggi delle vulnerabilità per ciascun livello di gravità in VAPT
             - recheck_data: Dizionario con i conteggi delle vulnerabilità per ciascun livello di gravità in Recheck
    """
    
    # Inizializza i dizionari per tenere traccia dei conteggi di gravità per VAPT e Recheck
    vapt_data = {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0}
    recheck_data = {'Critica': 0, 'Alta': 0, 'Media': 0, 'Bassa': 0}

    # Mappa le gravità in inglese a quelle in italiano
    severity_map = {'Critical': 'Critica', 'High': 'Alta', 'Medium': 'Media', 'Low': 'Bassa'}

    # Itera su ogni documento nei dati MongoDB
    for item in mongo_data:
        findings = item.get('findings', [])  # Ottieni la lista delle vulnerabilità (findings)
        audit_type = item.get('auditType', 'VAPT')  # Ottieni il tipo di audit, default a "VAPT" se non presente

        # Itera su ogni vulnerabilità per determinare il livello di gravità
        for finding in findings:
            severity = finding.get('severity', 'Unknown')  # Ottieni il livello di gravità
            severity_name = severity_map.get(severity, 'Unknown')  # Converte la gravità in italiano

            # Verifica che la gravità sia valida e conteggia in base al tipo di audit
            if severity_name in vapt_data:
                if audit_type.lower() == 'recheck':  # Se l'audit è di tipo "Recheck"
                    recheck_data[severity_name] += 1
                else:  # Altrimenti, conteggia nel dizionario VAPT
                    vapt_data[severity_name] += 1

    # Restituisce i conteggi delle vulnerabilità per VAPT e Recheck
    return vapt_data, recheck_data

def get_vuln_data_for_vapt_and_recheck_by_category(mongo_data):
    """
    Aggrega i dati delle vulnerabilità per tipologia (categoria) separandoli per tipo di audit: VAPT e Recheck.

    Questa funzione esamina i dati delle vulnerabilità provenienti da un database MongoDB,
    suddividendo le vulnerabilità per categoria (campo 'vulnType') e tipo di audit ("VAPT" o "Recheck").
    Restituisce i conteggi aggregati per ciascuna categoria sia per VAPT che per Recheck, e una lista 
    ordinata di tutte le categorie presenti.

    :param mongo_data: Lista di dizionari contenente documenti di vulnerabilità, dove ogni documento
                       ha un campo 'auditType' che indica il tipo di audit ("VAPT" o "Recheck")
                       e una lista di "findings" con il campo 'vulnType' che indica la categoria della vulnerabilità.
    :return: Tuple contenente tre elementi:
             - vapt_counts: Lista dei conteggi di vulnerabilità per ciascuna categoria in VAPT
             - recheck_counts: Lista dei conteggi di vulnerabilità per ciascuna categoria in Recheck
             - all_categories: Lista ordinata di tutte le categorie di vulnerabilità presenti
    """
    
    # Inizializza i dizionari per tenere traccia dei conteggi per categoria in VAPT e Recheck
    vapt_data_by_category = defaultdict(int)
    recheck_data_by_category = defaultdict(int)

    # Itera su ogni documento nei dati MongoDB
    for item in mongo_data:
        findings = item.get('findings', [])  # Ottiene la lista delle vulnerabilità (findings)
        audit_type = item.get('auditType', 'VAPT')  # Ottiene il tipo di audit, con default a "VAPT"

        # Itera su ogni vulnerabilità per determinare la categoria
        for finding in findings:
            vuln_type = finding.get('vulnType', 'Unknown')  # Ottiene la categoria della vulnerabilità
            
            # Incrementa il conteggio nel dizionario appropriato in base al tipo di audit
            if audit_type.lower() == 'recheck':  # Se l'audit è di tipo "Recheck"
                recheck_data_by_category[vuln_type] += 1
            else:  # Altrimenti, conteggia nel dizionario VAPT
                vapt_data_by_category[vuln_type] += 1

    # Combina le chiavi (categorie) di entrambi i dizionari e le ordina
    all_categories = sorted(set(vapt_data_by_category.keys()).union(set(recheck_data_by_category.keys())))
    
    # Crea le liste dei conteggi per ciascuna categoria in ordine
    vapt_counts = [vapt_data_by_category[category] for category in all_categories]
    recheck_counts = [recheck_data_by_category[category] for category in all_categories]

    # Restituisce i conteggi per VAPT e Recheck, insieme alla lista di tutte le categorie
    return vapt_counts, recheck_counts, all_categories

def get_vuln_data_for_vapt_and_recheck_by_name(mongo_data):
    """
    Aggrega i dati delle vulnerabilità per nome separandoli per tipo di audit: VAPT e Recheck.

    Questa funzione esamina i dati delle vulnerabilità provenienti da un database MongoDB,
    suddividendo le vulnerabilità per nome (campo 'title') e per tipo di audit ("VAPT" o "Recheck").
    Restituisce i conteggi aggregati per ciascun nome sia per VAPT che per Recheck, e una lista 
    ordinata di tutti i nomi delle vulnerabilità presenti.

    :param mongo_data: Lista di dizionari contenente documenti di vulnerabilità, dove ogni documento
                       ha un campo 'auditType' che indica il tipo di audit ("VAPT" o "Recheck")
                       e una lista di "findings" con il campo 'title' che indica il nome della vulnerabilità.
    :return: Tuple contenente tre elementi:
             - vapt_counts: Lista dei conteggi di vulnerabilità per ciascun nome in VAPT
             - recheck_counts: Lista dei conteggi di vulnerabilità per ciascun nome in Recheck
             - all_names: Lista ordinata di tutti i nomi delle vulnerabilità presenti
    """
    
    # Inizializza i dizionari per tenere traccia dei conteggi per nome in VAPT e Recheck
    vapt_data_by_name = defaultdict(int)
    recheck_data_by_name = defaultdict(int)

    # Itera su ogni documento nei dati MongoDB
    for item in mongo_data:
        findings = item.get('findings', [])  # Ottiene la lista delle vulnerabilità (findings)
        audit_type = item.get('auditType', 'VAPT')  # Ottiene il tipo di audit, con default a "VAPT"

        # Itera su ogni vulnerabilità per determinare il nome
        for finding in findings:
            vuln_name = finding.get('title', 'Unknown')  # Ottiene il nome della vulnerabilità
            
            # Incrementa il conteggio nel dizionario appropriato in base al tipo di audit
            if audit_type.lower() == 'recheck':  # Se l'audit è di tipo "Recheck"
                recheck_data_by_name[vuln_name] += 1
            else:  # Altrimenti, conteggia nel dizionario VAPT
                vapt_data_by_name[vuln_name] += 1

    # Combina i nomi di entrambi i dizionari e li ordina
    all_names = sorted(set(vapt_data_by_name.keys()).union(set(recheck_data_by_name.keys())))
    
    # Crea le liste dei conteggi per ciascun nome in ordine
    vapt_counts = [vapt_data_by_name[name] for name in all_names]
    recheck_counts = [recheck_data_by_name[name] for name in all_names]

    # Restituisce i conteggi per VAPT e Recheck, insieme alla lista di tutti i nomi
    return vapt_counts, recheck_counts, all_names
